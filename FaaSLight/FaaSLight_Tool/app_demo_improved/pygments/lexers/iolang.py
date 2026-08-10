"""
    pygments.lexers.iolang
    ~~~~~~~~~~~~~~~~~~~~~~

    Lexers for the Io language.

    :copyright: Copyright 2006-present by the Pygments team, see AUTHORS.
    :license: BSD, see LICENSE for details.
"""

from pygments.lexer import RegexLexer
from pygments.token import Comment, Operator, Keyword, Name, String, Number, Whitespace
__all__ = ['IoLexer']


class IoLexer(RegexLexer):
    """
    For Io (a small, prototype-based programming language) source.
    """
    name = 'Io'
    url = 'http://iolanguage.com/'
    filenames = ['*.io']
    aliases = ['io']
    mimetypes = ['text/x-iosrc']
    version_added = '0.10'
    tokens = {'root': [('\\n', Whitespace), ('\\s+', Whitespace), ('//(.*?)$', Comment.Single), ('#(.*?)$', Comment.Single), ('/(\\\\\\n)?[*](.|\\n)*?[*](\\\\\\n)?/', Comment.Multiline), ('/\\+', Comment.Multiline, 'nestedcomment'), ('"(\\\\\\\\|\\\\[^\\\\]|[^"\\\\])*"', String), ('::=|:=|=|\\(|\\)|;|,|\\*|-|\\+|>|<|@|!|/|\\||\\^|\\.|%|&|\\[|\\]|\\{|\\}', Operator), ('(clone|do|doFile|doString|method|for|if|else|elseif|then)\\b', Keyword), ('(nil|false|true)\\b', Name.Constant), ('(Object|list|List|Map|args|Sequence|Coroutine|File)\\b', Name.Builtin), ('[a-zA-Z_]\\w*', Name), ('(\\d+\\.?\\d*|\\d*\\.\\d+)([eE][+-]?[0-9]+)?', Number.Float), ('\\d+', Number.Integer)], 'nestedcomment': [('[^+/]+', Comment.Multiline), ('/\\+', Comment.Multiline, '#push'), ('\\+/', Comment.Multiline, '#pop'), ('[+/]', Comment.Multiline)]}


