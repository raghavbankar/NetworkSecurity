from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging
from networksecurity.components.data_ingestion import Data_Ingestion
from networksecurity.components.data_validation import Data_validation
from networksecurity.components.Model_trainer import ModelTrainer
from networksecurity.components.data_transfromation import Data_transformation
from networksecurity.entity.config_entity import Data_Ingestion_Config,Data_Validation_Config,Data_transform_config,Model_trainer_config
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

        data_transformation_config=Data_transform_config(training_pipelineconfig)
        data_transform=Data_transformation(data_validation_artifacts,data_transformation_config)
        logging.info("Data Transformation Initiated")
        data_transform_artifacts=data_transform.initiate_transformation()
        logging.info("Data Transformation Completed")
        print(data_transform_artifacts)

        logging.info("Model training Started")
        model_trainer_config = Model_trainer_config(training_pipelineconfig)
        model_trainer = ModelTrainer(model_trainer_config,data_transform_artifacts)
        model_trainer_artifact=model_trainer.initiate_model_trainer()

        logging.info("Model training artifact created")

    except Exception as e:
        raise NetworkSecurityException(e,sys)
    