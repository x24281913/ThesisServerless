"""
    pygments.lexers.markup
    ~~~~~~~~~~~~~~~~~~~~~~

    Lexers for non-HTML markup languages.

    :copyright: Copyright 2006-present by the Pygments team, see AUTHORS.
    :license: BSD, see LICENSE for details.
"""

import re
from pygments.lexers.html import XmlLexer
from pygments.lexers.javascript import JavascriptLexer
from pygments.lexers.css import CssLexer
from pygments.lexers.lilypond import LilyPondLexer
from pygments.lexers.data import JsonLexer
from pygments.lexer import RegexLexer, DelegatingLexer, include, bygroups, using, this, do_insertions, default, words
from pygments.token import Text, Comment, Operator, Keyword, Name, String, Number, Punctuation, Generic, Other, Whitespace, Literal
from pygments.util import get_bool_opt, ClassNotFound
__all__ = ['BBCodeLexer', 'MoinWikiLexer', 'RstLexer', 'TexLexer', 'GroffLexer', 'MozPreprocHashLexer', 'MozPreprocPercentLexer', 'MozPreprocXulLexer', 'MozPreprocJavascriptLexer', 'MozPreprocCssLexer', 'MarkdownLexer', 'OrgLexer', 'TiddlyWiki5Lexer', 'WikitextLexer']


class BBCodeLexer(RegexLexer):
    """
    A lexer that highlights BBCode(-like) syntax.
    """
    name = 'BBCode'
    aliases = ['bbcode']
    mimetypes = ['text/x-bbcode']
    url = 'https://www.bbcode.org/'
    version_added = '0.6'
    tokens = {'root': [('[^[]+', Text), ('\\[/?\\w+', Keyword, 'tag'), ('\\[', Text)], 'tag': [('\\s+', Text), ('(\\w+)(=)("?[^\\s"\\]]+"?)', bygroups(Name.Attribute, Operator, String)), ('(=)("?[^\\s"\\]]+"?)', bygroups(Operator, String)), ('\\]', Keyword, '#pop')]}



class MoinWikiLexer(RegexLexer):
    """
    For MoinMoin (and Trac) Wiki markup.
    """
    name = 'MoinMoin/Trac Wiki markup'
    aliases = ['trac-wiki', 'moin']
    filenames = []
    mimetypes = ['text/x-trac-wiki']
    url = 'https://moinmo.in'
    version_added = '0.7'
    flags = re.MULTILINE | re.IGNORECASE
    tokens = {'root': [('^#.*$', Comment), ('(!)(\\S+)', bygroups(Keyword, Text)), ('^(=+)([^=]+)(=+)(\\s*#.+)?$', bygroups(Generic.Heading, using(this), Generic.Heading, String)), ('(\\{\\{\\{)(\\n#!.+)?', bygroups(Name.Builtin, Name.Namespace), 'codeblock'), ("(\\'\\'\\'?|\\|\\||`|__|~~|\\^|,,|::)", Comment), ('^( +)([.*-])( )', bygroups(Text, Name.Builtin, Text)), ('^( +)([a-z]{1,5}\\.)( )', bygroups(Text, Name.Builtin, Text)), ('\\[\\[\\w+.*?\\]\\]', Keyword), ('(\\[[^\\s\\]]+)(\\s+[^\\]]+?)?(\\])', bygroups(Keyword, String, Keyword)), ('^----+$', Keyword), ("[^\\n\\'\\[{!_~^,|]+", Text), ('\\n', Text), ('.', Text)], 'codeblock': [('\\}\\}\\}', Name.Builtin, '#pop'), ('\\{\\{\\{', Text, '#push'), ('[^{}]+', Comment.Preproc), ('.', Comment.Preproc)]}



class RstLexer(RegexLexer):
    """
    For reStructuredText markup.

    Additional options accepted:

    `handlecodeblocks`
        Highlight the contents of ``.. sourcecode:: language``,
        ``.. code:: language`` and ``.. code-block:: language``
        directives with a lexer for the given language (default:
        ``True``).

        .. versionadded:: 0.8
    """
    name = 'reStructuredText'
    url = 'https://docutils.sourceforge.io/rst.html'
    aliases = ['restructuredtext', 'rst', 'rest']
    filenames = ['*.rst', '*.rest']
    mimetypes = ['text/x-rst', 'text/prs.fallenstein.rst']
    version_added = '0.7'
    flags = re.MULTILINE
    
    def _handle_sourcecode(self, match):
        from pygments.lexers import get_lexer_by_name
        yield (match.start(1), Punctuation, match.group(1))
        yield (match.start(2), Text, match.group(2))
        yield (match.start(3), Operator.Word, match.group(3))
        yield (match.start(4), Punctuation, match.group(4))
        yield (match.start(5), Text, match.group(5))
        yield (match.start(6), Keyword, match.group(6))
        yield (match.start(7), Text, match.group(7))
        lexer = None
        if self.handlecodeblocks:
            try:
                lexer = get_lexer_by_name(match.group(6).strip())
            except ClassNotFound:
                pass
        indention = match.group(8)
        indention_size = len(indention)
        code = indention + match.group(9) + match.group(10) + match.group(11)
        if lexer is None:
            yield (match.start(8), String, code)
            return
        ins = []
        codelines = code.splitlines(True)
        code = ''
        for line in codelines:
            if len(line) > indention_size:
                ins.append((len(code), [(0, Text, line[:indention_size])]))
                code += line[indention_size:]
            else:
                code += line
        yield from do_insertions(ins, lexer.get_tokens_unprocessed(code))
    closers = '\'")]}>’”»!?'
    unicode_delimiters = '‐‑‒–—\xa0'
    end_string_suffix = f'((?=$)|(?=[-/:.,; \\n\\x00{re.escape(unicode_delimiters)}{re.escape(closers)}]))'
    tokens = {'root': [('^(=+|-+|`+|:+|\\.+|\\\'+|"+|~+|\\^+|_+|\\*+|\\++|#+)([ \\t]*\\n)(.+)(\\n)(\\1)(\\n)', bygroups(Generic.Heading, Text, Generic.Heading, Text, Generic.Heading, Text)), ('^(\\S.*)(\\n)(={3,}|-{3,}|`{3,}|:{3,}|\\.{3,}|\\\'{3,}|"{3,}|~{3,}|\\^{3,}|_{3,}|\\*{3,}|\\+{3,}|#{3,})(\\n)', bygroups(Generic.Heading, Text, Generic.Heading, Text)), ('^(\\s*)([-*+])( .+\\n(?:\\1  .+\\n)*)', bygroups(Text, Number, using(this, state='inline'))), ('^(\\s*)([0-9#ivxlcmIVXLCM]+\\.)( .+\\n(?:\\1  .+\\n)*)', bygroups(Text, Number, using(this, state='inline'))), ('^(\\s*)(\\(?[0-9#ivxlcmIVXLCM]+\\))( .+\\n(?:\\1  .+\\n)*)', bygroups(Text, Number, using(this, state='inline'))), ('^(\\s*)([A-Z]+\\.)( .+\\n(?:\\1  .+\\n)+)', bygroups(Text, Number, using(this, state='inline'))), ('^(\\s*)(\\(?[A-Za-z]+\\))( .+\\n(?:\\1  .+\\n)+)', bygroups(Text, Number, using(this, state='inline'))), ('^(\\s*)(\\|)( .+\\n(?:\\|  .+\\n)*)', bygroups(Text, Operator, using(this, state='inline'))), ('^( *\\.\\.)(\\s*)((?:source)?code(?:-block)?)(::)([ \\t]*)([^\\n]+)(\\n[ \\t]*\\n)([ \\t]+)(.*)(\\n)((?:(?:\\8.*)?\\n)+)', _handle_sourcecode), ('^( *\\.\\.)(\\s*)([\\w:-]+?)(::)(?:([ \\t]*)(.*))', bygroups(Punctuation, Text, Operator.Word, Punctuation, Text, using(this, state='inline'))), ('^( *\\.\\.)(\\s*)(_(?:[^:\\\\]|\\\\.)+:)(.*?)$', bygroups(Punctuation, Text, Name.Tag, using(this, state='inline'))), ('^( *\\.\\.)(\\s*)(\\[.+\\])(.*?)$', bygroups(Punctuation, Text, Name.Tag, using(this, state='inline'))), ('^( *\\.\\.)(\\s*)(\\|.+\\|)(\\s*)([\\w:-]+?)(::)(?:([ \\t]*)(.*))', bygroups(Punctuation, Text, Name.Tag, Text, Operator.Word, Punctuation, Text, using(this, state='inline'))), ('^ *\\.\\..*(\\n( +.*\\n|\\n)+)?', Comment), ('^( *)(:(?:\\\\\\\\|\\\\:|[^:\\n])+:(?=\\s))([ \\t]*)', bygroups(Text, Name.Class, Text)), ('^(\\S.*(?<!::)\\n)((?:(?: +.*)\\n)+)', bygroups(using(this, state='inline'), using(this, state='inline'))), ('(::)(\\n[ \\t]*\\n)([ \\t]+)(.*)(\\n)((?:(?:\\3.*)?\\n)+)', bygroups(String.Escape, Text, String, String, Text, String)), include('inline')], 'inline': [('\\\\.', Text), ('``', String, 'literal'), ('(`.+?)(<.+?>)(`__?)', bygroups(String, String.Interpol, String)), ('`.+?`__?', String), ('(`.+?`)(:[a-zA-Z0-9:-]+?:)?', bygroups(Name.Variable, Name.Attribute)), ('(:[a-zA-Z0-9:-]+?:)(`.+?`)', bygroups(Name.Attribute, Name.Variable)), ('\\*\\*.+?\\*\\*', Generic.Strong), ('\\*.+?\\*', Generic.Emph), ('\\[.*?\\]_', String), ('<.+?>', Name.Tag), ('[^\\\\\\n\\[*`:]+', Text), ('.', Text)], 'literal': [('[^`]+', String), ('``' + end_string_suffix, String, '#pop'), ('`', String)]}
    
    def __init__(self, **options):
        self.handlecodeblocks = get_bool_opt(options, 'handlecodeblocks', True)
        RegexLexer.__init__(self, **options)
    
    def analyse_text(text):
        if (text[:2] == '..' and text[2:3] != '.'):
            return 0.3
        p1 = text.find('\n')
        p2 = text.find('\n', p1 + 1)
        if (p2 > -1 and p1 * 2 + 1 == p2 and text[p1 + 1] in '-=' and text[p1 + 1] == text[p2 - 1]):
            return 0.5



