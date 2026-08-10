"""
    pygments.lexers.pointless
    ~~~~~~~~~~~~~~~~~~~~~~~~~

    Lexers for Pointless.

    :copyright: Copyright 2006-present by the Pygments team, see AUTHORS.
    :license: BSD, see LICENSE for details.
"""

from pygments.lexer import RegexLexer, words
from pygments.token import Comment, Error, Keyword, Name, Number, Operator, Punctuation, String, Text
__all__ = ['PointlessLexer']


class PointlessLexer(RegexLexer):
    """
    For Pointless source code.
    """
    name = 'Pointless'
    url = 'https://ptls.dev'
    aliases = ['pointless']
    filenames = ['*.ptls']
    version_added = '2.7'
    ops = words(['+', '-', '*', '/', '**', '%', '+=', '-=', '*=', '/=', '**=', '%=', '|>', '=', '==', '!=', '<', '>', '<=', '>=', '=>', '$', '++'])
    keywords = words(['if', 'then', 'else', 'where', 'with', 'cond', 'case', 'and', 'or', 'not', 'in', 'as', 'for', 'requires', 'throw', 'try', 'catch', 'when', 'yield', 'upval'], suffix='\\b')
    tokens = {'root': [('[ \\n\\r]+', Text), ('--.*$', Comment.Single), ('"""', String, 'multiString'), ('"', String, 'string'), ('[\\[\\](){}:;,.]', Punctuation), (ops, Operator), (keywords, Keyword), ('\\d+|\\d*\\.\\d+', Number), ('(true|false)\\b', Name.Builtin), ('[A-Z][a-zA-Z0-9]*\\b', String.Symbol), ('output\\b', Name.Variable.Magic), ('(export|import)\\b', Keyword.Namespace), ('[a-z][a-zA-Z0-9]*\\b', Name.Variable)], 'multiString': [('\\\\.', String.Escape), ('"""', String, '#pop'), ('"', String), ('[^\\\\"]+', String)], 'string': [('\\\\.', String.Escape), ('"', String, '#pop'), ('\\n', Error), ('[^\\\\"]+', String)]}


