"""
This caching is very important for speed and memory optimizations. There's
nothing really spectacular, just some decorators. The following cache types are
available:

- ``time_cache`` can be used to cache something for just a limited time span,
  which can be useful if there's user interaction and the user cannot react
  faster than a certain time.

This module is one of the reasons why |jedi| is not thread-safe. As you can see
there are global variables, which are holding the cache information. Some of
these variables are being cleaned after every API usage.
"""

import time
from functools import wraps
from typing import Any, Dict, Tuple
from jedi import settings
from parso.cache import parser_cache
_time_caches: Dict[(str, Dict[(Any, Tuple[(float, Any)])])] = {}

def clear_time_caches(delete_all: bool = False) -> None:
    """ Jedi caches many things, that should be completed after each completion
    finishes.

    :param delete_all: Deletes also the cache that is normally not deleted,
        like parser cache, which is important for faster parsing.
    """
    import custom_funtemplate
    custom_funtemplate.rewrite_template('jedi.cache.clear_time_caches', 'clear_time_caches(delete_all=False)', {'_time_caches': _time_caches, 'parser_cache': parser_cache, 'time': time, 'delete_all': delete_all}, 0)

def signature_time_cache(time_add_setting):
    """
    This decorator works as follows: Call it with a setting and after that
    use the function with a callable that returns the key.
    But: This function is only called if the key is not available. After a
    certain amount of time (`time_add_setting`) the cache is invalid.

    If the given key is None, the function will not be cached.
    """
    
    def _temp(key_func):
        dct = {}
        _time_caches[time_add_setting] = dct
        
        def wrapper(*args, **kwargs):
            import custom_funtemplate
            return custom_funtemplate.rewrite_template('jedi.cache.signature_time_cache._temp.wrapper', 'wrapper(*args, **kwargs)', {'key_func': key_func, 'dct': dct, 'time': time, 'settings': settings, 'time_add_setting': time_add_setting, 'args': args, 'kwargs': kwargs}, 1)
        return wrapper
    return _temp

def time_cache(seconds):
    
    def decorator(func):
        cache = {}
        
        @wraps(func)
        def wrapper(*args, **kwargs):
            import custom_funtemplate
            return custom_funtemplate.rewrite_template('jedi.cache.time_cache.decorator.wrapper', 'wrapper(*args, **kwargs)', {'cache': cache, 'time': time, 'seconds': seconds, 'wraps': wraps, 'func': func, 'args': args, 'kwargs': kwargs}, 1)
        wrapper.clear_cache = lambda: cache.clear()
        return wrapper
    return decorator

def memoize_method(method):
    """A normal memoize function."""
    
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        import custom_funtemplate
        return custom_funtemplate.rewrite_template('jedi.cache.memoize_method.wrapper', 'wrapper(self, *args, **kwargs)', {'wraps': wraps, 'method': method, 'self': self, 'args': args, 'kwargs': kwargs}, 1)
    return wrapper