class TexLexer(RegexLexer):
    """
    Lexer for the TeX and LaTeX typesetting languages.
    """
    name = 'TeX'
    aliases = ['tex', 'latex']
    filenames = ['*.tex', '*.aux', '*.toc']
    mimetypes = ['text/x-tex', 'text/x-latex']
    url = 'https://tug.org'
    version_added = ''
    tokens = {'general': [('%.*?\\n', Comment), ('[{}]', Name.Builtin), ('[&_^]', Name.Builtin)], 'root': [('\\\\\\[', String.Backtick, 'displaymath'), ('\\\\\\(', String, 'inlinemath'), ('\\$\\$', String.Backtick, 'displaymath'), ('\\$', String, 'inlinemath'), ('\\\\([a-zA-Z@_:]+|\\S?)', Keyword, 'command'), ('\\\\$', Keyword), include('general'), ('[^\\\\$%&_^{}]+', Text)], 'math': [('\\\\([a-zA-Z]+|\\S?)', Name.Variable), include('general'), ('[0-9]+', Number), ('[-=!+*/()\\[\\]]', Operator), ('[^=!+*/()\\[\\]\\\\$%&_^{}0-9-]+', Name.Builtin)], 'inlinemath': [('\\\\\\)', String, '#pop'), ('\\$', String, '#pop'), include('math')], 'displaymath': [('\\\\\\]', String, '#pop'), ('\\$\\$', String, '#pop'), ('\\$', Name.Builtin), include('math')], 'command': [('\\[.*?\\]', Name.Attribute), ('\\*', Keyword), default('#pop')]}
    
    def analyse_text(text):
        for start in ('\\documentclass', '\\input', '\\documentstyle', '\\relax'):
            if text[:len(start)] == start:
                return True



class GroffLexer(RegexLexer):
    """
    Lexer for the (g)roff typesetting language, supporting groff
    extensions. Mainly useful for highlighting manpage sources.
    """
    name = 'Groff'
    aliases = ['groff', 'nroff', 'man']
    filenames = ['*.[1-9]', '*.man', '*.1p', '*.3pm']
    mimetypes = ['application/x-troff', 'text/troff']
    url = 'https://www.gnu.org/software/groff'
    version_added = '0.6'
    tokens = {'root': [('(\\.)(\\w+)', bygroups(Text, Keyword), 'request'), ('\\.', Punctuation, 'request'), ('[^\\\\\\n]+', Text, 'textline'), default('textline')], 'textline': [include('escapes'), ('[^\\\\\\n]+', Text), ('\\n', Text, '#pop')], 'escapes': [('\\\\"[^\\n]*', Comment), ('\\\\[fn]\\w', String.Escape), ('\\\\\\(.{2}', String.Escape), ('\\\\.\\[.*\\]', String.Escape), ('\\\\.', String.Escape), ('\\\\\\n', Text, 'request')], 'request': [('\\n', Text, '#pop'), include('escapes'), ('"[^\\n"]+"', String.Double), ('\\d+', Number), ('\\S+', String), ('\\s+', Text)]}
    
    def analyse_text(text):
        if text[:1] != '.':
            return False
        if text[:3] == '.\\"':
            return True
        if text[:4] == '.TH ':
            return True
        if (text[1:3].isalnum() and text[3].isspace()):
            return 0.9



class MozPreprocHashLexer(RegexLexer):
    """
    Lexer for Mozilla Preprocessor files (with '#' as the marker).

    Other data is left untouched.
    """
    name = 'mozhashpreproc'
    aliases = [name]
    filenames = []
    mimetypes = []
    url = 'https://firefox-source-docs.mozilla.org/build/buildsystem/preprocessor.html'
    version_added = '2.0'
    tokens = {'root': [('^#', Comment.Preproc, ('expr', 'exprstart')), ('.+', Other)], 'exprstart': [('(literal)(.*)', bygroups(Comment.Preproc, Text), '#pop:2'), (words(('define', 'undef', 'if', 'ifdef', 'ifndef', 'else', 'elif', 'elifdef', 'elifndef', 'endif', 'expand', 'filter', 'unfilter', 'include', 'includesubst', 'error')), Comment.Preproc, '#pop')], 'expr': [(words(('!', '!=', '==', '&&', '||')), Operator), ('(defined)(\\()', bygroups(Keyword, Punctuation)), ('\\)', Punctuation), ('[0-9]+', Number.Decimal), ('__\\w+?__', Name.Variable), ('@\\w+?@', Name.Class), ('\\w+', Name), ('\\n', Text, '#pop'), ('\\s+', Text), ('\\S', Punctuation)]}



class MozPreprocPercentLexer(MozPreprocHashLexer):
    """
    Lexer for Mozilla Preprocessor files (with '%' as the marker).

    Other data is left untouched.
    """
    name = 'mozpercentpreproc'
    aliases = [name]
    filenames = []
    mimetypes = []
    url = 'https://firefox-source-docs.mozilla.org/build/buildsystem/preprocessor.html'
    version_added = '2.0'
    tokens = {'root': [('^%', Comment.Preproc, ('expr', 'exprstart')), ('.+', Other)]}



class MozPreprocXulLexer(DelegatingLexer):
    """
    Subclass of the `MozPreprocHashLexer` that highlights unlexed data with the
    `XmlLexer`.
    """
    name = 'XUL+mozpreproc'
    aliases = ['xul+mozpreproc']
    filenames = ['*.xul.in']
    mimetypes = []
    url = 'https://firefox-source-docs.mozilla.org/build/buildsystem/preprocessor.html'
    version_added = '2.0'
    
    def __init__(self, **options):
        super().__init__(XmlLexer, MozPreprocHashLexer, **options)



