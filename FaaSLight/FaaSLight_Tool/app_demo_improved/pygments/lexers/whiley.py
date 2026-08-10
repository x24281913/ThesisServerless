"""
    pygments.lexers.whiley
    ~~~~~~~~~~~~~~~~~~~~~~

    Lexers for the Whiley language.

    :copyright: Copyright 2006-present by the Pygments team, see AUTHORS.
    :license: BSD, see LICENSE for details.
"""

from pygments.lexer import RegexLexer, bygroups, words
from pygments.token import Comment, Keyword, Name, Number, Operator, Punctuation, String, Text
__all__ = ['WhileyLexer']


class WhileyLexer(RegexLexer):
    """
    Lexer for the Whiley programming language.
    """
    name = 'Whiley'
    url = 'http://whiley.org/'
    filenames = ['*.whiley']
    aliases = ['whiley']
    mimetypes = ['text/x-whiley']
    version_added = '2.2'
    tokens = {'root': [('\\s+', Text), ('//.*', Comment.Single), ('/\\*\\*/', Comment.Multiline), ('(?s)/\\*\\*.*?\\*/', String.Doc), ('(?s)/\\*.*?\\*/', Comment.Multiline), (words(('if', 'else', 'while', 'for', 'do', 'return', 'switch', 'case', 'default', 'break', 'continue', 'requires', 'ensures', 'where', 'assert', 'assume', 'all', 'no', 'some', 'in', 'is', 'new', 'throw', 'try', 'catch', 'debug', 'skip', 'fail', 'finite', 'total'), suffix='\\b'), Keyword.Reserved), (words(('function', 'method', 'public', 'private', 'protected', 'export', 'native'), suffix='\\b'), Keyword.Declaration), ('(constant|type)(\\s+)([a-zA-Z_]\\w*)(\\s+)(is)\\b', bygroups(Keyword.Declaration, Text, Name, Text, Keyword.Reserved)), ('(true|false|null)\\b', Keyword.Constant), ('(bool|byte|int|real|any|void)\\b', Keyword.Type), ('(import)(\\s+)(\\*)([^\\S\\n]+)(from)\\b', bygroups(Keyword.Namespace, Text, Punctuation, Text, Keyword.Namespace)), ('(import)(\\s+)([a-zA-Z_]\\w*)([^\\S\\n]+)(from)\\b', bygroups(Keyword.Namespace, Text, Name, Text, Keyword.Namespace)), ('(package|import)\\b', Keyword.Namespace), (words(('i8', 'i16', 'i32', 'i64', 'u8', 'u16', 'u32', 'u64', 'uint', 'nat', 'toString'), suffix='\\b'), Name.Builtin), ('[01]+b', Number.Bin), ('[0-9]+\\.[0-9]+', Number.Float), ('[0-9]+\\.(?!\\.)', Number.Float), ('0x[0-9a-fA-F]+', Number.Hex), ('[0-9]+', Number.Integer), ("'[^\\\\]'", String.Char), ('(\')(\\\\[\'"\\\\btnfr])(\')', bygroups(String.Char, String.Escape, String.Char)), ('"', String, 'string'), ('[{}()\\[\\],.;]', Punctuation), ('[+\\-*/%&|<>^!~@=:?\\u2200\\u2203\\u2205\\u2282\\u2286\\u2283\\u2287\\u222A\\u2229\\u2264\\u2265\\u2208\\u2227\\u2228]', Operator), ('[a-zA-Z_]\\w*', Name)], 'string': [('"', String, '#pop'), ('\\\\[btnfr]', String.Escape), ('\\\\u[0-9a-fA-F]{4}', String.Escape), ('\\\\.', String), ('[^\\\\"]+', String)]}


