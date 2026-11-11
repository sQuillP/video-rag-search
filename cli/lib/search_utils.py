import json
import re
from pathlib import Path
from nltk import PorterStemmer
from functools import cache

CURRENT_DIRECTORY = Path(__file__).resolve().parent
stopwords_directory = f"{CURRENT_DIRECTORY}/../../data/stopwords.json"
stemmer = PorterStemmer()

def read_json(path: str):
    data = None
    with open(file=path, mode='r', encoding='utf-8') as file:
        data = file.read()
    return json.loads(data)


def clean(term: str) -> str:
    cleaned = re.sub(r'[^a-z A-Z0-9]', '', term).lower().strip()
    return cleaned


def tokenize_text(sentence:str):
    sentence_frags = re.split(r'\s+', sentence)
    stopwords = load_stopwords()
    tokens = []
    for word in sentence_frags:
        word = clean(word)
        if word in stopwords:
            continue

        stemmed_word = stemmer.stem(word)
        tokens.append(stemmed_word)
    return tokens


"""
    Returns a list of clean stopwords to use
"""
@cache
def load_stopwords():
    stopwords = read_json(stopwords_directory)
    cleaned_words = []
    for word in stopwords['words']:
        cleaned_words.append(clean(word))
    return set(cleaned_words)