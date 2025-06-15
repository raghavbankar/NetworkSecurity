from dataclasses import dataclass

@dataclass
class DataIngestionArtifact:
    trained_file_path:str
    test_file_path:str

@dataclass
class DataValidationArtifact:
    Data_validation_status:bool
    train_valid_filepath:str
    test_valid_filepath:str
    train_invalid_filepath:str
    test_invalid_filepath:str
    Drift_file_report_path:str

@dataclass
class DataTransformationArtifacts:
    transformed_object_file_path:str
    transformed_train_data:str
    transformed_test_data:str

@dataclass
class ClassificationMetrics:
    f1_score:float
    precision_score:float
    recall_score:float

@dataclass
class ModelTrainerArtifact:
    trained_model_file_path:str
    train_metric_artifacts:ClassificationMetrics
    test_metric_artifacts:ClassificationMetrics