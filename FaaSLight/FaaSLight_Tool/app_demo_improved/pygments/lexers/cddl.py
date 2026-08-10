"""
    pygments.lexers.cddl
    ~~~~~~~~~~~~~~~~~~~~

    Lexer for the Concise data definition language (CDDL), a notational
    convention to express CBOR and JSON data structures.

    More information:
    https://datatracker.ietf.org/doc/rfc8610/

    :copyright: Copyright 2006-present by the Pygments team, see AUTHORS.
    :license: BSD, see LICENSE for details.
"""

from pygments.lexer import RegexLexer, bygroups, include, words
from pygments.token import Comment, Error, Keyword, Name, Number, Operator, Punctuation, String, Whitespace
__all__ = ['CddlLexer']


class CddlLexer(RegexLexer):
    """
    Lexer for CDDL definitions.
    """
    name = 'CDDL'
    url = 'https://datatracker.ietf.org/doc/rfc8610/'
    aliases = ['cddl']
    filenames = ['*.cddl']
    mimetypes = ['text/x-cddl']
    version_added = '2.8'
    _prelude_types = ['any', 'b64legacy', 'b64url', 'bigfloat', 'bigint', 'bignint', 'biguint', 'bool', 'bstr', 'bytes', 'cbor-any', 'decfrac', 'eb16', 'eb64legacy', 'eb64url', 'encoded-cbor', 'false', 'float', 'float16', 'float16-32', 'float32', 'float32-64', 'float64', 'int', 'integer', 'mime-message', 'nil', 'nint', 'null', 'number', 'regexp', 'tdate', 'text', 'time', 'true', 'tstr', 'uint', 'undefined', 'unsigned', 'uri']
    _controls = ['.and', '.bits', '.cbor', '.cborseq', '.default', '.eq', '.ge', '.gt', '.le', '.lt', '.ne', '.regexp', '.size', '.within']
    _re_id = '[$@A-Z_a-z](?:[\\-\\.]+(?=[$@0-9A-Z_a-z])|[$@0-9A-Z_a-z])*'
    _re_uint = '(?:0b[01]+|0x[0-9a-fA-F]+|[1-9]\\d*|0(?!\\d))'
    _re_int = '-?' + _re_uint
    tokens = {'commentsandwhitespace': [('\\s+', Whitespace), (';.+$', Comment.Single)], 'root': [include('commentsandwhitespace'), (f'#(\\d\\.{_re_uint})?', Keyword.Type), (f'({_re_uint})?(\\*)({_re_uint})?', bygroups(Number, Operator, Number)), ('\\?|\\+', Operator), ('\\^', Operator), ('(\\.\\.\\.|\\.\\.)', Operator), (words(_controls, suffix='\\b'), Operator.Word), (f'&(?=\\s*({_re_id}|\\())', Operator), (f'~(?=\\s*{_re_id})', Operator), ('//|/(?!/)', Operator), ('=>|/==|/=|=', Operator), ('[\\[\\]{}\\(\\),<>:]', Punctuation), ("(b64)(')", bygroups(String.Affix, String.Single), 'bstrb64url'), ("(h)(')", bygroups(String.Affix, String.Single), 'bstrh'), ("'", String.Single, 'bstr'), (f'({_re_id})(\\s*)(:)', bygroups(String, Whitespace, Punctuation)), (words(_prelude_types, prefix='(?![\\-_$@])\\b', suffix='\\b(?![\\-_$@])'), Name.Builtin), (_re_id, Name.Class), ('0b[01]+', Number.Bin), ('0o[0-7]+', Number.Oct), ('0x[0-9a-fA-F]+(\\.[0-9a-fA-F]+)?p[+-]?\\d+', Number.Hex), ('0x[0-9a-fA-F]+', Number.Hex), (f'{_re_int}(?=(\\.\\d|e[+-]?\\d))(?:\\.\\d+)?(?:e[+-]?\\d+)?', Number.Float), (_re_int, Number.Integer), ('"(\\\\\\\\|\\\\"|[^"])*"', String.Double)], 'bstrb64url': [("'", String.Single, '#pop'), include('commentsandwhitespace'), ('\\\\.', String.Escape), ('[0-9a-zA-Z\\-_=]+', String.Single), ('.', Error)], 'bstrh': [("'", String.Single, '#pop'), include('commentsandwhitespace'), ('\\\\.', String.Escape), ('[0-9a-fA-F]+', String.Single), ('.', Error)], 'bstr': [("'", String.Single, '#pop'), ('\\\\.', String.Escape), ("[^'\\\\]+", String.Single)]}


