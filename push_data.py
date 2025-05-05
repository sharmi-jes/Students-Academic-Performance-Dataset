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



MONGO_DB_URL=os.getenv('MONGO_DB_URL')
print(MONGO_DB_URL)
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

         self.mongo_client=pymongo.MongoClient(MONGO_DB_URL)
         self.database=self.mongo_client[self.database]
         self.collection=self.database[self.collection]

         self.collection.insert_many(self.records)
         return len(self.records)
        except Exception as e:
           raise StudentException(e,sys)
        
if __name__=="__main__":
   file_path=r"D:\RESUME ML PROJECTS\Students' Academic Performance Dataset\Student_Data\xAPI-Edu-Data.csv"
   database="Sharmianyum"
   collection="Student_Data"
   student=StudentDataExtract()
   records=student.csv_to_json(file_path)
   print(records)
   no_of_records=student.insert_into_mongodb(records,database,collection)
   print(no_of_records)
