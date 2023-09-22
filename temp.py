import tweepy
import config
import re
import nltk
import pandas as pd
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix

# Define your Twitter API credentials
consumer_key = config.twitter_key
consumer_secret = config.twitter_secret
access_token = config.twitter_token_access
access_token_secret = config.twitter_token_secret

# Initialize Tweepy with your credentials
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

# Function to extract Twitter username from URL
def extract_username_from_url(url):
    match = re.search(r'(?:https?://twitter\.com/)?@?([A-Za-z0-9_]+)', url)
    if match:
        return match.group(1)
    return None

# Function to get user details by username
def get_user_details(username):
    try:
        user = api.get_user(screen_name=username)
        return user._json
    except tweepy.TweepyException as e:
        return {'error': str(e)}

# Load a sample dataset (you should have a labeled dataset of real and fake accounts)
data = [
    {"username": "elonmusk", "description": "CEO of SpaceX", "label": 0},
    {"username": "fakeuser123", "description": "Get rich quick!", "label": 1},
    # Add more data here
]

# Convert the dataset to a DataFrame
df = pd.DataFrame(data)

# Text preprocessing and feature extraction
nltk.download("stopwords")
stop_words = set(stopwords.words("english"))

def preprocess_text(text):
    # Remove special characters and numbers
    text = re.sub(r"[^a-zA-Z]", " ", text)
    # Convert to lowercase
    text = text.lower()
    # Tokenization and remove stopwords
    tokens = nltk.word_tokenize(text)
    tokens = [word for word in tokens if word not in stop_words]
    return " ".join(tokens)

df["description"] = df["description"].apply(preprocess_text)

# Split the dataset into train and test sets
X_train, X_test, y_train, y_test = train_test_split(
    df["description"], df["label"], test_size=0.2, random_state=42
)

# TF-IDF Vectorization
vectorizer = TfidfVectorizer()
X_train_tfidf = vectorizer.fit_transform(X_train)
X_test_tfidf = vectorizer.transform(X_test)

# Train a simple Random Forest Classifier
clf = RandomForestClassifier()
clf.fit(X_train_tfidf, y_train)

# Make predictions on the test set
y_pred = clf.predict(X_test_tfidf)

# Evaluate the model
accuracy = accuracy_score(y_test, y_pred)
conf_matrix = confusion_matrix(y_test, y_pred)
class_report = classification_report(y_test, y_pred)

print(f"Accuracy: {accuracy}")
print("Confusion Matrix:\n", conf_matrix)
print("Classification Report:\n", class_report)
