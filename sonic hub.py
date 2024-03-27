import pyodbc as po
import pyodbc
from faker import Faker
import random
import pyodbc as po
# Initialize Faker
fake = Faker()

# Connection variables
server = 'mcruebs04.isad.isadroot.ex.ac.uk'
database = 'BEMM459_GroupR'
username = 'GroupR'
password = 'YuhH722*Ny'

# Connection string
cnxn = po.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER=' +
                  server+';DATABASE='+database+';UID='+username+';PWD=' + password)
cursor = cnxn.cursor()

# SQL commands to create the tables
table_commands = [
    '''
    IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'Clients')
    BEGIN
        CREATE TABLE Clients (
            client_id INT IDENTITY(1,1) PRIMARY KEY,
            email VARCHAR(255),
            contact_number VARCHAR(20),
            social_media_handle VARCHAR(255),
            name VARCHAR(255)
        );
    END
    ''',
    '''
    IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'MusicTrackCatalogue')
    BEGIN
        CREATE TABLE MusicTrackCatalogue (
            track_id INT IDENTITY(1,1) PRIMARY KEY,
            genre VARCHAR(50),
            mood VARCHAR(50),
            tempo VARCHAR(50),
            duration INT,
            composer_id INT
            -- Assuming Composer table exists and composer_id is a FK, define FK relationship here if needed
        );
    END
    ''',
    '''
    IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'Reservation')
    BEGIN
        CREATE TABLE Reservation (
            reservation_id INT IDENTITY(1,1) PRIMARY KEY,
            client_id INT,
            track_id INT,
            reservation_date DATE,
            showtime DATETIME,
            FOREIGN KEY (client_id) REFERENCES Clients(client_id),
            FOREIGN KEY (track_id) REFERENCES MusicTrackCatalogue(track_id)
        );
    END
    ''',
    '''
    IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'CopyrightClaims')
    BEGIN
        CREATE TABLE CopyrightClaims (
            claim_id INT IDENTITY(1,1) PRIMARY KEY,
            track_id INT,
            claimant_name VARCHAR(MAX),
            claim_date DATE,
            status VARCHAR(50),
            FOREIGN KEY (track_id) REFERENCES MusicTrackCatalogue(track_id)
        );
    END
    ''',
    '''
    IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'CollaborationTermsOfAgreement')
    BEGIN
        CREATE TABLE CollaborationTermsOfAgreement (
            agreement_id INT IDENTITY(1,1) PRIMARY KEY,
            client_id INT,
            agreement_date DATE,
            terms TEXT,
            FOREIGN KEY (client_id) REFERENCES Clients(client_id)
        );
    END
    ''',
    '''
    IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'Composers')
    BEGIN
        CREATE TABLE Composers (
            composer_id INT IDENTITY(1,1) PRIMARY KEY,
            first_name VARCHAR(50),
            last_name VARCHAR(50),
            speciality VARCHAR(50),
            experience_years INT
            -- No need for a FK reference here based on your provided schema
        );
    END
    ''',
    '''
    IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'RoyaltyManagement')
BEGIN
    CREATE TABLE RoyaltyManagement (
        royalty_id INT IDENTITY(1,1) PRIMARY KEY,
        track_id INT,
        royalty_percentage DECIMAL(10,2),
        revenue_earned DECIMAL(18,2), -- Adding revenue_earned column
        payment_date DATE,
        payment_status VARCHAR(50),
        FOREIGN KEY (track_id) REFERENCES MusicTrackCatalogue(track_id)
    );
        
    END
    '''
]

# Execute the table creation commands
for command in table_commands:
    cursor.execute(command)
cnxn.commit()

# Clean up
#cursor.close()
#cnxn.close()

print("All tables created successfully.")

# Define the get_phone_number function
def get_phone_number():
    # Generate a phone number and truncate it to fit within the VARCHAR(20) limit
    return fake.phone_number()[:20]

# Insert fake data into Clients
for _ in range(70):
    email = fake.email()
    contact_number = get_phone_number()  # Ensure the function call matches the definition
    social_media_handle = '@' + fake.user_name()
    name = fake.name()
    cursor.execute("INSERT INTO Clients (email, contact_number, social_media_handle, name) VALUES (?, ?, ?, ?)",
                   email, contact_number, social_media_handle, name)
cnxn.commit()
# Assuming the initial setup and 'get_phone_number' function are already defined as shown previously

# Insert fake data into Composers
for _ in range(70):
    cursor.execute("INSERT INTO Composers (first_name, last_name, speciality, experience_years) VALUES (?, ?, ?, ?)",
                   fake.first_name(), fake.last_name(),
                   fake.word(ext_word_list=['Classical', 'Jazz', 'Rock', 'Electronic']),
                   random.randint(1, 40))