class MozPreprocJavascriptLexer(DelegatingLexer):
    """
    Subclass of the `MozPreprocHashLexer` that highlights unlexed data with the
    `JavascriptLexer`.
    """
    name = 'Javascript+mozpreproc'
    aliases = ['javascript+mozpreproc']
    filenames = ['*.js.in']
    mimetypes = []
    url = 'https://firefox-source-docs.mozilla.org/build/buildsystem/preprocessor.html'
    version_added = '2.0'
    
    def __init__(self, **options):
        super().__init__(JavascriptLexer, MozPreprocHashLexer, **options)



class MozPreprocCssLexer(DelegatingLexer):
    """
    Subclass of the `MozPreprocHashLexer` that highlights unlexed data with the
    `CssLexer`.
    """
    name = 'CSS+mozpreproc'
    aliases = ['css+mozpreproc']
    filenames = ['*.css.in']
    mimetypes = []
    url = 'https://firefox-source-docs.mozilla.org/build/buildsystem/preprocessor.html'
    version_added = '2.0'
    
    def __init__(self, **options):
        super().__init__(CssLexer, MozPreprocPercentLexer, **options)



class MarkdownLexer(RegexLexer):
    """
    For Markdown markup.
    """
    name = 'Markdown'
    url = 'https://daringfireball.net/projects/markdown/'
    aliases = ['markdown', 'md']
    filenames = ['*.md', '*.markdown']
    mimetypes = ['text/x-markdown']
    version_added = '2.2'
    flags = re.MULTILINE
    
    def _handle_codeblock(self, match):
        from pygments.lexers import get_lexer_by_name
        yield (match.start('initial'), String.Backtick, match.group('initial'))
        yield (match.start('lang'), String.Backtick, match.group('lang'))
        if match.group('afterlang') is not None:
            yield (match.start('whitespace'), Whitespace, match.group('whitespace'))
            yield (match.start('extra'), Text, match.group('extra'))
        yield (match.start('newline'), Whitespace, match.group('newline'))
        lexer = None
        if self.handlecodeblocks:
            try:
                lexer = get_lexer_by_name(match.group('lang').strip())
            except ClassNotFound:
                pass
        code = match.group('code')
        if lexer is None:
            yield (match.start('code'), String, code)
        else:
            yield from do_insertions([], lexer.get_tokens_unprocessed(code))
        yield (match.start('terminator'), String.Backtick, match.group('terminator'))
    tokens = {'root': [('(^#[^#].+)(\\n)', bygroups(Generic.Heading, Text)), ('(^#{2,6}[^#].+)(\\n)', bygroups(Generic.Subheading, Text)), ('^(.+)(\\n)(=+)(\\n)', bygroups(Generic.Heading, Text, Generic.Heading, Text)), ('^(.+)(\\n)(-+)(\\n)', bygroups(Generic.Subheading, Text, Generic.Subheading, Text)), ('^(\\s*)([*-] )(\\[[ xX]\\])( .+\\n)', bygroups(Whitespace, Keyword, Keyword, using(this, state='inline'))), ('^(\\s*)([*-])(\\s)(.+\\n)', bygroups(Whitespace, Keyword, Whitespace, using(this, state='inline'))), ('^(\\s*)([0-9]+\\.)( .+\\n)', bygroups(Whitespace, Keyword, using(this, state='inline'))), ('^(\\s*>\\s)(.+\\n)', bygroups(Keyword, Generic.Emph)), ('^(\\s*```\\n[\\w\\W]*?^\\s*```$\\n)', String.Backtick), ('(?x)\n              ^(?P<initial>\\s*```)\n              (?P<lang>[\\w\\-]+)\n              (?P<afterlang>\n                 (?P<whitespace>[^\\S\\n]+)\n                 (?P<extra>.*))?\n              (?P<newline>\\n)\n              (?P<code>(.|\\n)*?)\n              (?P<terminator>^\\s*```$\\n)\n              ', _handle_codeblock), include('inline')], 'inline': [('\\\\.', Text), ('([^`]?)(`[^`\\n]+`)', bygroups(Text, String.Backtick)), ('([^\\*]?)(\\*\\*[^* \\n][^*\\n]*\\*\\*)', bygroups(Text, Generic.Strong)), ('([^_]?)(__[^_ \\n][^_\\n]*__)', bygroups(Text, Generic.Strong)), ('([^\\*]?)(\\*[^* \\n][^*\\n]*\\*)', bygroups(Text, Generic.Emph)), ('([^_]?)(_[^_ \\n][^_\\n]*_)', bygroups(Text, Generic.Emph)), ('([^~]?)(~~[^~ \\n][^~\\n]*~~)', bygroups(Text, Generic.Deleted)), ('[@#][\\w/:]+', Name.Entity), ('(!?\\[)([^]]+)(\\])(\\()([^)]+)(\\))', bygroups(Text, Name.Tag, Text, Text, Name.Attribute, Text)), ('(\\[)([^]]+)(\\])(\\[)([^]]*)(\\])', bygroups(Text, Name.Tag, Text, Text, Name.Label, Text)), ('^(\\s*\\[)([^]]*)(\\]:\\s*)(.+)', bygroups(Text, Name.Label, Text, Name.Attribute)), ('[^\\\\\\s]+', Text), ('.', Text)]}
    
    def __init__(self, **options):
        self.handlecodeblocks = get_bool_opt(options, 'handlecodeblocks', True)
        RegexLexer.__init__(self, **options)



class OrgLexer(RegexLexer):
    """
    For Org Mode markup.
    """
    name = 'Org Mode'
    url = 'https://orgmode.org'
    aliases = ['org', 'orgmode', 'org-mode']
    filenames = ['*.org']
    mimetypes = ['text/org']
    version_added = '2.18'
    
    def _inline(start, end):
        return f'(?<!\\w){start}(.|\\n(?!\\n))+?{end}(?!\\w)'
    tokens = {'root': [('^# .*', Comment.Single), ('^(\\* )(COMMENT)( .*)', bygroups(Generic.Heading, Comment.Preproc, Generic.Heading)), ('^(\\*\\*+ )(COMMENT)( .*)', bygroups(Generic.Subheading, Comment.Preproc, Generic.Subheading)), ('^(\\* )(DONE)( .*)', bygroups(Generic.Heading, Generic.Deleted, Generic.Heading)), ('^(\\*\\*+ )(DONE)( .*)', bygroups(Generic.Subheading, Generic.Deleted, Generic.Subheading)), ('^(\\* )(TODO)( .*)', bygroups(Generic.Heading, Generic.Error, Generic.Heading)), ('^(\\*\\*+ )(TODO)( .*)', bygroups(Generic.Subheading, Generic.Error, Generic.Subheading)), ('^(\\* .+?)( :[a-zA-Z0-9_@:]+:)?$', bygroups(Generic.Heading, Generic.Emph)), ('^(\\*\\*+ .+?)( :[a-zA-Z0-9_@:]+:)?$', bygroups(Generic.Subheading, Generic.Emph)), ('^(?:( *)([+-] )|( +)(\\* ))(\\[[ X-]\\])?(.+ ::)?', bygroups(Whitespace, Keyword, Whitespace, Keyword, Generic.Prompt, Name.Label)), ('^( *)([0-9]+[.)])( \\[@[0-9]+\\])?', bygroups(Whitespace, Keyword, Generic.Emph)), ('(?i)^( *#\\+begin: *)((?:.|\\n)*?)(^ *#\\+end: *$)', bygroups(Operator.Word, using(this), Operator.Word)), ('(?i)^( *#\\+begin_comment *\\n)((?:.|\\n)*?)(^ *#\\+end_comment *$)', bygroups(Operator.Word, Comment.Multiline, Operator.Word)), ('(?i)^( *#\\+begin_src .*)((?:.|\\n)*?)(^ *#\\+end_src *$)', bygroups(Operator.Word, Text, Operator.Word)), ('(?i)^( *#\\+begin_\\w+)( *\\n)((?:.|\\n)*?)(^ *#\\+end_\\w+)( *$)', bygroups(Operator.Word, Whitespace, Text, Operator.Word, Whitespace)), ('^(#\\+\\w+:)(.*)$', bygroups(Name.Namespace, Text)), ('(?i)^( *:\\w+: *\\n)((?:.|\\n)*?)(^ *:end: *$)', bygroups(Name.Decorator, Comment.Special, Name.Decorator)), ('\\\\\\\\$', Operator), ('^\\s*CLOSED:\\s+', Generic.Deleted, 'dateline'), ('^\\s*(?:DEADLINE:|SCHEDULED:)\\s+', Generic.Error, 'dateline'), (_inline('\\*', '\\*+'), Generic.Strong), (_inline('/', '/'), Generic.Emph), (_inline('=', '='), String), (_inline('~', '~'), String), (_inline('\\+', '\\+'), Generic.Deleted), (_inline('_', '_+'), Generic.EmphStrong), ('<.+?>', Literal.Date), ('\\{\\{\\{.+?\\}\\}\\}', Comment.Preproc), ('(?<!\\[)\\[fn:.+?\\]', Name.Tag), ('(?s)(\\[\\[)(.*?)(\\]\\[)(.*?)(\\]\\])', bygroups(Punctuation, Name.Attribute, Punctuation, Name.Tag, Punctuation)), ('(?s)(\\[\\[)(.+?)(\\]\\])', bygroups(Punctuation, Name.Attribute, Punctuation)), ('(<<)(.+?)(>>)', bygroups(Punctuation, Name.Attribute, Punctuation)), ('^( *)(\\|[ -].*?[ -]\\|)$', bygroups(Whitespace, String)), ('[^#*+\\-0-9:\\\\/=~_<{\\[|\\n]+', Text), ('[#*+\\-0-9:\\\\/=~_<{\\[|\\n]', Text)], 'dateline': [('\\s*CLOSED:\\s+', Generic.Deleted), ('\\s*(?:DEADLINE:|SCHEDULED:)\\s+', Generic.Error), ('\\[.+?\\]', Literal.Date), ('<[^>]+?>', Literal.Date), ('(\\s*)$', Text, '#pop'), ('.', Text)]}



