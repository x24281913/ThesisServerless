import time
import os
import sys
import hashlib
import gc
import shutil
import platform
import logging
import warnings
import pickle
from pathlib import Path
from typing import Dict, Any
LOG = logging.getLogger(__name__)
_CACHED_FILE_MINIMUM_SURVIVAL = 60 * 10
'\nCached files should survive at least a few minutes.\n'
_CACHED_FILE_MAXIMUM_SURVIVAL = 60 * 60 * 24 * 30
'\nMaximum time for a cached file to survive if it is not\naccessed within.\n'
_CACHED_SIZE_TRIGGER = 600
"\nThis setting limits the amount of cached files. It's basically a way to start\ngarbage collection.\n\nThe reasoning for this limit being as big as it is, is the following:\n\nNumpy, Pandas, Matplotlib and Tensorflow together use about 500 files. This\nmakes Jedi use ~500mb of memory. Since we might want a bit more than those few\nlibraries, we just increase it a bit.\n"
_PICKLE_VERSION = 33
'\nVersion number (integer) for file system cache.\n\nIncrement this number when there are any incompatible changes in\nthe parser tree classes.  For example, the following changes\nare regarded as incompatible.\n\n- A class name is changed.\n- A class is moved to another module.\n- A __slot__ of a class is changed.\n'
_VERSION_TAG = '%s-%s%s-%s' % (platform.python_implementation(), sys.version_info[0], sys.version_info[1], _PICKLE_VERSION)
"\nShort name for distinguish Python implementations and versions.\n\nIt's a bit similar to `sys.implementation.cache_tag`.\nSee: http://docs.python.org/3/library/sys.html#sys.implementation\n"

def _get_default_cache_path():
    import custom_funtemplate
    return custom_funtemplate.rewrite_template('parso.cache._get_default_cache_path', '_get_default_cache_path()', {'platform': platform, 'Path': Path, 'os': os}, 1)
_default_cache_path = _get_default_cache_path()
'\nThe path where the cache is stored.\n\nOn Linux, this defaults to ``~/.cache/parso/``, on OS X to\n``~/Library/Caches/Parso/`` and on Windows to ``%LOCALAPPDATA%\\Parso\\Parso\\``.\nOn Linux, if environment variable ``$XDG_CACHE_HOME`` is set,\n``$XDG_CACHE_HOME/parso`` is used instead of the default one.\n'
_CACHE_CLEAR_THRESHOLD = 60 * 60 * 24

def _get_cache_clear_lock_path(cache_path=None):
    """
    The path where the cache lock is stored.

    Cache lock will prevent continous cache clearing and only allow garbage
    collection once a day (can be configured in _CACHE_CLEAR_THRESHOLD).
    """
    cache_path = (cache_path or _default_cache_path)
    return cache_path.joinpath('PARSO-CACHE-LOCK')
parser_cache: Dict[(str, Any)] = {}


class _NodeCacheItem:
    
    def __init__(self, node, lines, change_time=None):
        self.node = node
        self.lines = lines
        if change_time is None:
            change_time = time.time()
        self.change_time = change_time
        self.last_used = change_time


def load_module(hashed_grammar, file_io, cache_path=None):
    """
    Returns a module or None, if it fails.
    """
    import custom_funtemplate
    return custom_funtemplate.rewrite_template('parso.cache.load_module', 'load_module(hashed_grammar, file_io, cache_path=None)', {'parser_cache': parser_cache, 'time': time, '_load_from_file_system': _load_from_file_system, 'hashed_grammar': hashed_grammar, 'file_io': file_io, 'cache_path': cache_path}, 1)

def _load_from_file_system(hashed_grammar, path, p_time, cache_path=None):
    import custom_funtemplate
    return custom_funtemplate.rewrite_template('parso.cache._load_from_file_system', '_load_from_file_system(hashed_grammar, path, p_time, cache_path=None)', {'_get_hashed_path': _get_hashed_path, 'os': os, 'gc': gc, 'pickle': pickle, '_set_cache_item': _set_cache_item, 'LOG': LOG, 'hashed_grammar': hashed_grammar, 'path': path, 'p_time': p_time, 'cache_path': cache_path}, 1)

