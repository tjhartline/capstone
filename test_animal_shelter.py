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
        os.remove(self.db_path)

    def test_create_table(self):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='animals'")
            table_exists = cursor.fetchone() is not None
            self.assertTrue(table_exists)

    def test_create_index(self):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT name FROM sqlite_master WHERE type='index' AND name='idx_animal_type'")
            index_exists = cursor.fetchone() is not None
            self.assertTrue(index_exists)

    def test_create_record(self):
        data = {
            'name': 'Max',
            'animal_type': 'Dog',
            'breed': 'Labrador',
            'age': 3,
            'outcome_type': 'Adoption',
            'outcome_subtype': 'Foster',
            'sex_upon_outcome': 'Neutered Male',
        }
        self.shelter.create(data)
        result = self.shelter.read(("name = ?", ('Max',)))
        self.assertEqual(len(result), 1)
        self.assertEqual(result.iloc[0]['name'], 'Max')

    def test_read_all_data(self):
        data = self.shelter.read()
        self.assertIsInstance(data, pd.DataFrame)
        self.assertGreater(len(data), 0)

    def test_read_with_valid_query(self):
        query = ("animal_type = ?", ("Dog",))
        data = self.shelter.read(query)
        self.assertIsInstance(data, pd.DataFrame)
        self.assertTrue(all(data['animal_type'] == 'Dog'))

    def test_read_with_invalid_query_format(self):
        query = "invalid query"
        with self.assertRaises(ValueError):
            self.shelter.read(query)

    def test_read_with_invalid_query_condition(self):
        query = ("", ("Dog",))
        with self.assertRaises(ValueError):
            self.shelter.read(query)

    def test_read_with_invalid_query_parameters(self):
        query = ("animal_type = ?", "Dog")
        with self.assertRaises(ValueError):
            self.shelter.read(query)

    def test_read_with_sql_injection_attempt(self):
        query = ("animal_type = ?; DROP TABLE animals; --", ("Dog",))
        data = self.shelter.read(query)
        self.assertIsInstance(data, pd.DataFrame)
        self.assertTrue(all(data['animal_type'] == 'Dog'))
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='animals'")
            table_exists = cursor.fetchone() is not None
            self.assertTrue(table_exists)

    def test_update_record(self):
        data = {
            'name': 'Max',
            'animal_type': 'Dog',
            'breed': 'Labrador',
            'age': 3,
            'outcome_type': 'Adoption',
            'outcome_subtype': 'Foster',
            'sex_upon_outcome': 'Neutered Male',
        }
        self.shelter.create(data)
        updated_data = {'age': 4}
        self.shelter.update(("name = ?", ('Max',)), updated_data)
        result = self.shelter.read(("name = ?", ('Max',)))
        self.assertEqual(result.iloc[0]['age'], 4)

    def test_delete_record(self):
        data = {
            'name': 'Max',
            'animal_type': 'Dog',
            'breed': 'Labrador',
            'age': 3,
            'outcome_type': 'Adoption',
            'outcome_subtype': 'Foster',
            'sex_upon_outcome': 'Neutered Male',
        }
        self.shelter.create(data)
        self.shelter.delete(("name = ?", ('Max',)))
        result = self.shelter.read(("name = ?", ('Max',)))
        self.assertEqual(len(result), 0)

if __name__ == '__main__':
    unittest.main()
