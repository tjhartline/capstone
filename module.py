import sqlite3
import os

class AnimalShelter(object):
    def __init__(self, db_path='animals.db'):
        self.db_path = db_path
        self.create_table()

    def create_table(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS animals (
                _id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                age INTEGER,
                breed TEXT,
                outcome_type TEXT
            )
        ''')
        conn.commit()
        conn.close()

    def createOne(self, data):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO animals (name, age, breed, outcome_type) VALUES (?, ?, ?, ?)
        ''', (data['name'], data['age'], data['breed'], data['outcome_type']))
        conn.commit()
        conn.close()
        return True

    def read(self, query=None):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        if query is None:
            # Read all records if no query is provided
            cursor.execute('SELECT * FROM animals')
        else:
            # Apply the query
            cursor.execute('SELECT * FROM animals WHERE ' + query[0], query[1])

        result = cursor.fetchall()
        conn.close()

        # Convert results to a list of dictionaries
        columns = ['_id', 'name', 'age', 'breed', 'outcome_type']
        records = [dict(zip(columns, row)) for row in result]
        return records

    def update(self, query, update_data):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('UPDATE animals SET name=?, age=?, breed=?, outcome_type=? WHERE ' + query[0], (*update_data.values(), query[1]))
        conn.commit()
        conn.close()
        return True

    def delete(self, query):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('DELETE FROM animals WHERE ' + query[0], query[1])
        conn.commit()
        conn.close()
        return True
