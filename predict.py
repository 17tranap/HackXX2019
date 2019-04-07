import sys

from google.cloud import automl_v1beta1 as automl
from google.cloud.automl_v1beta1 import enums
from google.cloud.automl_v1beta1.proto import service_pb2

def predict(imageName, score_threshold=""):
    #model_id = "projects/ace-connection-236822/models/DefenseMoveEstimator"
    model_id = "ICN2459521650166688930"
    project_id = "ace-connection-236822"
    file_path = "/home/alexandria/hackathon/HackXX2019/"
    compute_region = "us-central1"
    automl_client = automl.AutoMlClient()

    # Get the full path of the model
    model_full_id = automl_client.model_path(project_id, compute_region, model_id)

    # Create client for prediction service
    prediction_client = automl.PredictionServiceClient()

    imagePathName = file_path + imageName
    with open(imagePathName, "rb") as image_file:
        content = image_file.read()
    
    payload = {"image": {"image_bytes": content}}

    params = {}
    if score_threshold:
        params = {"score_threshold": score_threshold}

    response = prediction_client.predict(model_full_id, payload, params)
    output = ""
    for result in response.payload:
        output += result.display_name

    return output
