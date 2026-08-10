"""
    pygments.util
    ~~~~~~~~~~~~~

    Utility functions.

    :copyright: Copyright 2006-present by the Pygments team, see AUTHORS.
    :license: BSD, see LICENSE for details.
"""

import re
from io import TextIOWrapper
split_path_re = re.compile('[/\\\\ ]')
doctype_lookup_re = re.compile('\n    <!DOCTYPE\\s+(\n     [a-zA-Z_][a-zA-Z0-9]*\n     (?: \\s+      # optional in HTML5\n     [a-zA-Z_][a-zA-Z0-9]*\\s+\n     "[^"]*")?\n     )\n     [^>]*>\n', re.DOTALL | re.MULTILINE | re.VERBOSE)
tag_re = re.compile('<(.+?)(\\s.*?)?>.*?</.+?>', re.IGNORECASE | re.DOTALL | re.MULTILINE)
xml_decl_re = re.compile('\\s*<\\?xml[^>]*\\?>', re.I)


class ClassNotFound(ValueError):
    """Raised if one of the lookup functions didn't find a matching class."""
    



class OptionError(Exception):
    """
    This exception will be raised by all option processing functions if
    the type or value of the argument is not correct.
    """
    


def get_choice_opt(options, optname, allowed, default=None, normcase=False):
    """
    If the key `optname` from the dictionary is not in the sequence
    `allowed`, raise an error, otherwise return it.
    """
    import custom_funtemplate
    return custom_funtemplate.rewrite_template('pygments.util.get_choice_opt', 'get_choice_opt(options, optname, allowed, default=None, normcase=False)', {'OptionError': OptionError, 'options': options, 'optname': optname, 'allowed': allowed, 'default': default, 'normcase': normcase}, 1)

def get_bool_opt(options, optname, default=None):
    """
    Intuitively, this is `options.get(optname, default)`, but restricted to
    Boolean value. The Booleans can be represented as string, in order to accept
    Boolean value from the command line arguments. If the key `optname` is
    present in the dictionary `options` and is not associated with a Boolean,
    raise an `OptionError`. If it is absent, `default` is returned instead.

    The valid string values for ``True`` are ``1``, ``yes``, ``true`` and
    ``on``, the ones for ``False`` are ``0``, ``no``, ``false`` and ``off``
    (matched case-insensitively).
    """
    import custom_funtemplate
    return custom_funtemplate.rewrite_template('pygments.util.get_bool_opt', 'get_bool_opt(options, optname, default=None)', {'OptionError': OptionError, 'options': options, 'optname': optname, 'default': default}, 1)

def get_int_opt(options, optname, default=None):
    """As :func:`get_bool_opt`, but interpret the value as an integer."""
    import custom_funtemplate
    return custom_funtemplate.rewrite_template('pygments.util.get_int_opt', 'get_int_opt(options, optname, default=None)', {'OptionError': OptionError, 'options': options, 'optname': optname, 'default': default}, 1)

def get_list_opt(options, optname, default=None):
    """
    If the key `optname` from the dictionary `options` is a string,
    split it at whitespace and return it. If it is already a list
    or a tuple, it is returned as a list.
    """
    import custom_funtemplate
    return custom_funtemplate.rewrite_template('pygments.util.get_list_opt', 'get_list_opt(options, optname, default=None)', {'OptionError': OptionError, 'options': options, 'optname': optname, 'default': default}, 1)

def docstring_headline(obj):
    import custom_funtemplate
    return custom_funtemplate.rewrite_template('pygments.util.docstring_headline', 'docstring_headline(obj)', {'obj': obj}, 1)

def make_analysator(f):
    """Return a static text analyser function that returns float values."""
    import custom_funtemplate
    return custom_funtemplate.rewrite_template('pygments.util.make_analysator', 'make_analysator(f)', {'f': f}, 1)