class TiddlyWiki5Lexer(RegexLexer):
    """
    For TiddlyWiki5 markup.
    """
    name = 'tiddler'
    url = 'https://tiddlywiki.com/#TiddlerFiles'
    aliases = ['tid']
    filenames = ['*.tid']
    mimetypes = ['text/vnd.tiddlywiki']
    version_added = '2.7'
    flags = re.MULTILINE
    
    def _handle_codeblock(self, match):
        """
        match args: 1:backticks, 2:lang_name, 3:newline, 4:code, 5:backticks
        """
        from pygments.lexers import get_lexer_by_name
        yield (match.start(1), String, match.group(1))
        yield (match.start(2), String, match.group(2))
        yield (match.start(3), Text, match.group(3))
        lexer = None
        if self.handlecodeblocks:
            try:
                lexer = get_lexer_by_name(match.group(2).strip())
            except ClassNotFound:
                pass
        code = match.group(4)
        if lexer is None:
            yield (match.start(4), String, code)
            return
        yield from do_insertions([], lexer.get_tokens_unprocessed(code))
        yield (match.start(5), String, match.group(5))
    
    def _handle_cssblock(self, match):
        """
        match args: 1:style tag 2:newline, 3:code, 4:closing style tag
        """
        from pygments.lexers import get_lexer_by_name
        yield (match.start(1), String, match.group(1))
        yield (match.start(2), String, match.group(2))
        lexer = None
        if self.handlecodeblocks:
            try:
                lexer = get_lexer_by_name('css')
            except ClassNotFound:
                pass
        code = match.group(3)
        if lexer is None:
            yield (match.start(3), String, code)
            return
        yield from do_insertions([], lexer.get_tokens_unprocessed(code))
        yield (match.start(4), String, match.group(4))
    tokens = {'root': [('^(title)(:\\s)(.+\\n)', bygroups(Keyword, Text, Generic.Heading)), ('^(!)([^!].+\\n)', bygroups(Generic.Heading, Text)), ('^(!{2,6})(.+\\n)', bygroups(Generic.Subheading, Text)), ('^(\\s*)([*#>]+)(\\s*)(.+\\n)', bygroups(Text, Keyword, Text, using(this, state='inline'))), ('^(<<<.*\\n)([\\w\\W]*?)(^<<<.*$)', bygroups(String, Text, String)), ('^(\\|.*?\\|h)$', bygroups(Generic.Strong)), ('^(\\|.*?\\|[cf])$', bygroups(Generic.Emph)), ('^(\\|.*?\\|k)$', bygroups(Name.Tag)), ('^(;.*)$', bygroups(Generic.Strong)), ('^(```\\n)([\\w\\W]*?)(^```$)', bygroups(String, Text, String)), ('^(```)(\\w+)(\\n)([\\w\\W]*?)(^```$)', _handle_codeblock), ('^(<style>)(\\n)([\\w\\W]*?)(^</style>$)', _handle_cssblock), include('keywords'), include('inline')], 'keywords': [(words(('\\define', '\\end', 'caption', 'created', 'modified', 'tags', 'title', 'type'), prefix='^', suffix='\\b'), Keyword)], 'inline': [('\\\\.', Text), ('\\d{17}', Number.Integer), ('(\\s)(//[^/]+//)((?=\\W|\\n))', bygroups(Text, Generic.Emph, Text)), ('(\\s)(\\^\\^[^\\^]+\\^\\^)', bygroups(Text, Generic.Emph)), ('(\\s)(,,[^,]+,,)', bygroups(Text, Generic.Emph)), ('(\\s)(__[^_]+__)', bygroups(Text, Generic.Strong)), ("(\\s)(''[^']+'')((?=\\W|\\n))", bygroups(Text, Generic.Strong, Text)), ('(\\s)(~~[^~]+~~)((?=\\W|\\n))', bygroups(Text, Generic.Deleted, Text)), ('<<[^>]+>>', Name.Tag), ('\\$\\$[^$]+\\$\\$', Name.Tag), ('\\$\\([^)]+\\)\\$', Name.Tag), ('^@@.*$', Name.Tag), ('</?[^>]+>', Name.Tag), ('`[^`]+`', String.Backtick), ('&\\S*?;', String.Regex), ('(\\[{2})([^]\\|]+)(\\]{2})', bygroups(Text, Name.Tag, Text)), ('(\\[{2})([^]\\|]+)(\\|)([^]\\|]+)(\\]{2})', bygroups(Text, Name.Tag, Text, Name.Attribute, Text)), ('(\\{{2})([^}]+)(\\}{2})', bygroups(Text, Name.Tag, Text)), ('(\\b.?.?tps?://[^\\s"]+)', bygroups(Name.Attribute)), ('[\\w]+', Text), ('.', Text)]}
    
    def __init__(self, **options):
        self.handlecodeblocks = get_bool_opt(options, 'handlecodeblocks', True)
        RegexLexer.__init__(self, **options)



