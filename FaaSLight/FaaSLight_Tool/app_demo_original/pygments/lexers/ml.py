"""
    pygments.lexers.ml
    ~~~~~~~~~~~~~~~~~~

    Lexers for ML family languages.

    :copyright: Copyright 2006-present by the Pygments team, see AUTHORS.
    :license: BSD, see LICENSE for details.
"""

import re
from pygments.lexer import RegexLexer, include, bygroups, default, words
from pygments.token import Text, Comment, Operator, Keyword, Name, String, Number, Punctuation, Error
__all__ = ['SMLLexer', 'OcamlLexer', 'OpaLexer', 'ReasonLexer', 'FStarLexer']


class SMLLexer(RegexLexer):
    """
    For the Standard ML language.
    """
    name = 'Standard ML'
    aliases = ['sml']
    filenames = ['*.sml', '*.sig', '*.fun']
    mimetypes = ['text/x-standardml', 'application/x-standardml']
    url = 'https://en.wikipedia.org/wiki/Standard_ML'
    version_added = '1.5'
    alphanumid_reserved = {'abstype', 'and', 'andalso', 'as', 'case', 'datatype', 'do', 'else', 'end', 'exception', 'fn', 'fun', 'handle', 'if', 'in', 'infix', 'infixr', 'let', 'local', 'nonfix', 'of', 'op', 'open', 'orelse', 'raise', 'rec', 'then', 'type', 'val', 'with', 'withtype', 'while', 'eqtype', 'functor', 'include', 'sharing', 'sig', 'signature', 'struct', 'structure', 'where'}
    symbolicid_reserved = {':', '\\|', '=', '=>', '->', '#', ':>'}
    nonid_reserved = {'(', ')', '[', ']', '{', '}', ',', ';', '...', '_'}
    alphanumid_re = "[a-zA-Z][\\w']*"
    symbolicid_re = '[!%&$#+\\-/:<=>?@\\\\~`^|*]+'
    
    def stringy(whatkind):
        return [('[^"\\\\]', whatkind), ('\\\\[\\\\"abtnvfr]', String.Escape), ('\\\\\\^[\\x40-\\x5e]', String.Escape), ('\\\\[0-9]{3}', String.Escape), ('\\\\u[0-9a-fA-F]{4}', String.Escape), ('\\\\\\s+\\\\', String.Interpol), ('"', whatkind, '#pop')]
    
    def long_id_callback(self, match):
        if match.group(1) in self.alphanumid_reserved:
            token = Error
        else:
            token = Name.Namespace
        yield (match.start(1), token, match.group(1))
        yield (match.start(2), Punctuation, match.group(2))
    
    def end_id_callback(self, match):
        if match.group(1) in self.alphanumid_reserved:
            token = Error
        elif match.group(1) in self.symbolicid_reserved:
            token = Error
        else:
            token = Name
        yield (match.start(1), token, match.group(1))
    
    def id_callback(self, match):
        str = match.group(1)
        if str in self.alphanumid_reserved:
            token = Keyword.Reserved
        elif str in self.symbolicid_reserved:
            token = Punctuation
        else:
            token = Name
        yield (match.start(1), token, str)
    tokens = {'whitespace': [('\\s+', Text), ('\\(\\*', Comment.Multiline, 'comment')], 'delimiters': [('\\(|\\[|\\{', Punctuation, 'main'), ('\\)|\\]|\\}', Punctuation, '#pop'), ("\\b(let|if|local)\\b(?!\\')", Keyword.Reserved, ('main', 'main')), ("\\b(struct|sig|while)\\b(?!\\')", Keyword.Reserved, 'main'), ("\\b(do|else|end|in|then)\\b(?!\\')", Keyword.Reserved, '#pop')], 'core': [('({})'.format('|'.join((re.escape(z) for z in nonid_reserved))), Punctuation), ('#"', String.Char, 'char'), ('"', String.Double, 'string'), ('~?0x[0-9a-fA-F]+', Number.Hex), ('0wx[0-9a-fA-F]+', Number.Hex), ('0w\\d+', Number.Integer), ('~?\\d+\\.\\d+[eE]~?\\d+', Number.Float), ('~?\\d+\\.\\d+', Number.Float), ('~?\\d+[eE]~?\\d+', Number.Float), ('~?\\d+', Number.Integer), ('#\\s*[1-9][0-9]*', Name.Label), (f'#\\s*({alphanumid_re})', Name.Label), (f'#\\s+({symbolicid_re})', Name.Label), ("\\b(datatype|abstype)\\b(?!\\')", Keyword.Reserved, 'dname'), ("\\b(exception)\\b(?!\\')", Keyword.Reserved, 'ename'), ("\\b(functor|include|open|signature|structure)\\b(?!\\')", Keyword.Reserved, 'sname'), ("\\b(type|eqtype)\\b(?!\\')", Keyword.Reserved, 'tname'), ("\\'[\\w\\']*", Name.Decorator), (f'({alphanumid_re})(\\.)', long_id_callback, 'dotted'), (f'({alphanumid_re})', id_callback), (f'({symbolicid_re})', id_callback)], 'dotted': [(f'({alphanumid_re})(\\.)', long_id_callback), (f'({alphanumid_re})', end_id_callback, '#pop'), (f'({symbolicid_re})', end_id_callback, '#pop'), ('\\s+', Error), ('\\S+', Error)], 'root': [default('main')], 'main': [include('whitespace'), ("\\b(val|and)\\b(?!\\')", Keyword.Reserved, 'vname'), ("\\b(fun)\\b(?!\\')", Keyword.Reserved, ('#pop', 'main-fun', 'fname')), include('delimiters'), include('core'), ('\\S+', Error)], 'main-fun': [include('whitespace'), ('\\s', Text), ('\\(\\*', Comment.Multiline, 'comment'), ("\\b(fun|and)\\b(?!\\')", Keyword.Reserved, 'fname'), ("\\b(val)\\b(?!\\')", Keyword.Reserved, ('#pop', 'main', 'vname')), ('\\|', Punctuation, 'fname'), ("\\b(case|handle)\\b(?!\\')", Keyword.Reserved, ('#pop', 'main')), include('delimiters'), include('core'), ('\\S+', Error)], 'char': stringy(String.Char), 'string': stringy(String.Double), 'breakout': [("(?=\\b({})\\b(?!\\'))".format('|'.join(alphanumid_reserved)), Text, '#pop')], 'sname': [include('whitespace'), include('breakout'), (f'({alphanumid_re})', Name.Namespace), default('#pop')], 'fname': [include('whitespace'), ("\\'[\\w\\']*", Name.Decorator), ('\\(', Punctuation, 'tyvarseq'), (f'({alphanumid_re})', Name.Function, '#pop'), (f'({symbolicid_re})', Name.Function, '#pop'), default('#pop')], 'vname': [include('whitespace'), ("\\'[\\w\\']*", Name.Decorator), ('\\(', Punctuation, 'tyvarseq'), (f'({alphanumid_re})(\\s*)(=(?!{symbolicid_re}))', bygroups(Name.Variable, Text, Punctuation), '#pop'), (f'({symbolicid_re})(\\s*)(=(?!{symbolicid_re}))', bygroups(Name.Variable, Text, Punctuation), '#pop'), (f'({alphanumid_re})', Name.Variable, '#pop'), (f'({symbolicid_re})', Name.Variable, '#pop'), default('#pop')], 'tname': [include('whitespace'), include('breakout'), ("\\'[\\w\\']*", Name.Decorator), ('\\(', Punctuation, 'tyvarseq'), (f'=(?!{symbolicid_re})', Punctuation, ('#pop', 'typbind')), (f'({alphanumid_re})', Keyword.Type), (f'({symbolicid_re})', Keyword.Type), ('\\S+', Error, '#pop')], 'typbind': [include('whitespace'), ("\\b(and)\\b(?!\\')", Keyword.Reserved, ('#pop', 'tname')), include('breakout'), include('core'), ('\\S+', Error, '#pop')], 'dname': [include('whitespace'), include('breakout'), ("\\'[\\w\\']*", Name.Decorator), ('\\(', Punctuation, 'tyvarseq'), ('(=)(\\s*)(datatype)', bygroups(Punctuation, Text, Keyword.Reserved), '#pop'), (f'=(?!{symbolicid_re})', Punctuation, ('#pop', 'datbind', 'datcon')), (f'({alphanumid_re})', Keyword.Type), (f'({symbolicid_re})', Keyword.Type), ('\\S+', Error, '#pop')], 'datbind': [include('whitespace'), ("\\b(and)\\b(?!\\')", Keyword.Reserved, ('#pop', 'dname')), ("\\b(withtype)\\b(?!\\')", Keyword.Reserved, ('#pop', 'tname')), ("\\b(of)\\b(?!\\')", Keyword.Reserved), (f'(\\|)(\\s*)({alphanumid_re})', bygroups(Punctuation, Text, Name.Class)), (f'(\\|)(\\s+)({symbolicid_re})', bygroups(Punctuation, Text, Name.Class)), include('breakout'), include('core'), ('\\S+', Error)], 'ename': [include('whitespace'), (f'(and\\b)(\\s+)({alphanumid_re})', bygroups(Keyword.Reserved, Text, Name.Class)), (f'(and\\b)(\\s*)({symbolicid_re})', bygroups(Keyword.Reserved, Text, Name.Class)), ("\\b(of)\\b(?!\\')", Keyword.Reserved), (f'({alphanumid_re})|({symbolicid_re})', Name.Class), default('#pop')], 'datcon': [include('whitespace'), (f'({alphanumid_re})', Name.Class, '#pop'), (f'({symbolicid_re})', Name.Class, '#pop'), ('\\S+', Error, '#pop')], 'tyvarseq': [('\\s', Text), ('\\(\\*', Comment.Multiline, 'comment'), ("\\'[\\w\\']*", Name.Decorator), (alphanumid_re, Name), (',', Punctuation), ('\\)', Punctuation, '#pop'), (symbolicid_re, Name)], 'comment': [('[^(*)]', Comment.Multiline), ('\\(\\*', Comment.Multiline, '#push'), ('\\*\\)', Comment.Multiline, '#pop'), ('[(*)]', Comment.Multiline)]}