def shebang_matches(text, regex):
    """Check if the given regular expression matches the last part of the
    shebang if one exists.

        >>> from pygments.util import shebang_matches
        >>> shebang_matches('#!/usr/bin/env python', r'python(2\.\d)?')
        True
        >>> shebang_matches('#!/usr/bin/python2.4', r'python(2\.\d)?')
        True
        >>> shebang_matches('#!/usr/bin/python-ruby', r'python(2\.\d)?')
        False
        >>> shebang_matches('#!/usr/bin/python/ruby', r'python(2\.\d)?')
        False
        >>> shebang_matches('#!/usr/bin/startsomethingwith python',
        ...                 r'python(2\.\d)?')
        True

    It also checks for common windows executable file extensions::

        >>> shebang_matches('#!C:\Python2.4\Python.exe', r'python(2\.\d)?')
        True

    Parameters (``'-f'`` or ``'--foo'`` are ignored so ``'perl'`` does
    the same as ``'perl -e'``)

    Note that this method automatically searches the whole string (eg:
    the regular expression is wrapped in ``'^$'``)
    """
    import custom_funtemplate
    return custom_funtemplate.rewrite_template('pygments.util.shebang_matches', 'shebang_matches(text, regex)', {'split_path_re': split_path_re, 're': re, 'text': text, 'regex': regex}, 1)

def doctype_matches(text, regex):
    """Check if the doctype matches a regular expression (if present).

    Note that this method only checks the first part of a DOCTYPE.
    eg: 'html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN"'
    """
    import custom_funtemplate
    return custom_funtemplate.rewrite_template('pygments.util.doctype_matches', 'doctype_matches(text, regex)', {'doctype_lookup_re': doctype_lookup_re, 're': re, 'text': text, 'regex': regex}, 1)

def html_doctype_matches(text):
    """Check if the file looks like it has a html doctype."""
    return doctype_matches(text, 'html')
_looks_like_xml_cache = {}

def looks_like_xml(text):
    """Check if a doctype exists or if we have some tags."""
    import custom_funtemplate
    return custom_funtemplate.rewrite_template('pygments.util.looks_like_xml', 'looks_like_xml(text)', {'xml_decl_re': xml_decl_re, '_looks_like_xml_cache': _looks_like_xml_cache, 'doctype_lookup_re': doctype_lookup_re, 'tag_re': tag_re, 'text': text}, 1)

def surrogatepair(c):
    """Given a unicode character code with length greater than 16 bits,
    return the two 16 bit surrogate pair.
    """
    return (55232 + (c >> 10), 56320 + (c & 1023))

def format_lines(var_name, seq, raw=False, indent_level=0):
    """Formats a sequence of strings for output."""
    import custom_funtemplate
    return custom_funtemplate.rewrite_template('pygments.util.format_lines', 'format_lines(var_name, seq, raw=False, indent_level=0)', {'var_name': var_name, 'seq': seq, 'raw': raw, 'indent_level': indent_level}, 1)

def duplicates_removed(it, already_seen=()):
    """
    Returns a list with duplicates removed from the iterable `it`.

    Order is preserved.
    """
    import custom_funtemplate
    return custom_funtemplate.rewrite_template('pygments.util.duplicates_removed', 'duplicates_removed(it, already_seen=())', {'it': it, 'already_seen': already_seen}, 1)


class Future:
    """Generic class to defer some work.

    Handled specially in RegexLexerMeta, to support regex string construction at
    first use.
    """
    
    def get(self):
        raise NotImplementedError


def guess_decode(text):
    """Decode *text* with guessed encoding.

    First try UTF-8; this should fail for non-UTF-8 encodings.
    Then try the preferred locale encoding.
    Fall back to latin-1, which always works.
    """
    import custom_funtemplate
    return custom_funtemplate.rewrite_template('pygments.util.guess_decode', 'guess_decode(text)', {'text': text}, 2)

def guess_decode_from_terminal(text, term):
    """Decode *text* coming from terminal *term*.

    First try the terminal encoding, if given.
    Then try UTF-8.  Then try the preferred locale encoding.
    Fall back to latin-1, which always works.
    """
    import custom_funtemplate
    return custom_funtemplate.rewrite_template('pygments.util.guess_decode_from_terminal', 'guess_decode_from_terminal(text, term)', {'guess_decode': guess_decode, 'text': text, 'term': term}, 2)

def terminal_encoding(term):
    """Return our best guess of encoding for the given *term*."""
    import custom_funtemplate
    return custom_funtemplate.rewrite_template('pygments.util.terminal_encoding', 'terminal_encoding(term)', {'term': term}, 1)


class UnclosingTextIOWrapper(TextIOWrapper):
    
    def close(self):
        self.flush()


