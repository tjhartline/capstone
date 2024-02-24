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
'''
import sqlite3

class AnimalShelter(object):
    def __init__(self, db_path=':memory:'):
        self.db_path = db_path
        self._create_table()

    def _create_table(self):
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
                age_upon_outcome_in_weeks REAL,
                rescue_type TEXT
            )
        '''
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(query_str)

    def unq_animal_types(self):
        query_str = 'SELECT DISTINCT animal_type FROM animals'

        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(query_str)
            result = cursor.fetchall()

        return [row[0] for row in result]

    def createOne(self, data):
        '''
        Implement the C in CRUD.
        Insert document into the specified SQLite table.
        '''
        if data:
            # Extract breed from the data
            breed = data.get('breed', 'N/A')

            # Categorize rescue type based on breed
            if breed in ['Labrador Retriever Mix', 'Chesapeake Bay Retriever', 'Newfoundland']:
                data['rescue_type'] = 'water'
            elif breed in ['German Shepard', 'Alaskan Malamute', 'Old English Sheepdog', 'Siberian Husky', 'Rottweiler']:
                data['rescue_type'] = 'mountain'
            elif breed in ['Doberman Pinscher', 'German Shepard', 'Golden Retriever', 'Bloodhound', 'Rottweiler']:
                data['rescue_type'] = 'disaster'
            else:
                data['rescue_type'] = 'unknown'  # Handle other breeds

            # Insert the data into the SQLite table
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                placeholders = ', '.join(['?' for _ in data])
                columns = ', '.join(data.keys())
                values = tuple(data.values())
                query_str = f'INSERT INTO animals ({columns}) VALUES ({placeholders})'
                cursor.execute(query_str, values)
                conn.commit()

            return True
        else:
            print('\nNothing to save, data parameter is empty.')
            return False

    def read(self, query=None):
        query_str = 'SELECT * FROM animals'
        params = None

        if query is not None:
            query_str += f" WHERE {query[0]}"
            params = query[1]

        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()

            if params is not None:
                cursor.execute(query_str, params)
            else:
                cursor.execute(query_str)

            result = cursor.fetchall()

        columns = [
            'animal_id', 'age_upon_outcome', 'animal_type', 'breed', 'color',
            'date_of_birth', 'datetime', 'monthyear', 'name', 'outcome_subtype',
            'outcome_type', 'sex_upon_outcome', 'location_lat', 'location_long',
            'age_upon_outcome_in_weeks', 'rescue_type'
        ]
        records = [dict(zip(columns, row)) for row in result]
        return records

    def update(self, query, update_data, multi=False):
        '''
        Implement the U in CRUD
        Update option
        '''
        if query:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                set_clause = ', '.join([f"{key} = ?" for key in update_data.keys()])
                query_str = f'UPDATE animals SET {set_clause} WHERE {query[0]}'
                params = tuple(update_data.values()) + query[1] if multi else (tuple(update_data.values()), *query[1])
                result = cursor.execute(query_str, params)
                conn.commit()
                print('\n\n')
                return result.rowcount
        else:
            print('\nQuery parameter is empty')
            return 0

    def delete(self, query, multi=False):
        '''
        Implement the D in CRUD.
        Options should be to delete one or delete many.
        '''
        if query:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                query_str = f'DELETE FROM animals WHERE {query[0]}'
                params = query[1] if multi else (query[1],)
                result = cursor.execute(query_str, params)
                conn.commit()
                print('\n\n')
                return result.rowcount
        else:
            print('\nQuery parameter is empty')
            return 0
