import os
import sys
from datetime import datetime
from networksecurity.constant import Training_pipeline

class Training_pipelineConfig:
    def __init__(self,timestamp=datetime.now()):
        timestamp=timestamp.strftime("%m_%d_%Y_%H_%M_%S")
        self.artifacts_name=Training_pipeline.ARTIFACT_DIR
        self.pipeline_name=Training_pipeline.PIPELINE_NAME
        self.artifact_dir=os.path.join(self.artifacts_name,timestamp)
        self.timestam:str = timestamp
    
class Data_Ingestion_Config:
    def __init__(self,training_pipeline_config:Training_pipelineConfig):
        self.data_ingestion_dir:str =os.path.join(
            training_pipeline_config.artifact_dir,Training_pipeline.DATA_INGESTION_DIR_NAME
        )
        self.data_ingestion_feature_store:str=os.path.join(
            self.data_ingestion_dir,Training_pipeline.DATA_INGESTION_FEATURE_STORE_DIR
        )
        self.training_file_path:str = os.path.join(
            self.data_ingestion_dir,Training_pipeline.DATA_INGESTION_INGESTED_DIR,Training_pipeline.TRAIN_FILE_NAME
        )
        self.testing_file_path:str = os.path.join(
            self.data_ingestion_dir,Training_pipeline.DATA_INGESTION_INGESTED_DIR,Training_pipeline.TEST_FILE_NAME
        )
        self.train_test_split_ratio:float = Training_pipeline.DATA_INGESTION_TRAIN_TEST_SPLIT_RATIO
        self.Database_name:str = Training_pipeline.DATA_INGESTION_DATABASE
        self.collection_name:str = Training_pipeline.DATA_INGESTION_COLLECTION

class Data_Validation_Config:
    def __init__(self,training_pipeline_config:Training_pipelineConfig):
        self.data_validation_dir:str=os.path.join(training_pipeline_config.artifact_dir,Training_pipeline.DATA_VALIDATION_DIR_NAME)
        self.valid_data_dir:str=os.path.join(self.data_validation_dir,Training_pipeline.DATA_VALIDATION_VALID)
        self.invalid_data_dir:str=os.path.join(self.data_validation_dir,Training_pipeline.DATA_VALIDATION_INVALID)
        self.train_valid_data:str=os.path.join(self.valid_data_dir,Training_pipeline.TRAIN_FILE_NAME)
        self.test_valid_data:str=os.path.join(self.valid_data_dir,Training_pipeline.TEST_FILE_NAME)
        self.train_invalid_data:str=os.path.join(self.invalid_data_dir,Training_pipeline.TRAIN_FILE_NAME)
        self.test_invalid_data:str=os.path.join(self.invalid_data_dir,Training_pipeline.TEST_FILE_NAME)
        self.drift_report_path:str=os.path.join(self.data_validation_dir,Training_pipeline.DATA_VALIDATION_DRIFT_REPORT_DIR,Training_pipeline.DATA_VALIDATION_DRIFT_REPORT_DIR)
