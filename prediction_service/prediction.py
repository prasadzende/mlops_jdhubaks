import yaml
import os
import json
import joblib
import numpy as np


params_path = "params.yaml"
# schema_path = os.path.join("prediction_service", "schema_in.json")

# class NotInRange(Exception):
#     def __init__(self, message="Values entered are not in expected range"):
#         self.message = message
#         super().__init__(self.message)

# class NotInCols(Exception):
#     def __init__(self, message="Not in cols"):
#         self.message = message
#         super().__init__(self.message)



def read_params(config_path=params_path):
    with open(config_path) as yaml_file:
        config = yaml.safe_load(yaml_file)
    return config

def predict(data):
    config = read_params(params_path)
    model_dir_path = config["webapp_model_dir"]
    model = joblib.load(model_dir_path)
    prediction = model.predict(data).tolist()[0]
    return prediction


def form_response(dict_request):
    #if validate_input(dict_request):
    data = dict_request.values()
    data = [list(map(float, data))]
    response = predict(data)
    return response

def api_response(dict_request):
    try:
        #if validate_input(dict_request):
        data = np.array([list(dict_request.values())])
        response = predict(data)
        response = {"response": response}
        return response
            


    except Exception as e:
        response = {"response": str(e) }
        return response