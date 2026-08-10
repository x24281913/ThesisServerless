"""
    pygments.lexers.bqn
    ~~~~~~~~~~~~~~~~~~~

    Lexer for BQN.

    :copyright: Copyright 2006-present by the Pygments team, see AUTHORS.
    :license: BSD, see LICENSE for details.
"""

from pygments.lexer import RegexLexer
from pygments.token import Comment, Operator, Keyword, Name, String, Number, Punctuation, Whitespace
__all__ = ['BQNLexer']


class BQNLexer(RegexLexer):
    """
    A simple BQN lexer.
    """
    name = 'BQN'
    url = 'https://mlochbaum.github.io/BQN/index.html'
    aliases = ['bqn']
    filenames = ['*.bqn']
    mimetypes = []
    version_added = '2.16'
    _iwc = '((?=[^𝕎𝕏𝔽𝔾𝕊𝕨𝕩𝕗𝕘𝕤𝕣])\\w)'
    tokens = {'root': [('\\s+', Whitespace), ('#.*$', Comment.Single), ("\\'((\\'\\')|[^\\'])*\\'", String.Single), ('"(("")|[^"])*"', String.Double), ('@', String.Symbol), ('[\\.⋄,\\[\\]⟨⟩‿]', Punctuation), ('[\\(\\)]', String.Regex), ('¯?[0-9](([0-9]|_)*\\.?([0-9]|_)+|([0-9]|_)*)([Ee][¯]?([0-9]|_)+)?|¯|∞|π|·', Number), ('[a-z]' + _iwc + '*', Name.Variable), ('[∘○⊸⟜⌾⊘◶⎉⚇⍟⎊]', Name.Property), ('_(𝕣|[a-zA-Z0-9]+)_', Name.Property), ('[˙˜˘¨⌜⁼´˝`𝕣]', Name.Attribute), ('_(𝕣|[a-zA-Z0-9]+)', Name.Attribute), ('[+\\-×÷\\⋆√⌊⌈∧∨¬|≤<>≥=≠≡≢⊣⊢⥊∾≍⋈↑↓↕«»⌽⍉/⍋⍒⊏⊑⊐⊒∊⍷⊔!𝕎𝕏𝔽𝔾𝕊]', Operator), ('[A-Z]' + _iwc + '*|•' + _iwc + '+', Operator), ('˙', Name.Constant), ('[←↩⇐]', Keyword.Declaration), ('[{}]', Keyword.Type), ('[;:?𝕨𝕩𝕗𝕘𝕤]', Name.Entity)]}


