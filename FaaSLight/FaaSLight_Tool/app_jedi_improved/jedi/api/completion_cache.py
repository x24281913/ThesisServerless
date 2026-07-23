from typing import Dict, Tuple, Callable
CacheValues = Tuple[(str, str, str)]
CacheValuesCallback = Callable[([], CacheValues)]
_cache: Dict[(str, Dict[(str, CacheValues)])] = {}

def save_entry(module_name: str, name: str, cache: CacheValues) -> None:
    import custom_funtemplate
    custom_funtemplate.rewrite_template('jedi.api.completion_cache.save_entry', 'save_entry(module_name, name, cache)', {'_cache': _cache, 'module_name': module_name, 'name': name, 'cache': cache}, 0)

def _create_get_from_cache(number: int) -> Callable[([str, str, CacheValuesCallback], str)]:
    import custom_funtemplate
    return custom_funtemplate.rewrite_template('jedi.api.completion_cache._create_get_from_cache', '_create_get_from_cache(number)', {'CacheValuesCallback': CacheValuesCallback, '_cache': _cache, 'save_entry': save_entry, 'number': number, 'Callable': Callable, 'str': str}, 1)
get_type = _create_get_from_cache(0)
get_docstring_signature = _create_get_from_cache(1)
get_docstring = _create_get_from_cache(2)