class OcamlLexer(RegexLexer):
    """
    For the OCaml language.
    """
    name = 'OCaml'
    url = 'https://ocaml.org/'
    aliases = ['ocaml']
    filenames = ['*.ml', '*.mli', '*.mll', '*.mly']
    mimetypes = ['text/x-ocaml']
    version_added = '0.7'
    keywords = ('and', 'as', 'assert', 'begin', 'class', 'constraint', 'do', 'done', 'downto', 'else', 'end', 'exception', 'external', 'false', 'for', 'fun', 'function', 'functor', 'if', 'in', 'include', 'inherit', 'initializer', 'lazy', 'let', 'match', 'method', 'module', 'mutable', 'new', 'object', 'of', 'open', 'private', 'raise', 'rec', 'sig', 'struct', 'then', 'to', 'true', 'try', 'type', 'val', 'virtual', 'when', 'while', 'with')
    keyopts = ('!=', '#', '&', '&&', '\\(', '\\)', '\\*', '\\+', ',', '-', '-\\.', '->', '\\.', '\\.\\.', ':', '::', ':=', ':>', ';', ';;', '<', '<-', '=', '>', '>]', '>\\}', '\\?', '\\?\\?', '\\[', '\\[<', '\\[>', '\\[\\|', ']', '_', '`', '\\{', '\\{<', '\\|', '\\|]', '\\}', '~')
    operators = '[!$%&*+\\./:<=>?@^|~-]'
    word_operators = ('asr', 'land', 'lor', 'lsl', 'lxor', 'mod', 'or')
    prefix_syms = '[!?~]'
    infix_syms = '[=<>@^|&+\\*/$%-]'
    primitives = ('unit', 'int', 'float', 'bool', 'string', 'char', 'list', 'array')
    tokens = {'escape-sequence': [('\\\\[\\\\"\\\'ntbr]', String.Escape), ('\\\\[0-9]{3}', String.Escape), ('\\\\x[0-9a-fA-F]{2}', String.Escape)], 'root': [('\\s+', Text), ('false|true|\\(\\)|\\[\\]', Name.Builtin.Pseudo), ("\\b([A-Z][\\w\\']*)(?=\\s*\\.)", Name.Namespace, 'dotted'), ("\\b([A-Z][\\w\\']*)", Name.Class), ('\\(\\*(?![)])', Comment, 'comment'), ('\\b({})\\b'.format('|'.join(keywords)), Keyword), ('({})'.format('|'.join(keyopts[::-1])), Operator), (f'({infix_syms}|{prefix_syms})?{operators}', Operator), ('\\b({})\\b'.format('|'.join(word_operators)), Operator.Word), ('\\b({})\\b'.format('|'.join(primitives)), Keyword.Type), ("[^\\W\\d][\\w']*", Name), ('-?\\d[\\d_]*(.[\\d_]*)?([eE][+\\-]?\\d[\\d_]*)', Number.Float), ('0[xX][\\da-fA-F][\\da-fA-F_]*', Number.Hex), ('0[oO][0-7][0-7_]*', Number.Oct), ('0[bB][01][01_]*', Number.Bin), ('\\d[\\d_]*', Number.Integer), ('\'(?:(\\\\[\\\\\\"\'ntbr ])|(\\\\[0-9]{3})|(\\\\x[0-9a-fA-F]{2}))\'', String.Char), ("'.'", String.Char), ("'", Keyword), ('"', String.Double, 'string'), ("[~?][a-z][\\w\\']*:", Name.Variable)], 'comment': [('[^(*)]+', Comment), ('\\(\\*', Comment, '#push'), ('\\*\\)', Comment, '#pop'), ('[(*)]', Comment)], 'string': [('[^\\\\"]+', String.Double), include('escape-sequence'), ('\\\\\\n', String.Double), ('"', String.Double, '#pop')], 'dotted': [('\\s+', Text), ('\\.', Punctuation), ("[A-Z][\\w\\']*(?=\\s*\\.)", Name.Namespace), ("[A-Z][\\w\\']*", Name.Class, '#pop'), ("[a-z_][\\w\\']*", Name, '#pop'), default('#pop')]}



