"""
    pygments.lexers.elm
    ~~~~~~~~~~~~~~~~~~~

    Lexer for the Elm programming language.

    :copyright: Copyright 2006-present by the Pygments team, see AUTHORS.
    :license: BSD, see LICENSE for details.
"""

from pygments.lexer import RegexLexer, words, include, bygroups
from pygments.token import Comment, Keyword, Name, Number, Punctuation, String, Whitespace
__all__ = ['ElmLexer']


class ElmLexer(RegexLexer):
    """
    For Elm source code.
    """
    name = 'Elm'
    url = 'https://elm-lang.org/'
    aliases = ['elm']
    filenames = ['*.elm']
    mimetypes = ['text/x-elm']
    version_added = '2.1'
    validName = "[a-z_][a-zA-Z0-9_\\']*"
    specialName = '^main '
    builtinOps = ('~', '||', '|>', '|', '`', '^', '\\', "'", '>>', '>=', '>', '==', '=', '<~', '<|', '<=', '<<', '<-', '<', '::', ':', '/=', '//', '/', '..', '.', '->', '-', '++', '+', '*', '&&', '%')
    reservedWords = words(('alias', 'as', 'case', 'else', 'if', 'import', 'in', 'let', 'module', 'of', 'port', 'then', 'type', 'where'), suffix='\\b')
    tokens = {'root': [('\\{-', Comment.Multiline, 'comment'), ('--.*', Comment.Single), ('\\s+', Whitespace), ('"', String, 'doublequote'), ('^(\\s*)(module)(\\s*)', bygroups(Whitespace, Keyword.Namespace, Whitespace), 'imports'), ('^(\\s*)(import)(\\s*)', bygroups(Whitespace, Keyword.Namespace, Whitespace), 'imports'), ('\\[glsl\\|.*', Name.Entity, 'shader'), (reservedWords, Keyword.Reserved), ('[A-Z][a-zA-Z0-9_]*', Keyword.Type), (specialName, Keyword.Reserved), (words(builtinOps, prefix='\\(', suffix='\\)'), Name.Function), (words(builtinOps), Name.Function), include('numbers'), (validName, Name.Variable), ('[,()\\[\\]{}]', Punctuation)], 'comment': [('-(?!\\})', Comment.Multiline), ('\\{-', Comment.Multiline, 'comment'), ('[^-}]', Comment.Multiline), ('-\\}', Comment.Multiline, '#pop')], 'doublequote': [('\\\\u[0-9a-fA-F]{4}', String.Escape), ('\\\\[nrfvb\\\\"]', String.Escape), ('[^"]', String), ('"', String, '#pop')], 'imports': [('\\w+(\\.\\w+)*', Name.Class, '#pop')], 'numbers': [('_?\\d+\\.(?=\\d+)', Number.Float), ('_?\\d+', Number.Integer)], 'shader': [('\\|(?!\\])', Name.Entity), ('\\|\\]', Name.Entity, '#pop'), ('(.*)(\\n)', bygroups(Name.Entity, Whitespace))]}


