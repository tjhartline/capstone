# animal_shelter.py
'''
|*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*|
|  ******** Author:          Tammy Hartline                                                                 |
|  ******** Version:         2.0.9                                                                          |
|  ******** Description:     Module file for animal shelter application.                                    |
|*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*|
|                                            Changelog:                                                     |
|*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*|
|  ###  Start -- 01/2024 - TH                                                                               |
|  [Altered the database from MongoDB to SQlite3 file storage database structure to be more efficient and   |
|  less "overkill" given the program only handles a single .csv file for the dashboard application.]        |
|  ### - End                                                                                                |
|*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*|
|  ###  Start -- 02/2024 - TH                                                                               |
|  [Updated each method to conform with SQlite3 syntax and structure and to optimize the queries.]          |
|  ### - End                                                                                                |
|*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*|
|  ###  Start -- 02/2024 - TH                                                                               |
|  [Removed some of the non-working CRUD methods, after several failed attempts to get them to work         |
|  using SQLite. Some that did not work were the update and delete methods. Intend to add them back once    |
|  the development is further along.]                                                                       |
|  ### - End                                                                                                |
|*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*|
|  ###  Start --02/2024 - TH                                                                                |
|  [Adding methods back in an attempt to complete the program with all of its original functionality        |
|  and features, and the enhancements working correctly.]                                                   |
|  ### - End                                                                                                |
|*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*|
|  ###  Start --02/2024 - TH                                                                                |
|  [Adding the unq_animal_types method to define a new column. Note, this was the issue in the app file     |
|  causing it not to launch on the server when running the main app.py file.]                               |
|  ### - End                                                                                                |
|*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*|
|  ###  Start --02/2024 - TH                                                                                |
|  [Finally removed unneeded methods and cleaned up code file to launch MVP.]                               |
|  ### - End                                                                                                |
|*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*|
'''
# Import required libraries
import sqlite3
import pandas as pd
import os

# Create animal shelter class
class AnimalShelter(object):
    def __init__(self, db_path=':memory:'):
        self.db_path = db_path
        self._create_table()


    # create table to store data using SQLite 
    def _create_table(self):
        # if the database is in memory, there is no need to create a table
        if self.db_path == ':memory:':
            db_file = "animals.db"
            # if the database file exists, there is no need to create a table
            if os.path.exists(db_file):
                return

        # checking if table exists and if not, create it with all the columns located in the csv file    
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
        # connect to sqlite3, create table and read in the csv file
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(query_str)
            df = pd.read_csv("./aac_shelter_outcomes.csv")
            df.to_sql('animals', conn, if_exists='replace', index=False)
                

    # Create a read method for querying the database
    def read(self, query=None):
        query_str = 'SELECT * FROM animals'
        params = None

        # if there is a query, add it to the query string
        if query is not None:
            query_str += f" WHERE {query[0]}"
            params = query[1]

        # connect to sqlite3 and read in the query
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()

            # if there are parameters, use them in the query
            if params is not None:
                df = pd.read_sql_query(query_str, conn, params=params)

            # if there are no parameters, just run the query
            else:
                df = pd.read_sql_query(query_str, conn)
            return df
