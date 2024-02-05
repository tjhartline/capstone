import sqlite3

class AnimalShelter(object):
    def __init__(self, db_path='animals.db'):
        self.db_path = db_path
        self.create_table()  # Call create_table during initialization

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

# Example usage
shelter = AnimalShelter()

# Example usage of read method
all_animals = shelter.read()
for animal in all_animals[:5]:  # Displaying the first 5 records for example
    print(animal)
