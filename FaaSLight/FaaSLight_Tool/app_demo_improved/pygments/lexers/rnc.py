"""
    pygments.lexers.rnc
    ~~~~~~~~~~~~~~~~~~~

    Lexer for Relax-NG Compact syntax

    :copyright: Copyright 2006-present by the Pygments team, see AUTHORS.
    :license: BSD, see LICENSE for details.
"""

from pygments.lexer import RegexLexer
from pygments.token import Text, Comment, Operator, Keyword, Name, String, Punctuation
__all__ = ['RNCCompactLexer']


class RNCCompactLexer(RegexLexer):
    """
    For RelaxNG-compact syntax.
    """
    name = 'Relax-NG Compact'
    url = 'http://relaxng.org'
    aliases = ['rng-compact', 'rnc']
    filenames = ['*.rnc']
    version_added = '2.2'
    tokens = {'root': [('namespace\\b', Keyword.Namespace), ('(?:default|datatypes)\\b', Keyword.Declaration), ('##.*$', Comment.Preproc), ('#.*$', Comment.Single), ('"[^"]*"', String.Double), ('(?:element|attribute|mixed)\\b', Keyword.Declaration, 'variable'), ('(text\\b|xsd:[^ ]+)', Keyword.Type, 'maybe_xsdattributes'), ('[,?&*=|~]|>>', Operator), ('[(){}]', Punctuation), ('.', Text)], 'variable': [('[^{]+', Name.Variable), ('\\{', Punctuation, '#pop')], 'maybe_xsdattributes': [('\\{', Punctuation, 'xsdattributes'), ('\\}', Punctuation, '#pop'), ('.', Text)], 'xsdattributes': [('[^ =}]', Name.Attribute), ('=', Operator), ('"[^"]*"', String.Double), ('\\}', Punctuation, '#pop'), ('.', Text)]}


