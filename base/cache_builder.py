import joblib
import os
from sklearn.metrics.pairwise import cosine_similarity
from .models import JournalArticle
from sklearn.feature_extraction.text import TfidfVectorizer
from django.shortcuts import get_object_or_404
BASE_DIR=os.getcwd()
JOURNAL_VECTORIZER = joblib.load(os.path.join(BASE_DIR,'joblib','vectorizer.joblib'))
JOURNAL_TFIDF_MATRIX = joblib.load(os.path.join(BASE_DIR,'joblib','journal_tfidf.joblib'))

journal_threshold = 3



def get_journal_index(user_input):
    user_tfidf = JOURNAL_VECTORIZER.transform([user_input])
    cosine_similarities = cosine_similarity(user_tfidf, JOURNAL_TFIDF_MATRIX).flatten()
    indices = cosine_similarities.argsort()[::-1]
    top_recommendations = [i for i in indices if cosine_similarities[i] > 0][:min(journal_threshold, len(indices))]
    print(top_recommendations)
    return top_recommendations
    
article_threshold = 10

def get_article_recommendations(user_input):
    l=[]
    recommended_journals = get_journal_index(user_input)
    for journal_id in recommended_journals:
        tfidf_matrix_file_path=os.path.join(BASE_DIR,'joblib',f"journal_tfidf_{journal_id}.joblib")
        vectorizer_file_path=os.path.join(BASE_DIR,'joblib',f"vectorizer_{journal_id}.joblib")
        tfidf_matrix=joblib.load(tfidf_matrix_file_path)
        vectorizer=joblib.load(vectorizer_file_path)
        user_tfidf = vectorizer.transform([user_input])
        cosine_similarities = cosine_similarity(user_tfidf, tfidf_matrix).flatten()
        indices = cosine_similarities.argsort()[::-1]
        top_recommendation_articles = [(cosine_similarities[i], i, journal_id) for i in indices if cosine_similarities[i] > 0][:min(10, len(indices))]
        l.extend(top_recommendation_articles)
    l.sort(reverse=True)
    return l

def get_links(user_input):
    l = []
    print("hi from get_links")
    recommendation_list = get_article_recommendations(user_input)
    # print(recommendation_list)
    for article in recommendation_list:
        cosine_similarity, article_id, journal_id = article
        try:
            article_obj = get_object_or_404(JournalArticle, publication_index=journal_id, article_index=article_id)
        except :
            print(journal_id,article_id)
            pass
        l.append((article_obj.article_tags,article_obj.url,article_obj.article_index,article_obj.publication_index))
    return l
def compare_user_input_with_tags(user_input):
    # tags = ' '.join(JOURNAL_MAIN['Tags'].values.tolist())
    # tags = set(tags.split())
    
    # user_words = set(user_input.lower().split())
    
    # if any(word in tags for word in user_words):
    #     return "valid"
    # else:
    #     return "invalid"
    return "valid"
    pass
