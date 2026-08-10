"""
    pygments.lexers.felix
    ~~~~~~~~~~~~~~~~~~~~~

    Lexer for the Felix language.

    :copyright: Copyright 2006-present by the Pygments team, see AUTHORS.
    :license: BSD, see LICENSE for details.
"""

from pygments.lexer import RegexLexer, include, bygroups, default, words, combined
from pygments.token import Text, Comment, Operator, Keyword, Name, String, Number, Punctuation, Whitespace
__all__ = ['FelixLexer']


class FelixLexer(RegexLexer):
    """
    For Felix source code.
    """
    name = 'Felix'
    url = 'http://www.felix-lang.org'
    aliases = ['felix', 'flx']
    filenames = ['*.flx', '*.flxh']
    mimetypes = ['text/x-felix']
    version_added = '1.2'
    preproc = ('elif', 'else', 'endif', 'if', 'ifdef', 'ifndef')
    keywords = ('_', '_deref', 'all', 'as', 'assert', 'attempt', 'call', 'callback', 'case', 'caseno', 'cclass', 'code', 'compound', 'ctypes', 'do', 'done', 'downto', 'elif', 'else', 'endattempt', 'endcase', 'endif', 'endmatch', 'enum', 'except', 'exceptions', 'expect', 'finally', 'for', 'forall', 'forget', 'fork', 'functor', 'goto', 'ident', 'if', 'incomplete', 'inherit', 'instance', 'interface', 'jump', 'lambda', 'loop', 'match', 'module', 'namespace', 'new', 'noexpand', 'nonterm', 'obj', 'of', 'open', 'parse', 'raise', 'regexp', 'reglex', 'regmatch', 'rename', 'return', 'the', 'then', 'to', 'type', 'typecase', 'typedef', 'typematch', 'typeof', 'upto', 'when', 'whilst', 'with', 'yield')
    keyword_directives = ('_gc_pointer', '_gc_type', 'body', 'comment', 'const', 'export', 'header', 'inline', 'lval', 'macro', 'noinline', 'noreturn', 'package', 'private', 'pod', 'property', 'public', 'publish', 'requires', 'todo', 'virtual', 'use')
    keyword_declarations = ('def', 'let', 'ref', 'val', 'var')
    keyword_types = ('unit', 'void', 'any', 'bool', 'byte', 'offset', 'address', 'caddress', 'cvaddress', 'vaddress', 'tiny', 'short', 'int', 'long', 'vlong', 'utiny', 'ushort', 'vshort', 'uint', 'ulong', 'uvlong', 'int8', 'int16', 'int32', 'int64', 'uint8', 'uint16', 'uint32', 'uint64', 'float', 'double', 'ldouble', 'complex', 'dcomplex', 'lcomplex', 'imaginary', 'dimaginary', 'limaginary', 'char', 'wchar', 'uchar', 'charp', 'charcp', 'ucharp', 'ucharcp', 'string', 'wstring', 'ustring', 'cont', 'array', 'varray', 'list', 'lvalue', 'opt', 'slice')
    keyword_constants = ('false', 'true')
    operator_words = ('and', 'not', 'in', 'is', 'isin', 'or', 'xor')
    name_builtins = ('_svc', 'while')
    name_pseudo = ('root', 'self', 'this')
    decimal_suffixes = '([tTsSiIlLvV]|ll|LL|([iIuU])(8|16|32|64))?'
    tokens = {'root': [include('whitespace'), (words(('axiom', 'ctor', 'fun', 'gen', 'proc', 'reduce', 'union'), suffix='\\b'), Keyword, 'funcname'), (words(('class', 'cclass', 'cstruct', 'obj', 'struct'), suffix='\\b'), Keyword, 'classname'), ('(instance|module|typeclass)\\b', Keyword, 'modulename'), (words(keywords, suffix='\\b'), Keyword), (words(keyword_directives, suffix='\\b'), Name.Decorator), (words(keyword_declarations, suffix='\\b'), Keyword.Declaration), (words(keyword_types, suffix='\\b'), Keyword.Type), (words(keyword_constants, suffix='\\b'), Keyword.Constant), include('operators'), ('0[xX]([0-9a-fA-F_]*\\.[0-9a-fA-F_]+|[0-9a-fA-F_]+)[pP][+\\-]?[0-9_]+[lLfFdD]?', Number.Float), ('[0-9_]+(\\.[0-9_]+[eE][+\\-]?[0-9_]+|\\.[0-9_]*|[eE][+\\-]?[0-9_]+)[lLfFdD]?', Number.Float), ('\\.(0|[1-9][0-9_]*)([eE][+\\-]?[0-9_]+)?[lLfFdD]?', Number.Float), (f'0[Bb][01_]+{decimal_suffixes}', Number.Bin), (f'0[0-7_]+{decimal_suffixes}', Number.Oct), (f'0[xX][0-9a-fA-F_]+{decimal_suffixes}', Number.Hex), (f'(0|[1-9][0-9_]*){decimal_suffixes}', Number.Integer), ('([rR][cC]?|[cC][rR])"""', String, 'tdqs'), ("([rR][cC]?|[cC][rR])'''", String, 'tsqs'), ('([rR][cC]?|[cC][rR])"', String, 'dqs'), ("([rR][cC]?|[cC][rR])'", String, 'sqs'), ('[cCfFqQwWuU]?"""', String, combined('stringescape', 'tdqs')), ("[cCfFqQwWuU]?'''", String, combined('stringescape', 'tsqs')), ('[cCfFqQwWuU]?"', String, combined('stringescape', 'dqs')), ("[cCfFqQwWuU]?'", String, combined('stringescape', 'sqs')), ('[\\[\\]{}:(),;?]', Punctuation), ('[a-zA-Z_]\\w*:>', Name.Label), ('({})\\b'.format('|'.join(name_builtins)), Name.Builtin), ('({})\\b'.format('|'.join(name_pseudo)), Name.Builtin.Pseudo), ('[a-zA-Z_]\\w*', Name)], 'whitespace': [('\\s+', Whitespace), include('comment'), ('(#)(\\s*)(if)(\\s+)(0)', bygroups(Comment.Preproc, Whitespace, Comment.Preproc, Whitespace, Comment.Preproc), 'if0'), ('#', Comment.Preproc, 'macro')], 'operators': [('({})\\b'.format('|'.join(operator_words)), Operator.Word), ('!=|==|<<|>>|\\|\\||&&|[-~+/*%=<>&^|.$]', Operator)], 'comment': [('//(.*?)$', Comment.Single), ('/[*]', Comment.Multiline, 'comment2')], 'comment2': [('[^/*]', Comment.Multiline), ('/[*]', Comment.Multiline, '#push'), ('[*]/', Comment.Multiline, '#pop'), ('[/*]', Comment.Multiline)], 'if0': [('^(\\s*)(#if.*?(?<!\\\\))(\\n)', bygroups(Whitespace, Comment, Whitespace), '#push'), ('^(\\s*)(#endif.*?(?<!\\\\))(\\n)', bygroups(Whitespace, Comment, Whitespace), '#pop'), ('(.*?)(\\n)', bygroups(Comment, Whitespace))], 'macro': [include('comment'), ('(import|include)(\\s+)(<[^>]*?>)', bygroups(Comment.Preproc, Whitespace, String), '#pop'), ('(import|include)(\\s+)("[^"]*?")', bygroups(Comment.Preproc, Whitespace, String), '#pop'), ("(import|include)(\\s+)('[^']*?')", bygroups(Comment.Preproc, Whitespace, String), '#pop'), ('[^/\\n]+', Comment.Preproc), ('/', Comment.Preproc), ('(?<=\\\\)\\n', Comment.Preproc), ('\\n', Whitespace, '#pop')], 'funcname': [include('whitespace'), ('[a-zA-Z_]\\w*', Name.Function, '#pop'), ('(?=\\()', Text, '#pop')], 'classname': [include('whitespace'), ('[a-zA-Z_]\\w*', Name.Class, '#pop'), ('(?=\\{)', Text, '#pop')], 'modulename': [include('whitespace'), ('\\[', Punctuation, ('modulename2', 'tvarlist')), default('modulename2')], 'modulename2': [include('whitespace'), ('([a-zA-Z_]\\w*)', Name.Namespace, '#pop:2')], 'tvarlist': [include('whitespace'), include('operators'), ('\\[', Punctuation, '#push'), ('\\]', Punctuation, '#pop'), (',', Punctuation), ('(with|where)\\b', Keyword), ('[a-zA-Z_]\\w*', Name)], 'stringescape': [('\\\\([\\\\abfnrtv"\\\']|\\n|N\\{.*?\\}|u[a-fA-F0-9]{4}|U[a-fA-F0-9]{8}|x[a-fA-F0-9]{2}|[0-7]{1,3})', String.Escape)], 'strings': [('%(\\([a-zA-Z0-9]+\\))?[-#0 +]*([0-9]+|[*])?(\\.([0-9]+|[*]))?[hlL]?[E-GXc-giorsux%]', String.Interpol), ('[^\\\\\\\'"%\\n]+', String), ('[\\\'"\\\\]', String), ('%', String)], 'nl': [('\\n', String)], 'dqs': [('"', String, '#pop'), ('\\\\\\\\|\\\\"|\\\\\\n', String.Escape), include('strings')], 'sqs': [("'", String, '#pop'), ("\\\\\\\\|\\\\'|\\\\\\n", String.Escape), include('strings')], 'tdqs': [('"""', String, '#pop'), include('strings'), include('nl')], 'tsqs': [("'''", String, '#pop'), include('strings'), include('nl')]}


