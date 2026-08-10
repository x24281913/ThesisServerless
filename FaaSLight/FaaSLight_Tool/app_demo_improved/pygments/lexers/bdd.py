"""
    pygments.lexers.bdd
    ~~~~~~~~~~~~~~~~~~~

    Lexer for BDD(Behavior-driven development).

    :copyright: Copyright 2006-present by the Pygments team, see AUTHORS.
    :license: BSD, see LICENSE for details.
"""

from pygments.lexer import RegexLexer, include
from pygments.token import Comment, Keyword, Name, String, Number, Text, Punctuation, Whitespace
__all__ = ['BddLexer']


class BddLexer(RegexLexer):
    """
    Lexer for BDD(Behavior-driven development), which highlights not only
    keywords, but also comments, punctuations, strings, numbers, and variables.
    """
    name = 'Bdd'
    aliases = ['bdd']
    filenames = ['*.feature']
    mimetypes = ['text/x-bdd']
    url = 'https://en.wikipedia.org/wiki/Behavior-driven_development'
    version_added = '2.11'
    step_keywords = 'Given|When|Then|Add|And|Feature|Scenario Outline|Scenario|Background|Examples|But'
    tokens = {'comments': [('^\\s*#.*$', Comment)], 'miscellaneous': [('(<|>|\\[|\\]|=|\\||:|\\(|\\)|\\{|\\}|,|\\.|;|-|_|\\$)', Punctuation), ('((?<=\\<)[^\\\\>]+(?=\\>))', Name.Variable), ('"([^\\"]*)"', String), ('^@\\S+', Name.Label)], 'numbers': [('(\\d+\\.?\\d*|\\d*\\.\\d+)([eE][+-]?[0-9]+)?', Number)], 'root': [('\\n|\\s+', Whitespace), (step_keywords, Keyword), include('comments'), include('miscellaneous'), include('numbers'), ('\\S+', Text)]}
    
    def analyse_text(self, text):
        return


