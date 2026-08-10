"""
    pygments.regexopt
    ~~~~~~~~~~~~~~~~~

    An algorithm that generates optimized regexes for matching long lists of
    literal strings.

    :copyright: Copyright 2006-present by the Pygments team, see AUTHORS.
    :license: BSD, see LICENSE for details.
"""

import re
from re import escape
from itertools import groupby
from operator import itemgetter
CS_ESCAPE = re.compile('[\\[\\^\\\\\\-\\]]')
FIRST_ELEMENT = itemgetter(0)

def commonprefix(m):
    """Given an iterable of strings, returns the longest common leading substring"""
    import custom_funtemplate
    return custom_funtemplate.rewrite_template('pygments.regexopt.commonprefix', 'commonprefix(m)', {'m': m}, 1)

def make_charset(letters):
    return '[' + CS_ESCAPE.sub(lambda m: '\\' + m.group(), ''.join(letters)) + ']'

def regex_opt_inner(strings, open_paren):
    """Return a regex that matches any string in the sorted list of strings."""
    import custom_funtemplate
    return custom_funtemplate.rewrite_template('pygments.regexopt.regex_opt_inner', 'regex_opt_inner(strings, open_paren)', {'escape': escape, 'regex_opt_inner': regex_opt_inner, 'make_charset': make_charset, 'commonprefix': commonprefix, 'groupby': groupby, 'strings': strings, 'open_paren': open_paren}, 1)

def regex_opt(strings, prefix='', suffix=''):
    """Return a compiled regex that matches any string in the given list.

    The strings to match must be literal strings, not regexes.  They will be
    regex-escaped.

    *prefix* and *suffix* are pre- and appended to the final regex.
    """
    strings = sorted(strings)
    return prefix + regex_opt_inner(strings, '(') + suffix

