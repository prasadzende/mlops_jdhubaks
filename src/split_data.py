import os
import argparse
import pandas as pd
from sklearn.model_selection import train_test_split
from get_data import read_params
from sklearn.decomposition import PCA

def split_and_saved_data(config_path):
    config = read_params(config_path)
    test_data_path = config["split_data"]["test_path"] 
    train_data_path = config["split_data"]["train_path"]
    raw_data_path = config["load_data"]["raw_dataset_csv"]
    split_ratio = config["split_data"]["test_size"]
    random_state = config["base"]["random_state"]
    target = config["base"]["target_col"]

    df = pd.read_csv(raw_data_path, sep=",")
    df.drop('Time',axis=1,inplace=True)
    pca = PCA(n_components=2)
    principalComponents = pca.fit_transform(df.drop(target,axis=1))

    principalDf = pd.DataFrame(data = principalComponents, 
                            columns = ['input_1', 'input_2'])
    final_df = pd.concat([df[target], principalDf],axis=1)  
    
    
    train, test = train_test_split(
        final_df,
        test_size=split_ratio, 
        random_state=random_state
        )   
    train.to_csv(train_data_path, sep=",", index=False, encoding="utf-8")
    test.to_csv(test_data_path, sep=",", index=False, encoding="utf-8")

if __name__=="__main__":
    args = argparse.ArgumentParser()
    args.add_argument("--config", default="params.yaml")
    parsed_args = args.parse_args()
    split_and_saved_data(config_path=parsed_args.config)