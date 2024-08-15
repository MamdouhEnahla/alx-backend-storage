#!/usr/bin/env python3
"""
Web Caching and Tracking
"""
import requests
import redis
from functools import wraps
from typing import Callable

store = redis.Redis()


def cache(ttl: int = 10) -> Callable:
    """
    Cache decorator with configurable TTL.
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            cached_key = f"cached:{args[0]}"
            cached_data = store.get(cached_key)
            if cached_data:
                return cached_data.decode("utf-8")

            result = func(*args, **kwargs)
            store.set(cached_key, result, ex=ttl)
            return result
        return wrapper
    return decorator


def count_access(func: Callable) -> Callable:
    """
    Decorator to count the number of accesses.
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        count_key = f"count:{args[0]}"
        store.incr(count_key)
        return func(*args, **kwargs)
    return wrapper


@cache()
@count_access
def get_page(url: str) -> str:
    """
    Fetches HTML content of a URL.
    """
    res = requests.get(url)
    return res.text
