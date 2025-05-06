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