import sqlite3
import csv
from datetime import datetime

class AnimalShelter(object):
    def __init__(self, db_path='animals.db'):
        self.db_path = db_path
        self.initialize_database()  # Call create_table during initialization

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
