import json
from chalice import Chalice
from utility import model
from dotenv import load_dotenv
import os
import logging
from chalice import Response

load_dotenv(os.path.join(os.path.dirname(__file__), '.env'))

app = Chalice(app_name="jigsaw-local")
app.log.setLevel(logging.DEBUG)

# Load environment variables
storage_location = os.getenv("bucket_name", "jigsaw-toxic-dataset")
model_file_uri = os.getenv("model_file_uri", "https://jigsaw-toxic-dataset.s3.us-east-1.amazonaws.com/toxic_comment_model.pkl")
vector_file_uri = os.getenv("vector_file_uri", "https://jigsaw-toxic-dataset.s3.us-east-1.amazonaws.com/vectorizer.pkl")



# Process a single text using the model
def process_single_text(text, model_uri, vector_uri, s3_uri):
    return model.predict_toxicity_from_s3(model_uri, vector_uri, s3_uri, text)


@app.route("/text", methods=["POST"], cors=True)
def read_text():
    app.log.debug("Entered read_text route")
    print("Entered read_text route")
    
    try:
        if not app.current_request.raw_body:
            app.log.error("Empty request body")
            return {"message": "Empty request body.", "success": False}

        request_data = json.loads(app.current_request.raw_body)
        app.log.debug(f"Parsed request data: {request_data}")

        if "text" not in request_data:
            app.log.error("Missing 'text' in request payload")
            return {"message": "Missing 'text' in request payload.", "success": False}

        if not isinstance(request_data["text"], str):
            app.log.error("Invalid 'text' type")
            return {"message": "'text' must be a string.", "success": False}

        text_data = request_data["text"]
        app.log.debug(f"Processing text: {text_data}")

        # Simulate processing
        toxicity = process_single_text(text_data, model_file_uri, vector_file_uri, storage_location)
        app.log.debug(f"Processed toxicity: {toxicity}")

        if not isinstance(toxicity, dict):
            value = True if toxicity > 0.7 else False
            result = {
                "value": value,
                "toxicity": float(toxicity),
            }
            return Response(
                status_code=200,
                headers={
                    'Content-Type': 'application/json',
                    'access-control-allow-origin': "*"
                },
                body=json.dumps(result)
            )
        else:
            return Response(
                status_code=200,
                headers={
                    'Content-Type': 'application/json',
                    'access-control-allow-origin': "*"
                },
                body=json.dumps(toxicity)
            )

    except Exception as err:
        app.log.error(f"Exception occurred: {err}", exc_info=True)
        return Response(
            status_code=500,
            headers={'Content-Type': 'application/json'},
            body=json.dumps({'error': str(e)})
        )


# Lambda handler
def lambda_handler(event, context):
    import copy

    app.log.debug(f"Received event: {json.dumps(event)}")
    try:
        # Create a copy of the event to avoid modifying the original
        event_copy = copy.deepcopy(event)

        # List of keys that Chalice expects in the event
        required_keys = [
            'resource', 'path', 'httpMethod', 'headers', 'multiValueHeaders',
            'queryStringParameters', 'multiValueQueryStringParameters', 'pathParameters',
            'stageVariables', 'requestContext', 'body', 'isBase64Encoded'
        ]

        # Ensure all required keys are present
        for key in required_keys:
            if key not in event_copy:
                if key == 'requestContext':
                    event_copy[key] = {
                        'accountId': '123456789012',
                        'resourceId': 'resourceId',
                        'stage': 'prod',
                        'requestId': context.aws_request_id,
                        'identity': {
                            'sourceIp': '127.0.0.1',
                            'userAgent': 'Custom User Agent'
                        },
                        'resourcePath': event_copy.get('path', '/'),
                        'httpMethod': event_copy.get('httpMethod', 'GET')
                    }
                elif key == 'headers':
                    event_copy[key] = {}
                elif key == 'multiValueHeaders':
                    event_copy[key] = {}
                elif key == 'path':
                    event_copy[key] = event_copy.get('resource', '/')
                else:
                    event_copy[key] = None

        # Handle CORS preflight (OPTIONS) requests
        if event_copy['httpMethod'] == 'OPTIONS':
            app.log.debug("Handling CORS preflight request")
            return {
                'statusCode': 200,
                'headers': {
                    'Access-Control-Allow-Origin': '*',
                    'Access-Control-Allow-Methods': 'POST,OPTIONS',
                    'Access-Control-Allow-Headers': 'Content-Type, Authorization',
                },
                'body': ''
            }

        response = app(event_copy, context)
        app.log.debug(f"Response from app: {response}")

        # Add CORS headers to the response
        if 'headers' not in response:
            response['headers'] = {}
        response['headers']['Access-Control-Allow-Origin'] = '*'
        response['headers']['Access-Control-Allow-Methods'] = 'POST,OPTIONS'
        response['headers']['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'

        return response
    except Exception as err:
        app.log.error(f"Unhandled exception in lambda_handler: {err}", exc_info=True)
        return {
            "statusCode": 500,
            "headers": {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'POST,OPTIONS',
                'Access-Control-Allow-Headers': 'Content-Type, Authorization',
            },
            "body": json.dumps({"message": str(err)})
        }

