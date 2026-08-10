"""
    pygments.lexers.jsx
    ~~~~~~~~~~~~~~~~~~~

    Lexers for JSX (React) and TSX (TypeScript flavor).

    :copyright: Copyright 2006-present by the Pygments team, see AUTHORS.
    :license: BSD, see LICENSE for details.
"""

import re
from pygments.lexer import bygroups, default, include, inherit
from pygments.lexers.javascript import JavascriptLexer, TypeScriptLexer
from pygments.token import Name, Operator, Punctuation, String, Text, Whitespace
__all__ = ['JsxLexer', 'TsxLexer']
_JSX_RULES = {'jsx': [('</?>', Punctuation), ('(<)(\\w+)(\\.?)', bygroups(Punctuation, Name.Tag, Punctuation), 'tag'), ('(</)(\\w+)(>)', bygroups(Punctuation, Name.Tag, Punctuation)), ('(</)(\\w+)', bygroups(Punctuation, Name.Tag), 'fragment')], 'tag': [('\\s+', Whitespace), ('([\\w-]+)(\\s*)(=)(\\s*)', bygroups(Name.Attribute, Whitespace, Operator, Whitespace), 'attr'), ('[{}]+', Punctuation), ('[\\w\\.]+', Name.Attribute), ('(/?)(\\s*)(>)', bygroups(Punctuation, Text, Punctuation), '#pop')], 'fragment': [('(.)(\\w+)', bygroups(Punctuation, Name.Attribute)), ('(>)', bygroups(Punctuation), '#pop')], 'attr': [('\\{', Punctuation, 'expression'), ('".*?"', String, '#pop'), ("'.*?'", String, '#pop'), default('#pop')], 'expression': [('\\{', Punctuation, '#push'), ('\\}', Punctuation, '#pop'), include('root')]}


class JsxLexer(JavascriptLexer):
    """For JavaScript Syntax Extension (JSX).
    """
    name = 'JSX'
    aliases = ['jsx', 'react']
    filenames = ['*.jsx', '*.react']
    mimetypes = ['text/jsx', 'text/typescript-jsx']
    url = 'https://facebook.github.io/jsx/'
    version_added = '2.17'
    flags = re.MULTILINE | re.DOTALL
    tokens = {'root': [include('jsx'), inherit], **_JSX_RULES}



class TsxLexer(TypeScriptLexer):
    """For TypeScript with embedded JSX
    """
    name = 'TSX'
    aliases = ['tsx']
    filenames = ['*.tsx']
    mimetypes = ['text/typescript-tsx']
    url = 'https://www.typescriptlang.org/docs/handbook/jsx.html'
    version_added = '2.19'
    flags = re.MULTILINE | re.DOTALL
    tokens = {'root': [include('jsx'), inherit], **_JSX_RULES}


