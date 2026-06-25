import mlflow.sklearn
import mlflow.sklearn
import numpy as np 
import pandas as pd
import sys,os
import mlflow 
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging

from networksecurity.entity.artifact_entity import DataTransformationArtifacts,ModelTrainerArtifact
from networksecurity.entity.config_entity import Model_trainer_config

from networksecurity.Utils.utils_main.utils import save_numpy,save_object,load_numpy_arrray,evaluate_model,load_object  
from networksecurity.Utils.ML_utils.metric.classifiacation_metric import get_classificatin_score
from networksecurity.Utils.ML_utils.Model.estimator import NetworkModel
#importing dagshub -- for remote repositories 

import dagshub
dagshub.init(repo_owner='raghavbankar', repo_name='NetworkSecurity', mlflow=True)

#importing models

from sklearn.linear_model import LogisticRegression
from sklearn.metrics import r2_score
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import (AdaBoostClassifier,GradientBoostingClassifier,RandomForestClassifier)
class ModelTrainer:
    def __init__(self,model_trainer_config:Model_trainer_config,data_transform_artifact:DataTransformationArtifacts):
        try:
            self.model_trainer_config=model_trainer_config
            self.data_transform_artifact=data_transform_artifact
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        
    def track_mlflow(self,best_model,classification_metrics):
        try:
            with mlflow.start_run():
                f1_score=classification_metrics.f1_score
                precision_score=classification_metrics.precision_score
                recall_score=classification_metrics.recall_score

                mlflow.log_metric("f1_score",f1_score)
                mlflow.log_metric("precision_score",precision_score)
                mlflow.log_metric("recall_score",recall_score)
                mlflow.sklearn.log_model(sk_model=best_model,name="Model")
        except Exception as e:
            raise NetworkSecurityException(e,sys)
 
        
    def train_model(self,x_train,y_train,x_test,y_test):
        try:
            models ={
                "Random Forest":RandomForestClassifier(verbose=1),
                "Decision Tree":DecisionTreeClassifier(),
                "Gradient Boosting":GradientBoostingClassifier(verbose=1),
                "Logistic Regression":LogisticRegression(verbose=1),
                "AdaBoost":AdaBoostClassifier()
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
            #Evaluation of models
            model_report:dict=evaluate_model(x_train=x_train,y_train=y_train,x_test=x_test,y_test=y_test,
                                             params=params,models=models)
            
            #To get the best model score from dict

            best_model_score = max(sorted(model_report.values()))

            #To get the best model name

            best_model_name = list(model_report.keys())[
                list(model_report.values()).index(best_model_score)
            ]

            best_model = models[best_model_name]
            y_train_pred=best_model.predict(x_train)

            classification_train_metrics=get_classificatin_score(y_true=y_train,y_pred=y_train_pred)

            ## Track the Mlflow

            self.track_mlflow(best_model,classification_train_metrics)

            y_test_pred=best_model.predict(x_test)

            classification_test_metrics=get_classificatin_score(y_true=y_test,y_pred=y_test_pred)

            self.track_mlflow(best_model,classification_test_metrics)

            #loading the transfromation pickle file
            preprocessor = load_object(file_path=self.data_transform_artifact.transformed_object_file_path)

            model_dir_path = os.path.dirname(self.model_trainer_config.model_trained_model_file_path)
            os.makedirs(model_dir_path,exist_ok=True)

            network_model=NetworkModel(preprocessor=preprocessor,model=best_model)
            save_object(self.model_trainer_config.model_trained_model_file_path,obj=network_model)

            #ModelTrainerArtifacts

            model_trainer_artfact=ModelTrainerArtifact(trained_model_file_path=self.model_trainer_config.model_trained_model_file_path,
                                 train_metric_artifacts=classification_train_metrics,
                                 test_metric_artifacts=classification_test_metrics)
            return model_trainer_artfact
        except Exception as e:
            raise NetworkSecurityException(e,sys)
    
    def initiate_model_trainer(self)->ModelTrainerArtifact:
        try:
            train_file_path=self.data_transform_artifact.transformed_train_data
            test_file_path=self.data_transform_artifact.transformed_test_data

            #loading training array and testing array
            train_arr = load_numpy_arrray(train_file_path)
            test_arr = load_numpy_arrray(test_file_path)

            x_train,y_train,x_test,y_test = (
                train_arr[:,:-1],
                train_arr[:,-1],
                test_arr[:,:-1],
                test_arr[:,-1]
            )

            model=self.train_model(x_train=x_train,y_train=y_train,x_test=x_test,y_test=y_test)
            return model

        except Exception as e:
            raise NetworkSecurityException(e,sys)

