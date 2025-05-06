from Student_Performace.components.data_ingestion import DataIngestion
# from networksecurity.components.data_validation import DataValidation
# from networksecurity.components.data_transformation import DataTransformation
from Student_Performace.exception.exception import StudentException
from Student_Performace.logging.logger import logging
from Student_Performace.entity.config_entity import DataIngestionconfig
from Student_Performace.entity.config_entity import TrainingPipelineConfig

# from networksecurity.components.model_trainer import ModelTrainer
# from networksecurity.entity.config_entity import ModelTrainerConfig
 

if __name__=="__main__":
    training_pipeline_config=TrainingPipelineConfig()
    data_ingestion_config=DataIngestionconfig(training_pipeline_config)
    data_ingestion=DataIngestion(data_ingestion_config)
    data_ingestion_artifact=data_ingestion.initiate_data_ingestion()
    print(data_ingestion_artifact)