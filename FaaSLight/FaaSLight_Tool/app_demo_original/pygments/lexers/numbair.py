"""
    pygments.lexers.numbair
    ~~~~~~~~~~~~~~~~~~~~~~~

    Lexer for other Numba Intermediate Representation.

    :copyright: Copyright 2006-present by the Pygments team, see AUTHORS.
    :license: BSD, see LICENSE for details.
"""

from pygments.lexer import RegexLexer, include, bygroups, words
from pygments.token import Whitespace, Name, String, Punctuation, Keyword, Operator, Number
__all__ = ['NumbaIRLexer']


class NumbaIRLexer(RegexLexer):
    """
    Lexer for Numba IR
    """
    name = 'Numba_IR'
    url = 'https://numba.readthedocs.io/en/stable/developer/architecture.html#stage-2-generate-the-numba-ir'
    aliases = ['numba_ir', 'numbair']
    filenames = ['*.numba_ir']
    mimetypes = ['text/x-numba_ir', 'text/x-numbair']
    version_added = '2.19'
    identifier = '\\$[a-zA-Z0-9._]+'
    fun_or_var = '([a-zA-Z_]+[a-zA-Z0-9]*)'
    tokens = {'root': [('(label)(\\ [0-9]+)(:)$', bygroups(Keyword, Name.Label, Punctuation)), ('=', Operator), include('whitespace'), include('keyword'), (identifier, Name.Variable), (fun_or_var + '(\\()', bygroups(Name.Function, Punctuation)), (fun_or_var + '(\\=)', bygroups(Name.Attribute, Punctuation)), (fun_or_var, Name.Constant), ('[0-9]+', Number), ('<[^>\\n]*>', String), ("[=<>{}\\[\\]()*.,!\\':]|x\\b", Punctuation)], 'keyword': [(words(('del', 'jump', 'call', 'branch'), suffix=' '), Keyword)], 'whitespace': [('(\\n|\\s)+', Whitespace)]}


