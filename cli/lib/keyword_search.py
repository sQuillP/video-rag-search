from pathlib import Path
from lib import search_utils
from nltk import PorterStemmer
from collections import defaultdict, Counter
import pickle
import math
from .constants import Constants

stemmer = PorterStemmer()
CURRENT_DIRECTORY = Path(__file__).resolve().parent
movies_directory = f"{CURRENT_DIRECTORY}/../../data/movies.json"
index_file_directory = f'{CURRENT_DIRECTORY}/../../cache/index.pkl'
docmap_file_directory = f'{CURRENT_DIRECTORY}/../../cache/docmap.pkl'
frequency_file_directory = f'{CURRENT_DIRECTORY}/../../cache/frequencies.pkl'
doc_lengths_file_directory = f'{CURRENT_DIRECTORY}/../../cache/doc_lengths.pkl'





class InvertedIndex:


    def __init__(self):
        self.initialize()

    def __add_document(self, doc_id, text):
        print('adding document ', doc_id)
        tokenized = search_utils.tokenize_text(text)
        self.docmap[doc_id] = text
        for token in tokenized:
            self.index[token].add(doc_id)
            self.term_frequencies[doc_id][token]+= 1
        self.doc_lengths[doc_id] += len(tokenized)

    def get_documents(self, term: str):
        doc_ids = list(self.index[term])
        doc_ids.sort()
        return doc_ids

    def build(self):
        try:
            movie_json = search_utils.read_json(movies_directory)
            movie_list = movie_json['movies']
            for movie in movie_list:
                content = f'{movie['title']} {movie['description']}'
                movie_id = movie['id']
                self.__add_document(movie_id,content)
            return True
        except BaseException as ex:
            print('unable to build...', str(ex))
            return False

    def get_tf(self, doc_id, term):
        if doc_id not in self.term_frequencies or term not in self.term_frequencies[doc_id]:
            print("not in here")
            return 0
        frequency = self.term_frequencies[doc_id][term]
        return frequency

    def tokenize_term(self, term:str):
        tokenized:list[str] = search_utils.tokenize_text(term)
        if len(tokenized) != 1:
            raise ValueError('Must provide exactly one word to be tokenized')
        return tokenized[0]

    def get_bm25_idf(self, term:str) -> float:
        token = self.tokenize_term(term)
        N = len(self.docmap.keys())
        df = len(self.index[token])
        bm25_idf = math.log((N - df + 0.5) / (df + 0.5) + 1)
        return bm25_idf

    def get_bm25_tf(self, doc_id:int, term:str, k1=Constants.BM25_K1, b=Constants.BM25_B):
        token = self.tokenize_term(term)
        doc_length = self.doc_lengths[doc_id]
        avg_doc_length = self.__get_avg_doc_length()
        length_norm = 1 - b + b * (doc_length / avg_doc_length)
        tf = self.get_tf(doc_id, token)
        bm25_sat = (tf * (k1 + 1)) / (tf + k1 * length_norm)
        return bm25_sat

    def __get_avg_doc_length(self) -> float:
        doc_ids = self.doc_lengths.keys()
        N = len(doc_ids)
        if N == 0:
            return 0
        current_sum = 0
        for key in doc_ids:
            current_sum += self.doc_lengths[key]
        average = (current_sum) / (N)

        print(f'N={N}, current_sum={current_sum}')
        return average

    def initialize(self):
        self.index = defaultdict(set)
        self.docmap = defaultdict(str)
        self.term_frequencies = defaultdict(Counter)
        self.doc_lengths = defaultdict(int)


    def bm25(self, doc_id:int, term:str):
        tf = self.get_bm25_tf(doc_id, term)
        idf = self.get_bm25_idf(term)

        score = tf + idf


    

    def save(self):
        try:
            print('writing index file')
            with open(index_file_directory, 'wb') as indexfile:
                pickle.dump(self.index,indexfile)
            print('writing document map')
            with open(docmap_file_directory, 'wb') as docmap:
                pickle.dump(self.docmap, docmap)
            print('writing frequency file')
            with open(frequency_file_directory, 'wb') as freq_file:
                pickle.dump(self.term_frequencies, freq_file)
            print('writing doc_len_file')
            with open(doc_lengths_file_directory, 'wb') as doc_len_file:
                pickle.dump(self.doc_lengths, doc_len_file)
            return True
        except Exception as e:
            print('PROBLEM WITH SAVING::: ',str(e))
            return False

    def load(self):
        try:
            with open(index_file_directory, 'rb') as index_file:
                self.index = pickle.load(index_file)
            with open(docmap_file_directory, 'rb') as docmap_file:
                self.docmap = pickle.load(docmap_file)
            with open(frequency_file_directory, 'rb') as frequency_file:
                self.term_frequencies = pickle.load(frequency_file)
            with open(doc_lengths_file_directory, 'rb') as doc_len_freq_file:
                self.doc_lengths = pickle.load(doc_len_freq_file)
            print('data successfully loaded')
            return True
        except FileNotFoundError as fnfe:
            print('Error loading cached files', str(fnfe))
            return False
        except BaseException as be:
            print('Base exception occurred: ', str(be))
            return False

# Left off at l7: Tokenization





def search_movies(title: str, inverted:InvertedIndex, count = 5):

    title = search_utils.clean(title)
    fragments = search_utils.tokenize_text(title)
    counter = 0
    results = []
    for token in fragments:
        for word in inverted.index.keys():
            if token == word:
                for id in inverted.get_documents(word):
                    if counter >= count:
                        return results
                    row = {'content': inverted.docmap[id], 'id': id}
                    results.append(row)
                    counter += 1
    return results