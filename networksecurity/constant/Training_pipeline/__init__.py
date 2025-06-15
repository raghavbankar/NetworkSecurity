import os
import sys
import pandas as pd
import numpy as np

"""
defining common constants variable for training pipeline
"""

TARGET_COLUMN="Result"
PIPELINE_NAME:str = "NetworkSecurity"
ARTIFACT_DIR: str = "Artifacts"
FILE_NAME:str ="phisingData.csv"
TRAIN_FILE_NAME:str = "train.csv"
TEST_FILE_NAME:str = "test.csv"
DATA_SCHEMA_FILE_PATH:str = os.path.join('Data_schema',"schema.yaml")

"""
Data Ingestion related constant start with DATA_INGESTION VAR NAME
"""
DATA_INGESTION_COLLECTION:str = "NetworkData"
DATA_INGESTION_DATABASE:str = "RaghavML"
DATA_INGESTION_DIR_NAME:str = "data_ingestion"
DATA_INGESTION_FEATURE_STORE_DIR:str = "feature_store"
DATA_INGESTION_INGESTED_DIR:str = "ingested"
DATA_INGESTION_TRAIN_TEST_SPLIT_RATIO:float = 0.2

"""Data validation constants"""

DATA_VALIDATION_DIR_NAME:str = "Data_Validation"
DATA_VALIDATION_VALID:str = "valid_Data"
DATA_VALIDATION_INVALID:str = "Invalid_Data"
DATA_VALIDATION_DRIFT_REPORT_DIR:str = "Drift_report"
DATA_VALIDATION_DRIFT_NAME:str = "report.yaml"

"""Data transformation constants"""

DATA_TRANSFORMATION_DIR_NAME:str = "Data_Transformation"
DATA_TRANSFORMATION_DATA_DIR:str = "Transformed"
DATA_TRANSFORMATION_OBJECT_DIR:str = "Transformed_object"
PREPROCESSING_OBJECT_FILE_NAME = "preprocessing.pkl"

## kkn imputer to replace nan values
DATA_TRANSFORMATION_IMPUTER_PARAMS: dict = {
    "missing_values": np.nan,
    "n_neighbors": 3,
    "weights": "uniform",
}

MODEL_TRAINER_DIR_NAME="Model_Trainer"
MODEL_TRAINER_TRAINED_MODEL_DIR="Trained_model"
MODEL_TRAINER_File_Name="Model.pkl"

EXPECTED_ACCURACY:float=0.6
MODEL_TRAINER_OVER_FITTING_UNDER_FITTING_THRESHOLD:float=0.05
