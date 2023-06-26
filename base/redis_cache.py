import redis
from decouple import config
import pickle
REDIS_CLIENT=redis.Redis(host=config('REDIS_HOST'),port=config('REDIS_PORT'),password=config('REDIS_PASSWORD'))
import pickle

STOP_WORDS_CACHE = None

def save_to_local_cache(filename, data):
    with open(filename, 'wb') as file:
        pickle.dump(data, file)
    print(f"Data saved to local cache: {filename}")

def load_from_local_cache(filename):
    try:
        with open(filename, 'rb') as file:
            data = pickle.load(file)
            print(f"Data loaded from local cache: {filename}")
            return data
    except FileNotFoundError:
        print(f"Data not found in local cache: {filename}")
        return None

def load_stop_words():
    global STOP_WORDS_CACHE
    if STOP_WORDS_CACHE is None:
        stop_words = load_from_local_cache('stop_words_cache.pkl')
        if stop_words is None:
            serialized_bytes = REDIS_CLIENT.get(f'stop_words_list_bytes.joblib')
            if serialized_bytes is not None:
                stop_words = pickle.loads(serialized_bytes)
                stop_words = list(stop_words)
                save_to_local_cache('stop_words_cache.pkl', stop_words)
                print("Stop words saved to local cache")
        STOP_WORDS_CACHE = stop_words
    return STOP_WORDS_CACHE


WORDS_CACHE = None

def load_words_cache():
    global WORDS_CACHE
    if WORDS_CACHE is None:
        words_list = load_from_local_cache('words_cache.pkl')
        if words_list is None:
            serialized_bytes = REDIS_CLIENT.get(f'stop_words_list_bytes.joblib')
            if serialized_bytes is not None:
                words_list = pickle.loads(serialized_bytes)
                words_list = list(words_list)
                save_to_local_cache('words_cache.pkl', words_list)
                print("Words cache saved to local cache")
        WORDS_CACHE = words_list
    return WORDS_CACHE

JOURNAL_TFIDF_MATRIX = None

def load_journal_tfidf_matrix():
    global JOURNAL_TFIDF_MATRIX
    if JOURNAL_TFIDF_MATRIX is None:
        matrix = load_from_local_cache('journal_tfidf_matrix.pkl')
        if matrix is None:
            serialized_matrix = REDIS_CLIENT.get('journal_tfidf_matrix.joblib')
            if serialized_matrix is not None:
                matrix = pickle.loads(serialized_matrix)
                save_to_local_cache('journal_tfidf_matrix.pkl', matrix)
                print("Journal TF-IDF matrix saved to local cache")
        JOURNAL_TFIDF_MATRIX = matrix
    return JOURNAL_TFIDF_MATRIX

JOURNAL_VECTORIZER = None

def load_journal_vectorizer():
    global JOURNAL_VECTORIZER
    if JOURNAL_VECTORIZER is None:
        vectorizer = load_from_local_cache('journal_vectorizer.pkl')
        if vectorizer is None:
            serialized_vectorizer = REDIS_CLIENT.get('vectorizer.joblib')
            if serialized_vectorizer is not None:
                vectorizer = pickle.loads(serialized_vectorizer)
                save_to_local_cache('journal_vectorizer.pkl', vectorizer)
                print("Journal vectorizer saved to local cache")
        JOURNAL_VECTORIZER = vectorizer
    return JOURNAL_VECTORIZER

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