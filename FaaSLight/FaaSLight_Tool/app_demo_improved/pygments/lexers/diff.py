"""
    pygments.lexers.diff
    ~~~~~~~~~~~~~~~~~~~~

    Lexers for diff/patch formats.

    :copyright: Copyright 2006-present by the Pygments team, see AUTHORS.
    :license: BSD, see LICENSE for details.
"""

import re
from pygments.lexer import RegexLexer, include, bygroups
from pygments.token import Text, Comment, Operator, Keyword, Name, Generic, Literal, Whitespace
__all__ = ['DiffLexer', 'DarcsPatchLexer', 'WDiffLexer']


class DiffLexer(RegexLexer):
    """
    Lexer for unified or context-style diffs or patches.
    """
    name = 'Diff'
    aliases = ['diff', 'udiff']
    filenames = ['*.diff', '*.patch']
    mimetypes = ['text/x-diff', 'text/x-patch']
    url = 'https://en.wikipedia.org/wiki/Diff'
    version_added = ''
    tokens = {'root': [('( )(.*)(\\n)', bygroups(Whitespace, Text, Whitespace)), ('(!.*|---)(\\n)', bygroups(Generic.Strong, Whitespace)), ('((?:< |-).*)(\\n)', bygroups(Generic.Deleted, Whitespace)), ('((?:> |\\+).*)(\\n)', bygroups(Generic.Inserted, Whitespace)), ('(@.*|\\d(?:,\\d+)?(?:a|c|d)\\d+(?:,\\d+)?)(\\n)', bygroups(Generic.Subheading, Whitespace)), ('((?:[Ii]ndex|diff).*)(\\n)', bygroups(Generic.Heading, Whitespace)), ('(=.*)(\\n)', bygroups(Generic.Heading, Whitespace)), ('(.*)(\\n)', bygroups(Text, Whitespace))]}
    
    def analyse_text(text):
        if text[:7] == 'Index: ':
            return True
        if text[:5] == 'diff ':
            return True
        if text[:4] == '--- ':
            return 0.9



class DarcsPatchLexer(RegexLexer):
    """
    DarcsPatchLexer is a lexer for the various versions of the darcs patch
    format.  Examples of this format are derived by commands such as
    ``darcs annotate --patch`` and ``darcs send``.
    """
    name = 'Darcs Patch'
    aliases = ['dpatch']
    filenames = ['*.dpatch', '*.darcspatch']
    url = 'https://darcs.net'
    version_added = '0.10'
    DPATCH_KEYWORDS = ('hunk', 'addfile', 'adddir', 'rmfile', 'rmdir', 'move', 'replace')
    tokens = {'root': [('<', Operator), ('>', Operator), ('\\{', Operator), ('\\}', Operator), ('(\\[)((?:TAG )?)(.*)(\\n)(.*)(\\*\\*)(\\d+)(\\s?)(\\])', bygroups(Operator, Keyword, Name, Whitespace, Name, Operator, Literal.Date, Whitespace, Operator)), ('(\\[)((?:TAG )?)(.*)(\\n)(.*)(\\*\\*)(\\d+)(\\s?)', bygroups(Operator, Keyword, Name, Whitespace, Name, Operator, Literal.Date, Whitespace), 'comment'), ('New patches:', Generic.Heading), ('Context:', Generic.Heading), ('Patch bundle hash:', Generic.Heading), ('(\\s*)({})(.*)(\\n)'.format('|'.join(DPATCH_KEYWORDS)), bygroups(Whitespace, Keyword, Text, Whitespace)), ('\\+', Generic.Inserted, 'insert'), ('-', Generic.Deleted, 'delete'), ('(.*)(\\n)', bygroups(Text, Whitespace))], 'comment': [('[^\\]].*\\n', Comment), ('\\]', Operator, '#pop')], 'specialText': [('\\n', Whitespace, '#pop'), ('\\[_[^_]*_]', Operator)], 'insert': [include('specialText'), ('\\[', Generic.Inserted), ('[^\\n\\[]+', Generic.Inserted)], 'delete': [include('specialText'), ('\\[', Generic.Deleted), ('[^\\n\\[]+', Generic.Deleted)]}



class WDiffLexer(RegexLexer):
    """
    A wdiff lexer.

    Note that:

    * It only works with normal output (without options like ``-l``).
    * If the target files contain "[-", "-]", "{+", or "+}",
      especially they are unbalanced, the lexer will get confused.
    """
    name = 'WDiff'
    url = 'https://www.gnu.org/software/wdiff/'
    aliases = ['wdiff']
    filenames = ['*.wdiff']
    mimetypes = []
    version_added = '2.2'
    flags = re.MULTILINE | re.DOTALL
    ins_op = '\\{\\+'
    ins_cl = '\\+\\}'
    del_op = '\\[\\-'
    del_cl = '\\-\\]'
    normal = '[^{}[\\]+-]+'
    tokens = {'root': [(ins_op, Generic.Inserted, 'inserted'), (del_op, Generic.Deleted, 'deleted'), (normal, Text), ('.', Text)], 'inserted': [(ins_op, Generic.Inserted, '#push'), (del_op, Generic.Inserted, '#push'), (del_cl, Generic.Inserted, '#pop'), (ins_cl, Generic.Inserted, '#pop'), (normal, Generic.Inserted), ('.', Generic.Inserted)], 'deleted': [(del_op, Generic.Deleted, '#push'), (ins_op, Generic.Deleted, '#push'), (ins_cl, Generic.Deleted, '#pop'), (del_cl, Generic.Deleted, '#pop'), (normal, Generic.Deleted), ('.', Generic.Deleted)]}


