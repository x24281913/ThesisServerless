"""
    pygments.lexers.sieve
    ~~~~~~~~~~~~~~~~~~~~~

    Lexer for Sieve file format.

    https://tools.ietf.org/html/rfc5228
    https://tools.ietf.org/html/rfc5173
    https://tools.ietf.org/html/rfc5229
    https://tools.ietf.org/html/rfc5230
    https://tools.ietf.org/html/rfc5232
    https://tools.ietf.org/html/rfc5235
    https://tools.ietf.org/html/rfc5429
    https://tools.ietf.org/html/rfc8580

    :copyright: Copyright 2006-present by the Pygments team, see AUTHORS.
    :license: BSD, see LICENSE for details.
"""

from pygments.lexer import RegexLexer, bygroups
from pygments.token import Comment, Name, Literal, String, Text, Punctuation, Keyword
__all__ = ['SieveLexer']


class SieveLexer(RegexLexer):
    """
    Lexer for sieve format.
    """
    name = 'Sieve'
    filenames = ['*.siv', '*.sieve']
    aliases = ['sieve']
    url = 'https://en.wikipedia.org/wiki/Sieve_(mail_filtering_language)'
    version_added = '2.6'
    tokens = {'root': [('\\s+', Text), ('[();,{}\\[\\]]', Punctuation), ('(?i)require', Keyword.Namespace), ('(?i)(:)(addresses|all|contains|content|create|copy|comparator|count|days|detail|domain|fcc|flags|from|handle|importance|is|localpart|length|lowerfirst|lower|matches|message|mime|options|over|percent|quotewildcard|raw|regex|specialuse|subject|text|under|upperfirst|upper|value)', bygroups(Name.Tag, Name.Tag)), ('(?i)(address|addflag|allof|anyof|body|discard|elsif|else|envelope|ereject|exists|false|fileinto|if|hasflag|header|keep|notify_method_capability|notify|not|redirect|reject|removeflag|setflag|size|spamtest|stop|string|true|vacation|virustest)', Name.Builtin), ('(?i)set', Keyword.Declaration), ('([0-9.]+)([kmgKMG])?', bygroups(Literal.Number, Literal.Number)), ('#.*$', Comment.Single), ('/\\*.*\\*/', Comment.Multiline), ('"[^"]*?"', String), ('text:', Name.Tag, 'text')], 'text': [('[^.].*?\\n', String), ('^\\.', Punctuation, '#pop')]}


