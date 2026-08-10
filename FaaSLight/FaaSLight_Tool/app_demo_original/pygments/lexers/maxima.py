"""
    pygments.lexers.maxima
    ~~~~~~~~~~~~~~~~~~~~~~

    Lexer for the computer algebra system Maxima.

    Derived from pygments/lexers/algebra.py.

    :copyright: Copyright 2006-present by the Pygments team, see AUTHORS.
    :license: BSD, see LICENSE for details.
"""

import re
from pygments.lexer import RegexLexer, bygroups, words
from pygments.token import Text, Comment, Operator, Keyword, Name, String, Number, Punctuation
__all__ = ['MaximaLexer']


class MaximaLexer(RegexLexer):
    """
    A Maxima lexer.
    Derived from pygments.lexers.MuPADLexer.
    """
    name = 'Maxima'
    url = 'http://maxima.sourceforge.net'
    aliases = ['maxima', 'macsyma']
    filenames = ['*.mac', '*.max']
    version_added = '2.11'
    keywords = ('if', 'then', 'else', 'elseif', 'do', 'while', 'repeat', 'until', 'for', 'from', 'to', 'downto', 'step', 'thru')
    constants = ('%pi', '%e', '%phi', '%gamma', '%i', 'und', 'ind', 'infinity', 'inf', 'minf', 'true', 'false', 'unknown', 'done')
    operators = ('.', ':', '=', '#', '+', '-', '*', '/', '^', '@', '>', '<', '|', '!', "'")
    operator_words = ('and', 'or', 'not')
    tokens = {'root': [('/\\*', Comment.Multiline, 'comment'), ('"(?:[^"\\\\]|\\\\.)*"', String), ('\\(|\\)|\\[|\\]|\\{|\\}', Punctuation), ('[,;$]', Punctuation), (words(constants), Name.Constant), (words(keywords), Keyword), (words(operators), Operator), (words(operator_words), Operator.Word), ('(?x)\n              ((?:[a-zA-Z_#][\\w#]*|`[^`]*`)\n              (?:::[a-zA-Z_#][\\w#]*|`[^`]*`)*)(\\s*)([(])', bygroups(Name.Function, Text.Whitespace, Punctuation)), ('(?x)\n              (?:[a-zA-Z_#%][\\w#%]*|`[^`]*`)\n              (?:::[a-zA-Z_#%][\\w#%]*|`[^`]*`)*', Name.Variable), ('[-+]?(\\d*\\.\\d+([bdefls][-+]?\\d+)?|\\d+(\\.\\d*)?[bdefls][-+]?\\d+)', Number.Float), ('[-+]?\\d+', Number.Integer), ('\\s+', Text.Whitespace), ('.', Text)], 'comment': [('[^*/]+', Comment.Multiline), ('/\\*', Comment.Multiline, '#push'), ('\\*/', Comment.Multiline, '#pop'), ('[*/]', Comment.Multiline)]}
    
    def analyse_text(text):
        strength = 0.0
        if re.search('\\$\\s*$', text, re.MULTILINE):
            strength += 0.05
        if ':=' in text:
            strength += 0.02
        return strength


