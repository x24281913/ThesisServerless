"""
    pygments.lexers.codeql
    ~~~~~~~~~~~~~~~~~~~~~~

    Lexer for CodeQL query language.

    The grammar is originating from:
    https://github.com/github/vscode-codeql/blob/main/syntaxes/README.md

    :copyright: Copyright 2006-present by the Pygments team, see AUTHORS.
    :license: BSD, see LICENSE for details.
"""

__all__ = ['CodeQLLexer']
import re
from pygments.lexer import RegexLexer, words
from pygments.token import Comment, Operator, Keyword, Name, String, Number, Punctuation, Whitespace


class CodeQLLexer(RegexLexer):
    name = 'CodeQL'
    aliases = ['codeql', 'ql']
    filenames = ['*.ql', '*.qll']
    mimetypes = []
    url = 'https://github.com/github/codeql'
    version_added = '2.19'
    flags = re.MULTILINE | re.UNICODE
    tokens = {'root': [('\\s+', Whitespace), ('//.*?\\n', Comment.Single), ('/\\*', Comment.Multiline, 'multiline-comments'), (words(('module', 'import', 'class', 'extends', 'implements', 'predicate', 'select', 'where', 'from', 'as', 'and', 'or', 'not', 'in', 'if', 'then', 'else', 'exists', 'forall', 'instanceof', 'private', 'predicate', 'abstract', 'cached', 'external', 'final', 'library', 'override', 'query'), suffix='\\b'), Keyword.Builtin), (words('this', prefix='\\b', suffix='\\b\\??:?'), Name.Builtin.Pseudo), (words(('boolean', 'date', 'float', 'int', 'string'), suffix='\\b'), Keyword.Type), ('"(\\\\\\\\|\\\\[^\\\\]|[^"\\\\])*"', String), ('[0-9]+\\.[0-9]+', Number.Float), ('[0-9]+', Number.Integer), ('<=|>=|<|>|=|!=|\\+|-|\\*|/', Operator), ('[.,;:\\[\\]{}()]+', Punctuation), ('@[a-zA-Z_]\\w*', Name.Variable), ('[A-Z][a-zA-Z0-9_]*', Name.Class), ('[a-z][a-zA-Z0-9_]*', Name.Variable)], 'multiline-comments': [('[^*/]+', Comment.Multiline), ('/\\*', Comment.Multiline, '#push'), ('\\*/', Comment.Multiline, '#pop'), ('[*/]', Comment.Multiline)]}


