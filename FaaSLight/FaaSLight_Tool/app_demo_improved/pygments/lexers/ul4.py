"""
    pygments.lexers.ul4
    ~~~~~~~~~~~~~~~~~~~

    Lexer for the UL4 templating language.

    :copyright: Copyright 2006-present by the Pygments team, see AUTHORS.
    :license: BSD, see LICENSE for details.
"""

import re
from pygments.lexer import RegexLexer, DelegatingLexer, bygroups, words, include
from pygments.token import Comment, Text, Keyword, String, Number, Literal, Name, Other, Operator
from pygments.lexers.web import HtmlLexer, XmlLexer, CssLexer, JavascriptLexer
from pygments.lexers.python import PythonLexer
__all__ = ['UL4Lexer', 'HTMLUL4Lexer', 'XMLUL4Lexer', 'CSSUL4Lexer', 'JavascriptUL4Lexer', 'PythonUL4Lexer']


class UL4Lexer(RegexLexer):
    """
    Generic lexer for UL4.
    """
    flags = re.MULTILINE | re.DOTALL
    name = 'UL4'
    aliases = ['ul4']
    filenames = ['*.ul4']
    url = 'https://python.livinglogic.de/UL4.html'
    version_added = '2.12'
    tokens = {'root': [('(<\\?)(\\s*)(ul4)(\\s*)(\\?>)', bygroups(Comment.Preproc, Text.Whitespace, Keyword, Text.Whitespace, Comment.Preproc)), ('(<\\?)(\\s*)(ul4)(\\s*)([a-zA-Z_][a-zA-Z_0-9]*)?', bygroups(Comment.Preproc, Text.Whitespace, Keyword, Text.Whitespace, Name.Function), 'ul4'), ('<\\?\\s*note\\s*\\?>', Comment, 'note'), ('<\\?\\s*note\\s.*?\\?>', Comment), ('<\\?\\s*doc\\s*\\?>', String.Doc, 'doc'), ('<\\?\\s*doc\\s.*?\\?>', String.Doc), ('<\\?\\s*ignore\\s*\\?>', Comment, 'ignore'), ('(<\\?)(\\s*)(def)(\\s*)([a-zA-Z_][a-zA-Z_0-9]*)?', bygroups(Comment.Preproc, Text.Whitespace, Keyword, Text.Whitespace, Name.Function), 'ul4'), ('(<\\?)(\\s*)(printx|print|for|if|elif|else|while|code|renderblocks?|render)\\b', bygroups(Comment.Preproc, Text.Whitespace, Keyword), 'ul4'), ('(<\\?)(\\s*)(end)\\b', bygroups(Comment.Preproc, Text.Whitespace, Keyword), 'end'), ('(<\\?)(\\s*)(whitespace)\\b', bygroups(Comment.Preproc, Text.Whitespace, Keyword), 'whitespace'), ('[^<]+', Other), ('<', Other)], 'ignore': [('<\\?\\s*ignore\\s*\\?>', Comment, '#push'), ('<\\?\\s*end\\s+ignore\\s*\\?>', Comment, '#pop'), ('[^<]+', Comment), ('.', Comment)], 'note': [('<\\?\\s*note\\s*\\?>', Comment, '#push'), ('<\\?\\s*end\\s+note\\s*\\?>', Comment, '#pop'), ('[^<]+', Comment), ('.', Comment)], 'doc': [('<\\?\\s*doc\\s*\\?>', String.Doc, '#push'), ('<\\?\\s*end\\s+doc\\s*\\?>', String.Doc, '#pop'), ('[^<]+', String.Doc), ('.', String.Doc)], 'ul4': [('\\?>', Comment.Preproc, '#pop'), ("'''", String, 'string13'), ('"""', String, 'string23'), ("'", String, 'string1'), ('"', String, 'string2'), ('\\d+\\.\\d*([eE][+-]?\\d+)?', Number.Float), ('\\.\\d+([eE][+-]?\\d+)?', Number.Float), ('\\d+[eE][+-]?\\d+', Number.Float), ('0[bB][01]+', Number.Bin), ('0[oO][0-7]+', Number.Oct), ('0[xX][0-9a-fA-F]+', Number.Hex), ('@\\(\\d\\d\\d\\d-\\d\\d-\\d\\d(T(\\d\\d:\\d\\d(:\\d\\d(\\.\\d{6})?)?)?)?\\)', Literal.Date), ('#[0-9a-fA-F]{8}', Literal.Color), ('#[0-9a-fA-F]{6}', Literal.Color), ('#[0-9a-fA-F]{3,4}', Literal.Color), ('\\d+', Number.Integer), ('//|==|!=|>=|<=|<<|>>|\\+=|-=|\\*=|/=|//=|<<=|>>=|&=|\\|=|^=|=|[\\[\\]{},:*/().~%&|<>^+-]', Operator), (words(('for', 'in', 'if', 'else', 'not', 'is', 'and', 'or'), suffix='\\b'), Keyword), (words(('None', 'False', 'True'), suffix='\\b'), Keyword.Constant), ('[a-zA-Z_][a-zA-Z0-9_]*', Name), ('\\s+', Text.Whitespace)], 'end': [('\\?>', Comment.Preproc, '#pop'), (words(('for', 'if', 'def', 'while', 'renderblock', 'renderblocks'), suffix='\\b'), Keyword), ('\\s+', Text)], 'whitespace': [('\\?>', Comment.Preproc, '#pop'), (words(('keep', 'strip', 'smart'), suffix='\\b'), Comment.Preproc), ('\\s+', Text.Whitespace)], 'stringescapes': [('\\\\[\\\\\'"abtnfr]', String.Escape), ('\\\\x[0-9a-fA-F]{2}', String.Escape), ('\\\\u[0-9a-fA-F]{4}', String.Escape), ('\\\\U[0-9a-fA-F]{8}', String.Escape)], 'string13': [("'''", String, '#pop'), include('stringescapes'), ("[^\\\\']+", String), ('.', String)], 'string23': [('"""', String, '#pop'), include('stringescapes'), ('[^\\\\"]+', String), ('.', String)], 'string1': [("'", String, '#pop'), include('stringescapes'), ("[^\\\\']+", String), ('.', String)], 'string2': [('"', String, '#pop'), include('stringescapes'), ('[^\\\\"]+', String), ('.', String)]}



