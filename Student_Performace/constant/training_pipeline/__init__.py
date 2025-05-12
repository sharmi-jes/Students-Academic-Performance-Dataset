import os
import sys
import numpy as np

'''Training pipeline related constant variables'''
TARGET_VARIABLE:str="Class"
ARTIFACT_DIR:str="Artifacts"
PIPELINE_NAME="Student_Performance"

TRAIN_FILE_NAME="train.csv"
TEST_FILE_NAME='test.csv'

SCHEMA_FILE_PATH=os.path.join("data_schema","schema.yaml")

USERNAME="datagirl088"
PASSOWRD="sharmila1"

'''Data ingestion related constants'''

DATA_INGESTION_COLLECTION_NAME="Student_Data"
DATA_INGESTION_DATABASE_NAME="Sharmianyum"
DATA_INGESTION_DIR_NAME="data_ingestion"
DATA_INGESTION_FEATURE_STORE_PATH="feature_store"
DATA_INGESTION_INGESTED_DIR='ingested'
DATA_INGESTION_SPLIT_RATIO:float=0.2


'''Data Validation related constant variables'''
DATA_VALIDATION_DIR_NAME:str="data_validation"
DATA_VALIDATION_VALID_DIR="validated"
DATA_VALIDATION_INVLAID_DIR="invalidated"
DATA_VALIDATION_DRIFT_REPORT_DIR='drift_report'
DATA_VALIDATION_DRIFT_REPORT_FILE_PATH="report.yaml"


'''Data Transformation related constant variables'''
DATA_TRANSFORMATION_DIR="data_transformation"
DATA_TRANSFORMATION_TRANSFORMED_DIR="transformed"
DATA_TRANSFORMATION_OBJECT_DIR="transformed_object"
DATA_TRANSFORMED_LABEL_ENCODER_FILE="label_object"

DATA_TRANSFORMATION_KNNIMPUTER={
    "missing_values":np.nan,
   "n_neighbors": 3,
    "weights":"uniform",
}

'''Model Trainer related constant variables
'''

MODEL_TRAINER_DIR="model_trainer"
MODEL_TRAINER_TRAINER_DIR="trained_model"
MODEL_TRAINER_EXPECTED_SCORE:float=0.6
MODEL_TRAINER_UNDERFITTING_THRESHOLD=0.5
MODEL_TRAINER_MODEL_FILE_PATH="model.pkl"
