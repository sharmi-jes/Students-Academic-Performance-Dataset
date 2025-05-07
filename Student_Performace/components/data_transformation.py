import os
import sys
import pandas as pd
from sklearn.pipeline import Pipeline
from sklearn.impute import KNNImputer
from sklearn.preprocessing import LabelEncoder
import numpy as np
from Student_Performace.constant import training_pipeline
from Student_Performace.exception.exception import StudentException
from Student_Performace.logging.logger import logging
from Student_Performace.entity.config_entity import DataTransformationConfig
from Student_Performace.entity.artfact_entity import DataValidationArtifact,DataTransformationArtifact
from Student_Performace.constant.training_pipeline import TARGET_VARIABLE
from Student_Performace.utils.main_utils.utils import save_object,save_numpy_array_data
from Student_Performace.constant.training_pipeline import DATA_TRANSFORMATION_KNNIMPUTER

label_encoder=LabelEncoder()

class DataTransformation:
    def __init__(self,data_validation_artifact:DataValidationArtifact,
                  data_transformation_config:DataTransformationConfig):
            try:
                self.data_validation_artifact=data_validation_artifact
                self.data_transformation_config=data_transformation_config
            except Exception as e:
                raise StudentException(e,sys)

    def read_data(filepath):
        try:
            return pd.read_csv(filepath)
        except Exception as e:
            raise StudentException(e,sys)

    def drop_some_cols(self,dataframe):
        try:
            
            dropped_cols=["NationalITy","PlaceofBirth","SectionID",'Unnamed: 0']
            return dataframe.drop(columns=dropped_cols,axis=1)
        except Exception as e:
            raise StudentException(e,sys)

    def get_data_transformer_object(cls)->Pipeline:
        """
        It initialises a KNNImputer object with the parameters specified in the training_pipeline.py file
        and returns a Pipeline object with the KNNImputer object as the first step.

        Args:
          cls: DataTransformation

        Returns:
          A Pipeline object
        """
        logging.info(
            "Entered get_data_trnasformer_object method of Trnasformation class"
        )
        try:
           imputer:KNNImputer=KNNImputer(**DATA_TRANSFORMATION_KNNIMPUTER)
           logging.info(
                f"Initialise KNNImputer with {DATA_TRANSFORMATION_KNNIMPUTER}"
            )
           processor:Pipeline=Pipeline([("imputer",imputer)])
           return processor
        except Exception as e:
            raise StudentException(e,sys)


    # def convert_categorical_to_numeric(self,dataframe):
    #     try:



    def initiate_data_transformation(self):
        try:
            # read the train and test data
            train_data=self.data_validation_artifact.valid_train_file_path
            test_data=self.data_validation_artifact.valid_test_file_path


            train_df=DataTransformation.read_data(train_data)
            test_df=DataTransformation.read_data(test_data)

            # drop some cols

            train_df=self.drop_some_cols(train_df)
            test_df=self.drop_some_cols(test_df)
            print(train_df.columns)


            # drop target varaibel
            input_feature_train_df=train_df.drop(columns=TARGET_VARIABLE,axis=1)
            target_feature_train_df=train_df[TARGET_VARIABLE]

            input_feature_test_df=test_df.drop(columns=TARGET_VARIABLE,axis=1)
            target_feature_test_df=test_df[TARGET_VARIABLE]

            print(input_feature_train_df.head())
             

            for col in input_feature_train_df:
                if input_feature_train_df[col].dtype=="object":
                    input_feature_train_df[col]=label_encoder.fit_transform(input_feature_train_df[col])
                    input_feature_test_df[col]=label_encoder.transform(input_feature_test_df[col])

            # input_feature_train_df=label_encoder.fit_transform(input_feature_train_df)
            # input_feature_test_df=label_encoder.transform(input_feature_test_df)

            preprocessor=self.get_data_transformer_object()
            preprocessor_object=preprocessor.fit(input_feature_train_df)
            transformed_object_train_file=preprocessor.transform(input_feature_train_df)
            transformed_object_test_file=preprocessor.transform(input_feature_test_df)

           

            # combine array
            train_array=np.c_[
                transformed_object_train_file,np.array(target_feature_train_df)
            ]

            test_array=np.c_[
                transformed_object_test_file,np.array(target_feature_test_df)
            ]
            

            save_numpy_array_data(self.data_transformation_config.transformation_train_file_path,array=train_array)
            save_numpy_array_data(self.data_transformation_config.transformation_test_file_path,array=test_array)
            save_object(self.data_transformation_config.transformation_object_dir,preprocessor_object)
            save_object( "final_model/preprocessor.pkl", preprocessor_object)

            data_transformation_artifact=DataTransformationArtifact(
                data_transformed_train_file=self.data_transformation_config.transformation_train_file_path,
                data_transformed_test_file=self.data_transformation_config.transformation_test_file_path,
                data_transformed_object_dir=self.data_transformation_config.transformation_object_dir
            )
            
            return data_transformation_artifact

        except Exception as e:
            raise StudentException(e,sys)




            


