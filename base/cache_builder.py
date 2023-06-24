import joblib
from sklearn.metrics.pairwise import cosine_similarity
import redis
import pickle
redis_client = redis.Redis(host='containers-us-west-160.railway.app', port=5875,password="YSueGOq98SZCXvuet2ey")
JOURNAL_VECTORIZER = joblib.load('vectorizer.joblib')
JOURNAL_TFIDF_MATRIX = joblib.load('journal_tfidf.joblib')









journal_threshold = 4

def get_journal_index(user_input):
    user_tfidf = JOURNAL_VECTORIZER.transform([user_input])
    cosine_similarities = cosine_similarity(user_tfidf, JOURNAL_TFIDF_MATRIX).flatten()
    indices = cosine_similarities.argsort()[::-1]
    top_recommendations = [i for i in indices if cosine_similarities[i] > 0][:min(journal_threshold, len(indices))]
    return top_recommendations
    
article_threshold = 10

def get_article_recommendations(user_input):
#     recommended_journals = get_journal_index(user_input)
#     l = []
#     for journal_id in recommended_journals:
#         user_tfidf = JOURNAL_MAIN['article_vectorizer'][journal_id].transform([user_input])
#         cosine_similarities = cosine_similarity(user_tfidf, JOURNAL_MAIN['article_matrix'][journal_id]).flatten()
#         indices = cosine_similarities.argsort()[::-1]
#         top_recommendation_articles = [(cosine_similarities[i], i, journal_id) for i in indices if cosine_similarities[i] > 0][:min(article_threshold, len(indices))]
#         l = l + top_recommendation_articles
#     l.sort(reverse=True)
#     return l
    pass
def get_links(user_input):
#     l = []
#     recommendation_list = get_article_recommendations(user_input)
#     for article in recommendation_list:
#         cosine_similarity, article_id, journal_id = article
#         l.append((JOURNAL_MAIN['article_df'][journal_id].iloc[article_id, 0], JOURNAL_MAIN['article_df'][journal_id].iloc[article_id, 1], article_id, journal_id))
#     return l
    pass
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
