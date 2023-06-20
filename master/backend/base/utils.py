import re
import nltk
from nltk.corpus import stopwords

nltk.download('stopwords')
stop_words = set(stopwords.words('english'))

def preprocessing(text):
    clean_text=''
    words = re.findall(r'\b\w+\b', text.lower())
    words = text.lower().split()
    for word in words:
        if( re.match(r'^[a-zA-Z]+$', word) and  word not in stop_words and len(word) >1 and word[1] != '.'):
            clean_text=clean_text+' '+word
    return clean_text
