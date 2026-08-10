"""
    pygments.lexers.fantom
    ~~~~~~~~~~~~~~~~~~~~~~

    Lexer for the Fantom language.

    :copyright: Copyright 2006-present by the Pygments team, see AUTHORS.
    :license: BSD, see LICENSE for details.
"""

from string import Template
from pygments.lexer import RegexLexer, include, bygroups, using, this, default, words
from pygments.token import Text, Comment, Operator, Keyword, Name, String, Number, Punctuation, Literal, Whitespace
__all__ = ['FantomLexer']


class FantomLexer(RegexLexer):
    """
    For Fantom source code.
    """
    name = 'Fantom'
    aliases = ['fan']
    filenames = ['*.fan']
    mimetypes = ['application/x-fantom']
    url = 'https://www.fantom.org'
    version_added = '1.5'
    
    def s(str):
        return Template(str).substitute(dict(pod='[\\"\\w\\.]+', eos='\\n|;', id='[a-zA-Z_]\\w*', type='(?:\\[|[a-zA-Z_]|\\|)[:\\w\\[\\]|\\->?]*?'))
    tokens = {'comments': [('(?s)/\\*.*?\\*/', Comment.Multiline), ('//.*?$', Comment.Single), ('\\*\\*.*?$', Comment.Special), ('#.*$', Comment.Single)], 'literals': [('\\b-?[\\d_]+(ns|ms|sec|min|hr|day)', Number), ('\\b-?[\\d_]*\\.[\\d_]+(ns|ms|sec|min|hr|day)', Number), ('\\b-?(\\d+)?\\.\\d+(f|F|d|D)?', Number.Float), ('\\b-?0x[0-9a-fA-F_]+', Number.Hex), ('\\b-?[\\d_]+', Number.Integer), ("'\\\\.'|'[^\\\\]'|'\\\\u[0-9a-f]{4}'", String.Char), ('"', Punctuation, 'insideStr'), ('`', Punctuation, 'insideUri'), ('\\b(true|false|null)\\b', Keyword.Constant), ('(?:(\\w+)(::))?(\\w+)(<\\|)(.*?)(\\|>)', bygroups(Name.Namespace, Punctuation, Name.Class, Punctuation, String, Punctuation)), ('(?:(\\w+)(::))?(\\w+)?(#)(\\w+)?', bygroups(Name.Namespace, Punctuation, Name.Class, Punctuation, Name.Function)), ('\\[,\\]', Literal), (s('($type)(\\[,\\])'), bygroups(using(this, state='inType'), Literal)), ('\\[:\\]', Literal), (s('($type)(\\[:\\])'), bygroups(using(this, state='inType'), Literal))], 'insideStr': [('\\\\\\\\', String.Escape), ('\\\\"', String.Escape), ('\\\\`', String.Escape), ('\\$\\w+', String.Interpol), ('\\$\\{.*?\\}', String.Interpol), ('"', Punctuation, '#pop'), ('.', String)], 'insideUri': [('\\\\\\\\', String.Escape), ('\\\\"', String.Escape), ('\\\\`', String.Escape), ('\\$\\w+', String.Interpol), ('\\$\\{.*?\\}', String.Interpol), ('`', Punctuation, '#pop'), ('.', String.Backtick)], 'protectionKeywords': [('\\b(public|protected|private|internal)\\b', Keyword)], 'typeKeywords': [('\\b(abstract|final|const|native|facet|enum)\\b', Keyword)], 'methodKeywords': [('\\b(abstract|native|once|override|static|virtual|final)\\b', Keyword)], 'fieldKeywords': [('\\b(abstract|const|final|native|override|static|virtual|readonly)\\b', Keyword)], 'otherKeywords': [(words(('try', 'catch', 'throw', 'finally', 'for', 'if', 'else', 'while', 'as', 'is', 'isnot', 'switch', 'case', 'default', 'continue', 'break', 'do', 'return', 'get', 'set'), prefix='\\b', suffix='\\b'), Keyword), ('\\b(it|this|super)\\b', Name.Builtin.Pseudo)], 'operators': [('\\+\\+|\\-\\-|\\+|\\-|\\*|/|\\|\\||&&|<=>|<=|<|>=|>|=|!|\\[|\\]', Operator)], 'inType': [('[\\[\\]|\\->:?]', Punctuation), (s('$id'), Name.Class), default('#pop')], 'root': [include('comments'), include('protectionKeywords'), include('typeKeywords'), include('methodKeywords'), include('fieldKeywords'), include('literals'), include('otherKeywords'), include('operators'), ('using\\b', Keyword.Namespace, 'using'), ('@\\w+', Name.Decorator, 'facet'), ('(class|mixin)(\\s+)(\\w+)', bygroups(Keyword, Whitespace, Name.Class), 'inheritance'), (s('($type)([ \\t]+)($id)(\\s*)(:=)'), bygroups(using(this, state='inType'), Whitespace, Name.Variable, Whitespace, Operator)), (s('($id)(\\s*)(:=)'), bygroups(Name.Variable, Whitespace, Operator)), (s('(\\.|(?:\\->))($id)(\\s*)(\\()'), bygroups(Operator, Name.Function, Whitespace, Punctuation), 'insideParen'), (s('(\\.|(?:\\->))($id)'), bygroups(Operator, Name.Function)), ('(new)(\\s+)(make\\w*)(\\s*)(\\()', bygroups(Keyword, Whitespace, Name.Function, Whitespace, Punctuation), 'insideMethodDeclArgs'), (s('($type)([ \\t]+)($id)(\\s*)(\\()'), bygroups(using(this, state='inType'), Whitespace, Name.Function, Whitespace, Punctuation), 'insideMethodDeclArgs'), (s('($type)(\\s+)($id)(\\s*)(,)'), bygroups(using(this, state='inType'), Whitespace, Name.Variable, Whitespace, Punctuation)), (s('($type)(\\s+)($id)(\\s*)(\\->)(\\s*)($type)(\\|)'), bygroups(using(this, state='inType'), Whitespace, Name.Variable, Whitespace, Punctuation, Whitespace, using(this, state='inType'), Punctuation)), (s('($type)(\\s+)($id)(\\s*)(\\|)'), bygroups(using(this, state='inType'), Whitespace, Name.Variable, Whitespace, Punctuation)), (s('($type)([ \\t]+)($id)'), bygroups(using(this, state='inType'), Whitespace, Name.Variable)), ('\\(', Punctuation, 'insideParen'), ('\\{', Punctuation, 'insideBrace'), ('\\s+', Whitespace), ('.', Text)], 'insideParen': [('\\)', Punctuation, '#pop'), include('root')], 'insideMethodDeclArgs': [('\\)', Punctuation, '#pop'), (s('($type)(\\s+)($id)(\\s*)(\\))'), bygroups(using(this, state='inType'), Whitespace, Name.Variable, Whitespace, Punctuation), '#pop'), include('root')], 'insideBrace': [('\\}', Punctuation, '#pop'), include('root')], 'inheritance': [('\\s+', Whitespace), (':|,', Punctuation), ('(?:(\\w+)(::))?(\\w+)', bygroups(Name.Namespace, Punctuation, Name.Class)), ('\\{', Punctuation, '#pop')], 'using': [('[ \\t]+', Whitespace), ('(\\[)(\\w+)(\\])', bygroups(Punctuation, Comment.Special, Punctuation)), ('(\\")?([\\w.]+)(\\")?', bygroups(Punctuation, Name.Namespace, Punctuation)), ('::', Punctuation, 'usingClass'), default('#pop')], 'usingClass': [('[ \\t]+', Whitespace), ('(as)(\\s+)(\\w+)', bygroups(Keyword.Declaration, Whitespace, Name.Class), '#pop:2'), ('[\\w$]+', Name.Class), default('#pop:2')], 'facet': [('\\s+', Whitespace), ('\\{', Punctuation, 'facetFields'), default('#pop')], 'facetFields': [include('comments'), include('literals'), include('operators'), ('\\s+', Whitespace), ('(\\s*)(\\w+)(\\s*)(=)', bygroups(Whitespace, Name, Whitespace, Operator)), ('\\}', Punctuation, '#pop'), ('\\s+', Whitespace), ('.', Text)]}


