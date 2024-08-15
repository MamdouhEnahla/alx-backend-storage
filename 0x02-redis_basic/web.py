#!/usr/bin/env python3
"""
Web Caching and Tracking
"""
import requests
import redis
from functools import wraps

store = redis.Redis()

def count_url_access(method):
    """counts how many times a URL is accessed."""
    @wraps(method)
    def wrapper(url):
        cached_key = f"cached:{url}"
        cached_data = store.get(cached_key)
        if cached_data:
            return cached_data.decode('utf-8')

        count_key = f"count:{url}"
        html = method(url)

        store.incr(count_key)
        store.set(cached_key, html)
        store.expire(cached_key, 10)
        return html
    return wrapper

@count_url_access
def get_page(url: str) -> str:
    """Retrieves and returns the HTML content of a URL."""
    response = requests.get(url)
    return response.text