def _set_cache_item(hashed_grammar, path, module_cache_item):
    import custom_funtemplate
    custom_funtemplate.rewrite_template('parso.cache._set_cache_item', '_set_cache_item(hashed_grammar, path, module_cache_item)', {'parser_cache': parser_cache, '_CACHED_SIZE_TRIGGER': _CACHED_SIZE_TRIGGER, 'time': time, '_CACHED_FILE_MINIMUM_SURVIVAL': _CACHED_FILE_MINIMUM_SURVIVAL, 'hashed_grammar': hashed_grammar, 'path': path, 'module_cache_item': module_cache_item}, 0)

def try_to_save_module(hashed_grammar, file_io, module, lines, pickling=True, cache_path=None):
    import custom_funtemplate
    custom_funtemplate.rewrite_template('parso.cache.try_to_save_module', 'try_to_save_module(hashed_grammar, file_io, module, lines, pickling=True, cache_path=None)', {'_NodeCacheItem': _NodeCacheItem, '_set_cache_item': _set_cache_item, '_save_to_file_system': _save_to_file_system, 'warnings': warnings, '_remove_cache_and_update_lock': _remove_cache_and_update_lock, 'hashed_grammar': hashed_grammar, 'file_io': file_io, 'module': module, 'lines': lines, 'pickling': pickling, 'cache_path': cache_path}, 0)

def _save_to_file_system(hashed_grammar, path, item, cache_path=None):
    with open(_get_hashed_path(hashed_grammar, path, cache_path=cache_path), 'wb') as f:
        pickle.dump(item, f, pickle.HIGHEST_PROTOCOL)

def clear_cache(cache_path=None):
    import custom_funtemplate
    custom_funtemplate.rewrite_template('parso.cache.clear_cache', 'clear_cache(cache_path=None)', {'_default_cache_path': _default_cache_path, 'shutil': shutil, 'parser_cache': parser_cache, 'cache_path': cache_path}, 0)

def clear_inactive_cache(cache_path=None, inactivity_threshold=_CACHED_FILE_MAXIMUM_SURVIVAL):
    import custom_funtemplate
    return custom_funtemplate.rewrite_template('parso.cache.clear_inactive_cache', 'clear_inactive_cache(cache_path=None, inactivity_threshold=_CACHED_FILE_MAXIMUM_SURVIVAL)', {'_default_cache_path': _default_cache_path, 'os': os, 'time': time, 'cache_path': cache_path, 'inactivity_threshold': inactivity_threshold, '_CACHED_FILE_MAXIMUM_SURVIVAL': _CACHED_FILE_MAXIMUM_SURVIVAL}, 1)

def _touch(path):
    import custom_funtemplate
    return custom_funtemplate.rewrite_template('parso.cache._touch', '_touch(path)', {'os': os, 'IOError': IOError, 'path': path}, 1)

def _remove_cache_and_update_lock(cache_path=None):
    import custom_funtemplate
    return custom_funtemplate.rewrite_template('parso.cache._remove_cache_and_update_lock', '_remove_cache_and_update_lock(cache_path=None)', {'_get_cache_clear_lock_path': _get_cache_clear_lock_path, 'os': os, '_CACHE_CLEAR_THRESHOLD': _CACHE_CLEAR_THRESHOLD, 'time': time, '_touch': _touch, 'clear_inactive_cache': clear_inactive_cache, 'cache_path': cache_path}, 1)

def _get_hashed_path(hashed_grammar, path, cache_path=None):
    import custom_funtemplate
    return custom_funtemplate.rewrite_template('parso.cache._get_hashed_path', '_get_hashed_path(hashed_grammar, path, cache_path=None)', {'_get_cache_directory_path': _get_cache_directory_path, 'hashlib': hashlib, 'os': os, 'hashed_grammar': hashed_grammar, 'path': path, 'cache_path': cache_path}, 1)

def _get_cache_directory_path(cache_path=None):
    import custom_funtemplate
    return custom_funtemplate.rewrite_template('parso.cache._get_cache_directory_path', '_get_cache_directory_path(cache_path=None)', {'_default_cache_path': _default_cache_path, '_VERSION_TAG': _VERSION_TAG, 'os': os, 'cache_path': cache_path}, 1)

