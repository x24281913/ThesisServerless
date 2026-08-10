"""
    pygments.lexers.rego
    ~~~~~~~~~~~~~~~~~~~~

    Lexers for the Rego policy languages.

    :copyright: Copyright 2006-present by the Pygments team, see AUTHORS.
    :license: BSD, see LICENSE for details.
"""

from pygments.lexer import RegexLexer, words
from pygments.token import Comment, Operator, Keyword, Name, String, Number, Punctuation, Whitespace


class RegoLexer(RegexLexer):
    """
    For Rego source.
    """
    name = 'Rego'
    url = 'https://www.openpolicyagent.org/docs/latest/policy-language/'
    filenames = ['*.rego']
    aliases = ['rego']
    mimetypes = ['text/x-rego']
    version_added = '2.19'
    reserved_words = ('as', 'contains', 'data', 'default', 'else', 'every', 'false', 'if', 'in', 'import', 'package', 'not', 'null', 'some', 'true', 'with')
    builtins = ('data', 'input')
    tokens = {'root': [('\\n', Whitespace), ('\\s+', Whitespace), ('#.*?$', Comment.Single), (words(reserved_words, suffix='\\b'), Keyword), (words(builtins, suffix='\\b'), Name.Builtin), ('[a-zA-Z_][a-zA-Z0-9_]*', Name), ('"(\\\\\\\\|\\\\"|[^"])*"', String.Double), ('`[^`]*`', String.Backtick), ('-?\\d+(\\.\\d+)?', Number), ('(==|!=|<=|>=|:=)', Operator), ('[=<>+\\-*/%&|]', Operator), ('[\\[\\]{}(),.:;]', Punctuation)]}

__all__ = ['RegoLexer']

