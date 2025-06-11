import sys,os
import pandas as pd
import numpy as np
from sklearn.impute import KNNImputer
from sklearn.pipeline import Pipeline

from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging

from networksecurity.entity.artifact_entity import DataValidationArtifact,DataTransformationArtifacts
from networksecurity.entity.config_entity import Data_Validation_Config,Data_transform_config
from networksecurity.entity.config_entity import Training_pipelineConfig

from networksecurity.constant.Training_pipeline import DATA_TRANSFORMATION_IMPUTER_PARAMS
from networksecurity.constant.Training_pipeline import TARGET_COLUMN

from networksecurity.Utils.utils_main.utils import save_numpy,save_object

class Data_transformation:
    def __init__(self,data_validation_artifacts:DataValidationArtifact,data_transfromation_config:Data_transform_config):
        try:
            self.data_validation_artifacts=data_validation_artifacts
            self.data_transformation_config=data_transfromation_config
        except Exception as e:
            raise NetworkSecurityException(e,sys)
    
    def get_preprocessor_object(self)->Pipeline:
        """
        This function is used to implement the KNNimputer 
        return pipeline object
        """
        try:
            imputer:KNNImputer=KNNImputer(**DATA_TRANSFORMATION_IMPUTER_PARAMS)
            preprocessor:Pipeline=Pipeline([("Imputer",imputer)])
            logging.info("Preprocessor object Created")
            return preprocessor
        except Exception as e:
            raise NetworkSecurityException(e,sys)
    def initiate_transformation(self):
        try:
            logging.info("Transformation Started")
            #reading the data from validation artifacts
            train_data=pd.read_csv(self.data_validation_artifacts.train_valid_filepath)
            test_data=pd.read_csv(self.data_validation_artifacts.test_valid_filepath)
            #droping the target feature
            train_features=train_data.drop(columns=TARGET_COLUMN,axis=1)
            train_target=train_data[TARGET_COLUMN]
            train_target=train_target.replace(-1,0)

            test_features=test_data.drop(columns=TARGET_COLUMN,axis=1)
            test_target=test_data[TARGET_COLUMN]
            test_target=test_target.replace(-1,0)
            #Preprocessing fitting operations
            logging.info("Preprocessing Started")
            preprocessor=self.get_preprocessor_object()

            preprocessor_object=preprocessor.fit(train_features)
            transformed_train_features=preprocessor_object.transform(train_features)
            transformed_test_features=preprocessor_object.transform(test_features)

            logging.info("Preprocessing Completed")

            transformed_train_df=np.c_[transformed_train_features,np.array(train_target)]
            transfromed_test_df=np.c_[transformed_test_features,np.array(test_target)]

            #Saving the numpy array into file
            save_numpy(file_path=self.data_transformation_config.data_transform_train_file_path,array=transformed_train_df)
            save_numpy(file_path=self.data_transformation_config.data_transform_test_file_path,array=transfromed_test_df)
            save_object(file_path=self.data_transformation_config.data_transform_processed_object_file,obj=preprocessor_object)

            transform_artifacts=DataTransformationArtifacts(
                transformed_object_file_path=self.data_transformation_config.data_transform_processed_object_file,
                transformed_train_data=self.data_transformation_config.data_transform_train_file_path,
                transformed_test_data=self.data_transformation_config.data_transform_test_file_path
            )
            logging.info("transformation completed")
            return transform_artifacts
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        