class OpaLexer(RegexLexer):
    """
    Lexer for the Opa language.
    """
    name = 'Opa'
    aliases = ['opa']
    filenames = ['*.opa']
    mimetypes = ['text/x-opa']
    url = 'http://opalang.org'
    version_added = '1.5'
    keywords = ('and', 'as', 'begin', 'case', 'client', 'css', 'database', 'db', 'do', 'else', 'end', 'external', 'forall', 'function', 'if', 'import', 'match', 'module', 'or', 'package', 'parser', 'rec', 'server', 'then', 'type', 'val', 'with', 'xml_parser')
    ident_re = '(([a-zA-Z_]\\w*)|(`[^`]*`))'
    op_re = '[.=\\-<>,@~%/+?*&^!]'
    punc_re = '[()\\[\\],;|]'
    tokens = {'escape-sequence': [('\\\\[\\\\"\\\'ntr}]', String.Escape), ('\\\\[0-9]{3}', String.Escape), ('\\\\x[0-9a-fA-F]{2}', String.Escape)], 'comments': [('/\\*', Comment, 'nested-comment'), ('//.*?$', Comment)], 'comments-and-spaces': [include('comments'), ('\\s+', Text)], 'root': [include('comments-and-spaces'), (words(keywords, prefix='\\b', suffix='\\b'), Keyword), ('@' + ident_re + '\\b', Name.Builtin.Pseudo), ('-?.[\\d]+([eE][+\\-]?\\d+)', Number.Float), ('-?\\d+.\\d*([eE][+\\-]?\\d+)', Number.Float), ('-?\\d+[eE][+\\-]?\\d+', Number.Float), ('0[xX][\\da-fA-F]+', Number.Hex), ('0[oO][0-7]+', Number.Oct), ('0[bB][01]+', Number.Bin), ('\\d+', Number.Integer), ('#[\\da-fA-F]{3,6}', Number.Integer), ('"', String.Double, 'string'), ('\'(?:(\\\\[\\\\\\"\'ntbr ])|(\\\\[0-9]{3})|(\\\\x[0-9a-fA-F]{2})|.)\'', String.Char), ('\\{', Operator, '#push'), ('\\}', Operator, '#pop'), ('<(?=[a-zA-Z>])', String.Single, 'html-open-tag'), ('[@?!]?(/\\w+)+(\\[_\\])?', Name.Variable), ('<-(?!' + op_re + ')', Name.Variable), ('\\b([A-Z]\\w*)(?=\\.)', Name.Namespace), ('=(?!' + op_re + ')', Keyword), (f'({op_re})+', Operator), (f'({punc_re})+', Operator), (':', Operator, 'type'), ("'" + ident_re, Keyword.Type), ('#' + ident_re, String.Single), ('#(?=\\{)', String.Single), (ident_re, Text)], 'type': [include('comments-and-spaces'), ('->', Keyword.Type), default(('#pop', 'type-lhs-1', 'type-with-slash'))], 'type-1': [include('comments-and-spaces'), ('\\(', Keyword.Type, ('#pop', 'type-tuple')), ('~?\\{', Keyword.Type, ('#pop', 'type-record')), (ident_re + '\\(', Keyword.Type, ('#pop', 'type-tuple')), (ident_re, Keyword.Type, '#pop'), ("'" + ident_re, Keyword.Type), default('#pop')], 'type-with-slash': [include('comments-and-spaces'), default(('#pop', 'slash-type-1', 'type-1'))], 'slash-type-1': [include('comments-and-spaces'), ('/', Keyword.Type, ('#pop', 'type-1')), default('#pop')], 'type-lhs-1': [include('comments-and-spaces'), ('->', Keyword.Type, ('#pop', 'type')), ('(?=,)', Keyword.Type, ('#pop', 'type-arrow')), default('#pop')], 'type-arrow': [include('comments-and-spaces'), (',(?=[^:]*?->)', Keyword.Type, 'type-with-slash'), ('->', Keyword.Type, ('#pop', 'type')), default('#pop')], 'type-tuple': [include('comments-and-spaces'), ('[^()/*]+', Keyword.Type), ('[/*]', Keyword.Type), ('\\(', Keyword.Type, '#push'), ('\\)', Keyword.Type, '#pop')], 'type-record': [include('comments-and-spaces'), ('[^{}/*]+', Keyword.Type), ('[/*]', Keyword.Type), ('\\{', Keyword.Type, '#push'), ('\\}', Keyword.Type, '#pop')], 'nested-comment': [('[^/*]+', Comment), ('/\\*', Comment, '#push'), ('\\*/', Comment, '#pop'), ('[/*]', Comment)], 'string': [('[^\\\\"{]+', String.Double), ('"', String.Double, '#pop'), ('\\{', Operator, 'root'), include('escape-sequence')], 'single-string': [("[^\\\\\\'{]+", String.Double), ("\\'", String.Double, '#pop'), ('\\{', Operator, 'root'), include('escape-sequence')], 'html-open-tag': [('[\\w\\-:]+', String.Single, ('#pop', 'html-attr')), ('>', String.Single, ('#pop', 'html-content'))], 'html-end-tag': [('[\\w\\-:]*>', String.Single, '#pop')], 'html-attr': [('\\s+', Text), ('[\\w\\-:]+=', String.Single, 'html-attr-value'), ('/>', String.Single, '#pop'), ('>', String.Single, ('#pop', 'html-content'))], 'html-attr-value': [("'", String.Single, ('#pop', 'single-string')), ('"', String.Single, ('#pop', 'string')), ('#' + ident_re, String.Single, '#pop'), ('#(?=\\{)', String.Single, ('#pop', 'root')), ('[^"\\\'{`=<>]+', String.Single, '#pop'), ('\\{', Operator, ('#pop', 'root'))], 'html-content': [('<!--', Comment, 'html-comment'), ('</', String.Single, ('#pop', 'html-end-tag')), ('<', String.Single, 'html-open-tag'), ('\\{', Operator, 'root'), ('[^<{]+', String.Single)], 'html-comment': [('-->', Comment, '#pop'), ('[^\\-]+|-', Comment)]}



