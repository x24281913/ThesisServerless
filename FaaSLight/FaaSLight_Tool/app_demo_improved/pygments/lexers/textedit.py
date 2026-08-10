"""
    pygments.lexers.textedit
    ~~~~~~~~~~~~~~~~~~~~~~~~

    Lexers for languages related to text processing.

    :copyright: Copyright 2006-present by the Pygments team, see AUTHORS.
    :license: BSD, see LICENSE for details.
"""

import re
from bisect import bisect
from pygments.lexer import RegexLexer, bygroups, default, include, this, using
from pygments.lexers.python import PythonLexer
from pygments.token import Comment, Keyword, Name, Number, Operator, Punctuation, String, Text, Whitespace
__all__ = ['AwkLexer', 'SedLexer', 'VimLexer']


class AwkLexer(RegexLexer):
    """
    For Awk scripts.
    """
    name = 'Awk'
    aliases = ['awk', 'gawk', 'mawk', 'nawk']
    filenames = ['*.awk']
    mimetypes = ['application/x-awk']
    url = 'https://en.wikipedia.org/wiki/AWK'
    version_added = '1.5'
    tokens = {'commentsandwhitespace': [('\\s+', Text), ('#.*$', Comment.Single)], 'slashstartsregex': [include('commentsandwhitespace'), ('/(\\\\.|[^[/\\\\\\n]|\\[(\\\\.|[^\\]\\\\\\n])*])+/\\B', String.Regex, '#pop'), ('(?=/)', Text, ('#pop', 'badregex')), default('#pop')], 'badregex': [('\\n', Text, '#pop')], 'root': [('^(?=\\s|/)', Text, 'slashstartsregex'), include('commentsandwhitespace'), ('\\+\\+|--|\\|\\||&&|in\\b|\\$|!?~|\\?|:|(\\*\\*|[-<>+*%\\^/!=|])=?', Operator, 'slashstartsregex'), ('[{(\\[;,]', Punctuation, 'slashstartsregex'), ('[})\\].]', Punctuation), ('(break|continue|do|while|exit|for|if|else|return)\\b', Keyword, 'slashstartsregex'), ('function\\b', Keyword.Declaration, 'slashstartsregex'), ('(atan2|cos|exp|int|log|rand|sin|sqrt|srand|gensub|gsub|index|length|match|split|sprintf|sub|substr|tolower|toupper|close|fflush|getline|next|nextfile|print|printf|strftime|systime|delete|system)\\b', Keyword.Reserved), ('(ARGC|ARGIND|ARGV|BEGIN|CONVFMT|ENVIRON|END|ERRNO|FIELDWIDTHS|FILENAME|FNR|FS|IGNORECASE|NF|NR|OFMT|OFS|ORFS|RLENGTH|RS|RSTART|RT|SUBSEP)\\b', Name.Builtin), ('[$a-zA-Z_]\\w*', Name.Other), ('[0-9][0-9]*\\.[0-9]+([eE][0-9]+)?[fd]?', Number.Float), ('0x[0-9a-fA-F]+', Number.Hex), ('[0-9]+', Number.Integer), ('"(\\\\\\\\|\\\\[^\\\\]|[^"\\\\])*"', String.Double), ("'(\\\\\\\\|\\\\[^\\\\]|[^'\\\\])*'", String.Single)]}



class SedLexer(RegexLexer):
    """
    Lexer for Sed script files.
    """
    name = 'Sed'
    aliases = ['sed', 'gsed', 'ssed']
    filenames = ['*.sed', '*.[gs]sed']
    mimetypes = ['text/x-sed']
    url = 'https://en.wikipedia.org/wiki/Sed'
    version_added = ''
    flags = re.MULTILINE
    _inside_delims = '((?:(?:\\\\[^\\n]|[^\\\\])*?\\\\\\n)*?(?:\\\\.|[^\\\\])*?)'
    tokens = {'root': [('\\s+', Whitespace), ('#.*$', Comment.Single), ('[0-9]+', Number.Integer), ('\\$', Operator), ('[{};,!]', Punctuation), ('[dDFgGhHlnNpPqQxz=]', Keyword), ('([berRtTvwW:])([^;\\n]*)', bygroups(Keyword, String.Single)), ('([aci])((?:.*?\\\\\\n)*(?:.*?[^\\\\]$))', bygroups(Keyword, String.Double)), ('([qQ])([0-9]*)', bygroups(Keyword, Number.Integer)), ('(/)' + _inside_delims + '(/)', bygroups(Punctuation, String.Regex, Punctuation)), ('(\\\\(.))' + _inside_delims + '(\\2)', bygroups(Punctuation, None, String.Regex, Punctuation)), ('(y)(.)' + _inside_delims + '(\\2)' + _inside_delims + '(\\2)', bygroups(Keyword, Punctuation, String.Single, Punctuation, String.Single, Punctuation)), ('(s)(.)' + _inside_delims + '(\\2)' + _inside_delims + '(\\2)((?:[gpeIiMm]|[0-9])*)', bygroups(Keyword, Punctuation, String.Regex, Punctuation, String.Single, Punctuation, Keyword))]}



