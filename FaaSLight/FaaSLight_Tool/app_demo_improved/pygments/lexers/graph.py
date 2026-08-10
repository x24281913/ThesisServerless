"""
    pygments.lexers.graph
    ~~~~~~~~~~~~~~~~~~~~~

    Lexers for graph query languages.

    :copyright: Copyright 2006-present by the Pygments team, see AUTHORS.
    :license: BSD, see LICENSE for details.
"""

import re
from pygments.lexer import RegexLexer, include, bygroups, using, this, words
from pygments.token import Keyword, Punctuation, Comment, Operator, Name, String, Number, Whitespace
__all__ = ['CypherLexer']


class CypherLexer(RegexLexer):
    """
    For Cypher Query Language

    For the Cypher version in Neo4j 3.3
    """
    name = 'Cypher'
    url = 'https://neo4j.com/docs/developer-manual/3.3/cypher/'
    aliases = ['cypher']
    filenames = ['*.cyp', '*.cypher']
    version_added = '2.0'
    flags = re.MULTILINE | re.IGNORECASE
    tokens = {'root': [include('clauses'), include('keywords'), include('relations'), include('strings'), include('whitespace'), include('barewords'), include('comment')], 'keywords': [('(create|order|match|limit|set|skip|start|return|with|where|delete|foreach|not|by|true|false)\\b', Keyword)], 'clauses': [('(create)(\\s+)(index|unique)\\b', bygroups(Keyword, Whitespace, Keyword)), ('(drop)(\\s+)(contraint|index)(\\s+)(on)\\b', bygroups(Keyword, Whitespace, Keyword, Whitespace, Keyword)), ('(ends)(\\s+)(with)\\b', bygroups(Keyword, Whitespace, Keyword)), ('(is)(\\s+)(node)(\\s+)(key)\\b', bygroups(Keyword, Whitespace, Keyword, Whitespace, Keyword)), ('(is)(\\s+)(null|unique)\\b', bygroups(Keyword, Whitespace, Keyword)), ('(load)(\\s+)(csv)(\\s+)(from)\\b', bygroups(Keyword, Whitespace, Keyword, Whitespace, Keyword)), ('(on)(\\s+)(match|create)\\b', bygroups(Keyword, Whitespace, Keyword)), ('(optional)(\\s+)(match)\\b', bygroups(Keyword, Whitespace, Keyword)), ('(order)(\\s+)(by)\\b', bygroups(Keyword, Whitespace, Keyword)), ('(starts)(\\s+)(with)\\b', bygroups(Keyword, Whitespace, Keyword)), ('(union)(\\s+)(all)\\b', bygroups(Keyword, Whitespace, Keyword)), ('(using)(\\s+)(periodic)(\\s+)(commit)\\b', bygroups(Keyword, Whitespace, Keyword, Whitespace, Keyword)), ('(using)(\\s+)(index)\\b', bygroups(Keyword, Whitespace, Keyword)), ('(using)(\\s+)(range|text|point)(\\s+)(index)\\b', bygroups(Keyword, Whitespace, Name, Whitespace, Keyword)), (words(('all', 'any', 'as', 'asc', 'ascending', 'assert', 'call', 'case', 'create', 'delete', 'desc', 'descending', 'distinct', 'end', 'fieldterminator', 'foreach', 'in', 'limit', 'match', 'merge', 'none', 'not', 'null', 'remove', 'return', 'set', 'skip', 'single', 'start', 'then', 'union', 'unwind', 'yield', 'where', 'when', 'with', 'collect'), suffix='\\b'), Keyword)], 'relations': [('(-\\[)(.*?)(\\]->)', bygroups(Operator, using(this), Operator)), ('(<-\\[)(.*?)(\\]-)', bygroups(Operator, using(this), Operator)), ('(-\\[)(.*?)(\\]-)', bygroups(Operator, using(this), Operator)), ('-->|<--|\\[|\\]', Operator), ('<|>|<>|=|<=|=>|\\(|\\)|\\||:|,|;', Punctuation), ('[.*{}]', Punctuation)], 'strings': [('([\\\'"])(?:\\\\[tbnrf\\\'"\\\\]|[^\\\\])*?\\1', String), ('`(?:``|[^`])+`', Name.Variable)], 'whitespace': [('\\s+', Whitespace)], 'barewords': [('[a-z]\\w*', Name), ('\\d+', Number)], 'comment': [('//.*$', Comment.Single)]}


