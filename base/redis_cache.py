import redis
from decouple import config
import pickle
REDIS_CLIENT=redis.Redis(host=config('REDIS_HOST'),port=config('REDIS_PORT'),password=config('REDIS_PASSWORD'))
import pickle

STOP_WORDS_CACHE = None

def load_stop_words():
    global STOP_WORDS_CACHE
    
    if STOP_WORDS_CACHE is None:
        try:
            with open('stop_words_cache.pkl', 'rb') as file:
                STOP_WORDS_CACHE = pickle.load(file)
                print("Stop words loaded from local cache")
        except FileNotFoundError:
            STOP_WORDS_CACHE = fetch_stop_words_from_redis()
            save_stop_words_to_local_cache()
            print("Stop words loaded from Redis and saved to local cache")
    
    return STOP_WORDS_CACHE

def fetch_stop_words_from_redis():
    # Connect to Redis and fetch the serialized stop words
    
    serialized_bytes = REDIS_CLIENT.get(f'stop_words_list_bytes.joblib')
    stop_words_list = pickle.loads(serialized_bytes)
    stop_words_list = list(stop_words_list)
    
    return stop_words_list

def save_stop_words_to_local_cache():
    global STOP_WORDS_CACHE
    
    with open('stop_words_cache.pkl', 'wb') as file:
        pickle.dump(STOP_WORDS_CACHE, file)
    
    print("Stop words saved to local cache")

# Call this function to get the stop words from the cache


def get_words_cache():
    serialized_bytes = REDIS_CLIENT.get(f'stop_words_list_bytes.joblib')
    words_list = pickle.loads(serialized_bytes)
    words_list = list(words_list)
    print("Words_setup")
    return words_list
def get_journal_tfidf_matrix():
    serialized_tfidf_matrix = REDIS_CLIENT.get('journal_tfidf_matrix.joblib')
    # Deserialize the TF-IDF vectorizer using pickle
    journal_tfidf_matrix = pickle.loads(serialized_tfidf_matrix)
    print("tfidf setup")
    return journal_tfidf_matrix
def get_journal_vectorizer():
    serialized_vectorizer = REDIS_CLIENT.get('vectorizer.joblib')
    vectorizer=pickle.loads(serialized_vectorizer)
    print("vectorizer setup")
    return vectorizer

from collections import OrderedDict

# Connect to Redis server

class MemoryLimitedCache:
    def __init__(self, max_size_bytes):
        self.max_size_bytes = max_size_bytes
        self.cache = OrderedDict()
        self.current_size_bytes = 0

    def get(self, key):
        if key in self.cache:
            # Move the accessed item to the end of the OrderedDict
            value = self.cache.pop(key)
            self.cache[key] = value
            return value
        return None

    def set(self, key, value, size_bytes):
        while self.current_size_bytes + size_bytes > self.max_size_bytes:
            # Remove the least recently used item from the cache to make room
            _, removed_value = self.cache.popitem(last=False)
            self.current_size_bytes -= removed_value[1]

        self.cache[key] = value
        self.current_size_bytes += size_bytes

def get_specific_journal(index):
    cache = MemoryLimitedCache(max_size_bytes=30 * 1024 * 1024)  # Set the maximum cache size to 30 MB
    
    # Check if the data exists in the cache
    cached_data = cache.get(index)
    if cached_data is not None:
        return cached_data

    # Retrieve the serialized TF-IDF matrix and vectorizer from Redis cache
    serialized_tfidf_matrix = REDIS_CLIENT.get(f'journal_tfidf_matrix_{index}.joblib')
    serialized_vectorizer = REDIS_CLIENT.get(f'vectorizer_{index}.joblib')

    if serialized_tfidf_matrix is None or serialized_vectorizer is None:
        return None  # Handle the case when data is not found in cache

    # Deserialize the TF-IDF matrix and vectorizer using pickle
    tfidf_matrix = pickle.loads(serialized_tfidf_matrix)
    vectorizer = pickle.loads(serialized_vectorizer)

    # Calculate the size of the data in bytes
    size_bytes = serialized_tfidf_matrix.__sizeof__() + serialized_vectorizer.__sizeof__()

    # Save the data to the cache
    cache.set(index, (tfidf_matrix, vectorizer), size_bytes)

    return tfidf_matrix, vectorizer