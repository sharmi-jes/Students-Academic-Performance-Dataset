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
from Student_Performace.entity.artfact_entity import DataValidationArtifact, DataTransformationArtifact
from Student_Performace.constant.training_pipeline import TARGET_VARIABLE, DATA_TRANSFORMATION_KNNIMPUTER
from Student_Performace.utils.main_utils.utils import save_object, save_numpy_array_data

class DataTransformation:
    def __init__(self, data_validation_artifact: DataValidationArtifact,
                 data_transformation_config: DataTransformationConfig):
        try:
            self.data_validation_artifact = data_validation_artifact
            self.data_transformation_config = data_transformation_config
        except Exception as e:
            raise StudentException(e, sys)

    @staticmethod
    def read_data(filepath):
        try:
            df = pd.read_csv(filepath)
            df = df.drop(columns=["Unnamed: 0", "NationalITy", "PlaceofBirth", "SectionID"], axis=1)
            return df
        except Exception as e:
            raise StudentException(e, sys)

    @classmethod
    def get_data_transformer_object(cls) -> Pipeline:
        logging.info("Entered get_data_trnasformer_object method of Trnasformation class")
        try:
            imputer: KNNImputer = KNNImputer(**DATA_TRANSFORMATION_KNNIMPUTER)
            logging.info(f"Initialised KNNImputer with {DATA_TRANSFORMATION_KNNIMPUTER}")
            processor: Pipeline = Pipeline([("imputer", imputer)])
            return processor
        except Exception as e:
            raise StudentException(e, sys)

    def initiate_data_transformation(self):
        try:
            # read the train and test data
            train_data = self.data_validation_artifact.valid_train_file_path
            test_data = self.data_validation_artifact.valid_test_file_path

            train_df = DataTransformation.read_data(train_data)
            test_df = DataTransformation.read_data(test_data)

            print(f"Training columns: {train_df.columns}")

            # split input and target features
            input_feature_train_df = train_df.drop(columns=TARGET_VARIABLE, axis=1)
            target_feature_train_df = train_df[TARGET_VARIABLE]

            input_feature_test_df = test_df.drop(columns=TARGET_VARIABLE, axis=1)
            target_feature_test_df = test_df[TARGET_VARIABLE]

            # Label encoding for categorical columns
            label_encoders = {}
            for col in input_feature_train_df.columns:
                if input_feature_train_df[col].dtype == "object":
                    le = LabelEncoder()
                    input_feature_train_df[col] = le.fit_transform(input_feature_train_df[col])
                    input_feature_test_df[col] = le.transform(input_feature_test_df[col])
                    label_encoders[col] = le  # Save encoder for this column

            print("Encoded Test Data:")
            print(input_feature_test_df)

            # Apply KNN Imputer
            preprocessor = self.get_data_transformer_object()
            preprocessor_object = preprocessor.fit(input_feature_train_df)
            transformed_train_array = preprocessor.transform(input_feature_train_df)
            transformed_test_array = preprocessor.transform(input_feature_test_df)

            # Combine features and target
            train_array = np.c_[transformed_train_array, np.array(target_feature_train_df)]
            test_array = np.c_[transformed_test_array, np.array(target_feature_test_df)]

            # Save transformed data and objects
            save_numpy_array_data(self.data_transformation_config.transformation_train_file_path, array=train_array)
            save_numpy_array_data(self.data_transformation_config.transformation_test_file_path, array=test_array)
            save_object(self.data_transformation_config.transformation_object_dir, preprocessor_object)
            save_object("final_model/preprocessor.pkl", preprocessor_object)

            # ✅ Save label encoders
            save_object("final_model/label_encoders.pkl", label_encoders)

            # Return artifact
            data_transformation_artifact = DataTransformationArtifact(
                data_transformed_train_file=self.data_transformation_config.transformation_train_file_path,
                data_transformed_test_file=self.data_transformation_config.transformation_test_file_path,
                data_transformed_object_dir=self.data_transformation_config.transformation_object_dir,
                data_transformed_label_encoder_file=self.data_transformation_config.transformed_label_encoder_file
            )

            return data_transformation_artifact

        except Exception as e:
            raise StudentException(e, sys)





            


