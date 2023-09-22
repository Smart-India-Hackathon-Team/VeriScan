#!/usr/bin/env python3

import nltk

# Download the "stopwords" dataset
nltk.download('stopwords')

# Import stopwords after downloading
from nltk.corpus import stopwords

# Load English stopwords
stop_words = set(stopwords.words("english"))
