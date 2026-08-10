"""
    pygments.lexers.jmespath
    ~~~~~~~~~~~~~~~~~~~~~~~~

    Lexers for the JMESPath language

    :copyright: Copyright 2006-present by the Pygments team, see AUTHORS.
    :license: BSD, see LICENSE for details.
"""

from pygments.lexer import RegexLexer, bygroups, include
from pygments.token import String, Punctuation, Whitespace, Name, Operator, Number, Literal, Keyword
__all__ = ['JMESPathLexer']


class JMESPathLexer(RegexLexer):
    """
    For JMESPath queries.
    """
    name = 'JMESPath'
    url = 'https://jmespath.org'
    filenames = ['*.jp']
    aliases = ['jmespath', 'jp']
    version_added = ''
    tokens = {'string': [("'(\\\\(.|\\n)|[^'\\\\])*'", String)], 'punctuation': [('(\\[\\?|[\\.\\*\\[\\],:\\(\\)\\{\\}\\|])', Punctuation)], 'ws': [(' |\\t|\\n|\\r', Whitespace)], 'dq-identifier': [('[^\\\\"]+', Name.Variable), ('\\\\"', Name.Variable), ('.', Punctuation, '#pop')], 'identifier': [('(&)?(")', bygroups(Name.Variable, Punctuation), 'dq-identifier'), ('(")?(&?[A-Za-z][A-Za-z0-9_-]*)(")?', bygroups(Punctuation, Name.Variable, Punctuation))], 'root': [include('ws'), include('string'), ('(==|!=|<=|>=|<|>|&&|\\|\\||!)', Operator), include('punctuation'), ('@', Name.Variable.Global), ('(&?[A-Za-z][A-Za-z0-9_]*)(\\()', bygroups(Name.Function, Punctuation)), ('(&)(\\()', bygroups(Name.Variable, Punctuation)), include('identifier'), ('-?\\d+', Number), ('`', Literal, 'literal')], 'literal': [include('ws'), include('string'), include('punctuation'), ('(false|true|null)\\b', Keyword.Constant), include('identifier'), ('-?\\d+\\.?\\d*([eE][-+]\\d+)?', Number), ('\\\\`', Literal), ('`', Literal, '#pop')]}


