import os
import sys

'''Training pipeline related constant variables'''
TARGET_VARIABLE:str="Class"
ARTIFACT_DIR:str="Artifacts"
PIPELINE_NAME="Student_Performance"

TRAIN_FILE_NAME="train.csv"
TEST_FILE_NAME='test.csv'

SCHEMA_FILE_PATH=os.path.join("data_schema","schema.yaml")


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