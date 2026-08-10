"""
    pygments.lexers.trafficscript
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    Lexer for RiverBed's TrafficScript (RTS) language.

    :copyright: Copyright 2006-present by the Pygments team, see AUTHORS.
    :license: BSD, see LICENSE for details.
"""

from pygments.lexer import RegexLexer
from pygments.token import String, Number, Name, Keyword, Operator, Text, Comment
__all__ = ['RtsLexer']


class RtsLexer(RegexLexer):
    """
    For Riverbed Stingray Traffic Manager
    """
    name = 'TrafficScript'
    aliases = ['trafficscript', 'rts']
    filenames = ['*.rts']
    url = 'https://riverbed.com'
    version_added = '2.1'
    tokens = {'root': [("'(\\\\\\\\|\\\\[^\\\\]|[^'\\\\])*'", String), ('"', String, 'escapable-string'), ('(0x[0-9a-fA-F]+|\\d+)', Number), ('\\d+\\.\\d+', Number.Float), ('\\$[a-zA-Z](\\w|_)*', Name.Variable), ('(if|else|for(each)?|in|while|do|break|sub|return|import)', Keyword), ('[a-zA-Z][\\w.]*', Name.Function), ('[-+*/%=,;(){}<>^.!~|&\\[\\]\\?\\:]', Operator), ('(>=|<=|==|!=|&&|\\|\\||\\+=|.=|-=|\\*=|/=|%=|<<=|>>=|&=|\\|=|\\^=|>>|<<|\\+\\+|--|=>)', Operator), ('[ \\t\\r]+', Text), ('#[^\\n]*', Comment)], 'escapable-string': [('\\\\[tsn]', String.Escape), ('[^"]', String), ('"', String, '#pop')]}


