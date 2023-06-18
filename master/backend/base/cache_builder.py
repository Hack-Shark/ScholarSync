import os
import re

import nltk
from nltk.corpus import stopwords
from nltk.tag import pos_tag
from nltk.tokenize import word_tokenize

nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
nltk.download('stopwords')
stop_words = set(stopwords.words('english'))
import pandas as pd
from joblib import Memory
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
# Set the base directory
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Set the cache directory
CACHE_DIR = os.path.join(BASE_DIR, 'cache')

# Create the cache directory if it doesn't exist
if not os.path.exists(CACHE_DIR):
    os.makedirs(CACHE_DIR)

def get_paragraph(row,index):
  ans=''
  for x in row[index]:
    ans=ans+'  '+x.lower()
  return ans
def get_clean_text(row,index):
    if not isinstance(row[index], str):
        return '' 
    clean_text=''
    words = re.findall(r'\b\w+\b', row[index].lower())
    words = row[index].lower().split()
    for word in words:
        if( re.match(r'^[a-zA-Z]+$', word) and  word not in stop_words and len(word) >1 and word[1] != '.'):
            clean_text=clean_text+' '+word
    return clean_text
def combine(row,indices):
    ans=''
    for i in indices:
      ans=ans+' '+row[i]
    return ans
# Create a memory object with the cache directory
memory = Memory(CACHE_DIR)
journal_threshold=4

@memory.cache
def get_main_df(): 
    curr_dir=os.getcwd()
    data_file_path=os.path.join(curr_dir,'../training_data/springer_data.csv')
    main=pd.read_csv(data_file_path)
    main=main[main['Language']=='en']
    main=main.drop(['Language','Item DOI'],axis=1)
    return main

MAIN=get_main_df()

@memory.cache
def get_journal_df():
    journal_art = MAIN.groupby('Publication Title')['Item Title'].apply(list).reset_index(name='Articles')
    journal_art.set_index(['Publication Title'],inplace=True)
    journal_auth = MAIN.groupby('Publication Title')['Authors'].apply(list).reset_index(name='Authors')
    journal_auth.set_index(['Publication Title'],inplace=True)
    journal_key= MAIN.drop_duplicates(subset=["Publication Title", "Keywords"], keep='first')
    journal_key=journal_key.drop(['Item Title','Authors','Publication Year','URL'],axis=1)
    journal_key.set_index(['Publication Title'],inplace=True)
    journal_main = pd.concat([journal_key, journal_art,journal_auth], axis=1, join='inner')
    journal_main=journal_main.reset_index()
    journal_main['Articles']=journal_main.apply(get_paragraph,index='Articles',axis=1)
    journal_main['Articles']=journal_main.apply(get_clean_text,index='Articles',axis=1)
    journal_main['Authors']=journal_main.apply(get_paragraph,index='Authors',axis=1)
    journal_main['Authors']=journal_main.apply(get_clean_text,index='Authors',axis=1)
    journal_main['Keywords']=journal_main.apply(get_clean_text,index=1,axis=1)
    journal_main['Tokenized'] = journal_main['Articles'].apply(word_tokenize)
    journal_main['Tagged'] = journal_main['Tokenized'].apply(pos_tag)
    journal_main['Tags'] = journal_main['Tagged'].apply(lambda x: [word for word, tag in x if tag.startswith('NN') or tag.startswith('JJ')])
    journal_main['Tags'] = journal_main['Tags'].apply(lambda x: [word for word in x if word.lower() not in stop_words])
    journal_main['Tags']=journal_main.apply(get_paragraph,index='Tags',axis=1)
    journal_main=journal_main.drop(['Articles','Tokenized','Tagged'],axis=1)
    journal_main['Tags']=journal_main.apply(combine,indices=['Keywords','Tags','Authors'],axis=1)
    journal_main['Tags']=journal_main.apply(get_clean_text,index='Tags',axis=1)
    journal_main=journal_main.drop(['Keywords','Authors'],axis=1)
    return journal_main


