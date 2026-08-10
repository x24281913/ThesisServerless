"""
    pygments.lexers.rell
    ~~~~~~~~~~~~~~~~~~~~

    Lexers for the Rell language.

    :copyright: Copyright 2006-present by the Pygments team, see AUTHORS.
    :license: BSD, see LICENSE for details.
"""

from pygments.lexer import RegexLexer, bygroups, default, words
from pygments.token import Comment, Keyword, Name, String, Number, Punctuation, Whitespace
__all__ = ['RellLexer']


class RellLexer(RegexLexer):
    """
    A Lexer for Rell.
    """
    name = 'Rell'
    url = 'https://docs.chromia.com/rell/rell-intro'
    aliases = ['rell']
    filenames = ['*.rell']
    mimetypes = ['text/x-rell']
    version_added = '2.20'
    ident = '[a-zA-Z_][a-zA-Z0-9_]*'
    tokens = {'root': [(words(('big_integer', 'boolean', 'byte_array', 'decimal', 'gtv', 'integer', 'json', 'list', 'map', 'mutable', 'set', 'text', 'virtual'), suffix='\\b'), Keyword.Type), ('(false|true|null)\\b', Keyword.Constant), ('(entity|enum|namespace|object|struct)\\b', Keyword.Declaration), ('(function|operation|query)\\b', Keyword.Declaration, 'function'), (words(('abstract', 'and', 'break', 'continue', 'create', 'delete', 'else', 'for', 'if', 'import', 'in', 'index', 'key', 'limit', 'module', 'not', 'offset', 'or', 'override', 'return', 'update', 'val', 'var', 'when', 'while'), suffix='\\b'), Keyword.Reserved), ('//.*?$', Comment.Single), ('/\\*(.|\\n|\\r)*?\\*/', Comment.Multiline), ('"(\\\\\\\\|\\\\"|[^"])*"', String.Double), ("\\'(\\\\\\\\|\\\\\\'|[^\\\\\\'])*\\'", String.Single), ('-?[0-9]*\\.[0-9]+([eE][+-][0-9]+)?', Number.Float), ('-?[0-9]+([eE][+-][0-9]+|[lL])?', Number.Integer), ('x(\\\'[a-fA-F0-9]*\\\'|"[a-fA-F0-9]*")', String.Binary), ('(\\.)([ \\n\\t\\r]*)(' + ident + ')', bygroups(Punctuation, Whitespace, Name.Attribute)), ('[{}():;,]+', Punctuation), ('[ \\n\\t\\r]+', Whitespace), ('@[a-zA-Z_][a-zA-Z0-9_]*', Name.Decorator), ('[~^*!%&\\[\\]<>|+=/?\\-@\\$]', Punctuation.Marker), (ident, Name), ('(\\.)+', Punctuation)], 'function': [('[ \\n\\t\\r]+', Whitespace), (ident, Name.Function, '#pop'), default('#pop')]}


