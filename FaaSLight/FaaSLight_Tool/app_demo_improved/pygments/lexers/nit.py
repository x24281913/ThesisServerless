"""
    pygments.lexers.nit
    ~~~~~~~~~~~~~~~~~~~

    Lexer for the Nit language.

    :copyright: Copyright 2006-present by the Pygments team, see AUTHORS.
    :license: BSD, see LICENSE for details.
"""

from pygments.lexer import RegexLexer, words
from pygments.token import Text, Comment, Operator, Keyword, Name, String, Number, Punctuation
__all__ = ['NitLexer']


class NitLexer(RegexLexer):
    """
    For nit source.
    """
    name = 'Nit'
    url = 'http://nitlanguage.org'
    aliases = ['nit']
    filenames = ['*.nit']
    version_added = '2.0'
    tokens = {'root': [('#.*?$', Comment.Single), (words(('package', 'module', 'import', 'class', 'abstract', 'interface', 'universal', 'enum', 'end', 'fun', 'type', 'init', 'redef', 'isa', 'do', 'readable', 'writable', 'var', 'intern', 'extern', 'public', 'protected', 'private', 'intrude', 'if', 'then', 'else', 'while', 'loop', 'for', 'in', 'and', 'or', 'not', 'implies', 'return', 'continue', 'break', 'abort', 'assert', 'new', 'is', 'once', 'super', 'self', 'true', 'false', 'nullable', 'null', 'as', 'isset', 'label', '__debug__'), suffix='(?=[\\r\\n\\t( ])'), Keyword), ('[A-Z]\\w*', Name.Class), ('"""(([^\\\'\\\\]|\\\\.)|\\\\r|\\\\n)*((\\{\\{?)?(""?\\{\\{?)*""""*)', String), ("\\'\\'\\'(((\\\\.|[^\\'\\\\])|\\\\r|\\\\n)|\\'((\\\\.|[^\\'\\\\])|\\\\r|\\\\n)|\\'\\'((\\\\.|[^\\'\\\\])|\\\\r|\\\\n))*\\'\\'\\'", String), ('"""(([^\\\'\\\\]|\\\\.)|\\\\r|\\\\n)*((""?)?(\\{\\{?""?)*\\{\\{\\{\\{*)', String), ('\\}\\}\\}(((\\\\.|[^\\\'\\\\])|\\\\r|\\\\n))*(""?)?(\\{\\{?""?)*\\{\\{\\{\\{*', String), ('\\}\\}\\}(((\\\\.|[^\\\'\\\\])|\\\\r|\\\\n))*(\\{\\{?)?(""?\\{\\{?)*""""*', String), ('"(\\\\.|([^"}{\\\\]))*"', String), ('"(\\\\.|([^"}{\\\\]))*\\{', String), ('\\}(\\\\.|([^"}{\\\\]))*\\{', String), ('\\}(\\\\.|([^"}{\\\\]))*"', String), ("(\\'[^\\'\\\\]\\')|(\\'\\\\.\\')", String.Char), ('[0-9]+', Number.Integer), ('[0-9]*.[0-9]+', Number.Float), ('0(x|X)[0-9A-Fa-f]+', Number.Hex), ('[a-z]\\w*', Name), ('_\\w+', Name.Variable.Instance), ('==|!=|<==>|>=|>>|>|<=|<<|<|\\+|-|=|/|\\*|%|\\+=|-=|!|@', Operator), ('\\(|\\)|\\[|\\]|,|\\.\\.\\.|\\.\\.|\\.|::|:', Punctuation), ('`\\{[^`]*`\\}', Text), ('[\\r\\n\\t ]+', Text)]}


