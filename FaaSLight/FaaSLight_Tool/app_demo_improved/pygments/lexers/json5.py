"""
    pygments.lexers.json5
    ~~~~~~~~~~~~~~~~~~~~~

    Lexer for Json5 file format.

    :copyright: Copyright 2006-present by the Pygments team, see AUTHORS.
    :license: BSD, see LICENSE for details.
"""

from pygments.lexer import include, RegexLexer, words
from pygments.token import Comment, Keyword, Name, Number, Punctuation, String, Whitespace
__all__ = ['Json5Lexer']

def string_rules(quote_mark):
    return [(f'[^{quote_mark}\\\\]+', String), ('\\\\.', String.Escape), ('\\\\', Punctuation), (quote_mark, String, '#pop')]

def quoted_field_name(quote_mark):
    return [(f'([^{quote_mark}\\\\]|\\\\.)*{quote_mark}', Name.Variable, ('#pop', 'object_value'))]


class Json5Lexer(RegexLexer):
    """Lexer for JSON5 data structures."""
    name = 'JSON5'
    aliases = ['json5']
    filenames = ['*.json5']
    url = 'https://json5.org'
    version_added = '2.19'
    tokens = {'_comments': [('(//|#).*\\n', Comment.Single), ('/\\*\\*([^/]|/(?!\\*))*\\*/', String.Doc), ('/\\*([^/]|/(?!\\*))*\\*/', Comment)], 'root': [include('_comments'), ("'", String, 'singlestring'), ('"', String, 'doublestring'), ('[+-]?0[xX][0-9a-fA-F]+', Number.Hex), ('[+-.]?[0-9]+[.]?[0-9]?([eE][-]?[0-9]+)?', Number.Float), ('\\{', Punctuation, 'object'), ('\\[', Punctuation, 'array'), (words(['false', 'Infinity', '+Infinity', '-Infinity', 'NaN', 'null', 'true'], suffix='\\b'), Keyword), ('\\s+', Whitespace), (':', Punctuation)], 'singlestring': string_rules("'"), 'doublestring': string_rules('"'), 'array': [(',', Punctuation), ('\\]', Punctuation, '#pop'), include('root')], 'object': [('\\s+', Whitespace), ('\\}', Punctuation, '#pop'), ('\\b([^:]+)', Name.Variable, 'object_value'), ('"', Name.Variable, 'double_field_name'), ("'", Name.Variable, 'single_field_name'), include('_comments')], 'double_field_name': quoted_field_name('"'), 'single_field_name': quoted_field_name("'"), 'object_value': [(',', Punctuation, '#pop'), ('\\}', Punctuation, '#pop:2'), include('root')]}


