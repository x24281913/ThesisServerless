"""
    pygments.lexers.hare
    ~~~~~~~~~~~~~~~~~~~~

    Lexers for the Hare language.

    :copyright: Copyright 2006-present by the Pygments team, see AUTHORS.
    :license: BSD, see LICENSE for details.
"""

from pygments.lexer import RegexLexer, include, words
from pygments.token import Comment, Operator, Keyword, Name, String, Number, Punctuation, Whitespace
__all__ = ['HareLexer']


class HareLexer(RegexLexer):
    """
    Lexer for the Hare programming language.
    """
    name = 'Hare'
    url = 'https://harelang.org/'
    aliases = ['hare']
    filenames = ['*.ha']
    mimetypes = ['text/x-hare']
    version_added = '2.19'
    _ws = '(?:\\s|//.*?\\n|/[*].*?[*]/)+'
    _ws1 = '\\s*(?:/[*].*?[*]/\\s*)?'
    tokens = {'whitespace': [('^use.*;', Comment.Preproc), ('@[a-z]+', Comment.Preproc), ('\\n', Whitespace), ('\\s+', Whitespace), ('//.*?$', Comment.Single)], 'statements': [('"', String, 'string'), ('`[^`]*`', String), ("'(\\\\.|\\\\[0-7]{1,3}|\\\\x[a-fA-F0-9]{1,2}|[^\\\\\\'\\n])'", String.Char), ('(\\d+\\.\\d*|\\.\\d+|\\d+)[eE][+-]?\\d+[LlUu]*', Number.Float), ('(\\d+\\.\\d*|\\.\\d+|\\d+[fF])[fF]?', Number.Float), ('0x[0-9a-fA-F]+[LlUu]*', Number.Hex), ('0o[0-7]+[LlUu]*', Number.Oct), ('\\d+[zui]?(\\d+)?', Number.Integer), ('[~!%^&*+=|?:<>/-]', Operator), (words(('as', 'is', '=>', '..', '...')), Operator), ('[()\\[\\],.{};]+', Punctuation), (words(('abort', 'align', 'alloc', 'append', 'assert', 'case', 'const', 'def', 'defer', 'delete', 'else', 'enum', 'export', 'fn', 'for', 'free', 'if', 'let', 'len', 'match', 'offset', 'return', 'static', 'struct', 'switch', 'type', 'union', 'yield', 'vastart', 'vaarg', 'vaend'), suffix='\\b'), Keyword), ('(bool|int|uint|uintptr|u8|u16|u32|u64|i8|i16|i32|i64|f32|f64|null|done|never|void|nullable|rune|size|valist)\\b', Keyword.Type), ('(true|false|null)\\b', Name.Builtin), ('[a-zA-Z_]\\w*', Name)], 'string': [('"', String, '#pop'), ('\\\\([\\\\abfnrtv"\\\']|x[a-fA-F0-9]{2,4}|u[a-fA-F0-9]{4}|U[a-fA-F0-9]{8}|[0-7]{1,3})', String.Escape), ('[^\\\\"\\n]+', String), ('\\\\', String)], 'root': [include('whitespace'), include('statements')]}