class ReasonLexer(RegexLexer):
    """
    For the ReasonML language.
    """
    name = 'ReasonML'
    url = 'https://reasonml.github.io/'
    aliases = ['reasonml', 'reason']
    filenames = ['*.re', '*.rei']
    mimetypes = ['text/x-reasonml']
    version_added = '2.6'
    keywords = ('as', 'assert', 'begin', 'class', 'constraint', 'do', 'done', 'downto', 'else', 'end', 'exception', 'external', 'false', 'for', 'fun', 'esfun', 'function', 'functor', 'if', 'in', 'include', 'inherit', 'initializer', 'lazy', 'let', 'switch', 'module', 'pub', 'mutable', 'new', 'nonrec', 'object', 'of', 'open', 'pri', 'rec', 'sig', 'struct', 'then', 'to', 'true', 'try', 'type', 'val', 'virtual', 'when', 'while', 'with')
    keyopts = ('!=', '#', '&', '&&', '\\(', '\\)', '\\*', '\\+', ',', '-', '-\\.', '=>', '\\.', '\\.\\.', '\\.\\.\\.', ':', '::', ':=', ':>', ';', ';;', '<', '<-', '=', '>', '>]', '>\\}', '\\?', '\\?\\?', '\\[', '\\[<', '\\[>', '\\[\\|', ']', '_', '`', '\\{', '\\{<', '\\|', '\\|\\|', '\\|]', '\\}', '~')
    operators = '[!$%&*+\\./:<=>?@^|~-]'
    word_operators = ('and', 'asr', 'land', 'lor', 'lsl', 'lsr', 'lxor', 'mod', 'or')
    prefix_syms = '[!?~]'
    infix_syms = '[=<>@^|&+\\*/$%-]'
    primitives = ('unit', 'int', 'float', 'bool', 'string', 'char', 'list', 'array')
    tokens = {'escape-sequence': [('\\\\[\\\\"\\\'ntbr]', String.Escape), ('\\\\[0-9]{3}', String.Escape), ('\\\\x[0-9a-fA-F]{2}', String.Escape)], 'root': [('\\s+', Text), ('false|true|\\(\\)|\\[\\]', Name.Builtin.Pseudo), ("\\b([A-Z][\\w\\']*)(?=\\s*\\.)", Name.Namespace, 'dotted'), ("\\b([A-Z][\\w\\']*)", Name.Class), ('//.*?\\n', Comment.Single), ('\\/\\*(?!/)', Comment.Multiline, 'comment'), ('\\b({})\\b'.format('|'.join(keywords)), Keyword), ('({})'.format('|'.join(keyopts[::-1])), Operator.Word), (f'({infix_syms}|{prefix_syms})?{operators}', Operator), ('\\b({})\\b'.format('|'.join(word_operators)), Operator.Word), ('\\b({})\\b'.format('|'.join(primitives)), Keyword.Type), ("[^\\W\\d][\\w']*", Name), ('-?\\d[\\d_]*(.[\\d_]*)?([eE][+\\-]?\\d[\\d_]*)', Number.Float), ('0[xX][\\da-fA-F][\\da-fA-F_]*', Number.Hex), ('0[oO][0-7][0-7_]*', Number.Oct), ('0[bB][01][01_]*', Number.Bin), ('\\d[\\d_]*', Number.Integer), ('\'(?:(\\\\[\\\\\\"\'ntbr ])|(\\\\[0-9]{3})|(\\\\x[0-9a-fA-F]{2}))\'', String.Char), ("'.'", String.Char), ("'", Keyword), ('"', String.Double, 'string'), ("[~?][a-z][\\w\\']*:", Name.Variable)], 'comment': [('[^/*]+', Comment.Multiline), ('\\/\\*', Comment.Multiline, '#push'), ('\\*\\/', Comment.Multiline, '#pop'), ('\\*', Comment.Multiline)], 'string': [('[^\\\\"]+', String.Double), include('escape-sequence'), ('\\\\\\n', String.Double), ('"', String.Double, '#pop')], 'dotted': [('\\s+', Text), ('\\.', Punctuation), ("[A-Z][\\w\\']*(?=\\s*\\.)", Name.Namespace), ("[A-Z][\\w\\']*", Name.Class, '#pop'), ("[a-z_][\\w\\']*", Name, '#pop'), default('#pop')]}



