# animal_shelter.py
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
                age_upon_outcome_in_weeks REAL
            )
        '''
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(query_str)

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
            'age_upon_outcome_in_weeks'
        ]
        records = [dict(zip(columns, row)) for row in result]
        return records
