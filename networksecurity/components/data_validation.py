from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging

#from networksecurity.components.data_ingestion import Data_Ingestion
from networksecurity.entity.config_entity import Data_Validation_Config
from networksecurity.entity.artifact_entity import DataIngestionArtifact,DataValidationArtifact
from networksecurity.constant.Training_pipeline import DATA_SCHEMA_FILE_PATH
from networksecurity.Utils.utils_main.utils import read_yaml_file,write_yaml_file
import pandas as pd
import numpy as np
from scipy.stats import ks_2samp
import sys
import os

class Data_validation:
    def __init__(self,data_ingestion_artifact:DataIngestionArtifact,
                 data_validation_config:Data_Validation_Config,
                ):
        
        try:
            self.data_ingestion_artifact=data_ingestion_artifact
            self.data_validation_config=data_validation_config
            self.schmea_config=read_yaml_file(DATA_SCHEMA_FILE_PATH)
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        
    @staticmethod
    def read_data(file_path):
        try:
            return pd.read_csv(file_path)
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        
    def Validate_no_of_columns(self,dataframe:pd.DataFrame):
        try:
            _schema_len= len(self.schmea_config)
            logging.info(f"The length of the schema is {-_schema_len}")
            logging.info(f"The length of the dataframe is {len(dataframe)}")
            if(_schema_len==len(dataframe)):
                return True
            else:
                return False
            
        except Exception as e:
            raise NetworkSecurityException(e,sys)
    
    def validate_numerical_columns(self,dataframe:pd.DataFrame):
        try:
            schema_num_columns=len(self.schmea_config["numerical_columns"])
            logging.info("The number of num columns in schema is {schema_num_columns}")
            num_columns_dataframe=len(dataframe.select_dtypes(include='int').columns)
            logging.info("The number of num column in the dataframe is {num_columns_dataframe}")
            if(schema_num_columns==num_columns_dataframe):
                return True
            else:
                return False
        except Exception as e:
            raise NetworkSecurityException(e,sys)
    
    def Check_dataset_drift(self,base_data,cur_data,threshold=0.05)->bool:
        try:
            report={}
            status=True
            for columns in base_data.columns:
                d1=base_data[columns]
                d2=cur_data[columns]
                is_same_value=ks_2samp(d1,d2)
                if threshold<=is_same_value.pvalue:
                    is_found=False
                else:
                    is_found=True
                    status=False
                
                report.update({
                    columns:{
                        "pvalue":is_same_value.pvalue,
                        "drift_status":is_found,
                    }})
            drif_report_file_path=self.data_validation_config.drift_report_path
            dir_path=os.path.dirname(drif_report_file_path)
            os.makedirs(dir_path,exist_ok=True)

            write_yaml_file(drif_report_file_path,report)
            return status
        except Exception as e:
            raise NetworkSecurityException(e,sys)
       
    def initiate_validation(self)->DataValidationArtifact:
        try:
            #Reading Test and Train data from Artifact
            train_dataframe=Data_validation.read_data(self.data_ingestion_artifact.trained_file_path)
            test_dataframe=Data_validation.read_data(self.data_ingestion_artifact.test_file_path)
            status=self.Validate_no_of_columns(train_dataframe)
            if not status:
                error_message="The Train Data is does not contain all columns.\n"
            status=self.Validate_no_of_columns(test_dataframe)
            if not status:
                error_message="The Test Data does not contain all columns.\n"
            status1=self.validate_numerical_columns(train_dataframe)
            if not status1:
                error_message="The Train Data is does not contain all numericals columns.\n"
            status1=self.validate_numerical_columns(test_dataframe)
            if not status1:
                error_message="The Test Data does not contain all numericals columns.\n"
            
            #Data drift checking

            status=self.Check_dataset_drift(train_dataframe,test_dataframe)

            dir_path=os.path.dirname(self.data_validation_config.train_valid_data)
            os.makedirs(dir_path,exist_ok=True)

            train_dataframe.to_csv(self.data_validation_config.train_valid_data,index=False,header=True)
            test_dataframe.to_csv(self.data_validation_config.test_valid_data,index=False,header=True)

            validation_artifact=DataValidationArtifact(
                Data_validation_status=status,
                train_valid_filepath=self.data_ingestion_artifact.trained_file_path,
                test_valid_filepath=self.data_ingestion_artifact.test_file_path,
                train_invalid_filepath=None,
                test_invalid_filepath=None,
                Drift_file_report_path=self.data_validation_config.drift_report_path
            )
            return validation_artifact
        except Exception as e:
            raise NetworkSecurityException(e,sys)


