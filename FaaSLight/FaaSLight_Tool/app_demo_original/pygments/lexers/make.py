"""
    pygments.lexers.make
    ~~~~~~~~~~~~~~~~~~~~

    Lexers for Makefiles and similar.

    :copyright: Copyright 2006-present by the Pygments team, see AUTHORS.
    :license: BSD, see LICENSE for details.
"""

import re
from pygments.lexer import Lexer, RegexLexer, include, bygroups, do_insertions, using
from pygments.token import Text, Comment, Operator, Keyword, Name, String, Punctuation, Whitespace
from pygments.lexers.shell import BashLexer
__all__ = ['MakefileLexer', 'BaseMakefileLexer', 'CMakeLexer']


class MakefileLexer(Lexer):
    """
    Lexer for BSD and GNU make extensions (lenient enough to handle both in
    the same file even).

    *Rewritten in Pygments 0.10.*
    """
    name = 'Makefile'
    aliases = ['make', 'makefile', 'mf', 'bsdmake']
    filenames = ['*.mak', '*.mk', 'Makefile', 'makefile', 'Makefile.*', 'GNUmakefile']
    mimetypes = ['text/x-makefile']
    url = 'https://en.wikipedia.org/wiki/Make_(software)'
    version_added = ''
    r_special = re.compile('^(?:\\.\\s*(include|undef|error|warning|if|else|elif|endif|for|endfor)|\\s*(ifeq|ifneq|ifdef|ifndef|else|endif|-?include|define|endef|:|vpath)|\\s*(if|else|endif))(?=\\s)')
    r_comment = re.compile('^\\s*@?#')
    
    def get_tokens_unprocessed(self, text):
        ins = []
        lines = text.splitlines(keepends=True)
        done = ''
        lex = BaseMakefileLexer(**self.options)
        backslashflag = False
        for line in lines:
            if (self.r_special.match(line) or backslashflag):
                ins.append((len(done), [(0, Comment.Preproc, line)]))
                backslashflag = line.strip().endswith('\\')
            elif self.r_comment.match(line):
                ins.append((len(done), [(0, Comment, line)]))
            else:
                done += line
        yield from do_insertions(ins, lex.get_tokens_unprocessed(done))
    
    def analyse_text(text):
        if re.search('\\$\\([A-Z_]+\\)', text):
            return 0.1



class BaseMakefileLexer(RegexLexer):
    """
    Lexer for simple Makefiles (no preprocessing).
    """
    name = 'Base Makefile'
    aliases = ['basemake']
    filenames = []
    mimetypes = []
    url = 'https://en.wikipedia.org/wiki/Make_(software)'
    version_added = '0.10'
    tokens = {'root': [('^(?:[\\t ]+.*\\n|\\n)+', using(BashLexer)), ('\\$[<@$+%?|*]', Keyword), ('\\s+', Whitespace), ('#.*?\\n', Comment), ('((?:un)?export)(\\s+)(?=[\\w${}\\t -]+\\n)', bygroups(Keyword, Whitespace), 'export'), ('(?:un)?export\\s+', Keyword), ('([\\w${}().-]+)(\\s*)([!?:+]?=)([ \\t]*)((?:.*\\\\\\n)+|.*\\n)', bygroups(Name.Variable, Whitespace, Operator, Whitespace, using(BashLexer))), ('"(\\\\\\\\|\\\\[^\\\\]|[^"\\\\])*"', String.Double), ("'(\\\\\\\\|\\\\[^\\\\]|[^'\\\\])*'", String.Single), ('([^\\n:]+)(:+)([ \\t]*)', bygroups(Name.Function, Operator, Whitespace), 'block-header'), ('\\$\\(', Keyword, 'expansion')], 'expansion': [('[^\\w$().-]+', Text), ('[\\w.-]+', Name.Variable), ('\\$', Keyword), ('\\(', Keyword, '#push'), ('\\)', Keyword, '#pop')], 'export': [('[\\w${}-]+', Name.Variable), ('\\n', Text, '#pop'), ('\\s+', Whitespace)], 'block-header': [('[,|]', Punctuation), ('#.*?\\n', Comment, '#pop'), ('\\\\\\n', Text), ('\\$\\(', Keyword, 'expansion'), ('[a-zA-Z_]+', Name), ('\\n', Whitespace, '#pop'), ('.', Text)]}



class CMakeLexer(RegexLexer):
    """
    Lexer for CMake files.
    """
    name = 'CMake'
    url = 'https://cmake.org/documentation/'
    aliases = ['cmake']
    filenames = ['*.cmake', 'CMakeLists.txt']
    mimetypes = ['text/x-cmake']
    version_added = '1.2'
    tokens = {'root': [('\\b(\\w+)([ \\t]*)(\\()', bygroups(Name.Builtin, Whitespace, Punctuation), 'args'), include('keywords'), include('ws')], 'args': [('\\(', Punctuation, '#push'), ('\\)', Punctuation, '#pop'), ('(\\$\\{)(.+?)(\\})', bygroups(Operator, Name.Variable, Operator)), ('(\\$ENV\\{)(.+?)(\\})', bygroups(Operator, Name.Variable, Operator)), ('(\\$<)(.+?)(>)', bygroups(Operator, Name.Variable, Operator)), ('(?s)".*?"', String.Double), ('\\\\\\S+', String), ('\\[(?P<level>=*)\\[[\\w\\W]*?\\](?P=level)\\]', String.Multiline), ('[^)$"# \\t\\n]+', String), ('\\n', Whitespace), include('keywords'), include('ws')], 'string': [], 'keywords': [('\\b(WIN32|UNIX|APPLE|CYGWIN|BORLAND|MINGW|MSVC|MSVC_IDE|MSVC60|MSVC70|MSVC71|MSVC80|MSVC90)\\b', Keyword)], 'ws': [('[ \\t]+', Whitespace), ('#\\[(?P<level>=*)\\[[\\w\\W]*?\\](?P=level)\\]', Comment), ('#.*\\n', Comment)]}
    
    def analyse_text(text):
        exp = '^[ \\t]*CMAKE_MINIMUM_REQUIRED[ \\t]*\\([ \\t]*VERSION[ \\t]*\\d+(\\.\\d+)*[ \\t]*([ \\t]FATAL_ERROR)?[ \\t]*\\)[ \\t]*(#[^\\n]*)?$'
        if re.search(exp, text, flags=re.MULTILINE | re.IGNORECASE):
            return 0.8
        return 0.0


