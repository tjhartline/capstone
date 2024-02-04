import os
import pandas as pd
from pymongo import MongoClient

username = os.getenv('MONGO_USERNAME')
pwd = os.getenv('MONGO_PASSWORD')
host = os.getenv('MONGO_HOST')
db_name = os.getenv('MONGO_DB')
col_name = os.getenv('MONGO_COLLECTION')
csv_filename = 'aac_animal_outcomes.csv'  # Updated CSV file name

# Get the current directory of the script
script_dir = os.path.dirname(os.path.realpath(__file__))

# Construct the full path to the CSV file within the repository
csv_path = os.path.join(script_dir, 'data', csv_filename)

client = MongoClient(f'mongodb+srv://{username}:{pwd}@{host}/{db_name}')
db = client[db_name]
collection = db[col_name]

df = pd.read_csv(csv_path)
data_dict = df.to_dict(orient='records')

# Clear existing data in the collection and insert new data
collection.delete_many({})
collection.insert_many(data_dict)
