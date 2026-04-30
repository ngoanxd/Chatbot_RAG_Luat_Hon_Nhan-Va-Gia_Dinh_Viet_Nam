import json
import os
from config import CACHE_PATH

class QueryCache:
    def __init__(self):
        self.cache = {}
        if os.path.exists(CACHE_PATH):
            with open(CACHE_PATH, "r", encoding="utf-8") as f:
                self.cache = json.load(f)

    def get(self, query):
        return self.cache.get(query)

    def set(self, query, value):
        self.cache[query] = value
        with open(CACHE_PATH, "w", encoding="utf-8") as f:
            json.dump(self.cache, f, ensure_ascii=False, indent=2)