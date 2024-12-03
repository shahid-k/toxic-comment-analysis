# Use AWS Lambda Python 3.11 base image
FROM public.ecr.aws/lambda/python:3.11

# Copy function code and dependencies
COPY app.py ${LAMBDA_TASK_ROOT}
COPY requirements.txt .
RUN pip install -r requirements.txt -t ${LAMBDA_TASK_ROOT}

# Copy supporting files
COPY utility/ ${LAMBDA_TASK_ROOT}/utility
COPY nltk_data/ ${LAMBDA_TASK_ROOT}/nltk_data
COPY .env ${LAMBDA_TASK_ROOT}/.env

# Copy model files (ensure these are included)
COPY utility/toxic_comment_model.pkl ${LAMBDA_TASK_ROOT}/utility/toxic_comment_model.pkl
COPY utility/vectorizer.pkl ${LAMBDA_TASK_ROOT}/utility/vectorizer.pkl

# Set the Lambda handler
CMD ["app.lambda_handler"]

ENV bucket_name=jigsaw-toxic-dataset
ENV model_file_uri=https://jigsaw-toxic-dataset.s3.us-east-1.amazonaws.com/toxic_comment_model.pkl
ENV vector_file_uri=https://jigsaw-toxic-dataset.s3.us-east-1.amazonaws.com/vectorizer.pkl