import os
import sys

import pymongo.mongo_client
from Student_Performace.logging import logger
from Student_Performace.exception.exception import StudentException
from dotenv import load_dotenv
load_dotenv()
import pandas as pd
import json
import numpy as np
import certifi
ca=certifi.where()
import pymongo

class StudentDataExtract():
    def __init__(self):
        try:
            pass
        except Exception as e:
            raise StudentException(e,sys)
        
    def csv_to_json(self,file_path):
        try:

         data=pd.read_csv(file_path)
         data.reset_index(drop=True,inplace=True)
         records=list(json.loads(data.T.to_json()).values())
         return records
        except Exception as e:
            raise StudentException(e,sys)
    
    def insert_into_mongodb(self,records,database,collection):
        try:

         self.records=records
         self.collection=collection
         self.database=database

         self.pymongo_client=pymongo.mongo_client('')
         self.database=self.pymongo_client[self.database]
         self.collection-=self.database[self.collection]

         self.collection.insert_many(self.records)
         return len(self.records)
        except Exception as e:
           raise StudentException(e,sys)