from pymongo import MongoClient
import os

class AnimalShelter(object):
    '''
    Begin CRUD implementation
    '''
    def __init__(self, username, pwd, host, port, db, col):
        uri = f'mongodb://{username}:{pwd}@{host}:{port}/{db}'
        self.client = MongoClient(uri)
        self.database = self.client[db]
        self.collection = self.database[col]

    def createOne(self, data):
        '''
        Implement the C in CRUD.
        Insert document into the specified MongoDB collection.
        '''
        if data:
            result = self.collection.insert_one(data)
            return True if result.inserted_id else False
        else:
            print('\nNothing to save, data parameter is empty.')
            return False

    def createMany(self, datas):
        '''
        Implement C but for more than 1 insertion
        '''
        if datas:
            result = self.collection.insert_many(datas)
            return True if result.inserted_ids else False
        else:
            print('\nNothing to save, data parameter is empty.')
            return False

    def read(self, query):
        print(f'\nQuery received: {query}, type: {type(query)}')  # Debugging line
        '''
        Implement the R in CRUD.
        Query documents from the specified MongoDB collection.
        '''

        if query is not None:  # This will be True for an empty dictionary
            result = list(self.collection.find(query))

            # Iterate through the results and categorize breeds
            categorized_results = []
            for doc in result:
                # Add breed categorization logic here based on your criteria
                breed = doc.get('breed', 'N/A')
                if breed in ['Labrador Retriever Mix', 'Chesapeake Bay Retriever', 'Newfoundland']:
                    doc['rescue_type'] = 'water'
                elif breed in ['German Shepard', 'Alaskan Malamute', 'Old English Sheepdog', 'Siberian Husky', 'Rottweiler']:
                    doc['rescue_type'] = 'mountain'
                elif breed in ['Doberman Pinscher', 'German Shepard', 'Golden Retriever', 'Bloodhound', 'Rottweiler']:
                    doc['rescue_type'] = 'disaster'
                else:
                    doc['rescue_type'] = 'unknown'  # Handle other breeds

                categorized_results.append(doc)

            print('\n')  # Add a newline before printing the results
            for doc in categorized_results:
                print(doc)
            print('\n')  # Add a newline after printing the results

            return categorized_results if categorized_results else []
        else:
            print('\nQuery parameter is empty. Nothing read. Test Failed.')
            return []

    def update(self, query, update_data, multi=False):
        '''
        Implement the U in CRUD
        Update option
        '''
        if query:
            if multi:
                result = self.collection.update_many(query, {"$set": update_data})
                print('\n\n')
            else:
                result = self.collection.update_one(query, {"$set": update_data})
                print('\n\n')
            return result.modified_count
        else:
            print('\nQuery parameter is empty')
            return 0

    def delete(self, query, multi=False):
        '''
        Implement the D in CRUD.
        Options should be to delete one or delete many.
        '''
        if query:
            if multi:
                result = self.collection.delete_many(query)
                print('\n\n')
            else:
                result = self.collection.delete_one(query)
                print('\n\n')
            return result.deleted_count
        else:
            print('\nQuery parameter is empty')
            return 0

