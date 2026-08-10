"""
    pygments.lexers.go
    ~~~~~~~~~~~~~~~~~~

    Lexers for the Google Go language.

    :copyright: Copyright 2006-present by the Pygments team, see AUTHORS.
    :license: BSD, see LICENSE for details.
"""

from pygments.lexer import RegexLexer, bygroups, words
from pygments.token import Text, Comment, Operator, Keyword, Name, String, Number, Punctuation, Whitespace
__all__ = ['GoLexer']


class GoLexer(RegexLexer):
    """
    For Go source.
    """
    name = 'Go'
    url = 'https://go.dev/'
    filenames = ['*.go']
    aliases = ['go', 'golang']
    mimetypes = ['text/x-gosrc']
    version_added = '1.2'
    tokens = {'root': [('\\n', Whitespace), ('\\s+', Whitespace), ('(\\\\)(\\n)', bygroups(Text, Whitespace)), ('//(.*?)$', Comment.Single), ('/(\\\\\\n)?[*](.|\\n)*?[*](\\\\\\n)?/', Comment.Multiline), ('(import|package)\\b', Keyword.Namespace), ('(var|func|struct|map|chan|type|interface|const)\\b', Keyword.Declaration), (words(('break', 'default', 'select', 'case', 'defer', 'go', 'else', 'goto', 'switch', 'fallthrough', 'if', 'range', 'continue', 'for', 'return'), suffix='\\b'), Keyword), ('(true|false|iota|nil)\\b', Keyword.Constant), (words(('uint', 'uint8', 'uint16', 'uint32', 'uint64', 'int', 'int8', 'int16', 'int32', 'int64', 'float', 'float32', 'float64', 'complex64', 'complex128', 'byte', 'rune', 'string', 'bool', 'error', 'uintptr', 'any', 'comparable', 'print', 'println', 'panic', 'recover', 'close', 'complex', 'real', 'imag', 'len', 'cap', 'append', 'copy', 'delete', 'new', 'make', 'min', 'max', 'clear'), suffix='\\b(\\()'), bygroups(Name.Builtin, Punctuation)), (words(('uint', 'uint8', 'uint16', 'uint32', 'uint64', 'int', 'int8', 'int16', 'int32', 'int64', 'float', 'float32', 'float64', 'complex64', 'complex128', 'byte', 'rune', 'string', 'bool', 'error', 'uintptr', 'any', 'comparable'), suffix='\\b'), Keyword.Type), ('\\d+i', Number), ('\\d+\\.\\d*([Ee][-+]\\d+)?i', Number), ('\\.\\d+([Ee][-+]\\d+)?i', Number), ('\\d+[Ee][-+]\\d+i', Number), ('\\d+(\\.\\d+[eE][+\\-]?\\d+|\\.\\d*|[eE][+\\-]?\\d+)', Number.Float), ('\\.\\d+([eE][+\\-]?\\d+)?', Number.Float), ('0[0-7]+', Number.Oct), ('0[xX][0-9a-fA-F]+', Number.Hex), ('(0|[1-9][0-9]*)', Number.Integer), ('\'(\\\\[\'"\\\\abfnrtv]|\\\\x[0-9a-fA-F]{2}|\\\\[0-7]{1,3}|\\\\u[0-9a-fA-F]{4}|\\\\U[0-9a-fA-F]{8}|[^\\\\])\'', String.Char), ('`[^`]*`', String), ('"(\\\\\\\\|\\\\[^\\\\]|[^"\\\\])*"', String), ('(<<=|>>=|<<|>>|<=|>=|&\\^=|&\\^|\\+=|-=|\\*=|/=|%=|&=|\\|=|&&|\\|\\||<-|\\+\\+|--|==|!=|:=|\\.\\.\\.|[+\\-*/%&]|~|\\|)', Operator), ('[|^<>=!()\\[\\]{}.,;:]', Punctuation), ('[^\\W\\d]\\w*', Name.Other)]}


