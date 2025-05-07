import os
import sys
from Student_Performace.constant import training_pipeline
from Stuudent_Performace.exception.exception import StudentException

from Student_Performace.entity.config_entity import ModelTrainerConfig
from Student_Performace.entity.artfact_entity import ClassificationMetric,ModelTrainerArtifact,DataTransformationArtifact
from Student_Performace.utility.main_utils.utils import load_numpy_array_data,load_object,evaluate_model
from Student_Performace.utils.ml_utils.metric import get_classification_score
from Student_Performace.utils.ml_utils.model.estimator import NetworkModel

class ModelTrainer:
    def __init__(self,model_trainer_config:ModelTrainerConfig,data_transformation_artifact:DataTransformationArtifact):
        try:

            self.model_trainer_config=model_trainer_config
            self.data_transformation_artifact=data_transformation_artifact

        except Exception as e:
            raise StudentException(e,sys)

    def train_model(self,X_train,y_train,x_test,y_test):
        models = {
                "Random Forest": RandomForestClassifier(verbose=1),
                "Decision Tree": DecisionTreeClassifier(),
                "Gradient Boosting": GradientBoostingClassifier(verbose=1),
                "Logistic Regression": LogisticRegression(verbose=1),
                "AdaBoost": AdaBoostClassifier(),
            }
        params={
            "Decision Tree": {
                'criterion':['gini', 'entropy', 'log_loss'],
                # 'splitter':['best','random'],
                # 'max_features':['sqrt','log2'],
            },
            "Random Forest":{
                # 'criterion':['gini', 'entropy', 'log_loss'],
                
                # 'max_features':['sqrt','log2',None],
                'n_estimators': [8,16,32,128,256]
            },
            "Gradient Boosting":{
                # 'loss':['log_loss', 'exponential'],
                'learning_rate':[.1,.01,.05,.001],
                'subsample':[0.6,0.7,0.75,0.85,0.9],
                # 'criterion':['squared_error', 'friedman_mse'],
                # 'max_features':['auto','sqrt','log2'],
                'n_estimators': [8,16,32,64,128,256]
            },
            "Logistic Regression":{},
            "AdaBoost":{
                'learning_rate':[.1,.01,.001],
                'n_estimators': [8,16,32,64,128,256]
            }
            
        }
        


    


            model_report:dict=evaluate_model(x_train,y_train,x_test,y_test,models,params)

            # best model score
            best_model_score=max(sorted(model_report.values()))

            # best model name

            best_model_name=list(model_report.keys())[
                list(model_report.values()).index(best_model_score)
            ]

            # best model
            best_model=models[best_model_name]

            y_train_pred=best_model.predict(x_train)

            classification_train_metric=get_classification_score(y_true=y_train,y_pred=y_train_pred)
            

            y_test_pred=best_model.predict(x_test)
            classification_test_metric=get_classification_score(y_true=y_test,y_pred=y_test_pred)
            #load the preprocessor object
            preprocessor=load_object(self.data_transformation_artifact.transformation_object_dir)

            os.makedirs(os.path.dirname(self.model_trainer_config.model_trainer_model_file_path))

            network_model=NetworkModel(preprocessor=preprocessor,model=best_model)

            save_object(self.model_trainer_config.model_trainer_model_file_path,obj=NetworkModel)

            save_object("final_model/model.pkl",best_model)


            model_trainer_artifact=ModelTrainerArtifact(trained_model_file_path=self.model_trainer_config.model_trainer_model_file_path,
                             train_metric_artifact=classification_train_metric,
                             test_metric_artifact=classification_test_metric
                             )
        logging.info(f"Model trainer artifact: {model_trainer_artifact}")
        return model_trainer_artifact




    def initiate_model_trainer(self):
        try:
            train_file_path=self.data_transformation_artifact.trained_file_path
            test_file_path=self.data_transformation_artifact.test_file_path


            # load numpy arrray data

            train_arr=load_numpy_array_data(train_file_path)
            test_arr=load_numpy_array_data(test_file_path)

            x_train,y_train,x_test,y_test=(
                train_arr[:,:-1],
                train_arr[:,-1],
                test_arr[:,:-1],
                test_arr[:,-1]
            )











