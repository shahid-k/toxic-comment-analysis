import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
import re
import boto3
import nltk
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer

class test_model():
        def __init__(self, bucket_name, model, vectorizer):
            self.client = boto3.client(bucket_name)
            self.bucket_name = storage_service.get_storage_location()
            self.storage_service = storage_service
            self.model = joblib.load('toxic_comment_model.pkl')  # Adjust path if needed
            self.vectorizer = joblib.load('vectorizer.pkl')  # Adjust path if vectorizer is separate

        def preprocess_text(self, text):
            nltk.download('stopwords')
            stop_words = set(stopwords.words('english'))  # Correct initialization
            ps = PorterStemmer()
            text = text.lower()
            # Remove special characters
            text = re.sub(r'[^\w\s]', '', text)
            # Tokenize and remove stopwords
            words = [ps.stem(word) for word in text.split() if word not in stop_words]
            return ' '.join(words)

        def is_toxic(self, comment):
            # Preprocess the input comment
            processed_comment = self.preprocess_text(comment)
            # Transform the comment using the vectorizer
            vectorized_comment = self.vectorizer.transform([processed_comment])
            # Predict toxicity
            prediction = self.model.predict(vectorized_comment)
            return bool(prediction[0])  # Return True for toxic, False otherwise
