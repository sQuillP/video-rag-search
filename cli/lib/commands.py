import math
from . import keyword_search

index = keyword_search.InvertedIndex()
index.load()


def build():
    # Must do this before creating new cache. Dump the old
    index.initialize()
    valid = index.build()
    if valid:
        print('successfully built the index')
    else:
        print('something went wrong building the index')
    success = index.save()
    if success:
        print('successfully saved the index')
    else:
        print('unable to save the index. Something went wrong...')

def idf(term: str):
    token = index.tokenize_term(term)
    counts = len(index.get_documents(token)) + 1
    total = len(index.docmap.keys()) + 1

    return math.log(total / counts)

def tf(doc_id:int, term:str):
    token = index.tokenize_term(term)
    frequency = index.get_tf(doc_id, token)
    return frequency

def tfidf(doc_id:int, term:str):
    token = index.tokenize_term(term)
    # TF-IDF = TF * IDF
    tf_score = tf(doc_id, token)
    idf_score = idf(token)
    tfidf_score = tf_score * idf_score

    return tfidf_score

def bm25idf(term:str):
    return index.get_bm25_idf(term=term)


def bm25tf(doc_id:int, term:str, k1:float, b:float):
    return index.get_bm25_tf(doc_id=doc_id, term=term, k1=k1, b=b)

