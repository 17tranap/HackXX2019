import sys

from google.cloud import automl_v1beta1
from google.cloud.automl_v1beta1.proto import service_pb2

#params: content is image
def get_prediction(content, project_id, model_id):
  prediction_client = automl_v1beta1.PredictionServiceClient()

  name = 'projects/{}/locations/us-central1/models/{}'.format(project_id, model_id)
  payload = {'image': {'image_bytes': content }}
  params = {}
  request = prediction_client.predict(name, payload, params)
  return request  # waits till request is returned

#if name == 'main':
#  file_path = sys.argv[1]
#  project_id = sys.argv[2]
#  model_id = sys.argv[3]
#
#  with open(file_path, 'rb') as ff:
#    content = ff.read()

model_id = "ICN2459521650166688930"
project_id = "ace-connection-236822"
#get_prediction(content, "ace-connection-236822",  "ICN2459521650166688930")
