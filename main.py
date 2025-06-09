from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging
from networksecurity.components.data_ingestion import Data_Ingestion
from networksecurity.components.data_validation import Data_validation
from networksecurity.entity.config_entity import Data_Ingestion_Config,Data_Validation_Config
from networksecurity.entity.config_entity import Training_pipelineConfig
import sys

if __name__=='__main__':
    try:
        training_pipelineconfig=Training_pipelineConfig()
        data_ingestion_config=Data_Ingestion_Config(training_pipelineconfig)
        data_ingestion=Data_Ingestion(data_ingestion_config)
        
        logging.info("Initiate the data ingestion")
        data_ingestion_artifact=data_ingestion.initiate_Data_Ingestion()
        logging.info("Data ingestion completed")
        print(data_ingestion_artifact)

        data_validation_config=Data_Validation_Config(training_pipelineconfig)
        data_validation=Data_validation(data_ingestion_artifact,data_validation_config)
        logging.info("Data Validation Initiated")
        data_validation_artifacts=data_validation.initiate_validation()
        logging.info("Data Validation completed")
        print(data_validation_artifacts)
    except Exception as e:
        raise NetworkSecurityException(e,sys)
    