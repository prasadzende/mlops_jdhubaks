# load the train and test
# train algo
# save the metrices, params
import os
import warnings
import sys
import pandas as pd
import numpy as np
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
from sklearn.model_selection import train_test_split
from sklearn.linear_model import ElasticNet
from get_data import read_params
from urllib.parse import urlparse
import argparse
import joblib
import json
import mlflow

def train_and_evaluate(config_path):
    config = read_params(config_path)
    test_data_path = config["split_data"]["test_path"]
    train_data_path = config["split_data"]["train_path"]
    n_components = config["base"]["n_components"]
    random_state = config["base"]["random_state"]
    model_dir = config["model_dir"]

    alpha = config["estimators"]["SGDClassifier"]["params"]["alpha"]
    l1_ratio = config["estimators"]["SGDClassifier"]["params"]["l1_ratio"]

    target = [config["base"]["target_col"]]

    train = pd.read_csv(train_data_path, sep=",")
    test = pd.read_csv(test_data_path, sep=",")

    train_y = train[target]
    test_y = test[target]

    # droppping time column from dataset - Temporary 
    train_x = train.drop(target, axis=1)
    test_x = test.drop(target, axis=1)

    from imblearn.over_sampling import SMOTE
    from imblearn.under_sampling import RandomUnderSampler
    from collections import Counter  

    #print('Distribution of y_train set Before over and under sampling: ', Counter(train_y))

    under = RandomUnderSampler(sampling_strategy=0.002)
    over = SMOTE(sampling_strategy=0.01)

    X_train_smote, y_train_smote = under.fit_resample(train_x, train_y)
    X_train_both, y_train_both = over.fit_resample(X_train_smote, y_train_smote)

    #print('Distribution of y_train set Before over and under sampling: ', Counter(y_train_both))

    
################### MLFLOW ###############################
    mlflow_config = config["mlflow_config"]
    remote_server_uri = mlflow_config["remote_server_uri"]

    mlflow.set_tracking_uri(remote_server_uri)

    mlflow.set_experiment(mlflow_config["experiment_name"])

    with mlflow.start_run(run_name=mlflow_config["run_name"]) as mlops_run:
        from sklearn.linear_model import SGDClassifier
        model = SGDClassifier(
            l1_ratio=l1_ratio,
            alpha=alpha,
            random_state=random_state
        )
        #model = SGDClassifier() 
        model.fit(X_train_both, y_train_both)

        from sklearn.metrics import accuracy_score, f1_score,recall_score,precision_score

        predicted_qualities = model.predict(test_x)

        mlflow.log_param("alpha", alpha)
        mlflow.log_param("l1_ratio", l1_ratio)

        mlflow.log_metric("accuracy", float(round(accuracy_score(y_pred=predicted_qualities,y_true=test_y),3)))
        #mlflow.log_metric("accuracy", '99.8')
        mlflow.log_metric("f1", float(round(f1_score(y_pred=predicted_qualities,y_true=test_y),3)))
        mlflow.log_metric("recall", float(round(recall_score(y_pred=predicted_qualities,y_true=test_y),3)))
        mlflow.log_metric("precision", float(round(precision_score(y_pred=predicted_qualities,y_true=test_y),3)))
        
        tracking_url_type_store = urlparse(mlflow.get_artifact_uri()).scheme
        
        if tracking_url_type_store != "file":
            mlflow.sklearn.log_model(
                model, 
                "model", 
                registered_model_name=mlflow_config["registered_model_name"])
        else:
            mlflow.sklearn.load_model(model, "model")
     
 


if __name__=="__main__":
    args = argparse.ArgumentParser()
    args.add_argument("--config", default="params.yaml")
    parsed_args = args.parse_args()
    train_and_evaluate(config_path=parsed_args.config)  