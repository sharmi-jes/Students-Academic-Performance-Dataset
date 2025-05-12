import os
import sys

from Student_Performace.components.data_ingestion import DataIngestion
from Student_Performace.components.data_validation import DataValidation
from Student_Performace.components.data_transformation import DataTransformation
from Student_Performace.components.model_trainer import ModelTrainer
from Student_Performace.exception.exception import StudentException
from Student_Performace.logging.logger import logging

from Student_Performace.entity.config_entity import (
    TrainingPipelineConfig,
    DataIngestionconfig,
    DataValidationConfig,
    DataTransformationConfig,
    ModelTrainerConfig
)

from Student_Performace.entity.artfact_entity import (
    DataIngestionArtifact,
    DataValidationArtifact,
    DataTransformationArtifact,
    ModelTrainerArtifact
)

class TrainingPipeline:
    def __init__(self):
        try:
            self.training_pipeline_config=TrainingPipelineConfig()
        except Exception as e:
            raise StudentException(e,sys)

    def start_data_ingestion(self):
        try:
            self.data_ingestion_config=DataIngestionconfig(self.training_pipeline_config)
            data_ingestion=DataIngestion(self.data_ingestion_config)
            data_ingestion_artifact=data_ingestion.initiate_data_ingestion()
            logging.info(f"Data ingstion process is completde and artifact {data_ingestion_artifact}")
            return data_ingestion_artifact
        except Exception as e:
            raise StudentException(e,sys)

    def start_data_validation(self,data_ingestion_artifact:DataIngestionArtifact):
        try:
            data_validation_config=DataValidationConfig(self.training_pipeline_config)
            data_validation=DataValidation(data_ingestion_artifact,data_validation_config)
            data_validation_artifact=data_validation.initiate_data_validation()
            logging.info(f"Data Validation process completed and artifact {data_validation_artifact}")
            return data_validation_artifact
        except Exception as e:
            raise StudentException(e,sys)

    def start_data_transformation(self,data_validation_artifact:DataValidationArtifact):
        try:
            data_transformation_config=DataTransformationConfig(self.training_pipeline_config)
            data_transformation=DataTransformation(data_validation_artifact,data_transformation_config)
            data_transformation_artifact=data_transformation.initiate_data_transformation()
            logging.info(f"Data Transformation completed and artifacts {data_transformation_artifact}")
            return data_transformation_artifact
        except Exception as e:
            raise StudentException(e,sys)
    
    def start_model_trainer(self,data_transformation_artifact:DataTransformationArtifact):
        try:
            model_trainer_config=ModelTrainerConfig(self.training_pipeline_config)
            model_trainer=ModelTrainer(data_transformation_artifact,model_trainer_config)
            model_trainer_artifact=model_trainer.initiate_model_trainer()
            logging.info(f"model trainer completed and artifact {model_trainer_artifact}")
            return model_trainer_artifact
        except Exception as e:
            raise StudentException(e,sys)

    def run_pipeline(self):
        data_ingestion_artifact=self.start_data_inegstion()
        data_validation_artifact=self.start_data_validation(data_ingestion_artifact)
        data_transformation_artifact=self.start_data_transformation(data_validation_artifact)
        model_trainer_artifact=self.start_model_trainer(data_transformation_artifact)
        return model_trainer_artifact