cnxn.commit()

# Fetch IDs for foreign key relationships
cursor.execute("SELECT client_id FROM Clients")
client_ids = [row[0] for row in cursor.fetchall()]

cursor.execute("SELECT composer_id FROM Composers")
composer_ids = [row[0] for row in cursor.fetchall()]

# Insert fake data into MusicTrackCatalogue
for _ in range(70):
    cursor.execute("INSERT INTO MusicTrackCatalogue (genre, mood, tempo, duration, composer_id) VALUES (?, ?, ?, ?, ?)",
                   fake.word(ext_word_list=['Pop', 'Rock', 'Classical', 'Jazz', 'Electronic']),
                   fake.word(ext_word_list=['Happy', 'Sad', 'Energetic', 'Calm']),
                   fake.word(ext_word_list=['Fast', 'Medium', 'Slow']),
                   random.randint(180, 360), random.choice(composer_ids))
cnxn.commit()

# Assuming you also fetch track_ids similar to how composer_ids and client_ids were fetched
cursor.execute("SELECT track_id FROM MusicTrackCatalogue")
track_ids = [row[0] for row in cursor.fetchall()]

# Insert fake data into Reservation
for _ in range(70):
    cursor.execute("INSERT INTO Reservation (client_id, track_id, reservation_date, showtime) VALUES (?, ?, ?, ?)",
                   random.choice(client_ids), random.choice(track_ids),
                   fake.date_between(start_date='-1y', end_date='today').isoformat(),
                   fake.date_time_between(start_date='-1y', end_date='now').isoformat())
cnxn.commit()


# Insert fake data into CopyrightClaims
for _ in range(70):
    cursor.execute("INSERT INTO CopyrightClaims (track_id, claimant_name, claim_date, status) VALUES (?, ?, ?, ?)",
                   random.choice(track_ids), fake.name(),
                   fake.date_between(start_date='-1y', end_date='today').isoformat(),
                   fake.random_element(elements=('Pending', 'Resolved', 'Rejected')))
cnxn.commit()

# Insert fake data into CollaborationTermsOfAgreement
for _ in range(70):
    cursor.execute("INSERT INTO CollaborationTermsOfAgreement (client_id, agreement_date, terms) VALUES (?, ?, ?)",
                   random.choice(client_ids),
                   fake.date_between(start_date='-1y', end_date='today').isoformat(),
                   fake.paragraph())
cnxn.commit()

# Insert fake data into RoyaltyManagement
for _ in range(70):
    cursor.execute("INSERT INTO RoyaltyManagement (track_id, royalty_percentage, payment_date, payment_status, revenue_earned) VALUES (?, ?, ?, ?, ?)",
                   random.choice(track_ids),
                   round(random.uniform(0.5, 15.0), 2),
                   fake.date_between(start_date='-1y', end_date='today').isoformat(),
                   fake.random_element(elements=('Paid', 'Unpaid', 'Pending')),
                   round(random.uniform(1, 100) * 100000, 2)) # Revenue in lakhs
cnxn.commit()
print("Sample data for all tables inserted successfully.")
# Check if date_of_birth column exists and add it if it doesn't
try:
    cursor.execute("""
    IF NOT EXISTS (SELECT * FROM INFORMATION_SCHEMA.COLUMNS 
                   WHERE TABLE_NAME = 'Clients' AND COLUMN_NAME = 'date_of_birth')
    BEGIN
        ALTER TABLE Clients ADD date_of_birth DATE
    END
    """)
    cnxn.commit()
    print("Checked for date_of_birth column and added to Clients table if it did not exist.")
except pyodbc.Error as e:
    print("Error checking or adding date_of_birth column:", e)

# Populate the date_of_birth column with random dates for every record if not already populated
try:
    cursor.execute("""
    UPDATE Clients 
    SET date_of_birth = DATEADD(year, -(ABS(CHECKSUM(NEWID())) % 50), GETDATE())
    WHERE date_of_birth IS NULL
    """)
    cnxn.commit()
    print("Populated date_of_birth column with random dates for all records in Clients table where date_of_birth was NULL.")
except pyodbc.Error as e:
    print("Error populating date_of_birth:", e)



# Delete commands
def delete_data_by_id(table_name, id_column, id_value):
    sql = f"DELETE FROM {table_name} WHERE {id_column} = ?"
    cursor.execute(sql, id_value)
    cnxn.commit()
    print(f"Data with {id_column} = {id_value} deleted successfully from {table_name}.")


table = 'Clients'
data_id = 2666
delete_data_by_id(table, 'client_id', data_id)
print(f"Deleted data from {table} of {data_id}")







# Remember to close your cursor and connection at the end of your script
cursor.close()
cnxn.close()
