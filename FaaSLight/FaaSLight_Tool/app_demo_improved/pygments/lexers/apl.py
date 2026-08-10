"""
    pygments.lexers.apl
    ~~~~~~~~~~~~~~~~~~~

    Lexers for APL.

    :copyright: Copyright 2006-present by the Pygments team, see AUTHORS.
    :license: BSD, see LICENSE for details.
"""

from pygments.lexer import RegexLexer
from pygments.token import Comment, Operator, Keyword, Name, String, Number, Punctuation, Whitespace
__all__ = ['APLLexer']


class APLLexer(RegexLexer):
    """
    A simple APL lexer.
    """
    name = 'APL'
    url = 'https://en.m.wikipedia.org/wiki/APL_(programming_language)'
    aliases = ['apl']
    filenames = ['*.apl', '*.aplf', '*.aplo', '*.apln', '*.aplc', '*.apli', '*.dyalog']
    version_added = '2.0'
    tokens = {'root': [('\\s+', Whitespace), ('[⍝#].*$', Comment.Single), ("\\'((\\'\\')|[^\\'])*\\'", String.Single), ('"(("")|[^"])*"', String.Double), ('[⋄◇()]', Punctuation), ('[\\[\\];]', String.Regex), ('⎕[A-Za-zΔ∆⍙][A-Za-zΔ∆⍙_¯0-9]*', Name.Function), ('[A-Za-zΔ∆⍙_][A-Za-zΔ∆⍙_¯0-9]*', Name.Variable), ('¯?(0[Xx][0-9A-Fa-f]+|[0-9]*\\.?[0-9]+([Ee][+¯]?[0-9]+)?|¯|∞)([Jj]¯?(0[Xx][0-9A-Fa-f]+|[0-9]*\\.?[0-9]+([Ee][+¯]?[0-9]+)?|¯|∞))?', Number), ('[\\.\\\\\\/⌿⍀¨⍣⍨⍠⍤∘⌸&⌶@⌺⍥⍛⍢]', Name.Attribute), ('[+\\-×÷⌈⌊∣|⍳?*⍟○!⌹<≤=>≥≠≡≢∊⍷∪∩~∨∧⍱⍲⍴,⍪⌽⊖⍉↑↓⊂⊃⌷⍋⍒⊤⊥⍕⍎⊣⊢⍁⍂≈⌸⍯↗⊆⊇⍸√⌾…⍮]', Operator), ('⍬', Name.Constant), ('[⎕⍞]', Name.Variable.Global), ('[←→]', Keyword.Declaration), ('[⍺⍵⍶⍹∇:]', Name.Builtin.Pseudo), ('[{}]', Keyword.Type)]}


