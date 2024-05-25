# animal_shelter.py
'''
|*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*|
|  ******** Author:          Tammy Hartline                                                                 |
|  ******** Version:         2.0.9                                                                          |
|  ******** Description:     Module file for animal shelter application.                                    |
|*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*|
|                                            Changelog:                                                     |
|*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*|
|  ###  Start -- 05/2024 - TH                                                                               |
|  [Altered the database from MongoDB to SQlite3 file storage database structure to be more efficient and   |
|  less "overkill" given the program only handles a single .csv file for the dashboard application.]        |
|  ### - End                                                                                                |
|*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*|
|  ###  Start -- 05/2024 - TH                                                                               |
|  [Updated each method to conform with SQlite3 syntax and structure and to optimize the queries.]          |
|  ### - End                                                                                                |
|*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*|
|  ###  Start -- 05/2024 - TH                                                                               |
|  [Removed some of the non-working CRUD methods, after several failed attempts to get them to work         |
|  using SQLite. Some that did not work were the update and delete methods. Intend to add them back once    |
|  the development is further along.]                                                                       |
|  ### - End                                                                                                |
|*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*|
|  ###  Start -- 05/2024 - TH                                                                                |
|  [Adding methods back in an attempt to complete the program with all of its original functionality        |
|  and features, and the enhancements working correctly.]                                                   |
|  ### - End                                                                                                |
|*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*|
|  ###  Start -- 05/2024 - TH                                                                                |
|  [Adding the unq_animal_types method to define a new column. Note, this was the issue in the app file     |
|  causing it not to launch on the server when running the main app.py file.]                               |
|  ### - End                                                                                                |
|*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*|
|  ###  Start -- 05/2024 - TH                                                                                |
|  [Finally removed unneeded methods and cleaned up code file to launch MVP.]                               |
|  ### - End                                                                                                |
|*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*|
'''
# Import required libraries
import sqlite3
import pandas as pd
import os

class AnimalShelter(object):
    def __init__(self, db_path=':memory:'):
        self.db_path = db_path
        self._create_table()
        self._create_index()

    def _create_table(self):
        if self.db_path == ':memory:':
            db_file = "animals.db"
            if os.path.exists(db_file):
                return

        query_str = '''
            CREATE TABLE IF NOT EXISTS animals (
                animal_id INTEGER PRIMARY KEY,
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
                sex_upon_outcome TEXT,
                location_lat REAL,
                location_long REAL,
                age_upon_outcome_in_weeks REAL
            )
        '''
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(query_str)
            df = pd.read_csv("./aac_shelter_outcomes.csv")
            df.to_sql('animals', conn, if_exists='replace', index=False)

    def _create_index(self):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_animal_type ON animals (animal_type)')
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_outcome_type ON animals (outcome_type)')

    def read(self, query=None):
        query_str = 'SELECT * FROM animals'
        params = None

        if query is not None:
            # Input validation and sanitization
            if not isinstance(query, tuple) or len(query) != 2:
                raise ValueError("Invalid query format. Expected a tuple of length 2.")
            
            query_condition, query_params = query
            if not isinstance(query_condition, str) or not query_condition.strip():
                raise ValueError("Invalid query condition. Expected a non-empty string.")
            
            if not isinstance(query_params, tuple):
                raise ValueError("Invalid query parameters. Expected a tuple.")
            
            # Sanitize the query condition to prevent SQL injection
            query_condition = query_condition.replace(';', '').replace('--', '')
            
            query_str += f" WHERE {query_condition}"
            params = query_params

        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()

                if params is not None:
                    df = pd.read_sql_query(query_str, conn, params=params)
                else:
                    df = pd.read_sql_query(query_str, conn)
                return df
        except sqlite3.Error as e:
            # Proper error handling
            print(f"An error occurred while executing the query: {e}")
            return None
