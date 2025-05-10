import os
from datetime import datetime
import sys
from Student_Performace.constant import training_pipeline

# from networksecurity.constant import training_pipeline

print(training_pipeline.PIPELINE_NAME)
print(training_pipeline.ARTIFACT_DIR)


class TrainingPipelineConfig:
    def __init__(self,timestamp=datetime.now()):
        timestamp=timestamp.strftime("%m_%d_%Y_%H_%M_%S")
        self.pipeline_name=training_pipeline.PIPELINE_NAME
        self.artifact_name=training_pipeline.ARTIFACT_DIR
        self.artifact_dir=os.path.join(self.artifact_name,timestamp)
        # self.model_dir=os.path.join("final_model")
        self.timestamp: str=timestamp


class DataIngestionconfig:
    def __init__(self,training_pipeline_config:TrainingPipelineConfig):
        self.data_ingestion_dir:str=os.path.join(training_pipeline_config.artifact_dir,training_pipeline.DATA_INGESTION_DIR_NAME)
        self.feature_store_path:str=os.path.join(self.data_ingestion_dir,training_pipeline.DATA_INGESTION_FEATURE_STORE_PATH)
        self.train_file_name:str=os.path.join(self.data_ingestion_dir,training_pipeline.TRAIN_FILE_NAME)
        self.test_file_name:str=os.path.join(self.data_ingestion_dir,training_pipeline.TEST_FILE_NAME)
        self.train_split_ratio=training_pipeline.DATA_INGESTION_SPLIT_RATIO
        self.database_name=training_pipeline.DATA_INGESTION_DATABASE_NAME
        self.collection_name=training_pipeline.DATA_INGESTION_COLLECTION_NAME


class DataValidationConfig:
    def __init__(self,training_pipeline_config:TrainingPipelineConfig):
        self.data_validated_dir:str=os.path.join(training_pipeline_config.artifact_dir,training_pipeline.DATA_VALIDATION_DIR_NAME)
        self.data_valid_dir:str=os.path.join(self.data_validated_dir,training_pipeline.DATA_VALIDATION_VALID_DIR)
        self.data_invalid_dir:str=os.path.join(self.data_validated_dir,training_pipeline.DATA_VALIDATION_INVLAID_DIR)
        self.valid_train_file:str=os.path.join(self.data_valid_dir,training_pipeline.TRAIN_FILE_NAME)
        self.invalid_train_file:str=os.path.join(self.data_invalid_dir,training_pipeline.TRAIN_FILE_NAME)
        
        self.valid_test_file:str=os.path.join(self.data_valid_dir,training_pipeline.TEST_FILE_NAME)
        
        self.invalid_test_file:str=os.path.join(self.data_invalid_dir,training_pipeline.TEST_FILE_NAME)

        self.report_file_path=os.path.join(
            self.data_validated_dir,
            training_pipeline.DATA_VALIDATION_DRIFT_REPORT_DIR,
            training_pipeline.DATA_VALIDATION_DRIFT_REPORT_FILE_PATH
        )
        


class DataTransformationConfig:
    def __init__(self,training_pipeline_config:TrainingPipelineConfig):
        self.data_transformation_dir:str=os.path.join(training_pipeline_config.artifact_dir,training_pipeline.DATA_TRANSFORMATION_DIR)
        self.transformation_train_file_path:str=os.path.join(self.data_transformation_dir,training_pipeline.TRAIN_FILE_NAME,training_pipeline.TRAIN_FILE_NAME.replace("csv", "npy"),)
        self.transformation_test_file_path:str=os.path.join(self.data_transformation_dir,training_pipeline.TEST_FILE_NAME,training_pipeline.TEST_FILE_NAME.replace("csv", "npy"),)
        self.transformation_object_dir:str=os.path.join(self.data_transformation_dir,training_pipeline.DATA_TRANSFORMATION_OBJECT_DIR)
        self.transformed_label_encoder_file:str=os.path.join(self.data_transformation_dir,training_pipeline.DATA_TRANSFORMED_LABEL_ENCODER_FILE)

    
class ModelTrainerConfig:
        def __init__(self,training_pipeline_config:TrainingPipelineConfig):
            self.model_trainer_dir:str=os.path.join(training_pipeline_config.artifact_dir,training_pipeline.MODEL_TRAINER_DIR)
            
            self.model_expected_score:float=training_pipeline.MODEL_TRAINER_EXPECTED_SCORE

            self.model_trainer_underfitting_threshold:float=training_pipeline.MODEL_TRAINER_UNDERFITTING_THRESHOLD
            self.model_trainer_model_file_path=os.path.join(self.model_trainer_dir,training_pipeline.MODEL_TRAINER_TRAINER_DIR,training_pipeline.MODEL_TRAINER_MODEL_FILE_PATH)