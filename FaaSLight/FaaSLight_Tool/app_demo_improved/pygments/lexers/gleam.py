"""
    pygments.lexers.gleam
    ~~~~~~~~~~~~~~~~~~~~~

    Lexer for the Gleam programming language.

    :copyright: Copyright 2006-present by the Pygments team, see AUTHORS.
    :license: BSD, see LICENSE for details.
"""

from pygments.lexer import RegexLexer, words, bygroups
from pygments.token import Comment, Operator, Keyword, Name, String, Number, Punctuation, Whitespace
__all__ = ['GleamLexer']


class GleamLexer(RegexLexer):
    """
    Lexer for the Gleam programming language (version 1.0.0).
    """
    name = 'Gleam'
    url = 'https://gleam.run/'
    filenames = ['*.gleam']
    aliases = ['gleam']
    mimetypes = ['text/x-gleam']
    version_added = '2.19'
    keywords = words(('as', 'assert', 'auto', 'case', 'const', 'delegate', 'derive', 'echo', 'else', 'fn', 'if', 'implement', 'import', 'let', 'macro', 'opaque', 'panic', 'pub', 'test', 'todo', 'type', 'use'), suffix='\\b')
    tokens = {'root': [('(///.*?)(\\n)', bygroups(String.Doc, Whitespace)), ('(//.*?)(\\n)', bygroups(Comment.Single, Whitespace)), (keywords, Keyword), ('([a-zA-Z_]+)(\\.)', bygroups(Keyword, Punctuation)), ('[()\\[\\]{}:;,@]+', Punctuation), ('(#|!=|!|==|\\|>|\\|\\||\\||\\->|<\\-|&&|<<|>>|\\.\\.|\\.|=)', Punctuation), ('(<>|\\+\\.?|\\-\\.?|\\*\\.?|/\\.?|%\\.?|<=\\.?|>=\\.?|<\\.?|>\\.?|=)', Operator), ('"(\\\\"|[^"])*"', String), ('\\b(let)(\\s+)(\\w+)', bygroups(Keyword, Whitespace, Name.Variable)), ('\\b(fn)(\\s+)(\\w+)', bygroups(Keyword, Whitespace, Name.Function)), ('[a-zA-Z_/]\\w*', Name), ('(\\d+(_\\d+)*\\.(?!\\.)(\\d+(_\\d+)*)?|\\.\\d+(_\\d+)*)([eEf][+-]?[0-9]+)?', Number.Float), ('\\d+(_\\d+)*[eEf][+-]?[0-9]+', Number.Float), ('0[xX][a-fA-F0-9]+(_[a-fA-F0-9]+)*(\\.([a-fA-F0-9]+(_[a-fA-F0-9]+)*)?)?p[+-]?\\d+', Number.Float), ('0[bB][01]+(_[01]+)*', Number.Bin), ('0[oO][0-7]+(_[0-7]+)*', Number.Oct), ('0[xX][a-fA-F0-9]+(_[a-fA-F0-9]+)*', Number.Hex), ('\\d+(_\\d+)*', Number.Integer), ('\\s+', Whitespace)]}


