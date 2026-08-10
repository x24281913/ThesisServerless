"""
    pygments.lexers.clean
    ~~~~~~~~~~~~~~~~~~~~~

    Lexer for the Clean language.

    :copyright: Copyright 2006-present by the Pygments team, see AUTHORS.
    :license: BSD, see LICENSE for details.
"""

from pygments.lexer import ExtendedRegexLexer, words, default, include, bygroups
from pygments.token import Comment, Error, Keyword, Literal, Name, Number, Operator, Punctuation, String, Whitespace
__all__ = ['CleanLexer']


class CleanLexer(ExtendedRegexLexer):
    """
    Lexer for the general purpose, state-of-the-art, pure and lazy functional
    programming language Clean.

    .. versionadded: 2.2
    """
    name = 'Clean'
    url = 'http://clean.cs.ru.nl/Clean'
    aliases = ['clean']
    filenames = ['*.icl', '*.dcl']
    version_added = ''
    keywords = ('case', 'ccall', 'class', 'code', 'code inline', 'derive', 'export', 'foreign', 'generic', 'if', 'in', 'infix', 'infixl', 'infixr', 'instance', 'let', 'of', 'otherwise', 'special', 'stdcall', 'where', 'with')
    modulewords = ('implementation', 'definition', 'system')
    lowerId = '[a-z`][\\w`]*'
    upperId = '[A-Z`][\\w`]*'
    funnyId = '[~@#$%\\^?!+\\-*<>\\\\/|&=:]+'
    scoreUpperId = '_' + upperId
    scoreLowerId = '_' + lowerId
    moduleId = '[a-zA-Z_][a-zA-Z0-9_.`]+'
    classId = '|'.join([lowerId, upperId, funnyId])
    tokens = {'root': [include('comments'), include('keywords'), include('module'), include('import'), include('whitespace'), include('literals'), include('operators'), include('delimiters'), include('names')], 'whitespace': [('\\s+', Whitespace)], 'comments': [('//.*\\n', Comment.Single), ('/\\*', Comment.Multiline, 'comments.in'), ('/\\*\\*', Comment.Special, 'comments.in')], 'comments.in': [('\\*\\/', Comment.Multiline, '#pop'), ('/\\*', Comment.Multiline, '#push'), ('[^*/]+', Comment.Multiline), ('\\*(?!/)', Comment.Multiline), ('/', Comment.Multiline)], 'keywords': [(words(keywords, prefix='\\b', suffix='\\b'), Keyword)], 'module': [(words(modulewords, prefix='\\b', suffix='\\b'), Keyword.Namespace), ('\\bmodule\\b', Keyword.Namespace, 'module.name')], 'module.name': [include('whitespace'), (moduleId, Name.Class, '#pop')], 'import': [('\\b(import)\\b(\\s*)', bygroups(Keyword, Whitespace), 'import.module'), ('\\b(from)\\b(\\s*)\\b(' + moduleId + ')\\b(\\s*)\\b(import)\\b', bygroups(Keyword, Whitespace, Name.Class, Whitespace, Keyword), 'import.what')], 'import.module': [('\\b(qualified)\\b(\\s*)', bygroups(Keyword, Whitespace)), ('(\\s*)\\b(as)\\b', bygroups(Whitespace, Keyword), ('#pop', 'import.module.as')), (moduleId, Name.Class), ('(\\s*)(,)(\\s*)', bygroups(Whitespace, Punctuation, Whitespace)), ('\\s+', Whitespace), default('#pop')], 'import.module.as': [include('whitespace'), (lowerId, Name.Class, '#pop'), (upperId, Name.Class, '#pop')], 'import.what': [('\\b(class)\\b(\\s+)(' + classId + ')', bygroups(Keyword, Whitespace, Name.Class), 'import.what.class'), ('\\b(instance)(\\s+)(' + classId + ')(\\s+)', bygroups(Keyword, Whitespace, Name.Class, Whitespace), 'import.what.instance'), ('(::)(\\s*)\\b(' + upperId + ')\\b', bygroups(Punctuation, Whitespace, Name.Class), 'import.what.type'), ('\\b(generic)\\b(\\s+)\\b(' + lowerId + '|' + upperId + ')\\b', bygroups(Keyword, Whitespace, Name)), include('names'), ('(,)(\\s+)', bygroups(Punctuation, Whitespace)), ('$', Whitespace, '#pop'), include('whitespace')], 'import.what.class': [(',', Punctuation, '#pop'), ('\\(', Punctuation, 'import.what.class.members'), ('$', Whitespace, '#pop:2'), include('whitespace')], 'import.what.class.members': [(',', Punctuation), ('\\.\\.', Punctuation), ('\\)', Punctuation, '#pop'), include('names')], 'import.what.instance': [('[,)]', Punctuation, '#pop'), ('\\(', Punctuation, 'import.what.instance'), ('$', Whitespace, '#pop:2'), include('whitespace'), include('names')], 'import.what.type': [(',', Punctuation, '#pop'), ('[({]', Punctuation, 'import.what.type.consesandfields'), ('$', Whitespace, '#pop:2'), include('whitespace')], 'import.what.type.consesandfields': [(',', Punctuation), ('\\.\\.', Punctuation), ('[)}]', Punctuation, '#pop'), include('names')], 'literals': [("\\'([^\\'\\\\]|\\\\(x[\\da-fA-F]+|\\d+|.))\\'", Literal.Char), ('[+~-]?0[0-7]+\\b', Number.Oct), ('[+~-]?\\d+\\.\\d+(E[+-]?\\d+)?', Number.Float), ('[+~-]?\\d+\\b', Number.Integer), ('[+~-]?0x[\\da-fA-F]+\\b', Number.Hex), ('True|False', Literal), ('"', String.Double, 'literals.stringd')], 'literals.stringd': [('[^\\\\"\\n]+', String.Double), ('"', String.Double, '#pop'), ('\\\\.', String.Double), ('[$\\n]', Error, '#pop')], 'operators': [('[-~@#$%\\^?!+*<>\\\\/|&=:.]+', Operator), ('\\b_+\\b', Operator)], 'delimiters': [('[,;(){}\\[\\]]', Punctuation), ("(\\')([\\w`.]+)(\\')", bygroups(Punctuation, Name.Class, Punctuation))], 'names': [(lowerId, Name), (scoreLowerId, Name), (funnyId, Name.Function), (upperId, Name.Class), (scoreUpperId, Name.Class)]}


