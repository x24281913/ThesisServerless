"""
    pygments.lexers.rita
    ~~~~~~~~~~~~~~~~~~~~

    Lexers for RITA language

    :copyright: Copyright 2006-present by the Pygments team, see AUTHORS.
    :license: BSD, see LICENSE for details.
"""

from pygments.lexer import RegexLexer
from pygments.token import Comment, Operator, Keyword, Name, Literal, Punctuation, Whitespace
__all__ = ['RitaLexer']


class RitaLexer(RegexLexer):
    """
    Lexer for RITA.
    """
    name = 'Rita'
    url = 'https://github.com/zaibacu/rita-dsl'
    filenames = ['*.rita']
    aliases = ['rita']
    mimetypes = ['text/rita']
    version_added = '2.11'
    tokens = {'root': [('\\n', Whitespace), ('\\s+', Whitespace), ('#(.*?)\\n', Comment.Single), ('@(.*?)\\n', Operator), ('"(\\w|\\d|\\s|(\\\\")|[\\\'_\\-./,\\?\\!])+?"', Literal), ('\\\'(\\w|\\d|\\s|(\\\\\\\')|["_\\-./,\\?\\!])+?\\\'', Literal), ('([A-Z_]+)', Keyword), ('([a-z0-9_]+)', Name), ('((->)|[!?+*|=])', Operator), ('[\\(\\),\\{\\}]', Punctuation)]}


