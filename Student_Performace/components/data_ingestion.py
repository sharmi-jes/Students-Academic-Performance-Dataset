import os
import sys
import numpy as np
from Student_Performace.exception.exception import StudentException
from Student_Performace.logging.logger import logging
from Student_Performace.entity.config_entity import DataIngestionconfig
import pymongo
from dotenv import load_dotenv
load_dotenv()
import pandas as pd
from sklearn.model_selection import train_test_split
MONGO_DB_URL=os.getenv('MONGO_DB_URL')


from Student_Performace.entity.artfact_entity import DataIngestionArtifact

logging.info("create the dataingestion class for perform the function")
class DataIngestion:
    def __init__(self,data_ingestion_config:DataIngestionconfig):
        try:
            self.data_ingestion_config=data_ingestion_config
        except Exception as e:
            raise StudentException(e,sys)
    logging.info("read the data from mongodb")
    # read the data from mongodb
    def export_collection_as_dataframe(self):
        try:
            database_name=self.data_ingestion_config.database_name
            collection_name=self.data_ingestion_config.collection_name
            self.mongo_client=pymongo.MongoClient(MONGO_DB_URL)

            collection=self.mongo_client[database_name][collection_name]

            df=pd.DataFrame(list(collection.find()))
            if "_id" in df.columns:
                df=df.drop(columns="_id",axis=1)
            df.replace({"nan",np.nan},inplace=True)
            return df
        except Exception as e:
            raise StudentException(e,sys)
    logging.info("store the data into store path as csv format")
    # store the data into feature store path
    def feature_store_path(self,dataframe:pd.DataFrame):
        try:
            feature_store_path=self.data_ingestion_config.feature_store_path
            dir_path=os.path.dirname(feature_store_path)
            os.makedirs(dir_path,exist_ok=True)

            dataframe.to_csv(feature_store_path,index=False,header=True)
            return dataframe

        except Exception as e:
            raise StudentExceptin(e,sys)
    logging.info("split the data as train and test")
    def split_the_data_train_test(self,dataframe:pd.DataFrame):
        try:
            train_set,test_set=train_test_split(dataframe,test_size=self.data_ingestion_config.train_split_ratio)
            dir_path=os.path.dirname(self.data_ingestion_config.train_file_name)

            os.makedirs(dir_path,exist_ok=True)

            train_set.to_csv(self.data_ingestion_config.train_file_name)
            test_set.to_csv(self.data_ingestion_config.test_file_name)
        except Exception as e:
            raise StudentException(e,sys)

    logging.info("initta ethe data ingestion function to call all fuction")
    def initiate_data_ingestion(self):
        try:

         dataframe=self.export_collection_as_dataframe()
         dataframe=self.feature_store_path(dataframe)
         dataframe=self.split_the_data_train_test(dataframe)
         data_ingestion_artifact=DataIngestionArtifact(self.data_ingestion_config.train_file_name,
         self.data_ingestion_config.test_file_name)

         return data_ingestion_artifact

        except Exception as e:
         raise StudentException(e,sys)

