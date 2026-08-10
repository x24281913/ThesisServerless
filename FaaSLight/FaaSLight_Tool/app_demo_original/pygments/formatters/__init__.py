"""
    pygments.formatters
    ~~~~~~~~~~~~~~~~~~~

    Pygments formatters.

    :copyright: Copyright 2006-present by the Pygments team, see AUTHORS.
    :license: BSD, see LICENSE for details.
"""

import re
import sys
import types
import fnmatch
from os.path import basename
from pygments.formatters._mapping import FORMATTERS
from pygments.plugin import find_plugin_formatters
from pygments.util import ClassNotFound
__all__ = ['get_formatter_by_name', 'get_formatter_for_filename', 'get_all_formatters', 'load_formatter_from_file'] + list(FORMATTERS)
_formatter_cache = {}
_pattern_cache = {}

def _fn_matches(fn, glob):
    """Return whether the supplied file name fn matches pattern filename."""
    import custom_funtemplate
    return custom_funtemplate.rewrite_template('pygments.formatters.__init__._fn_matches', '_fn_matches(fn, glob)', {'_pattern_cache': _pattern_cache, 're': re, 'fnmatch': fnmatch, 'fn': fn, 'glob': glob}, 1)

def _load_formatters(module_name):
    """Load a formatter (and all others in the module too)."""
    import custom_funtemplate
    custom_funtemplate.rewrite_template('pygments.formatters.__init__._load_formatters', '_load_formatters(module_name)', {'_formatter_cache': _formatter_cache, 'module_name': module_name}, 0)

def get_all_formatters():
    """Return a generator for all formatter classes."""
    import custom_funtemplate
    custom_funtemplate.rewrite_template('pygments.formatters.__init__.get_all_formatters', 'get_all_formatters()', {'FORMATTERS': FORMATTERS, '_formatter_cache': _formatter_cache, '_load_formatters': _load_formatters, 'find_plugin_formatters': find_plugin_formatters}, 0)

def find_formatter_class(alias):
    """Lookup a formatter by alias.

    Returns None if not found.
    """
    import custom_funtemplate
    return custom_funtemplate.rewrite_template('pygments.formatters.__init__.find_formatter_class', 'find_formatter_class(alias)', {'FORMATTERS': FORMATTERS, '_formatter_cache': _formatter_cache, '_load_formatters': _load_formatters, 'find_plugin_formatters': find_plugin_formatters, 'alias': alias}, 1)

def get_formatter_by_name(_alias, **options):
    """
    Return an instance of a :class:`.Formatter` subclass that has `alias` in its
    aliases list. The formatter is given the `options` at its instantiation.

    Will raise :exc:`pygments.util.ClassNotFound` if no formatter with that
    alias is found.
    """
    import custom_funtemplate
    return custom_funtemplate.rewrite_template('pygments.formatters.__init__.get_formatter_by_name', 'get_formatter_by_name(_alias, **options)', {'find_formatter_class': find_formatter_class, 'ClassNotFound': ClassNotFound, '_alias': _alias, 'options': options}, 1)

def load_formatter_from_file(filename, formattername='CustomFormatter', **options):
    """
    Return a `Formatter` subclass instance loaded from the provided file, relative
    to the current directory.

    The file is expected to contain a Formatter class named ``formattername``
    (by default, CustomFormatter). Users should be very careful with the input, because
    this method is equivalent to running ``eval()`` on the input file. The formatter is
    given the `options` at its instantiation.

    :exc:`pygments.util.ClassNotFound` is raised if there are any errors loading
    the formatter.

    .. versionadded:: 2.2
    """
    import custom_funtemplate
    return custom_funtemplate.rewrite_template('pygments.formatters.__init__.load_formatter_from_file', "load_formatter_from_file(filename, formattername='CustomFormatter', **options)", {'ClassNotFound': ClassNotFound, 'filename': filename, 'formattername': formattername, 'options': options}, 1)

def get_formatter_for_filename(fn, **options):
    """
    Return a :class:`.Formatter` subclass instance that has a filename pattern
    matching `fn`. The formatter is given the `options` at its instantiation.

    Will raise :exc:`pygments.util.ClassNotFound` if no formatter for that filename
    is found.
    """
    import custom_funtemplate
    return custom_funtemplate.rewrite_template('pygments.formatters.__init__.get_formatter_for_filename', 'get_formatter_for_filename(fn, **options)', {'basename': basename, 'FORMATTERS': FORMATTERS, '_fn_matches': _fn_matches, '_formatter_cache': _formatter_cache, '_load_formatters': _load_formatters, 'find_plugin_formatters': find_plugin_formatters, 'ClassNotFound': ClassNotFound, 'fn': fn, 'options': options}, 1)


class _automodule(types.ModuleType):
    """Automatically import formatters."""
    
    def __getattr__(self, name):
        info = FORMATTERS.get(name)
        if info:
            _load_formatters(info[0])
            cls = _formatter_cache[info[1]]
            setattr(self, name, cls)
            return cls
        raise AttributeError(name)

oldmod = sys.modules[__name__]
newmod = _automodule(__name__)
newmod.__dict__.update(oldmod.__dict__)
sys.modules[__name__] = newmod
del newmod.newmod, newmod.oldmod, newmod.sys, newmod.types

