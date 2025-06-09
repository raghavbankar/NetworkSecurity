
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging

#from networksecurity.components.data_ingestion import Data_Ingestion
from networksecurity.entity.config_entity import Data_Validation_Config
from networksecurity.entity.artifact_entity import DataIngestionArtifact,DataValidationArtifact
from networksecurity.constant.Training_pipeline import DATA_SCHEMA_FILE_PATH
from networksecurity.Utils.utils_main.utils import read_yaml_file
import pandas as pd
import numpy as np
from scipy.stats import ks_2samp
import sys
import os

class Data_validation:
    def __init__(self):
        try:
            self.schmea_config=read_yaml_file(file_path=DATA_SCHEMA_FILE_PATH)
        except Exception as e:
            raise NetworkSecurityException(e,sys)
    
    def validate_numerical_columns(self,dataframe:pd.DataFrame):
        schema_num_columns=len(self.schmea_config["numerical_columns"])
       
        num_columns_dataframe=len(dataframe.select_dtypes(include='int').columns)
    
        if(schema_num_columns==num_columns_dataframe):
            return True
        else:
            return False
    


if __name__ == "__main__":
    Data=Data_validation()
    train_dataframe=pd.read_csv(r"E:\projects\project2\Artifacts\06_06_2025_11_57_59\data_ingestion\ingested\train.csv")
    test_dataframe=pd.read_csv(r"E:\projects\project2\Artifacts\06_06_2025_11_57_59\data_ingestion\ingested\test.csv")
    print(len(Data.schmea_config["numerical_columns"]))
    x=Data.validate_numerical_columns(train_dataframe)
    y=Data.validate_numerical_columns(test_dataframe)

    print(x,y)