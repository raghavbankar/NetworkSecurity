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