import sqlite3
import csv
from datetime import datetime

class AnimalShelter(object):
    def __init__(self, db_path='animals.db'):
        self.db_path = db_path

    def create_table(self):
        query = '''
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
        '''
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(query)
            conn.commit()

    def initialize_database(self):
        self.create_table()

    def create_one(self, data):
        valid_id = ''.join(c if c.isalnum() else '_' for c in data['animal_id'])
        query = '''
            INSERT INTO animals (animal_id, name, age_upon_outcome, breed, outcome_type)
            VALUES (?, ?, ?, ?, ?)
        '''

        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()

            try:
                cursor.execute(query, (valid_id, data['name'], data['age_upon_outcome'], data['breed'], data['outcome_type']))
                conn.commit()
                return True
            except sqlite3.IntegrityError:
                print(f"Animal with ID {valid_id} already exists.")
                return False

    def read(self, query=None):
        query_str = 'SELECT * FROM animals'
        if query is not None:
            query_str += f" WHERE {query[0]}"

        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(query_str, query[1] if query is not None else None)
            result = cursor.fetchall()

        columns = [
            'animal_id', 'age_upon_outcome', 'animal_type', 'breed', 'color',
            'date_of_birth', 'datetime', 'monthyear', 'name', 'outcome_subtype',
            'outcome_type', 'sex_upon_outcome', 'location_lat', 'location_long',
            'age_upon_outcome_in_weeks'
        ]
        records = [dict(zip(columns, row)) for row in result]
        return records

    def update(self, query, update_data):
        update_str = ', '.join([f"{key} = ?" for key in update_data.keys()])
        query_str = f'UPDATE animals SET {update_str} WHERE {query[0]}'

        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(query_str, [*update_data.values(), query[1]])
            conn.commit()
        return True

    def delete(self, query):
        query_str = f'DELETE FROM animals WHERE {query[0]}'

        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(query_str, query[1])
            conn.commit()

# Example usage
shelter = AnimalShelter()
shelter.initialize_database()

csv_file = 'aac_shelter_outcomes.csv'
try:
    with open(csv_file, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            shelter.create_one(row)
except FileNotFoundError:
    print(f"Error: CSV file '{csv_file}' not found.")

# Example usage of read method
all_animals = shelter.read()
for animal in all_animals[:5]:  # Displaying the first 5 records for example
    print(animal)
