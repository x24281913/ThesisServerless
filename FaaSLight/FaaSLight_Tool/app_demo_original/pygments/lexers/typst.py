"""
    pygments.lexers.typst
    ~~~~~~~~~~~~~~~~~~~~~

    Lexers for Typst language.

    :copyright: Copyright 2006-present by the Pygments team, see AUTHORS.
    :license: BSD, see LICENSE for details.
"""

from pygments.lexer import RegexLexer, words, bygroups, include
from pygments.token import Comment, Keyword, Name, String, Punctuation, Whitespace, Generic, Operator, Number, Text
from pygments.util import get_choice_opt
__all__ = ['TypstLexer']


class TypstLexer(RegexLexer):
    """
    For Typst code.

    Additional options accepted:

    `start`
        Specifies the starting state of the lexer (one of 'markup', 'math',
        'code'). The default is 'markup'.
    """
    name = 'Typst'
    aliases = ['typst']
    filenames = ['*.typ']
    mimetypes = ['text/x-typst']
    url = 'https://typst.app'
    version_added = '2.18'
    MATH_SHORTHANDS = ('[|', '|]', '||', '*', ':=', '::=', '...', "'", '-', '=:', '!=', '>>', '>=', '>>>', '<<', '<=', '<<<', '->', '|->', '=>', '|=>', '==>', '-->', '~~>', '~>', '>->', '->>', '<-', '<==', '<--', '<~~', '<~', '<-<', '<<-', '<->', '<=>', '<==>', '<-->', '>', '<', '~', ':', '|')
    tokens = {'root': [include('markup')], 'into_code': [(words(('#let', '#set', '#show'), suffix='\\b'), Keyword.Declaration, 'inline_code'), (words(('#import', '#include'), suffix='\\b'), Keyword.Namespace, 'inline_code'), (words(('#if', '#for', '#while', '#export'), suffix='\\b'), Keyword.Reserved, 'inline_code'), ('#\\{', Punctuation, 'code'), ('#\\(', Punctuation, 'code'), ('(#[a-zA-Z_][a-zA-Z0-9_-]*)(\\[)', bygroups(Name.Function, Punctuation), 'markup'), ('(#[a-zA-Z_][a-zA-Z0-9_-]*)(\\()', bygroups(Name.Function, Punctuation), 'code'), (words(('#true', '#false', '#none', '#auto'), suffix='\\b'), Keyword.Constant), ('#[a-zA-Z_][a-zA-Z0-9_]*', Name.Variable), ('#0x[0-9a-fA-F]+', Number.Hex), ('#0b[01]+', Number.Bin), ('#0o[0-7]+', Number.Oct), ('#[0-9]+[\\.e][0-9]+', Number.Float), ('#[0-9]+', Number.Integer)], 'markup': [include('comment'), ('^\\s*=+.*$', Generic.Heading), ('[*][^*]*[*]', Generic.Strong), ('_[^_]*_', Generic.Emph), ('\\$', Punctuation, 'math'), ('`[^`]*`', String.Backtick), ('^(\\s*)(-)(\\s+)', bygroups(Whitespace, Punctuation, Whitespace)), ('^(\\s*)(\\+)(\\s+)', bygroups(Whitespace, Punctuation, Whitespace)), ('^(\\s*)([0-9]+\\.)', bygroups(Whitespace, Punctuation)), ('^(\\s*)(/)(\\s+)([^:]+)(:)', bygroups(Whitespace, Punctuation, Whitespace, Name.Variable, Punctuation)), ('<[a-zA-Z_][a-zA-Z0-9_-]*>', Name.Label), ('@[a-zA-Z_][a-zA-Z0-9_-]*', Name.Label), ('\\\\#', Text), include('into_code'), ('```(?:.|\\n)*?```', String.Backtick), ("https?://[0-9a-zA-Z~/%#&=\\',;.+?]*", Generic.Emph), (words(('---', '\\', '~', '--', '...'), suffix='\\B'), Punctuation), ('\\\\\\[', Punctuation), ('\\\\\\]', Punctuation), ('\\[', Punctuation, '#push'), ('\\]', Punctuation, '#pop'), ('[ \\t]+\\n?|\\n', Whitespace), ('((?![*_$`<@\\\\#\\] ]|https?://).)+', Text)], 'math': [include('comment'), (words(('\\_', '\\^', '\\&')), Text), (words(('_', '^', '&', ';')), Punctuation), (words(('+', '/', '=') + MATH_SHORTHANDS), Operator), ('\\\\', Punctuation), ('\\\\\\$', Punctuation), ('\\$', Punctuation, '#pop'), include('into_code'), ('([a-zA-Z][a-zA-Z0-9-]*)(\\s*)(\\()', bygroups(Name.Function, Whitespace, Punctuation)), ('([a-zA-Z][a-zA-Z0-9-]*)(:)', bygroups(Name.Variable, Punctuation)), ('([a-zA-Z][a-zA-Z0-9-]*)', Name.Variable), ('[0-9]+(\\.[0-9]+)?', Number), ('\\.{1,3}|\\(|\\)|,|\\{|\\}', Punctuation), ('"[^"]*"', String.Double), ('[ \\t\\n]+', Whitespace)], 'comment': [('//.*$', Comment.Single), ('/[*](.|\\n)*?[*]/', Comment.Multiline)], 'code': [include('comment'), ('\\[', Punctuation, 'markup'), ('\\(|\\{', Punctuation, 'code'), ('\\)|\\}', Punctuation, '#pop'), ('"[^"]*"', String.Double), (',|\\.{1,2}', Punctuation), ('=', Operator), (words(('and', 'or', 'not'), suffix='\\b'), Operator.Word), ('=>|<=|==|!=|>|<|-=|\\+=|\\*=|/=|\\+|-|\\\\|\\*', Operator), ('([a-zA-Z_][a-zA-Z0-9_-]*)(:)', bygroups(Name.Variable, Punctuation)), ('([a-zA-Z_][a-zA-Z0-9_-]*)(\\()', bygroups(Name.Function, Punctuation), 'code'), (words(('as', 'break', 'export', 'continue', 'else', 'for', 'if', 'in', 'return', 'while'), suffix='\\b'), Keyword.Reserved), (words(('import', 'include'), suffix='\\b'), Keyword.Namespace), (words(('auto', 'none', 'true', 'false'), suffix='\\b'), Keyword.Constant), ('([0-9.]+)(mm|pt|cm|in|em|fr|%)', bygroups(Number, Keyword.Reserved)), ('0x[0-9a-fA-F]+', Number.Hex), ('0b[01]+', Number.Bin), ('0o[0-7]+', Number.Oct), ('[0-9]+[\\.e][0-9]+', Number.Float), ('[0-9]+', Number.Integer), (words(('let', 'set', 'show'), suffix='\\b'), Keyword.Declaration), ('([a-zA-Z_][a-zA-Z0-9_-]*)', Name.Variable), ('[ \\t\\n]+', Whitespace), (':', Punctuation)], 'inline_code': [(';\\b', Punctuation, '#pop'), ('\\n', Whitespace, '#pop'), include('code')]}
    
    def __init__(self, **options):
        self.start_state = get_choice_opt(options, 'start', ['markup', 'code', 'math'], 'markup', True)
        RegexLexer.__init__(self, **options)
    
    def get_tokens_unprocessed(self, text):
        stack = ['root']
        if self.start_state != 'markup':
            stack.append(self.start_state)
        yield from RegexLexer.get_tokens_unprocessed(self, text, stack)


