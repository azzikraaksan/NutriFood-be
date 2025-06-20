import joblib
import pickle
import numpy as np
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from rank_bm25 import BM25Okapi
import re

vectorizer = joblib.load('model/vectorizer_tfidf.joblib')
tfidf_matrix = joblib.load('model/tfidf_matrix.joblib')
bm25 = joblib.load('model/bm25_model.joblib')

with open('model/tokenized_corpus.pkl', 'rb') as f:
    tokenized_corpus = pickle.load(f)

with open('model/datalink.pkl', 'rb') as f:
    datalink = pickle.load(f)

with open('model/dokumen.pkl', 'rb') as f:
    dokumen = pickle.load(f)

def preprocess_query(query):
    query = str(query).lower()
    query = re.sub(r'[^a-zA-Z0-9\s]', '', query)  
    query = re.sub(r'\d+', ' ', query)            
    query = re.sub(r'\s{2,}', ' ', query)        
    return query.strip()

def search_cosine(query):
    query = preprocess_query(query)
    query_vector = vectorizer.transform([query])
    similarities = cosine_similarity(query_vector, tfidf_matrix).flatten()
    ranked_indices = similarities.argsort()[::-1]
    return [
        {
            'judul': datalink.iloc[i]['judul_clean'],
            'link': datalink.iloc[i]['link'],
            'gambar': dokumen.iloc[i]['gambar'],
            'score': float(similarities[i]),
            'bahan': dokumen.iloc[i]['bahan'],
            'tahapan': dokumen.iloc[i]['tahapan'],
            'gizi': dokumen.iloc[i]['ringkasan_gizi']
        }
        for i in ranked_indices if similarities[i] > 0
    ]

def search_bm25(query):
    query_tokens = query.lower().split()
    scores = bm25.get_scores(query_tokens)
    ranked_indices = np.argsort(scores)[::-1]
    return [
        {
            'judul': datalink.iloc[i]['judul_clean'],
            'link': datalink.iloc[i]['link'],
            'gambar': dokumen.iloc[i]['gambar'],
            'score': float(scores[i]),
            'bahan': dokumen.iloc[i]['bahan'],
            'tahapan': dokumen.iloc[i]['tahapan'],
            'gizi': dokumen.iloc[i]['ringkasan_gizi']
        }
        for i in ranked_indices if scores[i] > 0
    ]