"""
    pygments.lexers.xorg
    ~~~~~~~~~~~~~~~~~~~~

    Lexers for Xorg configs.

    :copyright: Copyright 2006-present by the Pygments team, see AUTHORS.
    :license: BSD, see LICENSE for details.
"""

from pygments.lexer import RegexLexer, bygroups
from pygments.token import Comment, String, Name, Text
__all__ = ['XorgLexer']


class XorgLexer(RegexLexer):
    """Lexer for xorg.conf files."""
    name = 'Xorg'
    url = 'https://www.x.org/wiki/'
    aliases = ['xorg.conf']
    filenames = ['xorg.conf']
    mimetypes = []
    version_added = ''
    tokens = {'root': [('\\s+', Text), ('#.*$', Comment), ('((?:Sub)?Section)(\\s+)("\\w+")', bygroups(String.Escape, Text, String.Escape)), ('(End(?:Sub)?Section)', String.Escape), ('(\\w+)(\\s+)([^\\n#]+)', bygroups(Name.Builtin, Text, Name.Constant))]}


