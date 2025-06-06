import os
import sys

import pymongo.mongo_client
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging

#Importing Configuration classs
from networksecurity.entity.config_entity import Data_Ingestion_Config
from networksecurity.entity.artifact_entity import DataIngestionArtifact
import pymongo
import pandas as pd
import numpy as np
from dotenv import load_dotenv
from typing import List
from sklearn.model_selection import train_test_split

load_dotenv()

MONGODB_URL= os.getenv("MONGO_DB")

class Data_Ingestion:
    def __init__(self,data_ingestion_config:Data_Ingestion_Config):
       try: 
        self.data_ingestion_config = data_ingestion_config
       except Exception as e:
          raise NetworkSecurityException(e,sys)
       
    def export_collection_as_dataframe(self):
       """Read Data from MongoDB"""
       try: 
            database_name = self.data_ingestion_config.Database_name
            collection_name = self.data_ingestion_config.collection_name
            self.Mongo_client = pymongo.MongoClient(MONGODB_URL)
            collection=self.Mongo_client[database_name][collection_name]

            df=pd.DataFrame(list(collection.find()))
            if "_id" in df.columns.to_list():
               df=df.drop(columns=["_id"],axis=1)
            
            df.replace({"na":np.nan},inplace=True)
            
            return df
       except Exception as e:
          raise NetworkSecurityException(e,sys)
    
    def export_data_to_feature_store(self,dataframe:pd.DataFrame):
       try:
           feature_path = self.data_ingestion_config.data_ingestion_feature_store
           #making folder
           dir_path=os.path.dirname(feature_path)
           os.makedirs(dir_path,exist_ok=True)
           dataframe.to_csv(self.data_ingestion_config.data_ingestion_feature_store,index=False,header=True)
           return dataframe

       except Exception as e:
          raise NetworkSecurityException(e,sys)
       
    def split_data_train_test(self,dataframe:pd.DataFrame):
       try:
          train_data,test_data= train_test_split(dataframe,test_size=self.data_ingestion_config.train_test_split_ratio)
          logging.info("Performed Train test split")
          train_data=pd.DataFrame(train_data)
          test_data=pd.DataFrame(test_data)
          #making folder
          dir_path_train=os.path.dirname(self.data_ingestion_config.training_file_path)
          os.makedirs(dir_path_train,exist_ok=True)

          dir_path_test=os.path.dirname(self.data_ingestion_config.testing_file_path)
          os.makedirs(dir_path_test,exist_ok=True)
          
          train_data.to_csv(self.data_ingestion_config.training_file_path,index=False,header=True)
          test_data.to_csv(self.data_ingestion_config.testing_file_path,index=False,header=True)

          logging.info("Exported Train and Test data")

       except Exception as e:
          raise NetworkSecurityException(e,sys)
        
    def initiate_Data_Ingestion(self):
       try:
          dataframe = self.export_collection_as_dataframe()
          dataframe=self.export_data_to_feature_store(dataframe)
          self.split_data_train_test(dataframe)
          ingestion_artifact=DataIngestionArtifact(trained_file_path=self.data_ingestion_config.training_file_path,
                                                   test_file_path=self.data_ingestion_config.testing_file_path)
          return ingestion_artifact
       except Exception as e:
          raise NetworkSecurityException(e,sys)
        