"""
Michael Harrington

This file trades shortens times by trading space using memoization
"""

def Memoize(func):
    cache = {}

    def wrapper(*args):
        key = tuple(args)
        if key not in cache:
            cache[key] = func(*args)
        
        return cache[key]

    return wrapper

