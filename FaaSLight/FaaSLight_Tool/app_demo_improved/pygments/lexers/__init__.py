"""
    pygments.lexers
    ~~~~~~~~~~~~~~~

    Pygments lexers.

    :copyright: Copyright 2006-present by the Pygments team, see AUTHORS.
    :license: BSD, see LICENSE for details.
"""

import re
import sys
import types
import fnmatch
from os.path import basename
from pygments.lexers._mapping import LEXERS
from pygments.modeline import get_filetype_from_buffer
from pygments.plugin import find_plugin_lexers
from pygments.util import ClassNotFound, guess_decode
COMPAT = {'Python3Lexer': 'PythonLexer', 'Python3TracebackLexer': 'PythonTracebackLexer', 'LeanLexer': 'Lean3Lexer'}
__all__ = ['get_lexer_by_name', 'get_lexer_for_filename', 'find_lexer_class', 'guess_lexer', 'load_lexer_from_file'] + list(LEXERS) + list(COMPAT)
_lexer_cache = {}
_pattern_cache = {}

def _fn_matches(fn, glob):
    """Return whether the supplied file name fn matches pattern filename."""
    import custom_funtemplate
    return custom_funtemplate.rewrite_template('pygments.lexers.__init__._fn_matches', '_fn_matches(fn, glob)', {'_pattern_cache': _pattern_cache, 're': re, 'fnmatch': fnmatch, 'fn': fn, 'glob': glob}, 1)

def _load_lexers(module_name):
    """Load a lexer (and all others in the module too)."""
    import custom_funtemplate
    custom_funtemplate.rewrite_template('pygments.lexers.__init__._load_lexers', '_load_lexers(module_name)', {'_lexer_cache': _lexer_cache, 'module_name': module_name}, 0)

def get_all_lexers(plugins=True):
    """Return a generator of tuples in the form ``(name, aliases,
    filenames, mimetypes)`` of all know lexers.

    If *plugins* is true (the default), plugin lexers supplied by entrypoints
    are also returned.  Otherwise, only builtin ones are considered.
    """
    import custom_funtemplate
    custom_funtemplate.rewrite_template('pygments.lexers.__init__.get_all_lexers', 'get_all_lexers(plugins=True)', {'LEXERS': LEXERS, 'find_plugin_lexers': find_plugin_lexers, 'plugins': plugins}, 0)

def find_lexer_class(name):
    """
    Return the `Lexer` subclass that with the *name* attribute as given by
    the *name* argument.
    """
    import custom_funtemplate
    return custom_funtemplate.rewrite_template('pygments.lexers.__init__.find_lexer_class', 'find_lexer_class(name)', {'_lexer_cache': _lexer_cache, 'LEXERS': LEXERS, '_load_lexers': _load_lexers, 'find_plugin_lexers': find_plugin_lexers, 'name': name}, 1)

def find_lexer_class_by_name(_alias):
    """
    Return the `Lexer` subclass that has `alias` in its aliases list, without
    instantiating it.

    Like `get_lexer_by_name`, but does not instantiate the class.

    Will raise :exc:`pygments.util.ClassNotFound` if no lexer with that alias is
    found.

    .. versionadded:: 2.2
    """
    import custom_funtemplate
    return custom_funtemplate.rewrite_template('pygments.lexers.__init__.find_lexer_class_by_name', 'find_lexer_class_by_name(_alias)', {'ClassNotFound': ClassNotFound, 'LEXERS': LEXERS, '_lexer_cache': _lexer_cache, '_load_lexers': _load_lexers, 'find_plugin_lexers': find_plugin_lexers, '_alias': _alias}, 1)

def get_lexer_by_name(_alias, **options):
    """
    Return an instance of a `Lexer` subclass that has `alias` in its
    aliases list. The lexer is given the `options` at its
    instantiation.

    Will raise :exc:`pygments.util.ClassNotFound` if no lexer with that alias is
    found.
    """
    import custom_funtemplate
    return custom_funtemplate.rewrite_template('pygments.lexers.__init__.get_lexer_by_name', 'get_lexer_by_name(_alias, **options)', {'ClassNotFound': ClassNotFound, 'LEXERS': LEXERS, '_lexer_cache': _lexer_cache, '_load_lexers': _load_lexers, 'find_plugin_lexers': find_plugin_lexers, '_alias': _alias, 'options': options}, 1)

def load_lexer_from_file(filename, lexername='CustomLexer', **options):
    """Load a lexer from a file.

    This method expects a file located relative to the current working
    directory, which contains a Lexer class. By default, it expects the
    Lexer to be name CustomLexer; you can specify your own class name
    as the second argument to this function.

    Users should be very careful with the input, because this method
    is equivalent to running eval on the input file.

    Raises ClassNotFound if there are any problems importing the Lexer.

    .. versionadded:: 2.2
    """
    import custom_funtemplate
    return custom_funtemplate.rewrite_template('pygments.lexers.__init__.load_lexer_from_file', "load_lexer_from_file(filename, lexername='CustomLexer', **options)", {'ClassNotFound': ClassNotFound, 'filename': filename, 'lexername': lexername, 'options': options}, 1)

