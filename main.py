from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging import logger
from networksecurity.components.data_ingestion import Data_Ingestion
from networksecurity.entity.config_entity import Data_Ingestion_Config
from networksecurity.entity.config_entity import Training_pipelineConfig
import sys

if __name__=='__main__':
    try:
        training_pipelineconfig=Training_pipelineConfig()
        data_ingestion_config=Data_Ingestion_Config(training_pipelineconfig)
        data_ingestion=Data_Ingestion(data_ingestion_config)
        data_ingestion_artifact=data_ingestion.initiate_Data_Ingestion()
        print(data_ingestion_artifact)
    except Exception as e:
        raise NetworkSecurityException(e,sys)
    