class FStarLexer(RegexLexer):
    """
    For the F* language.
    """
    name = 'FStar'
    url = 'https://www.fstar-lang.org/'
    aliases = ['fstar']
    filenames = ['*.fst', '*.fsti']
    mimetypes = ['text/x-fstar']
    version_added = '2.7'
    keywords = ('abstract', 'attributes', 'noeq', 'unopteq', 'andbegin', 'by', 'default', 'effect', 'else', 'end', 'ensures', 'exception', 'exists', 'false', 'forall', 'fun', 'function', 'if', 'in', 'include', 'inline', 'inline_for_extraction', 'irreducible', 'logic', 'match', 'module', 'mutable', 'new', 'new_effect', 'noextract', 'of', 'open', 'opaque', 'private', 'range_of', 'reifiable', 'reify', 'reflectable', 'requires', 'set_range_of', 'sub_effect', 'synth', 'then', 'total', 'true', 'try', 'type', 'unfold', 'unfoldable', 'val', 'when', 'with', 'not')
    decl_keywords = ('let', 'rec')
    assume_keywords = ('assume', 'admit', 'assert', 'calc')
    keyopts = ('~', '-', '/\\\\', '\\\\/', '<:', '<@', '\\(\\|', '\\|\\)', '#', 'u#', '&', '\\(', '\\)', '\\(\\)', ',', '~>', '->', '<-', '<--', '<==>', '==>', '\\.', '\\?', '\\?\\.', '\\.\\[', '\\.\\(', '\\.\\(\\|', '\\.\\[\\|', '\\{:pattern', ':', '::', ':=', ';', ';;', '=', '%\\[', '!\\{', '\\[', '\\[@', '\\[\\|', '\\|>', '\\]', '\\|\\]', '\\{', '\\|', '\\}', '\\$')
    operators = '[!$%&*+\\./:<=>?@^|~-]'
    prefix_syms = '[!?~]'
    infix_syms = '[=<>@^|&+\\*/$%-]'
    primitives = ('unit', 'int', 'float', 'bool', 'string', 'char', 'list', 'array')
    tokens = {'escape-sequence': [('\\\\[\\\\"\\\'ntbr]', String.Escape), ('\\\\[0-9]{3}', String.Escape), ('\\\\x[0-9a-fA-F]{2}', String.Escape)], 'root': [('\\s+', Text), ('false|true|False|True|\\(\\)|\\[\\]', Name.Builtin.Pseudo), ("\\b([A-Z][\\w\\']*)(?=\\s*\\.)", Name.Namespace, 'dotted'), ("\\b([A-Z][\\w\\']*)", Name.Class), ('\\(\\*(?![)])', Comment, 'comment'), ('\\/\\/.+$', Comment), ('\\b({})\\b'.format('|'.join(keywords)), Keyword), ('\\b({})\\b'.format('|'.join(assume_keywords)), Name.Exception), ('\\b({})\\b'.format('|'.join(decl_keywords)), Keyword.Declaration), ('({})'.format('|'.join(keyopts[::-1])), Operator), (f'({infix_syms}|{prefix_syms})?{operators}', Operator), ('\\b({})\\b'.format('|'.join(primitives)), Keyword.Type), ("[^\\W\\d][\\w']*", Name), ('-?\\d[\\d_]*(.[\\d_]*)?([eE][+\\-]?\\d[\\d_]*)', Number.Float), ('0[xX][\\da-fA-F][\\da-fA-F_]*', Number.Hex), ('0[oO][0-7][0-7_]*', Number.Oct), ('0[bB][01][01_]*', Number.Bin), ('\\d[\\d_]*', Number.Integer), ('\'(?:(\\\\[\\\\\\"\'ntbr ])|(\\\\[0-9]{3})|(\\\\x[0-9a-fA-F]{2}))\'', String.Char), ("'.'", String.Char), ("'", Keyword), ("\\`([\\w\\'.]+)\\`", Operator.Word), ('\\`', Keyword), ('"', String.Double, 'string'), ("[~?][a-z][\\w\\']*:", Name.Variable)], 'comment': [('[^(*)]+', Comment), ('\\(\\*', Comment, '#push'), ('\\*\\)', Comment, '#pop'), ('[(*)]', Comment)], 'string': [('[^\\\\"]+', String.Double), include('escape-sequence'), ('\\\\\\n', String.Double), ('"', String.Double, '#pop')], 'dotted': [('\\s+', Text), ('\\.', Punctuation), ("[A-Z][\\w\\']*(?=\\s*\\.)", Name.Namespace), ("[A-Z][\\w\\']*", Name.Class, '#pop'), ("[a-z_][\\w\\']*", Name, '#pop'), default('#pop')]}


