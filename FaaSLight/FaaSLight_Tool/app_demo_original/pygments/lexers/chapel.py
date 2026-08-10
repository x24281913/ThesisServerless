"""
    pygments.lexers.chapel
    ~~~~~~~~~~~~~~~~~~~~~~

    Lexer for the Chapel language.

    :copyright: Copyright 2006-present by the Pygments team, see AUTHORS.
    :license: BSD, see LICENSE for details.
"""

from pygments.lexer import RegexLexer, bygroups, words
from pygments.token import Text, Comment, Operator, Keyword, Name, String, Number, Punctuation, Whitespace
__all__ = ['ChapelLexer']


class ChapelLexer(RegexLexer):
    """
    For Chapel source.
    """
    name = 'Chapel'
    url = 'https://chapel-lang.org/'
    filenames = ['*.chpl']
    aliases = ['chapel', 'chpl']
    version_added = '2.0'
    known_types = ('bool', 'bytes', 'complex', 'imag', 'int', 'locale', 'nothing', 'opaque', 'range', 'real', 'string', 'uint', 'void')
    type_modifiers_par = ('atomic', 'single', 'sync')
    type_modifiers_mem = ('borrowed', 'owned', 'shared', 'unmanaged')
    type_modifiers = (*type_modifiers_par, *type_modifiers_mem)
    declarations = ('config', 'const', 'in', 'inout', 'out', 'param', 'ref', 'type', 'var')
    constants = ('false', 'nil', 'none', 'true')
    other_keywords = ('align', 'as', 'begin', 'break', 'by', 'catch', 'cobegin', 'coforall', 'continue', 'defer', 'delete', 'dmapped', 'do', 'domain', 'else', 'enum', 'except', 'export', 'extern', 'for', 'forall', 'foreach', 'forwarding', 'if', 'implements', 'import', 'index', 'init', 'inline', 'label', 'lambda', 'let', 'lifetime', 'local', 'new', 'noinit', 'on', 'only', 'otherwise', 'override', 'pragma', 'primitive', 'private', 'prototype', 'public', 'reduce', 'require', 'return', 'scan', 'select', 'serial', 'sparse', 'subdomain', 'then', 'this', 'throw', 'throws', 'try', 'use', 'when', 'where', 'while', 'with', 'yield', 'zip')
    tokens = {'root': [('\\n', Whitespace), ('\\s+', Whitespace), ('\\\\\\n', Text), ('//(.*?)\\n', Comment.Single), ('/(\\\\\\n)?[*](.|\\n)*?[*](\\\\\\n)?/', Comment.Multiline), (words(declarations, suffix='\\b'), Keyword.Declaration), (words(constants, suffix='\\b'), Keyword.Constant), (words(known_types, suffix='\\b'), Keyword.Type), (words((*type_modifiers, *other_keywords), suffix='\\b'), Keyword), ('@', Keyword, 'attributename'), ('(iter)(\\s+)', bygroups(Keyword, Whitespace), 'procname'), ('(proc)(\\s+)', bygroups(Keyword, Whitespace), 'procname'), ('(operator)(\\s+)', bygroups(Keyword, Whitespace), 'procname'), ('(class|interface|module|record|union)(\\s+)', bygroups(Keyword, Whitespace), 'classname'), ('\\d+i', Number), ('\\d+\\.\\d*([Ee][-+]\\d+)?i', Number), ('\\.\\d+([Ee][-+]\\d+)?i', Number), ('\\d+[Ee][-+]\\d+i', Number), ('(\\d*\\.\\d+)([eE][+-]?[0-9]+)?i?', Number.Float), ('\\d+[eE][+-]?[0-9]+i?', Number.Float), ('0[bB][01]+', Number.Bin), ('0[xX][0-9a-fA-F]+', Number.Hex), ('0[oO][0-7]+', Number.Oct), ('[0-9]+', Number.Integer), ('"(\\\\\\\\|\\\\"|[^"])*"', String), ("'(\\\\\\\\|\\\\'|[^'])*'", String), ('(=|\\+=|-=|\\*=|/=|\\*\\*=|%=|&=|\\|=|\\^=|&&=|\\|\\|=|<<=|>>=|<=>|<~>|\\.\\.|by|#|\\.\\.\\.|&&|\\|\\||!|&|\\||\\^|~|<<|>>|==|!=|<=|>=|<|>|[+\\-*/%]|\\*\\*)', Operator), ('[:;,.?()\\[\\]{}]', Punctuation), ('[a-zA-Z_][\\w$]*', Name.Other)], 'classname': [('[a-zA-Z_][\\w$]*', Name.Class, '#pop')], 'procname': [('([a-zA-Z_][.\\w$]*|\\~[a-zA-Z_][.\\w$]*|[+*/!~%<>=&^|\\-:]{1,2})', Name.Function, '#pop'), ('\\(', Punctuation, 'receivertype'), ('\\)+\\.', Punctuation)], 'receivertype': [(words(type_modifiers, suffix='\\b'), Keyword), (words(known_types, suffix='\\b'), Keyword.Type), ('[^()]*', Name.Other, '#pop')], 'attributename': [('[a-zA-Z_][.\\w$]*', Name.Decorator, '#pop')]}


