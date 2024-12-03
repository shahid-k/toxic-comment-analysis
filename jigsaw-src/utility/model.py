import boto3
import joblib
import re
import os
from nltk import download
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
import nltk
# from joblib import Parallel, delayed

# Set up nltk data path
# nltk.download('stopwords', download_dir='./nltk_data')
nltk.data.path.append('/var/task/nltk_data')

# Initialize S3 client
s3_client = boto3.client('s3')

# Initialize stopwords and stemmer
stop_words = set(stopwords.words('english'))

ps = PorterStemmer()

# Preprocess text
def preprocess_text(text):
    text = text.lower()
    text = re.sub(r'[^\w\s]', '', text)
    words = [ps.stem(word) for word in text.split() if word not in stop_words]
    return ' '.join(words)

# Predict toxicity from S3
def predict_toxicity_from_s3(model_uri, vectorizer_uri, s3_uri, text):
    try:
        # Paths for the downloaded files
        # model_path = '/var/task/utility/toxic_comment_model.pkl'
        # vectorizer_path = '/var/task/utility/vectorizer.pkl'

        model_path = './utility/toxic_comment_model.pkl'
        vectorizer_path = './utility/vectorizer.pkl'


        print(model_uri.split('/')[2], '/'.join(model_uri.split('/')[3:]), model_path)
        print(vectorizer_uri.split('/')[2], '/'.join(vectorizer_uri.split('/')[3:]), vectorizer_path)

        # Download model and vectorizer from S3
        # s3_client.download_file(s3_uri, '/'.join(model_uri.split('/')[3:]), model_path)
        # s3_client.download_file(s3_uri, '/'.join(vectorizer_uri.split('/')[3:]), vectorizer_path)

        # Load the model and vectorizer
        model = joblib.load(model_path)
        vectorizer = joblib.load(vectorizer_path)

        # Preprocess the input text
        processed_text = preprocess_text(text)

        # Vectorize the comment and predict toxicity
        vectorized_comment = vectorizer.transform([processed_text])
        prediction = model.predict(vectorized_comment)

        return prediction[0]  # Return the prediction result
    except Exception as err:
        print(str(err))
        return {"message": str(err), "success": False}
    finally:
        s3_client.close()

# Wrapper function to process a single text
def process_single_text(text, model_uri, vectorizer_uri, s3_uri):
    return predict_toxicity_from_s3(model_uri, vectorizer_uri, s3_uri, text)

