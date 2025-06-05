import json
import os
import sys
from dotenv import load_dotenv
load_dotenv()
Mongo_db_url=os.getenv("MONGO_DB")
print(Mongo_db_url)

import certifi
ca=certifi.where()

import pandas as pd
import numpy as np
import pymongo
from networksecurity.logging import logger
from networksecurity.exception.exception import NetworkSecurityException

class Network_data():
    def __init__(self):
        try:
            pass
        except Exception as e:
            raise NetworkSecurityException(e,sys)

    def csv_to_json(self,file_path):
        try:
            data=pd.read_csv(file_path)
            data.reset_index(inplace=True,drop=True)
            ##Recored is the list of json(key value pair of the data set)
            record=list(json.loads(data.T.to_json()).values())
            return record
        except Exception as e:
            raise NetworkSecurityException(e,sys)
     
    
    def data_to_mongo(self,records,database,collection):
        try:
            self.database = database
            self.collection=collection
            self.records = records

            self.mongo_client =pymongo.MongoClient(Mongo_db_url)
            self.database = self.mongo_client[self.database]

            self.collection = self.database[self.collection]
            self.collection.insert_many(self.records)
            return (len(self.records))
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        
if __name__=='__main__':
    File_path =r'E:\projects\project2\Network_Data\phisingData.csv'
    Database="RaghavML"
    Collection="NetworkData"
    networkobj=Network_data()
    records=networkobj.csv_to_json(File_path)
    no_of_records=networkobj.data_to_mongo(records,Database,Collection)
    print(no_of_records)


    