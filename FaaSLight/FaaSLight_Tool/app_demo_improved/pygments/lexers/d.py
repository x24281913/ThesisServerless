"""
    pygments.lexers.d
    ~~~~~~~~~~~~~~~~~

    Lexers for D languages.

    :copyright: Copyright 2006-present by the Pygments team, see AUTHORS.
    :license: BSD, see LICENSE for details.
"""

from pygments.lexer import RegexLexer, include, words, bygroups
from pygments.token import Comment, Keyword, Name, String, Number, Punctuation, Whitespace
__all__ = ['DLexer', 'CrocLexer', 'MiniDLexer']


class DLexer(RegexLexer):
    """
    For D source.
    """
    name = 'D'
    url = 'https://dlang.org/'
    filenames = ['*.d', '*.di']
    aliases = ['d']
    mimetypes = ['text/x-dsrc']
    version_added = '1.2'
    tokens = {'root': [('\\n', Whitespace), ('\\s+', Whitespace), ('(//.*?)(\\n)', bygroups(Comment.Single, Whitespace)), ('/(\\\\\\n)?[*](.|\\n)*?[*](\\\\\\n)?/', Comment.Multiline), ('/\\+', Comment.Multiline, 'nested_comment'), (words(('abstract', 'alias', 'align', 'asm', 'assert', 'auto', 'body', 'break', 'case', 'cast', 'catch', 'class', 'const', 'continue', 'debug', 'default', 'delegate', 'delete', 'deprecated', 'do', 'else', 'enum', 'export', 'extern', 'finally', 'final', 'foreach_reverse', 'foreach', 'for', 'function', 'goto', 'if', 'immutable', 'import', 'interface', 'invariant', 'inout', 'in', 'is', 'lazy', 'mixin', 'module', 'new', 'nothrow', 'out', 'override', 'package', 'pragma', 'private', 'protected', 'public', 'pure', 'ref', 'return', 'scope', 'shared', 'static', 'struct', 'super', 'switch', 'synchronized', 'template', 'this', 'throw', 'try', 'typeid', 'typeof', 'union', 'unittest', 'version', 'volatile', 'while', 'with', '__gshared', '__traits', '__vector', '__parameters'), suffix='\\b'), Keyword), (words(('typedef', ), suffix='\\b'), Keyword.Removed), (words(('bool', 'byte', 'cdouble', 'cent', 'cfloat', 'char', 'creal', 'dchar', 'double', 'float', 'idouble', 'ifloat', 'int', 'ireal', 'long', 'real', 'short', 'ubyte', 'ucent', 'uint', 'ulong', 'ushort', 'void', 'wchar'), suffix='\\b'), Keyword.Type), ('(false|true|null)\\b', Keyword.Constant), (words(('__FILE__', '__FILE_FULL_PATH__', '__MODULE__', '__LINE__', '__FUNCTION__', '__PRETTY_FUNCTION__', '__DATE__', '__EOF__', '__TIME__', '__TIMESTAMP__', '__VENDOR__', '__VERSION__'), suffix='\\b'), Keyword.Pseudo), ('macro\\b', Keyword.Reserved), ('(string|wstring|dstring|size_t|ptrdiff_t)\\b', Name.Builtin), ('0[xX]([0-9a-fA-F_]*\\.[0-9a-fA-F_]+|[0-9a-fA-F_]+)[pP][+\\-]?[0-9_]+[fFL]?[i]?', Number.Float), ('[0-9_]+(\\.[0-9_]+[eE][+\\-]?[0-9_]+|\\.[0-9_]*|[eE][+\\-]?[0-9_]+)[fFL]?[i]?', Number.Float), ('\\.(0|[1-9][0-9_]*)([eE][+\\-]?[0-9_]+)?[fFL]?[i]?', Number.Float), ('0[Bb][01_]+', Number.Bin), ('0[0-7_]+', Number.Oct), ('0[xX][0-9a-fA-F_]+', Number.Hex), ('(0|[1-9][0-9_]*)([LUu]|Lu|LU|uL|UL)?', Number.Integer), ('\'(\\\\[\'"?\\\\abfnrtv]|\\\\x[0-9a-fA-F]{2}|\\\\[0-7]{1,3}|\\\\u[0-9a-fA-F]{4}|\\\\U[0-9a-fA-F]{8}|\\\\&\\w+;|.)\'', String.Char), ('r"[^"]*"[cwd]?', String), ('`[^`]*`[cwd]?', String), ('"(\\\\\\\\|\\\\[^\\\\]|[^"\\\\])*"[cwd]?', String), ('\\\\([\'\\"?\\\\abfnrtv]|x[0-9a-fA-F]{2}|[0-7]{1,3}|u[0-9a-fA-F]{4}|U[0-9a-fA-F]{8}|&\\w+;)', String), ('x"[0-9a-fA-F_\\s]*"[cwd]?', String), ('q"\\[', String, 'delimited_bracket'), ('q"\\(', String, 'delimited_parenthesis'), ('q"<', String, 'delimited_angle'), ('q"\\{', String, 'delimited_curly'), ('q"([a-zA-Z_]\\w*)\\n.*?\\n\\1"', String), ('q"(.).*?\\1"', String), ('q\\{', String, 'token_string'), ('@([a-zA-Z_]\\w*)?', Name.Decorator), ('(~=|\\^=|%=|\\*=|==|!>=|!<=|!<>=|!<>|!<|!>|!=|>>>=|>>>|>>=|>>|>=|<>=|<>|<<=|<<|<=|\\+\\+|\\+=|--|-=|\\|\\||\\|=|&&|&=|\\.\\.\\.|\\.\\.|/=)|[/.&|\\-+<>!()\\[\\]{}?,;:$=*%^~]', Punctuation), ('[a-zA-Z_]\\w*', Name), ('(#line)(\\s)(.*)(\\n)', bygroups(Comment.Special, Whitespace, Comment.Special, Whitespace))], 'nested_comment': [('[^+/]+', Comment.Multiline), ('/\\+', Comment.Multiline, '#push'), ('\\+/', Comment.Multiline, '#pop'), ('[+/]', Comment.Multiline)], 'token_string': [('\\{', Punctuation, 'token_string_nest'), ('\\}', String, '#pop'), include('root')], 'token_string_nest': [('\\{', Punctuation, '#push'), ('\\}', Punctuation, '#pop'), include('root')], 'delimited_bracket': [('[^\\[\\]]+', String), ('\\[', String, 'delimited_inside_bracket'), ('\\]"', String, '#pop')], 'delimited_inside_bracket': [('[^\\[\\]]+', String), ('\\[', String, '#push'), ('\\]', String, '#pop')], 'delimited_parenthesis': [('[^()]+', String), ('\\(', String, 'delimited_inside_parenthesis'), ('\\)"', String, '#pop')], 'delimited_inside_parenthesis': [('[^()]+', String), ('\\(', String, '#push'), ('\\)', String, '#pop')], 'delimited_angle': [('[^<>]+', String), ('<', String, 'delimited_inside_angle'), ('>"', String, '#pop')], 'delimited_inside_angle': [('[^<>]+', String), ('<', String, '#push'), ('>', String, '#pop')], 'delimited_curly': [('[^{}]+', String), ('\\{', String, 'delimited_inside_curly'), ('\\}"', String, '#pop')], 'delimited_inside_curly': [('[^{}]+', String), ('\\{', String, '#push'), ('\\}', String, '#pop')]}



