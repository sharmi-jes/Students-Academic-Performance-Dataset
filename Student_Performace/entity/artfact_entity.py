


from dataclasses import dataclass

@dataclass
class DataIngestionArtifact:
    train_file_path:str
    test_file_path:str
@dataclass
class DataValidationArtifact:
    validation_status: bool
    valid_train_file_path: str
    valid_test_file_path: str
    invalid_train_file_path: str
    invalid_test_file_path: str
    drift_report_file_path: str


@dataclass
class DataTransformationArtifact:
    data_transformed_object_dir:str
    data_transformed_train_file:str
    data_transformed_test_file:str
@dataclass
class ClassificationMetricArtifact:
    accuracy_score: float
    precision: float
    recall: float
    f1_score: float  # <-- new


@dataclass
class ModelTrainerArtifact:
    model_file_path:str
    train_metric:ClassificationMetricArtifact
    test_metric:ClassificationMetricArtifact