def find_lexer_class_for_filename(_fn, code=None):
    """Get a lexer for a filename.

    If multiple lexers match the filename pattern, use ``analyse_text()`` to
    figure out which one is more appropriate.

    Returns None if not found.
    """
    import custom_funtemplate
    return custom_funtemplate.rewrite_template('pygments.lexers.__init__.find_lexer_class_for_filename', 'find_lexer_class_for_filename(_fn, code=None)', {'basename': basename, 'LEXERS': LEXERS, '_fn_matches': _fn_matches, '_lexer_cache': _lexer_cache, '_load_lexers': _load_lexers, 'find_plugin_lexers': find_plugin_lexers, 'guess_decode': guess_decode, '_fn': _fn, 'code': code}, 2)

def get_lexer_for_filename(_fn, code=None, **options):
    """Get a lexer for a filename.

    Return a `Lexer` subclass instance that has a filename pattern
    matching `fn`. The lexer is given the `options` at its
    instantiation.

    Raise :exc:`pygments.util.ClassNotFound` if no lexer for that filename
    is found.

    If multiple lexers match the filename pattern, use their ``analyse_text()``
    methods to figure out which one is more appropriate.
    """
    import custom_funtemplate
    return custom_funtemplate.rewrite_template('pygments.lexers.__init__.get_lexer_for_filename', 'get_lexer_for_filename(_fn, code=None, **options)', {'find_lexer_class_for_filename': find_lexer_class_for_filename, 'ClassNotFound': ClassNotFound, '_fn': _fn, 'code': code, 'options': options}, 1)

def get_lexer_for_mimetype(_mime, **options):
    """
    Return a `Lexer` subclass instance that has `mime` in its mimetype
    list. The lexer is given the `options` at its instantiation.

    Will raise :exc:`pygments.util.ClassNotFound` if not lexer for that mimetype
    is found.
    """
    import custom_funtemplate
    return custom_funtemplate.rewrite_template('pygments.lexers.__init__.get_lexer_for_mimetype', 'get_lexer_for_mimetype(_mime, **options)', {'LEXERS': LEXERS, '_lexer_cache': _lexer_cache, '_load_lexers': _load_lexers, 'find_plugin_lexers': find_plugin_lexers, 'ClassNotFound': ClassNotFound, '_mime': _mime, 'options': options}, 1)

def _iter_lexerclasses(plugins=True):
    """Return an iterator over all lexer classes."""
    import custom_funtemplate
    custom_funtemplate.rewrite_template('pygments.lexers.__init__._iter_lexerclasses', '_iter_lexerclasses(plugins=True)', {'LEXERS': LEXERS, '_lexer_cache': _lexer_cache, '_load_lexers': _load_lexers, 'find_plugin_lexers': find_plugin_lexers, 'plugins': plugins}, 0)

def guess_lexer_for_filename(_fn, _text, **options):
    """
    As :func:`guess_lexer()`, but only lexers which have a pattern in `filenames`
    or `alias_filenames` that matches `filename` are taken into consideration.

    :exc:`pygments.util.ClassNotFound` is raised if no lexer thinks it can
    handle the content.
    """
    import custom_funtemplate
    return custom_funtemplate.rewrite_template('pygments.lexers.__init__.guess_lexer_for_filename', 'guess_lexer_for_filename(_fn, _text, **options)', {'basename': basename, '_iter_lexerclasses': _iter_lexerclasses, '_fn_matches': _fn_matches, 'ClassNotFound': ClassNotFound, '_fn': _fn, '_text': _text, 'options': options}, 1)

def guess_lexer(_text, **options):
    """
    Return a `Lexer` subclass instance that's guessed from the text in
    `text`. For that, the :meth:`.analyse_text()` method of every known lexer
    class is called with the text as argument, and the lexer which returned the
    highest value will be instantiated and returned.

    :exc:`pygments.util.ClassNotFound` is raised if no lexer thinks it can
    handle the content.
    """
    import custom_funtemplate
    return custom_funtemplate.rewrite_template('pygments.lexers.__init__.guess_lexer', 'guess_lexer(_text, **options)', {'guess_decode': guess_decode, 'get_filetype_from_buffer': get_filetype_from_buffer, 'get_lexer_by_name': get_lexer_by_name, 'ClassNotFound': ClassNotFound, '_iter_lexerclasses': _iter_lexerclasses, '_text': _text, 'options': options}, 1)


class _automodule(types.ModuleType):
    """Automatically import lexers."""
    
    def __getattr__(self, name):
        info = LEXERS.get(name)
        if info:
            _load_lexers(info[0])
            cls = _lexer_cache[info[1]]
            setattr(self, name, cls)
            return cls
        if name in COMPAT:
            return getattr(self, COMPAT[name])
        raise AttributeError(name)

oldmod = sys.modules[__name__]
newmod = _automodule(__name__)
newmod.__dict__.update(oldmod.__dict__)
sys.modules[__name__] = newmod
del newmod.newmod, newmod.oldmod, newmod.sys, newmod.types

