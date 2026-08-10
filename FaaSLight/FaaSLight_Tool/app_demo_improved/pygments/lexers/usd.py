"""
    pygments.lexers.usd
    ~~~~~~~~~~~~~~~~~~~

    The module that parses Pixar's Universal Scene Description file format.

    :copyright: Copyright 2006-present by the Pygments team, see AUTHORS.
    :license: BSD, see LICENSE for details.
"""

from pygments.lexer import RegexLexer, bygroups
from pygments.lexer import words as words_
from pygments.lexers._usd_builtins import COMMON_ATTRIBUTES, KEYWORDS, OPERATORS, SPECIAL_NAMES, TYPES
from pygments.token import Comment, Keyword, Name, Number, Operator, Punctuation, String, Text, Whitespace
__all__ = ['UsdLexer']

def _keywords(words, type_):
    return [(words_(words, prefix='\\b', suffix='\\b'), type_)]
_TYPE = '(\\w+(?:\\[\\])?)'
_BASE_ATTRIBUTE = '(\\w+(?:\\:\\w+)*)(?:(\\.)(timeSamples))?'
_WHITESPACE = '([ \\t]+)'


class UsdLexer(RegexLexer):
    """
    A lexer that parses Pixar's Universal Scene Description file format.
    """
    name = 'USD'
    url = 'https://graphics.pixar.com/usd/release/index.html'
    aliases = ['usd', 'usda']
    filenames = ['*.usd', '*.usda']
    version_added = '2.6'
    tokens = {'root': [(f'(custom){_WHITESPACE}(uniform)(\\s+){_TYPE}(\\s+){_BASE_ATTRIBUTE}(\\s*)(=)', bygroups(Keyword.Token, Whitespace, Keyword.Token, Whitespace, Keyword.Type, Whitespace, Name.Attribute, Text, Name.Keyword.Tokens, Whitespace, Operator)), (f'(custom){_WHITESPACE}{_TYPE}(\\s+){_BASE_ATTRIBUTE}(\\s*)(=)', bygroups(Keyword.Token, Whitespace, Keyword.Type, Whitespace, Name.Attribute, Text, Name.Keyword.Tokens, Whitespace, Operator)), (f'(uniform){_WHITESPACE}{_TYPE}(\\s+){_BASE_ATTRIBUTE}(\\s*)(=)', bygroups(Keyword.Token, Whitespace, Keyword.Type, Whitespace, Name.Attribute, Text, Name.Keyword.Tokens, Whitespace, Operator)), (f'{_TYPE}{_WHITESPACE}{_BASE_ATTRIBUTE}(\\s*)(=)', bygroups(Keyword.Type, Whitespace, Name.Attribute, Text, Name.Keyword.Tokens, Whitespace, Operator))] + _keywords(KEYWORDS, Keyword.Tokens) + _keywords(SPECIAL_NAMES, Name.Builtins) + _keywords(COMMON_ATTRIBUTES, Name.Attribute) + [('\\b\\w+:[\\w:]+\\b', Name.Attribute)] + _keywords(OPERATORS, Operator) + [(type_ + '\\[\\]', Keyword.Type) for type_ in TYPES] + _keywords(TYPES, Keyword.Type) + [('[(){}\\[\\]]', Punctuation), ('#.*?$', Comment.Single), (',', Punctuation), (';', Punctuation), ('=', Operator), ('[-]*([0-9]*[.])?[0-9]+(?:e[+-]*\\d+)?', Number), ("'''(?:.|\\n)*?'''", String), ('"""(?:.|\\n)*?"""', String), ("'.*?'", String), ('".*?"', String), ('<(\\.\\./)*([\\w/]+|[\\w/]+\\.\\w+[\\w:]*)>', Name.Namespace), ('@.*?@', String.Interpol), ('\\(.*"[.\\\\n]*".*\\)', String.Doc), ('\\A#usda .+$', Comment.Hashbang), ('\\s+', Whitespace), ('\\w+', Text), ('[_:.]+', Punctuation)]}