class HTMLUL4Lexer(DelegatingLexer):
    """
    Lexer for UL4 embedded in HTML.
    """
    name = 'HTML+UL4'
    aliases = ['html+ul4']
    filenames = ['*.htmlul4']
    url = 'https://python.livinglogic.de/UL4.html'
    version_added = ''
    
    def __init__(self, **options):
        super().__init__(HtmlLexer, UL4Lexer, **options)



class XMLUL4Lexer(DelegatingLexer):
    """
    Lexer for UL4 embedded in XML.
    """
    name = 'XML+UL4'
    aliases = ['xml+ul4']
    filenames = ['*.xmlul4']
    url = 'https://python.livinglogic.de/UL4.html'
    version_added = ''
    
    def __init__(self, **options):
        super().__init__(XmlLexer, UL4Lexer, **options)



class CSSUL4Lexer(DelegatingLexer):
    """
    Lexer for UL4 embedded in CSS.
    """
    name = 'CSS+UL4'
    aliases = ['css+ul4']
    filenames = ['*.cssul4']
    url = 'https://python.livinglogic.de/UL4.html'
    version_added = ''
    
    def __init__(self, **options):
        super().__init__(CssLexer, UL4Lexer, **options)



class JavascriptUL4Lexer(DelegatingLexer):
    """
    Lexer for UL4 embedded in Javascript.
    """
    name = 'Javascript+UL4'
    aliases = ['js+ul4']
    filenames = ['*.jsul4']
    url = 'https://python.livinglogic.de/UL4.html'
    version_added = ''
    
    def __init__(self, **options):
        super().__init__(JavascriptLexer, UL4Lexer, **options)



class PythonUL4Lexer(DelegatingLexer):
    """
    Lexer for UL4 embedded in Python.
    """
    name = 'Python+UL4'
    aliases = ['py+ul4']
    filenames = ['*.pyul4']
    url = 'https://python.livinglogic.de/UL4.html'
    version_added = ''
    
    def __init__(self, **options):
        super().__init__(PythonLexer, UL4Lexer, **options)


