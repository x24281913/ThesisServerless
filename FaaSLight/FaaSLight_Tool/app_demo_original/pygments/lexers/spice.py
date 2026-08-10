"""
    pygments.lexers.spice
    ~~~~~~~~~~~~~~~~~~~~~

    Lexers for the Spice programming language.

    :copyright: Copyright 2006-present by the Pygments team, see AUTHORS.
    :license: BSD, see LICENSE for details.
"""

from pygments.lexer import RegexLexer, bygroups, words
from pygments.token import Text, Comment, Operator, Keyword, Name, String, Number, Punctuation, Whitespace
__all__ = ['SpiceLexer']


class SpiceLexer(RegexLexer):
    """
    For Spice source.
    """
    name = 'Spice'
    url = 'https://www.spicelang.com'
    filenames = ['*.spice']
    aliases = ['spice', 'spicelang']
    mimetypes = ['text/x-spice']
    version_added = '2.11'
    tokens = {'root': [('\\n', Whitespace), ('\\s+', Whitespace), ('\\\\\\n', Text), ('//(.*?)\\n', Comment.Single), ('/(\\\\\\n)?[*]{2}(.|\\n)*?[*](\\\\\\n)?/', String.Doc), ('/(\\\\\\n)?[*](.|\\n)*?[*](\\\\\\n)?/', Comment.Multiline), ('(import|as)\\b', Keyword.Namespace), ('(f|p|type|struct|interface|enum|alias|operator)\\b', Keyword.Declaration), (words(('if', 'else', 'switch', 'case', 'default', 'for', 'foreach', 'do', 'while', 'break', 'continue', 'fallthrough', 'return', 'assert', 'unsafe', 'ext', 'cast'), suffix='\\b'), Keyword), (words(('const', 'signed', 'unsigned', 'inline', 'public', 'heap', 'compose'), suffix='\\b'), Keyword.Pseudo), (words(('new', 'yield', 'stash', 'pick', 'sync', 'class'), suffix='\\b'), Keyword.Reserved), ('(true|false|nil)\\b', Keyword.Constant), (words(('double', 'int', 'short', 'long', 'byte', 'char', 'string', 'bool', 'dyn'), suffix='\\b'), Keyword.Type), (words(('printf', 'sizeof', 'alignof', 'len', 'panic'), suffix='\\b(\\()'), bygroups(Name.Builtin, Punctuation)), ('[-]?[0-9]*[.][0-9]+([eE][+-]?[0-9]+)?', Number.Double), ('0[bB][01]+[slu]?', Number.Bin), ('0[oO][0-7]+[slu]?', Number.Oct), ('0[xXhH][0-9a-fA-F]+[slu]?', Number.Hex), ('(0[dD])?[0-9]+[slu]?', Number.Integer), ('"(\\\\\\\\|\\\\[^\\\\]|[^"\\\\])*"', String), ("\\'(\\\\\\\\|\\\\[^\\\\]|[^\\'\\\\])\\'", String.Char), ('<<=|>>=|<<|>>|<=|>=|\\+=|-=|\\*=|/=|\\%=|\\|=|&=|\\^=|&&|\\|\\||&|\\||\\+\\+|--|\\%|\\^|\\~|==|!=|->|::|[.]{3}|#!|#|[+\\-*/&]', Operator), ('[|<>=!()\\[\\]{}.,;:\\?]', Punctuation), ('[^\\W\\d]\\w*', Name.Other)]}


