"""
    pygments.lexers.ambient
    ~~~~~~~~~~~~~~~~~~~~~~~

    Lexers for AmbientTalk language.

    :copyright: Copyright 2006-present by the Pygments team, see AUTHORS.
    :license: BSD, see LICENSE for details.
"""

import re
from pygments.lexer import RegexLexer, include, words, bygroups
from pygments.token import Comment, Operator, Keyword, Name, String, Number, Punctuation, Whitespace
__all__ = ['AmbientTalkLexer']


class AmbientTalkLexer(RegexLexer):
    """
    Lexer for AmbientTalk source code.
    """
    name = 'AmbientTalk'
    url = 'https://code.google.com/p/ambienttalk'
    filenames = ['*.at']
    aliases = ['ambienttalk', 'ambienttalk/2', 'at']
    mimetypes = ['text/x-ambienttalk']
    version_added = '2.0'
    flags = re.MULTILINE | re.DOTALL
    builtin = words(('if:', 'then:', 'else:', 'when:', 'whenever:', 'discovered:', 'disconnected:', 'reconnected:', 'takenOffline:', 'becomes:', 'export:', 'as:', 'object:', 'actor:', 'mirror:', 'taggedAs:', 'mirroredBy:', 'is:'))
    tokens = {'root': [('\\s+', Whitespace), ('//.*?\\n', Comment.Single), ('/\\*.*?\\*/', Comment.Multiline), ('(def|deftype|import|alias|exclude)\\b', Keyword), (builtin, Name.Builtin), ('(true|false|nil)\\b', Keyword.Constant), ('(~|lobby|jlobby|/)\\.', Keyword.Constant, 'namespace'), ('"(\\\\\\\\|\\\\[^\\\\]|[^"\\\\])*"', String), ('\\|', Punctuation, 'arglist'), ('<:|[*^!%&<>+=,./?-]|:=', Operator), ('`[a-zA-Z_]\\w*', String.Symbol), ('[a-zA-Z_]\\w*:', Name.Function), ('[{}()\\[\\];`]', Punctuation), ('(self|super)\\b', Name.Variable.Instance), ('[a-zA-Z_]\\w*', Name.Variable), ('@[a-zA-Z_]\\w*', Name.Class), ('@\\[', Name.Class, 'annotations'), include('numbers')], 'numbers': [('(\\d+\\.\\d*|\\d*\\.\\d+)([eE][+-]?[0-9]+)?', Number.Float), ('\\d+', Number.Integer)], 'namespace': [('[a-zA-Z_]\\w*\\.', Name.Namespace), ('[a-zA-Z_]\\w*:', Name.Function, '#pop'), ('[a-zA-Z_]\\w*(?!\\.)', Name.Function, '#pop')], 'annotations': [('(.*?)\\]', Name.Class, '#pop')], 'arglist': [('\\|', Punctuation, '#pop'), ('(\\s*)(,)(\\s*)', bygroups(Whitespace, Punctuation, Whitespace)), ('[a-zA-Z_]\\w*', Name.Variable)]}


