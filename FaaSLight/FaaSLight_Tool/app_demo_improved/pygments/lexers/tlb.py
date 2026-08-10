"""
    pygments.lexers.tlb
    ~~~~~~~~~~~~~~~~~~~

    Lexers for TL-b.

    :copyright: Copyright 2006-present by the Pygments team, see AUTHORS.
    :license: BSD, see LICENSE for details.
"""

from pygments.lexer import RegexLexer, include, words
from pygments.token import Operator, Name, Number, Whitespace, Punctuation, Comment
__all__ = ['TlbLexer']


class TlbLexer(RegexLexer):
    """
    For TL-b source code.
    """
    name = 'Tl-b'
    aliases = ['tlb']
    filenames = ['*.tlb']
    url = 'https://docs.ton.org/#/overviews/TL-B'
    version_added = ''
    tokens = {'root': [('\\s+', Whitespace), include('comments'), ('[0-9]+', Number), (words(('+', '-', '*', '=', '?', '~', '.', '^', '==', '<', '>', '<=', '>=', '!=')), Operator), (words(('##', '#<', '#<=')), Name.Tag), ('#[0-9a-f]*_?', Name.Tag), ('\\$[01]*_?', Name.Tag), ('[a-zA-Z_][0-9a-zA-Z_]*', Name), ('[;():\\[\\]{}]', Punctuation)], 'comments': [('//.*', Comment.Singleline), ('/\\*', Comment.Multiline, 'comment')], 'comment': [('[^/*]+', Comment.Multiline), ('/\\*', Comment.Multiline, '#push'), ('\\*/', Comment.Multiline, '#pop'), ('[*/]', Comment.Multiline)]}


