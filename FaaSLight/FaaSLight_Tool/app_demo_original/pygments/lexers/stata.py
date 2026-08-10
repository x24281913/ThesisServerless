"""
    pygments.lexers.stata
    ~~~~~~~~~~~~~~~~~~~~~

    Lexer for Stata

    :copyright: Copyright 2006-present by the Pygments team, see AUTHORS.
    :license: BSD, see LICENSE for details.
"""

import re
from pygments.lexer import RegexLexer, default, include, words
from pygments.token import Comment, Keyword, Name, Number, String, Text, Operator
from pygments.lexers._stata_builtins import builtins_base, builtins_functions
__all__ = ['StataLexer']


class StataLexer(RegexLexer):
    """
    For Stata do files.
    """
    name = 'Stata'
    url = 'http://www.stata.com/'
    version_added = '2.2'
    aliases = ['stata', 'do']
    filenames = ['*.do', '*.ado']
    mimetypes = ['text/x-stata', 'text/stata', 'application/x-stata']
    flags = re.MULTILINE | re.DOTALL
    tokens = {'root': [include('comments'), include('strings'), include('macros'), include('numbers'), include('keywords'), include('operators'), include('format'), ('.', Text)], 'comments': [('(^//|(?<=\\s)//)(?!/)', Comment.Single, 'comments-double-slash'), ('^\\s*\\*', Comment.Single, 'comments-star'), ('/\\*', Comment.Multiline, 'comments-block'), ('(^///|(?<=\\s)///)', Comment.Special, 'comments-triple-slash')], 'comments-block': [('/\\*', Comment.Multiline, '#push'), ('\\*/\\*', Comment.Multiline), ('(\\*/\\s+\\*(?!/)[^\\n]*)|(\\*/)', Comment.Multiline, '#pop'), ('.', Comment.Multiline)], 'comments-star': [('///.*?\\n', Comment.Single, ('#pop', 'comments-triple-slash')), ('(^//|(?<=\\s)//)(?!/)', Comment.Single, ('#pop', 'comments-double-slash')), ('/\\*', Comment.Multiline, 'comments-block'), ('.(?=\\n)', Comment.Single, '#pop'), ('.', Comment.Single)], 'comments-triple-slash': [('\\n', Comment.Special, '#pop'), ('//.*?(?=\\n)', Comment.Single, '#pop'), ('.', Comment.Special)], 'comments-double-slash': [('\\n', Text, '#pop'), ('.', Comment.Single)], 'strings': [('`"', String, 'string-compound'), ('(?<!`)"', String, 'string-regular')], 'string-compound': [('`"', String, '#push'), ('"\\\'', String, '#pop'), ('\\\\\\\\|\\\\"|\\\\\\$|\\\\`|\\\\\\n', String.Escape), include('macros'), ('.', String)], 'string-regular': [('(")(?!\\\')|(?=\\n)', String, '#pop'), ('\\\\\\\\|\\\\"|\\\\\\$|\\\\`|\\\\\\n', String.Escape), include('macros'), ('.', String)], 'macros': [('\\$(\\{|(?=[$`]))', Name.Variable.Global, 'macro-global-nested'), ('\\$', Name.Variable.Global, 'macro-global-name'), ('`', Name.Variable, 'macro-local')], 'macro-local': [('`', Name.Variable, '#push'), ("'", Name.Variable, '#pop'), ('\\$(\\{|(?=[$`]))', Name.Variable.Global, 'macro-global-nested'), ('\\$', Name.Variable.Global, 'macro-global-name'), ('.', Name.Variable)], 'macro-global-nested': [('\\$(\\{|(?=[$`]))', Name.Variable.Global, '#push'), ('\\}', Name.Variable.Global, '#pop'), ('\\$', Name.Variable.Global, 'macro-global-name'), ('`', Name.Variable, 'macro-local'), ('\\w', Name.Variable.Global), default('#pop')], 'macro-global-name': [('\\$(\\{|(?=[$`]))', Name.Variable.Global, 'macro-global-nested', '#pop'), ('\\$', Name.Variable.Global, 'macro-global-name', '#pop'), ('`', Name.Variable, 'macro-local', '#pop'), ('\\w{1,32}', Name.Variable.Global, '#pop')], 'keywords': [(words(builtins_functions, prefix='\\b', suffix='(?=\\()'), Name.Function), (words(builtins_base, prefix='(^\\s*|\\s)', suffix='\\b'), Keyword)], 'operators': [('-|==|<=|>=|<|>|&|!=', Operator), ('\\*|\\+|\\^|/|!|~|==|~=', Operator)], 'numbers': [('\\b[+-]?([0-9]+(\\.[0-9]+)?|\\.[0-9]+|\\.)([eE][+-]?[0-9]+)?[i]?\\b', Number)], 'format': [('%-?\\d{1,2}(\\.\\d{1,2})?[gfe]c?', Name.Other), ('%(21x|16H|16L|8H|8L)', Name.Other), ('%-?(tc|tC|td|tw|tm|tq|th|ty|tg)\\S{0,32}', Name.Other), ('%[-~]?\\d{1,4}s', Name.Other)]}


