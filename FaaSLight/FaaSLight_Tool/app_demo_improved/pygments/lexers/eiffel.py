"""
    pygments.lexers.eiffel
    ~~~~~~~~~~~~~~~~~~~~~~

    Lexer for the Eiffel language.

    :copyright: Copyright 2006-present by the Pygments team, see AUTHORS.
    :license: BSD, see LICENSE for details.
"""

from pygments.lexer import RegexLexer, include, words, bygroups
from pygments.token import Comment, Operator, Keyword, Name, String, Number, Punctuation, Whitespace
__all__ = ['EiffelLexer']


class EiffelLexer(RegexLexer):
    """
    For Eiffel source code.
    """
    name = 'Eiffel'
    url = 'https://www.eiffel.com'
    aliases = ['eiffel']
    filenames = ['*.e']
    mimetypes = ['text/x-eiffel']
    version_added = '2.0'
    tokens = {'root': [('[^\\S\\n]+', Whitespace), ('--.*?$', Comment.Single), ('[^\\S\\n]+', Whitespace), ('(?i)(true|false|void|current|result|precursor)\\b', Keyword.Constant), ('(?i)(not|xor|implies|or)\\b', Operator.Word), ('(?i)(and)(?:(\\s+)(then))?\\b', bygroups(Operator.Word, Whitespace, Operator.Word)), ('(?i)(or)(?:(\\s+)(else))?\\b', bygroups(Operator.Word, Whitespace, Operator.Word)), (words(('across', 'agent', 'alias', 'all', 'as', 'assign', 'attached', 'attribute', 'check', 'class', 'convert', 'create', 'debug', 'deferred', 'detachable', 'do', 'else', 'elseif', 'end', 'ensure', 'expanded', 'export', 'external', 'feature', 'from', 'frozen', 'if', 'inherit', 'inspect', 'invariant', 'like', 'local', 'loop', 'none', 'note', 'obsolete', 'old', 'once', 'only', 'redefine', 'rename', 'require', 'rescue', 'retry', 'select', 'separate', 'then', 'undefine', 'until', 'variant', 'when'), prefix='(?i)\\b', suffix='\\b'), Keyword.Reserved), ('"\\[([^\\]%]|%(.|\\n)|\\][^"])*?\\]"', String), ('"([^"%\\n]|%.)*?"', String), include('numbers'), ("'([^'%]|%'|%%)'", String.Char), ('(//|\\\\\\\\|>=|<=|:=|/=|~|/~|[\\\\?!#%&@|+/\\-=>*$<^\\[\\]])', Operator), ('([{}():;,.])', Punctuation), ('([a-z]\\w*)|([A-Z][A-Z0-9_]*[a-z]\\w*)', Name), ('([A-Z][A-Z0-9_]*)', Name.Class), ('\\n+', Whitespace)], 'numbers': [('0[xX][a-fA-F0-9]+', Number.Hex), ('0[bB][01]+', Number.Bin), ('0[cC][0-7]+', Number.Oct), ('([0-9]+\\.[0-9]*)|([0-9]*\\.[0-9]+)', Number.Float), ('[0-9]+', Number.Integer)]}


