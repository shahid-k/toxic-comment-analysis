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
        # model.test_model()
    except Exception as err:
        return('Some error occured ', err)