class WikitextLexer(RegexLexer):
    """
    For MediaWiki Wikitext.

    Parsing Wikitext is tricky, and results vary between different MediaWiki
    installations, so we only highlight common syntaxes (built-in or from
    popular extensions), and also assume templates produce no unbalanced
    syntaxes.
    """
    name = 'Wikitext'
    url = 'https://www.mediawiki.org/wiki/Wikitext'
    aliases = ['wikitext', 'mediawiki']
    filenames = []
    mimetypes = ['text/x-wiki']
    version_added = '2.15'
    flags = re.MULTILINE
    
    def nowiki_tag_rules(tag_name):
        return [(f'(?i)(</)({tag_name})(\\s*)(>)', bygroups(Punctuation, Name.Tag, Whitespace, Punctuation), '#pop'), include('entity'), include('text')]
    
    def plaintext_tag_rules(tag_name):
        return [(f'(?si)(.*?)(</)({tag_name})(\\s*)(>)', bygroups(Text, Punctuation, Name.Tag, Whitespace, Punctuation), '#pop')]
    
    def delegate_tag_rules(tag_name, lexer, **lexer_kwargs):
        return [(f'(?i)(</)({tag_name})(\\s*)(>)', bygroups(Punctuation, Name.Tag, Whitespace, Punctuation), '#pop'), (f'(?si).+?(?=</{tag_name}\\s*>)', using(lexer, **lexer_kwargs))]
    
    def text_rules(token):
        return [('\\w+', token), ('[^\\S\\n]+', token), ('(?s).', token)]
    
    def handle_syntaxhighlight(self, match, ctx):
        from pygments.lexers import get_lexer_by_name
        attr_content = match.group()
        start = 0
        index = 0
        while True:
            index = attr_content.find('>', start)
            if attr_content[index - 2:index] != '--':
                break
            start = index + 1
        if index == -1:
            yield from self.get_tokens_unprocessed(attr_content, stack=['root', 'attr'])
            return
        attr = attr_content[:index]
        yield from self.get_tokens_unprocessed(attr, stack=['root', 'attr'])
        yield (match.start(3) + index, Punctuation, '>')
        lexer = None
        content = attr_content[index + 1:]
        lang_match = re.findall('\\blang=("|\\\'|)(\\w+)(\\1)', attr)
        if len(lang_match) >= 1:
            lang = lang_match[-1][1]
            try:
                lexer = get_lexer_by_name(lang)
            except ClassNotFound:
                pass
        if lexer is None:
            yield (match.start() + index + 1, Text, content)
        else:
            yield from lexer.get_tokens_unprocessed(content)
    
    def handle_score(self, match, ctx):
        attr_content = match.group()
        start = 0
        index = 0
        while True:
            index = attr_content.find('>', start)
            if attr_content[index - 2:index] != '--':
                break
            start = index + 1
        if index == -1:
            yield from self.get_tokens_unprocessed(attr_content, stack=['root', 'attr'])
            return
        attr = attr_content[:index]
        content = attr_content[index + 1:]
        yield from self.get_tokens_unprocessed(attr, stack=['root', 'attr'])
        yield (match.start(3) + index, Punctuation, '>')
        lang_match = re.findall('\\blang=("|\\\'|)(\\w+)(\\1)', attr)
        lang = (lang_match[-1][1] if len(lang_match) >= 1 else 'lilypond')
        if lang == 'lilypond':
            yield from LilyPondLexer().get_tokens_unprocessed(content)
        else:
            yield (match.start() + index + 1, Text, content)
    title_char = ' %!"$&\\\'()*,\\-./0-9:;=?@A-Z\\\\\\^_`~+\\u0080-\\uFFFF'
    nbsp_char = '(?:\\t|&nbsp;|&\\#0*160;|&\\#[Xx]0*[Aa]0;|[ \\xA0\\u1680\\u2000-\\u200A\\u202F\\u205F\\u3000])'
    link_address = '(?:[0-9.]+|\\[[0-9a-f:.]+\\]|[^\\x00-\\x20"<>\\[\\]\\x7F\\xA0\\u1680\\u2000-\\u200A\\u202F\\u205F\\u3000\\uFFFD])'
    link_char_class = '[^\\x00-\\x20"<>\\[\\]\\x7F\\xA0\\u1680\\u2000-\\u200A\\u202F\\u205F\\u3000\\uFFFD]'
    double_slashes_i = {'__FORCETOC__', '__NOCONTENTCONVERT__', '__NOCC__', '__NOEDITSECTION__', '__NOGALLERY__', '__NOTITLECONVERT__', '__NOTC__', '__NOTOC__', '__TOC__'}
    double_slashes = {'__EXPECTUNUSEDCATEGORY__', '__HIDDENCAT__', '__INDEX__', '__NEWSECTIONLINK__', '__NOINDEX__', '__NONEWSECTIONLINK__', '__STATICREDIRECT__', '__NOGLOBAL__', '__DISAMBIG__', '__EXPECTED_UNCONNECTED_PAGE__'}
    protocols = {'bitcoin:', 'ftp://', 'ftps://', 'geo:', 'git://', 'gopher://', 'http://', 'https://', 'irc://', 'ircs://', 'magnet:', 'mailto:', 'mms://', 'news:', 'nntp://', 'redis://', 'sftp://', 'sip:', 'sips:', 'sms:', 'ssh://', 'svn://', 'tel:', 'telnet://', 'urn:', 'worldwind://', 'xmpp:', '//'}
    non_relative_protocols = protocols - {'//'}
    html_tags = {'abbr', 'b', 'bdi', 'bdo', 'big', 'blockquote', 'br', 'caption', 'center', 'cite', 'code', 'data', 'dd', 'del', 'dfn', 'div', 'dl', 'dt', 'em', 'font', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'hr', 'i', 'ins', 'kbd', 'li', 'link', 'mark', 'meta', 'ol', 'p', 'q', 'rb', 'rp', 'rt', 'rtc', 'ruby', 's', 'samp', 'small', 'span', 'strike', 'strong', 'sub', 'sup', 'table', 'td', 'th', 'time', 'tr', 'tt', 'u', 'ul', 'var', 'wbr'}
    parser_tags = {'graph', 'charinsert', 'rss', 'chem', 'categorytree', 'nowiki', 'inputbox', 'math', 'hiero', 'score', 'pre', 'ref', 'translate', 'imagemap', 'templatestyles', 'languages', 'noinclude', 'mapframe', 'section', 'poem', 'syntaxhighlight', 'includeonly', 'tvar', 'onlyinclude', 'templatedata', 'langconvert', 'timeline', 'dynamicpagelist', 'gallery', 'maplink', 'ce', 'references'}
    variant_langs = {'zh', 'zh-hans', 'zh-hant', 'zh-cn', 'zh-hk', 'zh-mo', 'zh-my', 'zh-sg', 'zh-tw', 'wuu', 'wuu-hans', 'wuu-hant', 'uz', 'uz-latn', 'uz-cyrl', 'tly', 'tly-cyrl', 'tg', 'tg-latn', 'sr', 'sr-ec', 'sr-el', 'shi', 'shi-tfng', 'shi-latn', 'sh-latn', 'sh-cyrl', 'ku', 'ku-arab', 'ku-latn', 'iu', 'ike-cans', 'ike-latn', 'gan', 'gan-hans', 'gan-hant', 'en', 'en-x-piglatin', 'crh', 'crh-cyrl', 'crh-latn', 'ban', 'ban-bali', 'ban-x-dharma', 'ban-x-palmleaf', 'ban-x-pku'}
    magic_vars_i = {'ARTICLEPATH', 'INT', 'PAGEID', 'SCRIPTPATH', 'SERVER', 'SERVERNAME', 'STYLEPATH'}
    magic_vars = {'!', '=', 'BASEPAGENAME', 'BASEPAGENAMEE', 'CASCADINGSOURCES', 'CONTENTLANGUAGE', 'CONTENTLANG', 'CURRENTDAY', 'CURRENTDAY2', 'CURRENTDAYNAME', 'CURRENTDOW', 'CURRENTHOUR', 'CURRENTMONTH', 'CURRENTMONTH2', 'CURRENTMONTH1', 'CURRENTMONTHABBREV', 'CURRENTMONTHNAME', 'CURRENTMONTHNAMEGEN', 'CURRENTTIME', 'CURRENTTIMESTAMP', 'CURRENTVERSION', 'CURRENTWEEK', 'CURRENTYEAR', 'DIRECTIONMARK', 'DIRMARK', 'FULLPAGENAME', 'FULLPAGENAMEE', 'LOCALDAY', 'LOCALDAY2', 'LOCALDAYNAME', 'LOCALDOW', 'LOCALHOUR', 'LOCALMONTH', 'LOCALMONTH2', 'LOCALMONTH1', 'LOCALMONTHABBREV', 'LOCALMONTHNAME', 'LOCALMONTHNAMEGEN', 'LOCALTIME', 'LOCALTIMESTAMP', 'LOCALWEEK', 'LOCALYEAR', 'NAMESPACE', 'NAMESPACEE', 'NAMESPACENUMBER', 'NUMBEROFACTIVEUSERS', 'NUMBEROFADMINS', 'NUMBEROFARTICLES', 'NUMBEROFEDITS', 'NUMBEROFFILES', 'NUMBEROFPAGES', 'NUMBEROFUSERS', 'PAGELANGUAGE', 'PAGENAME', 'PAGENAMEE', 'REVISIONDAY', 'REVISIONDAY2', 'REVISIONID', 'REVISIONMONTH', 'REVISIONMONTH1', 'REVISIONSIZE', 'REVISIONTIMESTAMP', 'REVISIONUSER', 'REVISIONYEAR', 'ROOTPAGENAME', 'ROOTPAGENAMEE', 'SITENAME', 'SUBJECTPAGENAME', 'ARTICLEPAGENAME', 'SUBJECTPAGENAMEE', 'ARTICLEPAGENAMEE', 'SUBJECTSPACE', 'ARTICLESPACE', 'SUBJECTSPACEE', 'ARTICLESPACEE', 'SUBPAGENAME', 'SUBPAGENAMEE', 'TALKPAGENAME', 'TALKPAGENAMEE', 'TALKSPACE', 'TALKSPACEE'}
    parser_functions_i = {'ANCHORENCODE', 'BIDI', 'CANONICALURL', 'CANONICALURLE', 'FILEPATH', 'FORMATNUM', 'FULLURL', 'FULLURLE', 'GENDER', 'GRAMMAR', 'INT', '\\#LANGUAGE', 'LC', 'LCFIRST', 'LOCALURL', 'LOCALURLE', 'NS', 'NSE', 'PADLEFT', 'PADRIGHT', 'PAGEID', 'PLURAL', 'UC', 'UCFIRST', 'URLENCODE'}
    parser_functions = {'BASEPAGENAME', 'BASEPAGENAMEE', 'CASCADINGSOURCES', 'DEFAULTSORT', 'DEFAULTSORTKEY', 'DEFAULTCATEGORYSORT', 'FULLPAGENAME', 'FULLPAGENAMEE', 'NAMESPACE', 'NAMESPACEE', 'NAMESPACENUMBER', 'NUMBERINGROUP', 'NUMINGROUP', 'NUMBEROFACTIVEUSERS', 'NUMBEROFADMINS', 'NUMBEROFARTICLES', 'NUMBEROFEDITS', 'NUMBEROFFILES', 'NUMBEROFPAGES', 'NUMBEROFUSERS', 'PAGENAME', 'PAGENAMEE', 'PAGESINCATEGORY', 'PAGESINCAT', 'PAGESIZE', 'PROTECTIONEXPIRY', 'PROTECTIONLEVEL', 'REVISIONDAY', 'REVISIONDAY2', 'REVISIONID', 'REVISIONMONTH', 'REVISIONMONTH1', 'REVISIONTIMESTAMP', 'REVISIONUSER', 'REVISIONYEAR', 'ROOTPAGENAME', 'ROOTPAGENAMEE', 'SUBJECTPAGENAME', 'ARTICLEPAGENAME', 'SUBJECTPAGENAMEE', 'ARTICLEPAGENAMEE', 'SUBJECTSPACE', 'ARTICLESPACE', 'SUBJECTSPACEE', 'ARTICLESPACEE', 'SUBPAGENAME', 'SUBPAGENAMEE', 'TALKPAGENAME', 'TALKPAGENAMEE', 'TALKSPACE', 'TALKSPACEE', 'INT', 'DISPLAYTITLE', 'PAGESINNAMESPACE', 'PAGESINNS'}
    tokens = {'root': [('(?xi)\n                (\\A\\s*?)(\\#REDIRECT:?) # may contain a colon\n                (\\s+)(\\[\\[) (?=[^\\]\\n]* \\]\\]$)\n            ', bygroups(Whitespace, Keyword, Whitespace, Punctuation), 'redirect-inner'), ('^(={2,6})(.+?)(\\1)(\\s*$\\n)', bygroups(Generic.Subheading, Generic.Subheading, Generic.Subheading, Whitespace)), ('^(=.+?=)(\\s*$\\n)', bygroups(Generic.Heading, Whitespace)), (words(double_slashes_i, prefix='(?i)'), Name.Function.Magic), (words(double_slashes), Name.Function.Magic), ('(?i)\\b(?:{}){}{}*'.format('|'.join(protocols), link_address, link_char_class), Name.Label), (f'\\b(?:RFC|PMID){nbsp_char}+[0-9]+\\b', Name.Function.Magic), ('(?x)\n                \\bISBN {nbsp_char}\n                (?: 97[89] {nbsp_dash}? )?\n                (?: [0-9] {nbsp_dash}? ){{9}} # escape format()\n                [0-9Xx]\\b\n            '.format(nbsp_char=nbsp_char, nbsp_dash=f'(?:-|{nbsp_char})'), Name.Function.Magic), include('list'), include('inline'), include('text')], 'redirect-inner': [('(\\]\\])(\\s*?\\n)', bygroups(Punctuation, Whitespace), '#pop'), ('(\\#)([^#]*?)', bygroups(Punctuation, Name.Label)), (f'(?i)[{title_char}]+', Name.Tag)], 'list': [('^;', Keyword, 'dt'), ('^[#:*]+', Keyword), ('^-{4,}', Keyword)], 'inline': [('~{3,5}', Keyword), include('entity'), ("('')(''')(?!')", bygroups(Generic.Emph, Generic.EmphStrong), 'inline-italic-bold'), ("'''(?!')", Generic.Strong, 'inline-bold'), ("''(?!')", Generic.Emph, 'inline-italic'), include('replaceable'), ('(?xi)\n                (\\[\\[)\n                    (File|Image) (:)\n                    ((?: [{}] | \\{{{{2,3}}[^{{}}]*?\\}}{{2,3}} | <!--[\\s\\S]*?--> )*)\n                    (?: (\\#) ([{}]*?) )?\n                '.format(title_char, f'{title_char}#'), bygroups(Punctuation, Name.Namespace, Punctuation, using(this, state=['wikilink-name']), Punctuation, Name.Label), 'medialink-inner'), ('(?xi)\n                (\\[\\[)(?!{}) # Should not contain URLs\n                    (?: ([{}]*) (:))?\n                    ((?: [{}] | \\{{{{2,3}}[^{{}}]*?\\}}{{2,3}} | <!--[\\s\\S]*?--> )*?)\n                    (?: (\\#) ([{}]*?) )?\n                (\\]\\])\n                '.format('|'.join(protocols), title_char.replace('/', ''), title_char, f'{title_char}#'), bygroups(Punctuation, Name.Namespace, Punctuation, using(this, state=['wikilink-name']), Punctuation, Name.Label, Punctuation)), ('(?xi)\n                (\\[\\[)(?!{})\n                    (?: ([{}]*) (:))?\n                    ((?: [{}] | \\{{{{2,3}}[^{{}}]*?\\}}{{2,3}} | <!--[\\s\\S]*?--> )*?)\n                    (?: (\\#) ([{}]*?) )?\n                    (\\|)\n                '.format('|'.join(protocols), title_char.replace('/', ''), title_char, f'{title_char}#'), bygroups(Punctuation, Name.Namespace, Punctuation, using(this, state=['wikilink-name']), Punctuation, Name.Label, Punctuation), 'wikilink-inner'), ('(?xi)\n                (\\[)\n                    ((?:{}) {} {}*)\n                    (\\s*)\n                '.format('|'.join(protocols), link_address, link_char_class), bygroups(Punctuation, Name.Label, Whitespace), 'extlink-inner'), ('^(:*)(\\s*?)(\\{\\|)([^\\n]*)$', bygroups(Keyword, Whitespace, Punctuation, using(this, state=['root', 'attr'])), 'table'), ('(?i)(<)({})\\b'.format('|'.join(html_tags)), bygroups(Punctuation, Name.Tag), 'tag-inner-ordinary'), ('(?i)(</)({})\\b(\\s*)(>)'.format('|'.join(html_tags)), bygroups(Punctuation, Name.Tag, Whitespace, Punctuation)), ('(?i)(<)(nowiki)\\b', bygroups(Punctuation, Name.Tag), ('tag-nowiki', 'tag-inner')), ('(?i)(<)(pre)\\b', bygroups(Punctuation, Name.Tag), ('tag-pre', 'tag-inner')), ('(?i)(<)(categorytree)\\b', bygroups(Punctuation, Name.Tag), ('tag-categorytree', 'tag-inner')), ('(?i)(<)(hiero)\\b', bygroups(Punctuation, Name.Tag), ('tag-hiero', 'tag-inner')), ('(?i)(<)(math)\\b', bygroups(Punctuation, Name.Tag), ('tag-math', 'tag-inner')), ('(?i)(<)(chem)\\b', bygroups(Punctuation, Name.Tag), ('tag-chem', 'tag-inner')), ('(?i)(<)(ce)\\b', bygroups(Punctuation, Name.Tag), ('tag-ce', 'tag-inner')), ('(?i)(<)(charinsert)\\b', bygroups(Punctuation, Name.Tag), ('tag-charinsert', 'tag-inner')), ('(?i)(<)(templatedata)\\b', bygroups(Punctuation, Name.Tag), ('tag-templatedata', 'tag-inner')), ('(?i)(<)(gallery)\\b', bygroups(Punctuation, Name.Tag), ('tag-gallery', 'tag-inner')), ('(?i)(<)(gallery)\\b', bygroups(Punctuation, Name.Tag), ('tag-graph', 'tag-inner')), ('(?i)(<)(dynamicpagelist)\\b', bygroups(Punctuation, Name.Tag), ('tag-dynamicpagelist', 'tag-inner')), ('(?i)(<)(inputbox)\\b', bygroups(Punctuation, Name.Tag), ('tag-inputbox', 'tag-inner')), ('(?i)(<)(rss)\\b', bygroups(Punctuation, Name.Tag), ('tag-rss', 'tag-inner')), ('(?i)(<)(imagemap)\\b', bygroups(Punctuation, Name.Tag), ('tag-imagemap', 'tag-inner')), ('(?i)(</)(syntaxhighlight)\\b(\\s*)(>)', bygroups(Punctuation, Name.Tag, Whitespace, Punctuation)), ('(?si)(<)(syntaxhighlight)\\b([^>]*?(?<!/)>.*?)(?=</\\2\\s*>)', bygroups(Punctuation, Name.Tag, handle_syntaxhighlight)), ('(?i)(<)(syntaxhighlight)\\b(\\s*?)((?:[^>]|-->)*?)(/\\s*?(?<!--)>)', bygroups(Punctuation, Name.Tag, Whitespace, using(this, state=['root', 'attr']), Punctuation)), ('(?i)(</)(source)\\b(\\s*)(>)', bygroups(Punctuation, Name.Tag, Whitespace, Punctuation)), ('(?si)(<)(source)\\b([^>]*?(?<!/)>.*?)(?=</\\2\\s*>)', bygroups(Punctuation, Name.Tag, handle_syntaxhighlight)), ('(?i)(<)(source)\\b(\\s*?)((?:[^>]|-->)*?)(/\\s*?(?<!--)>)', bygroups(Punctuation, Name.Tag, Whitespace, using(this, state=['root', 'attr']), Punctuation)), ('(?i)(</)(score)\\b(\\s*)(>)', bygroups(Punctuation, Name.Tag, Whitespace, Punctuation)), ('(?si)(<)(score)\\b([^>]*?(?<!/)>.*?)(?=</\\2\\s*>)', bygroups(Punctuation, Name.Tag, handle_score)), ('(?i)(<)(score)\\b(\\s*?)((?:[^>]|-->)*?)(/\\s*?(?<!--)>)', bygroups(Punctuation, Name.Tag, Whitespace, using(this, state=['root', 'attr']), Punctuation)), ('(?i)(<)({})\\b'.format('|'.join(parser_tags)), bygroups(Punctuation, Name.Tag), 'tag-inner-ordinary'), ('(?i)(</)({})\\b(\\s*)(>)'.format('|'.join(parser_tags)), bygroups(Punctuation, Name.Tag, Whitespace, Punctuation)), ('(?xi)\n                (-\\{{) # Use {{ to escape format()\n                    ([^|]) (\\|)\n                    (?:\n                        (?: ([^;]*?) (=>))?\n                        (\\s* (?:{variants}) \\s*) (:)\n                    )?\n                '.format(variants='|'.join(variant_langs)), bygroups(Punctuation, Keyword, Punctuation, using(this, state=['root', 'lc-raw']), Operator, Name.Label, Punctuation), 'lc-inner'), ('(?xi)\n                (-\\{)\n                    ([a-z\\s;-]*?) (\\|)\n                ', bygroups(Punctuation, using(this, state=['root', 'lc-flag']), Punctuation), 'lc-raw'), ('(?xi)\n                (-\\{{) (?!\\{{) # Use {{ to escape format()\n                    (?: (\\s* (?:{variants}) \\s*) (:))?\n                '.format(variants='|'.join(variant_langs)), bygroups(Punctuation, Name.Label, Punctuation), 'lc-inner')], 'wikilink-name': [include('replaceable'), ('[^{<]+', Name.Tag), ('(?s).', Name.Tag)], 'wikilink-inner': [('(?=\\[\\[)', Punctuation, '#pop'), ('\\]\\]', Punctuation, '#pop'), include('inline'), include('text')], 'medialink-inner': [('\\]\\]', Punctuation, '#pop'), ('(\\|)([^\\n=|]*)(=)', bygroups(Punctuation, Name.Attribute, Operator)), ('\\|', Punctuation), include('inline'), include('text')], 'quote-common': [('(?=\\]\\]|\\{\\{|\\}\\})', Punctuation, '#pop'), ('\\n', Text, '#pop')], 'inline-italic': [include('quote-common'), ("('')(''')(?!')", bygroups(Generic.Emph, Generic.Strong), ('#pop', 'inline-bold')), ("'''(?!')", Generic.EmphStrong, ('#pop', 'inline-italic-bold')), ("''(?!')", Generic.Emph, '#pop'), include('inline'), include('text-italic')], 'inline-bold': [include('quote-common'), ("(''')('')(?!')", bygroups(Generic.Strong, Generic.Emph), ('#pop', 'inline-italic')), ("'''(?!')", Generic.Strong, '#pop'), ("''(?!')", Generic.EmphStrong, ('#pop', 'inline-bold-italic')), include('inline'), include('text-bold')], 'inline-bold-italic': [include('quote-common'), ("('')(''')(?!')", bygroups(Generic.EmphStrong, Generic.Strong), '#pop'), ("'''(?!')", Generic.EmphStrong, ('#pop', 'inline-italic')), ("''(?!')", Generic.EmphStrong, ('#pop', 'inline-bold')), include('inline'), include('text-bold-italic')], 'inline-italic-bold': [include('quote-common'), ("(''')('')(?!')", bygroups(Generic.EmphStrong, Generic.Emph), '#pop'), ("'''(?!')", Generic.EmphStrong, ('#pop', 'inline-italic')), ("''(?!')", Generic.EmphStrong, ('#pop', 'inline-bold')), include('inline'), include('text-bold-italic')], 'lc-flag': [('\\s+', Whitespace), (';', Punctuation), *text_rules(Keyword)], 'lc-inner': [('(?xi)\n                (;)\n                (?: ([^;]*?) (=>))?\n                (\\s* (?:{variants}) \\s*) (:)\n                '.format(variants='|'.join(variant_langs)), bygroups(Punctuation, using(this, state=['root', 'lc-raw']), Operator, Name.Label, Punctuation)), (';?\\s*?\\}-', Punctuation, '#pop'), include('inline'), include('text')], 'lc-raw': [('\\}-', Punctuation, '#pop'), include('inline'), include('text')], 'replaceable': [('<!--[\\s\\S]*?(?:-->|\\Z)', Comment.Multiline), ('(?x)\n                (\\{{3})\n                    ([^|]*?)\n                    (?=\\}{3}|\\|)\n                ', bygroups(Punctuation, Name.Variable), 'parameter-inner'), ('(?i)(\\{{\\{{)(\\s*)({})(\\s*)(\\}}\\}})'.format('|'.join(magic_vars_i)), bygroups(Punctuation, Whitespace, Name.Function, Whitespace, Punctuation)), ('(\\{{\\{{)(\\s*)({})(\\s*)(\\}}\\}})'.format('|'.join(magic_vars)), bygroups(Punctuation, Whitespace, Name.Function, Whitespace, Punctuation)), ('\\{\\{', Punctuation, 'template-begin-space'), ('(?i)(<)(tvar)\\b(\\|)([^>]*?)(>)', bygroups(Punctuation, Name.Tag, Punctuation, String, Punctuation)), ('</>', Punctuation, '#pop'), ('(?i)(<)(tvar)\\b', bygroups(Punctuation, Name.Tag), 'tag-inner-ordinary'), ('(?i)(</)(tvar)\\b(\\s*)(>)', bygroups(Punctuation, Name.Tag, Whitespace, Punctuation))], 'parameter-inner': [('\\}{3}', Punctuation, '#pop'), ('\\|', Punctuation), include('inline'), include('text')], 'template-begin-space': [('<!--[\\s\\S]*?(?:-->|\\Z)', Comment.Multiline), ('\\s+', Whitespace), ('(?i)(\\#[{}]*?|{})(:)'.format(title_char, '|'.join(parser_functions_i)), bygroups(Name.Function, Punctuation), ('#pop', 'template-inner')), ('({})(:)'.format('|'.join(parser_functions)), bygroups(Name.Function, Punctuation), ('#pop', 'template-inner')), (f'(?i)([{title_char}]*?)(:)', bygroups(Name.Namespace, Punctuation), ('#pop', 'template-name')), default(('#pop', 'template-name'))], 'template-name': [('(\\s*?)(\\|)', bygroups(Text, Punctuation), ('#pop', 'template-inner')), ('\\}\\}', Punctuation, '#pop'), ('\\n', Text, '#pop'), include('replaceable'), *text_rules(Name.Tag)], 'template-inner': [('\\}\\}', Punctuation, '#pop'), ('\\|', Punctuation), ('(?x)\n                    (?<=\\|)\n                    ( (?: (?! \\{\\{ | \\}\\} )[^=\\|<])*? ) # Exclude templates and tags\n                    (=)\n                ', bygroups(Name.Label, Operator)), include('inline'), include('text')], 'table': [('^([ \\t\\n\\r\\0\\x0B]*?)(\\|\\})', bygroups(Whitespace, Punctuation), '#pop'), ('^([ \\t\\n\\r\\0\\x0B]*?)(\\|-+)(.*)$', bygroups(Whitespace, Punctuation, using(this, state=['root', 'attr']))), ('(?x)\n                ^([ \\t\\n\\r\\0\\x0B]*?)(\\|\\+)\n                # Exclude links, template and tags\n                (?: ( (?: (?! \\[\\[ | \\{\\{ )[^|\\n<] )*? )(\\|) )?\n                (.*?)$\n                ', bygroups(Whitespace, Punctuation, using(this, state=['root', 'attr']), Punctuation, Generic.Heading)), ('(?x)\n                ( ^(?:[ \\t\\n\\r\\0\\x0B]*?)\\| | \\|\\| )\n                (?: ( (?: (?! \\[\\[ | \\{\\{ )[^|\\n<] )*? )(\\|)(?!\\|) )?\n                ', bygroups(Punctuation, using(this, state=['root', 'attr']), Punctuation)), ('(?x)\n                ( ^(?:[ \\t\\n\\r\\0\\x0B]*?)!  )\n                (?: ( (?: (?! \\[\\[ | \\{\\{ )[^|\\n<] )*? )(\\|)(?!\\|) )?\n                ', bygroups(Punctuation, using(this, state=['root', 'attr']), Punctuation), 'table-header'), include('list'), include('inline'), include('text')], 'table-header': [('\\n', Text, '#pop'), ('(?x)\n                (!!|\\|\\|)\n                (?:\n                    ( (?: (?! \\[\\[ | \\{\\{ )[^|\\n<] )*? )\n                    (\\|)(?!\\|)\n                )?\n                ', bygroups(Punctuation, using(this, state=['root', 'attr']), Punctuation)), *text_rules(Generic.Subheading)], 'entity': [('&\\S*?;', Name.Entity)], 'dt': [('\\n', Text, '#pop'), include('inline'), (':', Keyword, '#pop'), include('text')], 'extlink-inner': [('\\]', Punctuation, '#pop'), include('inline'), include('text')], 'nowiki-ish': [include('entity'), include('text')], 'attr': [include('replaceable'), ('\\s+', Whitespace), ('(=)(\\s*)(")', bygroups(Operator, Whitespace, String.Double), 'attr-val-2'), ("(=)(\\s*)(')", bygroups(Operator, Whitespace, String.Single), 'attr-val-1'), ('(=)(\\s*)', bygroups(Operator, Whitespace), 'attr-val-0'), ('[\\w:-]+', Name.Attribute)], 'attr-val-0': [('\\s', Whitespace, '#pop'), include('replaceable'), *text_rules(String)], 'attr-val-1': [("'", String.Single, '#pop'), include('replaceable'), *text_rules(String.Single)], 'attr-val-2': [('"', String.Double, '#pop'), include('replaceable'), *text_rules(String.Double)], 'tag-inner-ordinary': [('/?\\s*>', Punctuation, '#pop'), include('tag-attr')], 'tag-inner': [('/\\s*>', Punctuation, '#pop:2'), ('\\s*>', Punctuation, '#pop'), include('tag-attr')], 'tag-attr': [include('replaceable'), ('\\s+', Whitespace), ('(=)(\\s*)(")', bygroups(Operator, Whitespace, String.Double), 'tag-attr-val-2'), ("(=)(\\s*)(')", bygroups(Operator, Whitespace, String.Single), 'tag-attr-val-1'), ('(=)(\\s*)', bygroups(Operator, Whitespace), 'tag-attr-val-0'), ('[\\w:-]+', Name.Attribute)], 'tag-attr-val-0': [('\\s', Whitespace, '#pop'), ('/?>', Punctuation, '#pop:2'), include('replaceable'), *text_rules(String)], 'tag-attr-val-1': [("'", String.Single, '#pop'), ('/?>', Punctuation, '#pop:2'), include('replaceable'), *text_rules(String.Single)], 'tag-attr-val-2': [('"', String.Double, '#pop'), ('/?>', Punctuation, '#pop:2'), include('replaceable'), *text_rules(String.Double)], 'tag-nowiki': nowiki_tag_rules('nowiki'), 'tag-pre': nowiki_tag_rules('pre'), 'tag-categorytree': plaintext_tag_rules('categorytree'), 'tag-dynamicpagelist': plaintext_tag_rules('dynamicpagelist'), 'tag-hiero': plaintext_tag_rules('hiero'), 'tag-inputbox': plaintext_tag_rules('inputbox'), 'tag-imagemap': plaintext_tag_rules('imagemap'), 'tag-charinsert': plaintext_tag_rules('charinsert'), 'tag-timeline': plaintext_tag_rules('timeline'), 'tag-gallery': plaintext_tag_rules('gallery'), 'tag-graph': plaintext_tag_rules('graph'), 'tag-rss': plaintext_tag_rules('rss'), 'tag-math': delegate_tag_rules('math', TexLexer, state='math'), 'tag-chem': delegate_tag_rules('chem', TexLexer, state='math'), 'tag-ce': delegate_tag_rules('ce', TexLexer, state='math'), 'tag-templatedata': delegate_tag_rules('templatedata', JsonLexer), 'text-italic': text_rules(Generic.Emph), 'text-bold': text_rules(Generic.Strong), 'text-bold-italic': text_rules(Generic.EmphStrong), 'text': text_rules(Text)}


