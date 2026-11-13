from pathlib import Path
from lib import search_utils
from nltk import PorterStemmer
from collections import defaultdict, Counter
import pickle

stemmer = PorterStemmer()
CURRENT_DIRECTORY = Path(__file__).resolve().parent
movies_directory = f"{CURRENT_DIRECTORY}/../../data/movies.json"
index_file_directory = f'{CURRENT_DIRECTORY}/../../cache/index.pkl'
docmap_file_directory = f'{CURRENT_DIRECTORY}/../../cache/docmap.pkl'
frequency_file_directory = f'{CURRENT_DIRECTORY}/../../cache/frequencies.pkl'




class InvertedIndex:

    def __init__(self):
        self.index = defaultdict(set)
        self.docmap = defaultdict(str)
        self.term_frequencies = defaultdict(Counter)

    def __add_document(self, doc_id, text):
        print('adding document ', doc_id)
        tokenized = search_utils.tokenize_text(text)
        self.docmap[doc_id] = text
        for token in tokenized:
            self.index[token].add(doc_id)
            self.term_frequencies[doc_id][token]+= 1

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
        tokenized = search_utils.tokenize_text(term)
        if len(tokenized) != 1:
            raise ValueError('Must provide exactly one word to be tokenized')
        return tokenized[0]


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

    # title = search_utils.clean(title)
    # title_fragments = re.split(r'\s+', title)
    # json_data = search_utils.read_json(movies_directory)
    # stopwords = set(search_utils.load_stopwords())
    # movies = json_data['movies']
    # results_list = []

    # for movie in movies:
    #     cleaned_title = search_utils.clean(movie['title'])
    #     for fragment in title_fragments:
    #         if fragment not in stopwords and stemmer.stem(fragment) in stemmer.stem(cleaned_title):
    #             results_list.append({'title': movie['title'], 'id': movie['id']})

    # results_list.sort(key= lambda x: x['id'])
    # shortened = results_list[:5]
    # return shortened