class VimLexer(RegexLexer):
    """
    Lexer for VimL script files.
    """
    name = 'VimL'
    aliases = ['vim']
    filenames = ['*.vim', '.vimrc', '.exrc', '.gvimrc', '_vimrc', '_exrc', '_gvimrc', 'vimrc', 'gvimrc']
    mimetypes = ['text/x-vim']
    url = 'https://www.vim.org'
    version_added = '0.8'
    flags = re.MULTILINE
    _python = 'py(?:t(?:h(?:o(?:n)?)?)?)?'
    tokens = {'root': [('^([ \\t:]*)(' + _python + ')([ \\t]*)(<<)([ \\t]*)(.*)((?:\\n|.)*)(\\6)', bygroups(using(this), Keyword, Text, Operator, Text, Text, using(PythonLexer), Text)), ('^([ \\t:]*)(' + _python + ')([ \\t])(.*)', bygroups(using(this), Keyword, Text, using(PythonLexer))), ('^\\s*".*', Comment), ('[ \\t]+', Text), ('/[^/\\\\\\n]*(?:\\\\[\\s\\S][^/\\\\\\n]*)*/', String.Regex), ('"[^"\\\\\\n]*(?:\\\\[\\s\\S][^"\\\\\\n]*)*"', String.Double), ("'[^\\n']*(?:''[^\\n']*)*'", String.Single), ('(?<=\\s)"[^\\-:.%#=*].*', Comment), ('-?\\d+', Number), ('#[0-9a-f]{6}', Number.Hex), ('^:', Punctuation), ('[()<>+=!|,~-]', Punctuation), ('\\b(let|if|else|endif|elseif|fun|function|endfunction)\\b', Keyword), ('\\b(NONE|bold|italic|underline|dark|light)\\b', Name.Builtin), ('\\b\\w+\\b', Name.Other), ('.', Text)]}
    
    def __init__(self, **options):
        from pygments.lexers._vim_builtins import auto, command, option
        self._cmd = command
        self._opt = option
        self._aut = auto
        RegexLexer.__init__(self, **options)
    
    def is_in(self, w, mapping):
        """
        It's kind of difficult to decide if something might be a keyword
        in VimL because it allows you to abbreviate them.  In fact,
        'ab[breviate]' is a good example.  :ab, :abbre, or :abbreviate are
        valid ways to call it so rather than making really awful regexps
        like::

            ab(?:b(?:r(?:e(?:v(?:i(?:a(?:t(?:e)?)?)?)?)?)?)?)?

        we match `\w+` and then call is_in() on those tokens.  See
        `scripts/get_vimkw.py` for how the lists are extracted.
        """
        p = bisect(mapping, (w, ))
        if p > 0:
            if (mapping[p - 1][0] == w[:len(mapping[p - 1][0])] and mapping[p - 1][1][:len(w)] == w):
                return True
        if p < len(mapping):
            return (mapping[p][0] == w[:len(mapping[p][0])] and mapping[p][1][:len(w)] == w)
        return False
    
    def get_tokens_unprocessed(self, text):
        for (index, token, value) in RegexLexer.get_tokens_unprocessed(self, text):
            if token is Name.Other:
                if self.is_in(value, self._cmd):
                    yield (index, Keyword, value)
                elif (self.is_in(value, self._opt) or self.is_in(value, self._aut)):
                    yield (index, Name.Builtin, value)
                else:
                    yield (index, Text, value)
            else:
                yield (index, token, value)


