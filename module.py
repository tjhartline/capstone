import sqlite3
import csv
from datetime import datetime

class AnimalShelter(object):
    def __init__(self, db_path='animals.db'):
        self.db_path = db_path
        self.create_table()

    def create_table(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS animals (
                animal_id TEXT PRIMARY KEY,
                age_upon_outcome TEXT,
                animal_type TEXT,
                breed TEXT,
                color TEXT,
                date_of_birth TEXT,
                datetime TEXT,
                monthyear TEXT,
                name TEXT,
                outcome_subtype TEXT,
                outcome_type TEXT,
                record_num INTEGER,
                sex_upon_outcome TEXT,
                location_lat REAL,
                location_long REAL,
                age_upon_outcome_in_weeks REAL
            )
        ''')
        conn.commit()
        conn.close()

    def createOne(self, data):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # Generate a valid ID based on animal_id
        animal_id = data['animal_id']
        valid_id = ''.join(c if c.isalnum() else '_' for c in animal_id)  # Replace invalid characters with underscores

        try:
            cursor.execute('''
                INSERT INTO animals (animal_id, name, age_upon_outcome, breed, outcome_type)
                VALUES (?, ?, ?, ?, ?)
            ''', (valid_id, data['name'], data['age_upon_outcome'], data['breed'], data['outcome_type']))
            conn.commit()
            return True
        except sqlite3.IntegrityError:
            # Handle duplicate animal_id (maybe update the record)
            print(f"Animal with ID {valid_id} already exists.")
            return False
        finally:
            conn.close()


    def read(self, query=None):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        if query is None:
            cursor.execute('SELECT * FROM animals')
        else:
            cursor.execute('SELECT * FROM animals WHERE ' + query[0], query[1])

        result = cursor.fetchall()
        conn.close()

        columns = [
            'animal_id', 'age_upon_outcome', 'animal_type', 'breed', 'color',
            'date_of_birth', 'datetime', 'monthyear', 'name', 'outcome_subtype',
            'outcome_type', 'sex_upon_outcome', 'location_lat', 'location_long',
            'age_upon_outcome_in_weeks'
        ]
        records = [dict(zip(columns, row)) for row in result]
        return records

    def update(self, query, update_data):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('UPDATE animals SET ' + ', '.join([f"{key} = ?" for key in update_data.keys()]) +
                       ' WHERE ' + query[0], [*update_data.values(), query[1]])
        conn.commit()
        conn.close()
        return True

    def delete(self, query):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('DELETE FROM animals WHERE ' + query[0], query[1])
        conn.commit()
        conn.close()

# Create SQLite database and populate it with data from CSV
shelter = AnimalShelter()
shelter.create_table()

csv_file = 'aac_shelter_outcomes.csv'
with open(csv_file, 'r') as file:
    reader = csv.DictReader(file)
    for row in reader:
        shelter.createOne(row)

# Example usage of read method
all_animals = shelter.read()
for animal in all_animals[:5]:  # Displaying the first 5 records for example
    print(animal)
