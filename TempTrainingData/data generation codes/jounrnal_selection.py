import pandas as pd
main=pd.read_csv('training_data\springer_data.csv')
main=main[main['Language']=='en']
main=main.drop(['Language','Item DOI'],axis=1)
main.head()
main.describe()

main.reset_index()
main.rename(columns={'index': 'ITem_ID'}, inplace=True)
main.head()

"""### Journal Dataframe"""

journal_art = main.groupby('Publication Title')['Item Title'].apply(list).reset_index(name='Articles')
journal_art.head()

journal_art.set_index(['Publication Title'],inplace=True)
journal_art.head()

journal_key= main.drop_duplicates(subset=["Publication Title", "Keywords"], keep='first')
journal_key=journal_key.drop(['Item Title','Authors','Publication Year','URL'],axis=1)
journal_key.head()
journal_key.set_index(['Publication Title'],inplace=True)

journal_key.head()

journal_main = pd.concat([journal_key, journal_art], axis=1, join='inner')
journal_main.head()

journal_main=journal_main.reset_index()
journal_main.head()

def get_paragraph(row):
  ans=''
  for x in row[2]:
    ans=ans+''+x.lower()
  return ans
journal_main['Articles']=journal_main.apply(get_paragraph,axis=1)
journal_main.head()

import nltk
from nltk.tokenize import word_tokenize
from nltk.tag import pos_tag
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
# Tokenize and perform POS tagging for each row
journal_main['Tokenized'] = journal_main['Articles'].apply(word_tokenize)
journal_main['Tagged'] = journal_main['Tokenized'].apply(pos_tag)
journal_main['Tags'] = journal_main['Tagged'].apply(lambda x: [word for word, tag in x if tag.startswith('NN') or tag.startswith('JJ')])
print(journal_main.head())
exit()
nltk.download('stopwords')
from nltk.corpus import stopwords
stop_words = set(stopwords.words('english'))
journal_main['Tags'] = journal_main['Tags'].apply(lambda x: [word for word in x if word.lower() not in stop_words])
journal_main.head()

# journal_main=journal_main.drop(['Articles','Tokenized','Tagged'],axis=1)
backup=journal_main
journal_main.head()

def get_tags(row):
  ans=''
  for x in row[2]:
    ans=ans+' '+x.lower()
  return ans
def combine_key(row):
  ans=row[2]+' '
  if(isinstance(row[1],str)):
    for x in row[1]:
      ans=ans+''+x.lower()
  return ans
journal_main['Tags']=journal_main.apply(get_tags,axis=1)
journal_main['Tags']=journal_main.apply(combine_key,axis=1)
journal_main.head()

journal_main=journal_main.drop(['keywords'],axis=1)
journal_main.head()

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
vectorizer = TfidfVectorizer()
tfidf_matrix = vectorizer.fit_transform(journal_main['Tags'])

user_input = "AI in natural language processing"
user_tfidf = vectorizer.transform([user_input])
cosine_similarities = cosine_similarity(user_tfidf, tfidf_matrix).flatten()
top_recommendations = cosine_similarities.argsort()[::-1][:3]
print(top_recommendations)
for x in top_recommendations:
  print(journal_main['Publication Title'][x])
  print(journal_main['Tags'][x])
  print()

# journal_main.to_csv('journal_tags.csv')