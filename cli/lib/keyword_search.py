from pathlib import Path
from lib import search_utils
import re
from nltk import PorterStemmer
from collections import defaultdict
import pickle

stemmer = PorterStemmer()
CURRENT_DIRECTORY = Path(__file__).resolve().parent
movies_directory = f"{CURRENT_DIRECTORY}/../../data/movies.json"
index_file_directory = f'{CURRENT_DIRECTORY}/../../cache/index.pkl'
docmap_file_directory = f'{CURRENT_DIRECTORY}/../../cache/docmap.pkl'





class InvertedIndex:

    def __init__(self):
        self.index = defaultdict(set)
        self.docmap = defaultdict(str)

    def __add_document(self, doc_id, text):
        print('adding document ', doc_id)
        tokenized = search_utils.tokenize_text(text)
        self.docmap[doc_id] = text
        for token in tokenized:
            self.index[token].add(doc_id)

    def get_documents(self, term):
        doc_ids = list(self.index[term])
        doc_ids.sort()
        return doc_ids

    def build(self):
        movie_json = search_utils.read_json(movies_directory)
        movie_list = movie_json['movies']
        for movie in movie_list:
            content = f'{movie['title']} {movie['description']}'
            movie_id = movie['id']
            self.__add_document(movie_id,content)

    def save(self):
        try:
            with open(index_file_directory, 'wb') as indexfile:
                pickle.dump(self.index,indexfile)
            with open(docmap_file_directory, 'wb') as docmap:
                pickle.dump(self.docmap, docmap)
        except Exception as e:
            print('PROBLEM WITH SAVING::: ',str(e))
            exit(1)
        

# Left off at l7: Tokenization





def search_movies(title: str):
    title = search_utils.clean(title)
    title_fragments = re.split(r'\s+', title)
    json_data = search_utils.read_json(movies_directory)
    stopwords = set(search_utils.load_stopwords())
    movies = json_data['movies']
    results_list = []

    for movie in movies:
        cleaned_title = search_utils.clean(movie['title'])
        for fragment in title_fragments:
            if fragment not in stopwords and stemmer.stem(fragment) in stemmer.stem(cleaned_title):
                results_list.append({'title': movie['title'], 'id': movie['id']})

    results_list.sort(key= lambda x: x['id'])
    shortened = results_list[:5]
    return shortened
