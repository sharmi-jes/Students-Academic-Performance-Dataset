import os
import sys

'''Training pipeline related constant variables'''
TARGET_VARIABLE:str="Class"
ARTIFACT_DIR:str="Artifacts"
PIPELINE_NAME="Student_Performance"

TRAIN_FILE_NAME="train.csv"
TEST_FILE_NAME='test.csv'


'''Data ingestion related constants'''

DATA_INGESTION_COLLECTION_NAME="Student_Data"
DATA_INGESTION_DATABASE_NAME="Sharmianyum"
DATA_INGESTION_DIR_NAME="data_ingestion"
DATA_INGESTION_FEATURE_STORE_PATH="feature_store"
DATA_INGESTION_INGESTED_DIR='ingested'
DATA_INGESTION_SPLIT_RATIO:float=0.2