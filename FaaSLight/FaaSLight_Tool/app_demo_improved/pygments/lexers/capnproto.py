"""
    pygments.lexers.capnproto
    ~~~~~~~~~~~~~~~~~~~~~~~~~

    Lexers for the Cap'n Proto schema language.

    :copyright: Copyright 2006-present by the Pygments team, see AUTHORS.
    :license: BSD, see LICENSE for details.
"""

from pygments.lexer import RegexLexer, default
from pygments.token import Text, Comment, Keyword, Name, Literal, Whitespace
__all__ = ['CapnProtoLexer']


class CapnProtoLexer(RegexLexer):
    """
    For Cap'n Proto source.
    """
    name = "Cap'n Proto"
    url = 'https://capnproto.org'
    filenames = ['*.capnp']
    aliases = ['capnp']
    version_added = '2.2'
    tokens = {'root': [('#.*?$', Comment.Single), ('@[0-9a-zA-Z]*', Name.Decorator), ('=', Literal, 'expression'), (':', Name.Class, 'type'), ('\\$', Name.Attribute, 'annotation'), ('(struct|enum|interface|union|import|using|const|annotation|extends|in|of|on|as|with|from|fixed)\\b', Keyword), ('[\\w.]+', Name), ('[^#@=:$\\w\\s]+', Text), ('\\s+', Whitespace)], 'type': [('[^][=;,(){}$]+', Name.Class), ('[\\[(]', Name.Class, 'parentype'), default('#pop')], 'parentype': [('[^][;()]+', Name.Class), ('[\\[(]', Name.Class, '#push'), ('[])]', Name.Class, '#pop'), default('#pop')], 'expression': [('[^][;,(){}$]+', Literal), ('[\\[(]', Literal, 'parenexp'), default('#pop')], 'parenexp': [('[^][;()]+', Literal), ('[\\[(]', Literal, '#push'), ('[])]', Literal, '#pop'), default('#pop')], 'annotation': [('[^][;,(){}=:]+', Name.Attribute), ('[\\[(]', Name.Attribute, 'annexp'), default('#pop')], 'annexp': [('[^][;()]+', Name.Attribute), ('[\\[(]', Name.Attribute, '#push'), ('[])]', Name.Attribute, '#pop'), default('#pop')]}