class CrocLexer(RegexLexer):
    """
    For Croc source.
    """
    name = 'Croc'
    url = 'http://jfbillingsley.com/croc'
    filenames = ['*.croc']
    aliases = ['croc']
    mimetypes = ['text/x-crocsrc']
    version_added = ''
    tokens = {'root': [('\\n', Whitespace), ('\\s+', Whitespace), ('(//.*?)(\\n)', bygroups(Comment.Single, Whitespace)), ('/\\*', Comment.Multiline, 'nestedcomment'), (words(('as', 'assert', 'break', 'case', 'catch', 'class', 'continue', 'default', 'do', 'else', 'finally', 'for', 'foreach', 'function', 'global', 'namespace', 'if', 'import', 'in', 'is', 'local', 'module', 'return', 'scope', 'super', 'switch', 'this', 'throw', 'try', 'vararg', 'while', 'with', 'yield'), suffix='\\b'), Keyword), ('(false|true|null)\\b', Keyword.Constant), ('([0-9][0-9_]*)(?=[.eE])(\\.[0-9][0-9_]*)?([eE][+\\-]?[0-9_]+)?', Number.Float), ('0[bB][01][01_]*', Number.Bin), ('0[xX][0-9a-fA-F][0-9a-fA-F_]*', Number.Hex), ('([0-9][0-9_]*)(?![.eE])', Number.Integer), ('\'(\\\\[\'"\\\\nrt]|\\\\x[0-9a-fA-F]{2}|\\\\[0-9]{1,3}|\\\\u[0-9a-fA-F]{4}|\\\\U[0-9a-fA-F]{8}|.)\'', String.Char), ('@"(""|[^"])*"', String), ('@`(``|[^`])*`', String), ("@'(''|[^'])*'", String), ('"(\\\\\\\\|\\\\[^\\\\]|[^"\\\\])*"', String), ('(~=|\\^=|%=|\\*=|==|!=|>>>=|>>>|>>=|>>|>=|<=>|\\?=|-\\>|<<=|<<|<=|\\+\\+|\\+=|--|-=|\\|\\||\\|=|&&|&=|\\.\\.|/=)|[-/.&$@|\\+<>!()\\[\\]{}?,;:=*%^~#\\\\]', Punctuation), ('[a-zA-Z_]\\w*', Name)], 'nestedcomment': [('[^*/]+', Comment.Multiline), ('/\\*', Comment.Multiline, '#push'), ('\\*/', Comment.Multiline, '#pop'), ('[*/]', Comment.Multiline)]}



class MiniDLexer(CrocLexer):
    """
    For MiniD source. MiniD is now known as Croc.
    """
    name = 'MiniD'
    filenames = []
    aliases = ['minid']
    mimetypes = ['text/x-minidsrc']
    version_added = ''


