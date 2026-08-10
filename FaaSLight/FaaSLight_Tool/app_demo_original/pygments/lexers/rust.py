"""
    pygments.lexers.rust
    ~~~~~~~~~~~~~~~~~~~~

    Lexers for the Rust language.

    :copyright: Copyright 2006-present by the Pygments team, see AUTHORS.
    :license: BSD, see LICENSE for details.
"""

from pygments.lexer import RegexLexer, include, bygroups, words, default
from pygments.token import Text, Comment, Operator, Keyword, Name, String, Number, Punctuation, Whitespace
__all__ = ['RustLexer']


class RustLexer(RegexLexer):
    """
    Lexer for the Rust programming language (version 1.47).
    """
    name = 'Rust'
    url = 'https://www.rust-lang.org/'
    filenames = ['*.rs', '*.rs.in']
    aliases = ['rust', 'rs']
    mimetypes = ['text/rust', 'text/x-rust']
    version_added = '1.6'
    keyword_types = (words(('u8', 'u16', 'u32', 'u64', 'u128', 'i8', 'i16', 'i32', 'i64', 'i128', 'usize', 'isize', 'f32', 'f64', 'char', 'str', 'bool'), suffix='\\b'), Keyword.Type)
    builtin_funcs_types = (words(('Copy', 'Send', 'Sized', 'Sync', 'Unpin', 'Drop', 'Fn', 'FnMut', 'FnOnce', 'drop', 'Box', 'ToOwned', 'Clone', 'PartialEq', 'PartialOrd', 'Eq', 'Ord', 'AsRef', 'AsMut', 'Into', 'From', 'Default', 'Iterator', 'Extend', 'IntoIterator', 'DoubleEndedIterator', 'ExactSizeIterator', 'Option', 'Some', 'None', 'Result', 'Ok', 'Err', 'String', 'ToString', 'Vec'), suffix='\\b'), Name.Builtin)
    builtin_macros = (words(('asm', 'assert', 'assert_eq', 'assert_ne', 'cfg', 'column', 'compile_error', 'concat', 'concat_idents', 'dbg', 'debug_assert', 'debug_assert_eq', 'debug_assert_ne', 'env', 'eprint', 'eprintln', 'file', 'format', 'format_args', 'format_args_nl', 'global_asm', 'include', 'include_bytes', 'include_str', 'is_aarch64_feature_detected', 'is_arm_feature_detected', 'is_mips64_feature_detected', 'is_mips_feature_detected', 'is_powerpc64_feature_detected', 'is_powerpc_feature_detected', 'is_x86_feature_detected', 'line', 'llvm_asm', 'log_syntax', 'macro_rules', 'matches', 'module_path', 'option_env', 'panic', 'print', 'println', 'stringify', 'thread_local', 'todo', 'trace_macros', 'unimplemented', 'unreachable', 'vec', 'write', 'writeln'), suffix='!'), Name.Function.Magic)
    tokens = {'root': [('#![^[\\r\\n].*$', Comment.Preproc), default('base')], 'base': [('\\n', Whitespace), ('\\s+', Whitespace), ('//!.*?\\n', String.Doc), ('///(\\n|[^/].*?\\n)', String.Doc), ('//(.*?)\\n', Comment.Single), ('/\\*\\*(\\n|[^/*])', String.Doc, 'doccomment'), ('/\\*!', String.Doc, 'doccomment'), ('/\\*', Comment.Multiline, 'comment'), ('\\$([a-zA-Z_]\\w*|\\(,?|\\),?|,?)', Comment.Preproc), (words(('as', 'async', 'await', 'box', 'const', 'crate', 'dyn', 'else', 'extern', 'for', 'if', 'impl', 'in', 'loop', 'match', 'move', 'mut', 'pub', 'ref', 'return', 'static', 'super', 'trait', 'unsafe', 'use', 'where', 'while'), suffix='\\b'), Keyword), (words(('abstract', 'become', 'do', 'final', 'macro', 'override', 'priv', 'typeof', 'try', 'unsized', 'virtual', 'yield'), suffix='\\b'), Keyword.Reserved), ('(true|false)\\b', Keyword.Constant), ('self\\b', Name.Builtin.Pseudo), ('mod\\b', Keyword, 'modname'), ('let\\b', Keyword.Declaration), ('fn\\b', Keyword, 'funcname'), ('(struct|enum|type|union)\\b', Keyword, 'typename'), ('(default)(\\s+)(type|fn)\\b', bygroups(Keyword, Whitespace, Keyword)), keyword_types, ('[sS]elf\\b', Name.Builtin.Pseudo), builtin_funcs_types, builtin_macros, ('::\\b', Punctuation), ('(?::|->)', Punctuation, 'typename'), ("(break|continue)(\\b\\s*)(\\'[A-Za-z_]\\w*)?", bygroups(Keyword, Text.Whitespace, Name.Label)), ('\'(\\\\[\'"\\\\nrt]|\\\\x[0-7][0-9a-fA-F]|\\\\0|\\\\u\\{[0-9a-fA-F]{1,6}\\}|.)\'', String.Char), ('b\'(\\\\[\'"\\\\nrt]|\\\\x[0-9a-fA-F]{2}|\\\\0|\\\\u\\{[0-9a-fA-F]{1,6}\\}|.)\'', String.Char), ('0b[01_]+', Number.Bin, 'number_lit'), ('0o[0-7_]+', Number.Oct, 'number_lit'), ('0[xX][0-9a-fA-F_]+', Number.Hex, 'number_lit'), ('[0-9][0-9_]*(\\.[0-9_]+[eE][+\\-]?[0-9_]+|\\.[0-9_]*(?!\\.)|[eE][+\\-]?[0-9_]+)', Number.Float, 'number_lit'), ('[0-9][0-9_]*', Number.Integer, 'number_lit'), ('b"', String, 'bytestring'), ('"', String, 'string'), ('(?s)b?r(#*)".*?"\\1', String), ("'", Operator, 'lifetime'), ('\\.\\.=?', Operator), ('[{}()\\[\\],.;]', Punctuation), ('[+\\-*/%&|<>^!~@=:?]', Operator), ('[a-zA-Z_]\\w*', Name), ('r#[a-zA-Z_]\\w*', Name), ('#!?\\[', Comment.Preproc, 'attribute['), ('#', Punctuation)], 'comment': [('[^*/]+', Comment.Multiline), ('/\\*', Comment.Multiline, '#push'), ('\\*/', Comment.Multiline, '#pop'), ('[*/]', Comment.Multiline)], 'doccomment': [('[^*/]+', String.Doc), ('/\\*', String.Doc, '#push'), ('\\*/', String.Doc, '#pop'), ('[*/]', String.Doc)], 'modname': [('\\s+', Whitespace), ('[a-zA-Z_]\\w*', Name.Namespace, '#pop'), default('#pop')], 'funcname': [('\\s+', Whitespace), ('[a-zA-Z_]\\w*', Name.Function, '#pop'), default('#pop')], 'typename': [('\\s+', Whitespace), ('&', Keyword.Pseudo), ("'", Operator, 'lifetime'), builtin_funcs_types, keyword_types, ('[a-zA-Z_]\\w*', Name.Class, '#pop'), default('#pop')], 'lifetime': [('(static|_)', Name.Builtin), ('[a-zA-Z_]+\\w*', Name.Attribute), default('#pop')], 'number_lit': [('[ui](8|16|32|64|size)', Keyword, '#pop'), ('f(32|64)', Keyword, '#pop'), default('#pop')], 'string': [('"', String, '#pop'), ('\\\\[\'"\\\\nrt]|\\\\x[0-7][0-9a-fA-F]|\\\\0|\\\\u\\{[0-9a-fA-F]{1,6}\\}', String.Escape), ('[^\\\\"]+', String), ('\\\\', String)], 'bytestring': [('\\\\x[89a-fA-F][0-9a-fA-F]', String.Escape), include('string')], 'attribute_common': [('"', String, 'string'), ('\\[', Comment.Preproc, 'attribute[')], 'attribute[': [include('attribute_common'), ('\\]', Comment.Preproc, '#pop'), ('[^"\\]\\[]+', Comment.Preproc)]}


