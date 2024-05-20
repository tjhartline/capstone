import unittest
import sqlite3
import os
import pandas as pd
from animal_shelter import AnimalShelter

class TestAnimalShelter(unittest.TestCase):
    def setUp(self):
        self.db_path = 'test_animals.db'
        self.shelter = AnimalShelter(self.db_path)

    def tearDown(self):
        # Remove the test database file after each test
        os.remove(self.db_path)

    def test_create_table(self):
        # Check if the 'animals' table is created
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='animals'")
            result = cursor.fetchone()
            self.assertIsNotNone(result)

    def test_read_all_data(self):
        # Test reading all data from the 'animals' table
        data = self.shelter.read()
        self.assertIsInstance(data, pd.DataFrame)
        self.assertGreater(len(data), 0)

    def test_read_with_query(self):
        # Test reading data with a specific query
        query = ["animal_type = ?", ("Dog",)]
        data = self.shelter.read(query)
        self.assertIsInstance(data, pd.DataFrame)
        self.assertTrue(all(data['animal_type'] == 'Dog'))

if __name__ == '__main__':
    unittest.main()
