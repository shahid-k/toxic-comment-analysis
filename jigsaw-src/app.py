from chalice import Chalice
import os
import json
from utils import model
from dotenv import load_dotenv

load_dotenv()

app = Chalice(app_name='jigsaw-src')

storage_location = os.getenv('bucket_name')
model_file_uri = os.getenv('model_file_uri')
vector_file_uri = os.getenv('vector_file_uri')

@app.route('/text',methods = ['POST'], cors = True)
def read_text():
    try:
        request_data = json.loads(app.current_request.raw_body)
        text_data = request_data['text']
        model_obj = model.predict_toxicity_from_s3(storage_location, model_file_uri, vector_file_uri)
        toxicity = model_obj.is_toxic(text_data)
        return True if toxicity>0.7 else False
    except Exception as err:
        return('Some error occured ', err)

