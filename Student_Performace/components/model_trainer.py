import os
import sys
from Student_Performace.constant import training_pipeline
from Student_Performace.exception.exception import StudentException
from Student_Performace.entity.config_entity import ModelTrainerConfig
from Student_Performace.logging.logger import logging
from Student_Performace.entity.artfact_entity import ClassificationMetricArtifact, ModelTrainerArtifact, DataTransformationArtifact
from Student_Performace.utils.main_utils.utils import load_numpy_array_data, load_object, evaluate_model,save_object
from Student_Performace.utils.ml_utils.metric.classification_metric import get_classification_score
from Student_Performace.utils.ml_utils.model.estimator import NetworkModel
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import r2_score
import mlflow
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import (
    AdaBoostClassifier,
    GradientBoostingClassifier,
    RandomForestClassifier,
)
from sklearn.model_selection import GridSearchCV

import dagshub
import os
dagshub.init(
    repo_owner='sharmi-jes',
    repo_name='Students-Academic-Performance-Dataset',
    mlflow=True
#     token=os.getenv("DAGSHUB_TOKEN")
 )



class ModelTrainer:
    def __init__(self, model_trainer_config: ModelTrainerConfig, data_transformation_artifact: DataTransformationArtifact):
        try:
            self.model_trainer_config = model_trainer_config
            self.data_transformation_artifact = data_transformation_artifact
        except Exception as e:
            raise StudentException(e, sys)

    def mlflow_track(self,best_model,classificationmetric):
        try:
            with mlflow.start_run():
    #              accuracy_score: float
    # precision: float
    # recall: float
    # recall: float  # <-- new

                accuracy_score=classificationmetric.accuracy_score
                precision=classificationmetric.precision
                recall=classificationmetric.recall
                f1_score=classificationmetric.f1_score



                mlflow.log_metric("accuracy_score",accuracy_score)
                mlflow.log_metric("precision",precision)
                mlflow.log_metric("recall",recall)
                mlflow.log_metric("f1_score",f1_score)
                mlflow.sklearn.log_model(best_model,'model')
        except Exception as e:
            raise StudentException(e,sys)


    def train_model(self, x_train, y_train, x_test, y_test):
        models = {
            "Random Forest": RandomForestClassifier(verbose=1),
            "Decision Tree": DecisionTreeClassifier(),
            "Gradient Boosting": GradientBoostingClassifier(verbose=1),
            "Logistic Regression": LogisticRegression(verbose=1),
            "AdaBoost": AdaBoostClassifier(),
        }

        params = {
            "Decision Tree": [{'criterion': ['gini', 'entropy', 'log_loss'], 'splitter': ['best', 'random']}],
            "Random Forest": [{'n_estimators': [8, 16, 32, 128, 256]}],
            "Gradient Boosting": [
                {'learning_rate': [.1, .01, .05, .001], 'subsample': [0.6, 0.7, 0.75, 0.85, 0.9], 'n_estimators': [8, 16, 32, 64, 128, 256]}
            ],
            "Logistic Regression": [{}],
            "AdaBoost": [{'learning_rate': [.1, .01, .001], 'n_estimators': [8, 16, 32, 64, 128, 256]}]
        }

        # Evaluate models and get the report
        model_report = evaluate_model(x_train, y_train, x_test, y_test, models, params)

        # Find the best model based on the report
        best_model_score = max(sorted(model_report.values()))
        best_model_name = list(model_report.keys())[list(model_report.values()).index(best_model_score)]
        best_model = models[best_model_name]

        # If GridSearchCV is used, ensure you extract the best model and fit it again
        if isinstance(best_model, GridSearchCV):
            best_model = best_model.best_estimator_

        # Fit the best model to the training data
        best_model.fit(x_train, y_train)

        # Now make predictions
        y_train_pred = best_model.predict(x_train)
        y_test_pred = best_model.predict(x_test)

        # Evaluate classification metrics for train and test data
        classification_train_metric = get_classification_score(y_true=y_train, y_pred=y_train_pred)
        
        self.mlflow_track(best_model,classification_train_metric)

        classification_test_metric = get_classification_score(y_true=y_test, y_pred=y_test_pred)

        self.mlflow_track(best_model,classification_test_metric)

        # Load the preprocessor object used for data transformation
        preprocessor = load_object(self.data_transformation_artifact.data_transformed_object_dir)
        label_encoder=load_object(self.data_transformation_artifact.data_transformed_label_encoder_file)

        # Ensure directory exists before saving the model
        os.makedirs(os.path.dirname(self.model_trainer_config.model_trainer_model_file_path), exist_ok=True)

        # Create a network model with the preprocessor and the best model
        network_model = NetworkModel(preprocessor=preprocessor, model=best_model,encoder=label_encoder)

        # Save the model to the specified location
        save_object(self.model_trainer_config.model_trainer_model_file_path, obj=network_model)
        save_object("final_model/model.pkl", best_model)

        # Create an artifact for the trained model
        model_trainer_artifact = ModelTrainerArtifact(
            model_file_path=self.model_trainer_config.model_trainer_model_file_path,
            train_metric=classification_train_metric,
            test_metric=classification_test_metric
        )

        # Log and return the model trainer artifact
        logging.info(f"Model trainer artifact: {model_trainer_artifact}")
        return model_trainer_artifact

    def initiate_model_trainer(self):
        try:
            train_file_path = self.data_transformation_artifact.data_transformed_train_file
            test_file_path = self.data_transformation_artifact.data_transformed_test_file

            # Load numpy array data
            train_arr = load_numpy_array_data(train_file_path)
            test_arr = load_numpy_array_data(test_file_path)

            # Split the data into features and target
            x_train, y_train, x_test, y_test = (
                train_arr[:, :-1],
                train_arr[:, -1],
                test_arr[:, :-1],
                test_arr[:, -1]
            )

            # Train the model and return the artifact
            model_trainer_artifact = self.train_model(x_train, y_train, x_test, y_test)
            return model_trainer_artifact
        except Exception as e:
            raise StudentException(e, sys)














