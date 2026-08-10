"""
    pygments.lexers.soong
    ~~~~~~~~~~~~~~~~~~~~~

    Lexers for Soong (Android.bp Blueprint) files.

    :copyright: Copyright 2006-present by the Pygments team, see AUTHORS.
    :license: BSD, see LICENSE for details.
"""

from pygments.lexer import RegexLexer, bygroups, include
from pygments.token import Comment, Name, Number, Operator, Punctuation, String, Whitespace
__all__ = ['SoongLexer']


class SoongLexer(RegexLexer):
    name = 'Soong'
    version_added = '2.18'
    url = 'https://source.android.com/docs/setup/reference/androidbp'
    aliases = ['androidbp', 'bp', 'soong']
    filenames = ['Android.bp']
    tokens = {'root': [('(\\w*)(\\s*)(\\+?=)(\\s*)', bygroups(Name.Variable, Whitespace, Operator, Whitespace), 'assign-rhs'), ('(\\w*)(\\s*)(\\{)', bygroups(Name.Function, Whitespace, Punctuation), 'in-rule'), include('comments'), ('\\s+', Whitespace)], 'assign-rhs': [include('expr'), ('\\n', Whitespace, '#pop')], 'in-list': [include('expr'), include('comments'), ('\\s+', Whitespace), (',', Punctuation), ('\\]', Punctuation, '#pop')], 'in-map': [('(\\w+)(:)(\\s*)', bygroups(Name, Punctuation, Whitespace)), include('expr'), include('comments'), ('\\s+', Whitespace), (',', Punctuation), ('\\}', Punctuation, '#pop')], 'in-rule': [include('in-map')], 'comments': [('//.*', Comment.Single), ('/(\\\\\\n)?[*](.|\\n)*?[*](\\\\\\n)?/', Comment.Multiline)], 'expr': [('(true|false)\\b', Name.Builtin), ('0x[0-9a-fA-F]+', Number.Hex), ('\\d+', Number.Integer), ('".*?"', String), ('\\{', Punctuation, 'in-map'), ('\\[', Punctuation, 'in-list'), ('\\w+', Name)]}


