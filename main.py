from Student_Performace.components.data_ingestion import DataIngestion
from Student_Performace.components.data_validation import DataValidation
from Student_Performace.components.data_transformation import DataTransformation
from Student_Performace.exception.exception import StudentException
from Student_Performace.logging.logger import logging
from Student_Performace.entity.config_entity import DataIngestionconfig,DataValidationConfig,DataTransformationConfig
from Student_Performace.entity.config_entity import TrainingPipelineConfig

# from networksecurity.components.model_trainer import ModelTrainer
# from networksecurity.entity.config_entity import ModelTrainerConfig
 

if __name__ == "__main__":
    training_pipeline_config = TrainingPipelineConfig()
    data_ingestion_config = DataIngestionconfig(training_pipeline_config)
    data_ingestion = DataIngestion(data_ingestion_config)
    data_ingestion_artifact = data_ingestion.initiate_data_ingestion()
    print(data_ingestion_artifact)

    logging.info("Data Validation Process started")
    data_validation_config = DataValidationConfig(training_pipeline_config)
    data_validation = DataValidation(data_ingestion_artifact, data_validation_config)
    data_validation_artifacts = data_validation.initiate_data_validation()  # FIXED variable name
    print(data_validation_artifacts)  # PRINTING the correct variable


    logging.info("Data TRansformation Process started")
    data_transformation_config=DataTransformationConfig(training_pipeline_config)
    data_transformation=DataTransformation(data_validation_artifacts,data_transformation_config)
    data_transformation_artifacts=data_transformation.initiate_data_transformation()
    print(data_transformation_artifacts)