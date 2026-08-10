"""
    pygments.lexers.dns
    ~~~~~~~~~~~~~~~~~~~

    Pygments lexers for DNS

    :copyright: Copyright 2006-present by the Pygments team, see AUTHORS.
    :license: BSD, see LICENSE for details.
"""

import re
from pygments.token import Comment, Operator, Keyword, Name, String, Number, Punctuation, Whitespace, Literal
from pygments.lexer import RegexLexer, bygroups, include
__all__ = ['DnsZoneLexer']
CLASSES = ['IN', 'CS', 'CH', 'HS']
CLASSES_RE = '(' + '|'.join(CLASSES) + ')'


class DnsZoneLexer(RegexLexer):
    """
    Lexer for DNS zone file
    """
    flags = re.MULTILINE
    name = 'Zone'
    aliases = ['zone']
    filenames = ['*.zone']
    url = 'https://datatracker.ietf.org/doc/html/rfc1035'
    mimetypes = ['text/dns']
    version_added = '2.16'
    tokens = {'root': [('([ \\t]*)(;.*)(\\n)', bygroups(Whitespace, Comment.Single, Whitespace)), ('^\\$ORIGIN\\b', Keyword, 'values'), ('^\\$TTL\\b', Keyword, 'values'), ('^\\$INCLUDE\\b', Comment.Preproc, 'include'), ('^\\$[A-Z]+\\b', Keyword, 'values'), ('^(@)([ \\t]+)(?:([0-9]+[smhdw]?)([ \\t]+))?(?:' + CLASSES_RE + '([ \t]+))?([A-Z]+)([ \t]+)', bygroups(Operator, Whitespace, Number.Integer, Whitespace, Name.Class, Whitespace, Keyword.Type, Whitespace), 'values'), ('^([^ \\t\\n]*)([ \\t]+)(?:([0-9]+[smhdw]?)([ \\t]+))?(?:' + CLASSES_RE + '([ \t]+))?([A-Z]+)([ \t]+)', bygroups(Name, Whitespace, Number.Integer, Whitespace, Name.Class, Whitespace, Keyword.Type, Whitespace), 'values'), ('^(Operator)([ \\t]+)(?:' + CLASSES_RE + '([ \t]+))?(?:([0-9]+[smhdw]?)([ \t]+))?([A-Z]+)([ \t]+)', bygroups(Name, Whitespace, Number.Integer, Whitespace, Name.Class, Whitespace, Keyword.Type, Whitespace), 'values'), ('^([^ \\t\\n]*)([ \\t]+)(?:' + CLASSES_RE + '([ \t]+))?(?:([0-9]+[smhdw]?)([ \t]+))?([A-Z]+)([ \t]+)', bygroups(Name, Whitespace, Number.Integer, Whitespace, Name.Class, Whitespace, Keyword.Type, Whitespace), 'values')], 'values': [('\\n', Whitespace, '#pop'), ('\\(', Punctuation, 'nested'), include('simple-value')], 'nested': [('\\)', Punctuation, '#pop'), include('multiple-simple-values')], 'simple-value': [('(;.*)', bygroups(Comment.Single)), ('[ \\t]+', Whitespace), ('@\\b', Operator), ('"', String, 'string'), ('[0-9]+[smhdw]?$', Number.Integer), ('([0-9]+[smhdw]?)([ \\t]+)', bygroups(Number.Integer, Whitespace)), ('\\S+', Literal)], 'multiple-simple-values': [include('simple-value'), ('[\\n]+', Whitespace)], 'include': [('([ \\t]+)([^ \\t\\n]+)([ \\t]+)([-\\._a-zA-Z]+)([ \\t]+)(;.*)?$', bygroups(Whitespace, Comment.PreprocFile, Whitespace, Name, Whitespace, Comment.Single), '#pop'), ('([ \\t]+)([^ \\t\\n]+)([ \\t\\n]+)$', bygroups(Whitespace, Comment.PreprocFile, Whitespace), '#pop')], 'string': [('\\\\"', String), ('"', String, '#pop'), ('[^"]+', String)]}
    
    def analyse_text(text):
        return text.startswith('$ORIGIN')