TEMP_JOURNAL_MAIN=get_journal_df()

@memory.cache
def get_tfidf_journal_matrix():
    journal_main=TEMP_JOURNAL_MAIN
    journal_vectorizer = TfidfVectorizer(decode_error='ignore',strip_accents='ascii')
    journal_tfidf_matrix = journal_vectorizer.fit_transform(journal_main['Tags'])
    return journal_tfidf_matrix,journal_vectorizer

JOURNAL_TFIDF_MATRIX,JOURNAL_VECTORIZER=get_tfidf_journal_matrix()

def get_journal_index(user_input):
    user_tfidf = JOURNAL_VECTORIZER.transform([user_input])
    cosine_similarities = cosine_similarity(user_tfidf, JOURNAL_TFIDF_MATRIX).flatten()
    indices = cosine_similarities.argsort()[::-1]
    top_recommendations = [i for i in indices if cosine_similarities[i] > 0][:min(journal_threshold, len(indices))]
    return top_recommendations

def get_article_df(row):
    article = MAIN.loc[MAIN['Publication Title'] == TEMP_JOURNAL_MAIN['Publication Title'][row.name]].copy()
    article['Item Title']=article.apply(get_clean_text,index='Item Title',axis=1)
    article['Authors']=article.apply(get_clean_text,index='Authors',axis=1)
    article['Tokenized'] = article['Item Title'].apply(word_tokenize)
    article['Tagged'] = article['Tokenized'].apply(pos_tag)
    article['Tags'] = article['Tagged'].apply(lambda x: [word for word, tag in x if tag.startswith('NN') or tag.startswith('JJ')and word.lower() not in stop_words])
    article['Tags']=article.apply(get_paragraph,index='Tags',axis=1)
    article['Tags']=article.apply(lambda x : x['Tags']+' '+x['Authors']+' '+str(x['Publication Year']),axis=1)
    article=article.drop(['Keywords','Publication Title','Tokenized','Tagged','Authors','Publication Year'],axis=1)
    article.reset_index(inplace=True)
    article.set_index('index', inplace=True)
    return article

def get_vectorizer(row):
    vectorizer = TfidfVectorizer(decode_error='ignore',strip_accents='ascii')
    return vectorizer
def get_tfidf_matrix(row):
    tfidf_matrix = row['article_vectorizer'].fit_transform(row['article_df']['Tags'])
    return tfidf_matrix

@memory.cache
def preprocess_article_df():
    journal_main=TEMP_JOURNAL_MAIN
    journal_main['article_df']=journal_main.apply(get_article_df,axis=1)
    journal_main['article_vectorizer']=journal_main.apply(get_vectorizer,axis=1)
    journal_main['article_matrix']=journal_main.apply(get_tfidf_matrix,axis=1)
    return journal_main

JOURNAL_MAIN=preprocess_article_df()


article_threshold=10

def get_article_recommendations(user_input):
    recommended_journals=get_journal_index(user_input)
    l=[]
    for journal_id in recommended_journals:
        user_tfidf=JOURNAL_MAIN['article_vectorizer'][journal_id].transform([user_input])
        cosine_similarities = cosine_similarity(user_tfidf, JOURNAL_MAIN['article_matrix'][journal_id]).flatten()
        indices = cosine_similarities.argsort()[::-1]
        top_recommendation_articles = [(cosine_similarities[i],i,journal_id) for i in indices if cosine_similarities[i] > 0][:min(article_threshold, len(indices))]
        l=l+top_recommendation_articles
    l.sort(reverse=True)
    return l

def get_links(user_input):
    l=[]
    recommendation_list=get_article_recommendations(user_input)
    for article in recommendation_list:
        cosine_similarity,article_id,journal_id=article
        l.append((JOURNAL_MAIN['article_df'][journal_id].iloc[article_id,0],JOURNAL_MAIN['article_df'][journal_id].iloc[article_id,1]))
        # print(name,url)
    return l

