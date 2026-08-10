"""
    pygments.lexers.futhark
    ~~~~~~~~~~~~~~~~~~~~~~~

    Lexer for the Futhark language

    :copyright: Copyright 2006-present by the Pygments team, see AUTHORS.
    :license: BSD, see LICENSE for details.
"""

from pygments.lexer import RegexLexer, bygroups
from pygments.token import Comment, Operator, Keyword, Name, String, Number, Punctuation, Whitespace
from pygments import unistring as uni
__all__ = ['FutharkLexer']


class FutharkLexer(RegexLexer):
    """
    A Futhark lexer
    """
    name = 'Futhark'
    url = 'https://futhark-lang.org/'
    aliases = ['futhark']
    filenames = ['*.fut']
    mimetypes = ['text/x-futhark']
    version_added = '2.8'
    num_types = ('i8', 'i16', 'i32', 'i64', 'u8', 'u16', 'u32', 'u64', 'f32', 'f64')
    other_types = ('bool', )
    reserved = ('if', 'then', 'else', 'def', 'let', 'loop', 'in', 'with', 'type', 'type~', 'type^', 'val', 'entry', 'for', 'while', 'do', 'case', 'match', 'include', 'import', 'module', 'open', 'local', 'assert', '_')
    ascii = ('NUL', 'SOH', '[SE]TX', 'EOT', 'ENQ', 'ACK', 'BEL', 'BS', 'HT', 'LF', 'VT', 'FF', 'CR', 'S[OI]', 'DLE', 'DC[1-4]', 'NAK', 'SYN', 'ETB', 'CAN', 'EM', 'SUB', 'ESC', '[FGRU]S', 'SP', 'DEL')
    num_postfix = '({})?'.format('|'.join(num_types))
    identifier_re = "[a-zA-Z_][a-zA-Z_0-9']*"
    tokens = {'root': [('--(.*?)$', Comment.Single), ('\\s+', Whitespace), ('\\(\\)', Punctuation), ("\\b({})(?!\\')\\b".format('|'.join(reserved)), Keyword.Reserved), ("\\b({})(?!\\')\\b".format('|'.join(num_types + other_types)), Keyword.Type), ('#\\[([a-zA-Z_\\(\\) ]*)\\]', Comment.Preproc), (f'[#!]?({identifier_re}\\.)*{identifier_re}', Name), ('\\\\', Operator), ('[-+/%=!><|&*^][-+/%=!><|&*^.]*', Operator), ("[][(),:;`{}?.\\'~^]", Punctuation), ('0[xX]_*[\\da-fA-F](_*[\\da-fA-F])*_*[pP][+-]?\\d(_*\\d)*' + num_postfix, Number.Float), ('0[xX]_*[\\da-fA-F](_*[\\da-fA-F])*\\.[\\da-fA-F](_*[\\da-fA-F])*(_*[pP][+-]?\\d(_*\\d)*)?' + num_postfix, Number.Float), ('\\d(_*\\d)*_*[eE][+-]?\\d(_*\\d)*' + num_postfix, Number.Float), ('\\d(_*\\d)*\\.\\d(_*\\d)*(_*[eE][+-]?\\d(_*\\d)*)?' + num_postfix, Number.Float), ('0[bB]_*[01](_*[01])*' + num_postfix, Number.Bin), ('0[xX]_*[\\da-fA-F](_*[\\da-fA-F])*' + num_postfix, Number.Hex), ('\\d(_*\\d)*' + num_postfix, Number.Integer), ("'", String.Char, 'character'), ('"', String, 'string'), ('\\[[a-zA-Z_\\d]*\\]', Keyword.Type), ('\\(\\)', Name.Builtin)], 'character': [("[^\\\\']'", String.Char, '#pop'), ('\\\\', String.Escape, 'escape'), ("'", String.Char, '#pop')], 'string': [('[^\\\\"]+', String), ('\\\\', String.Escape, 'escape'), ('"', String, '#pop')], 'escape': [('[abfnrtv"\\\'&\\\\]', String.Escape, '#pop'), ('\\^[][' + uni.Lu + '@^_]', String.Escape, '#pop'), ('|'.join(ascii), String.Escape, '#pop'), ('o[0-7]+', String.Escape, '#pop'), ('x[\\da-fA-F]+', String.Escape, '#pop'), ('\\d+', String.Escape, '#pop'), ('(\\s+)(\\\\)', bygroups(Whitespace, String.Escape), '#pop')]}


