"""
    pygments.lexers.ruby
    ~~~~~~~~~~~~~~~~~~~~

    Lexers for Ruby and related languages.

    :copyright: Copyright 2006-present by the Pygments team, see AUTHORS.
    :license: BSD, see LICENSE for details.
"""

import re
from pygments.lexer import Lexer, RegexLexer, ExtendedRegexLexer, include, bygroups, default, LexerContext, do_insertions, words, line_re
from pygments.token import Text, Comment, Operator, Keyword, Name, String, Number, Punctuation, Error, Generic, Whitespace
from pygments.util import shebang_matches
__all__ = ['RubyLexer', 'RubyConsoleLexer', 'FancyLexer']
RUBY_OPERATORS = ('*', '**', '-', '+', '-@', '+@', '/', '%', '&', '|', '^', '`', '~', '[]', '[]=', '<<', '>>', '<', '<>', '<=>', '>', '>=', '==', '===')


class RubyLexer(ExtendedRegexLexer):
    """
    For Ruby source code.
    """
    name = 'Ruby'
    url = 'http://www.ruby-lang.org'
    aliases = ['ruby', 'rb', 'duby']
    filenames = ['*.rb', '*.rbw', 'Rakefile', '*.rake', '*.gemspec', '*.rbx', '*.duby', 'Gemfile', 'Vagrantfile']
    mimetypes = ['text/x-ruby', 'application/x-ruby']
    version_added = ''
    flags = re.DOTALL | re.MULTILINE
    
    def heredoc_callback(self, match, ctx):
        start = match.start(1)
        yield (start, Operator, match.group(1))
        yield (match.start(2), String.Heredoc, match.group(2))
        yield (match.start(3), String.Delimiter, match.group(3))
        yield (match.start(4), String.Heredoc, match.group(4))
        heredocstack = ctx.__dict__.setdefault('heredocstack', [])
        outermost = not bool(heredocstack)
        heredocstack.append((match.group(1) in ('<<-', '<<~'), match.group(3)))
        ctx.pos = match.start(5)
        ctx.end = match.end(5)
        if len(heredocstack) < 100:
            yield from self.get_tokens_unprocessed(context=ctx)
        else:
            yield (ctx.pos, String.Heredoc, match.group(5))
        ctx.pos = match.end()
        if outermost:
            for (tolerant, hdname) in heredocstack:
                lines = []
                for match in line_re.finditer(ctx.text, ctx.pos):
                    if tolerant:
                        check = match.group().strip()
                    else:
                        check = match.group().rstrip()
                    if check == hdname:
                        for amatch in lines:
                            yield (amatch.start(), String.Heredoc, amatch.group())
                        yield (match.start(), String.Delimiter, match.group())
                        ctx.pos = match.end()
                        break
                    else:
                        lines.append(match)
                else:
                    for amatch in lines:
                        yield (amatch.start(), Error, amatch.group())
            ctx.end = len(ctx.text)
            del heredocstack[:]
    
    def gen_rubystrings_rules():
        
        def intp_regex_callback(self, match, ctx):
            yield (match.start(1), String.Regex, match.group(1))
            nctx = LexerContext(match.group(3), 0, ['interpolated-regex'])
            for (i, t, v) in self.get_tokens_unprocessed(context=nctx):
                yield (match.start(3) + i, t, v)
            yield (match.start(4), String.Regex, match.group(4))
            ctx.pos = match.end()
        
        def intp_string_callback(self, match, ctx):
            yield (match.start(1), String.Other, match.group(1))
            nctx = LexerContext(match.group(3), 0, ['interpolated-string'])
            for (i, t, v) in self.get_tokens_unprocessed(context=nctx):
                yield (match.start(3) + i, t, v)
            yield (match.start(4), String.Other, match.group(4))
            ctx.pos = match.end()
        states = {}
        states['strings'] = [('\\:@{0,2}[a-zA-Z_]\\w*[!?]?', String.Symbol), (words(RUBY_OPERATORS, prefix='\\:@{0,2}'), String.Symbol), (":'(\\\\\\\\|\\\\[^\\\\]|[^'\\\\])*'", String.Symbol), (':"', String.Symbol, 'simple-sym'), ('([a-zA-Z_]\\w*)(:)(?!:)', bygroups(String.Symbol, Punctuation)), ('"', String.Double, 'simple-string-double'), ("'", String.Single, 'simple-string-single'), ('(?<!\\.)`', String.Backtick, 'simple-backtick')]
        for (name, ttype, end) in (('string-double', String.Double, '"'), ('string-single', String.Single, "'"), ('sym', String.Symbol, '"'), ('backtick', String.Backtick, '`')):
            states['simple-' + name] = [include('string-intp-escaped'), (f'[^\\\\{end}#]+', ttype), ('[\\\\#]', ttype), (end, ttype, '#pop')]
        for (lbrace, rbrace, bracecc, name) in (('\\{', '\\}', '{}', 'cb'), ('\\[', '\\]', '\\[\\]', 'sb'), ('\\(', '\\)', '()', 'pa'), ('<', '>', '<>', 'ab')):
            states[name + '-intp-string'] = [('\\\\[\\\\' + bracecc + ']', String.Other), (lbrace, String.Other, '#push'), (rbrace, String.Other, '#pop'), include('string-intp-escaped'), ('[\\\\#' + bracecc + ']', String.Other), ('[^\\\\#' + bracecc + ']+', String.Other)]
            states['strings'].append(('%[QWx]?' + lbrace, String.Other, name + '-intp-string'))
            states[name + '-string'] = [('\\\\[\\\\' + bracecc + ']', String.Other), (lbrace, String.Other, '#push'), (rbrace, String.Other, '#pop'), ('[\\\\#' + bracecc + ']', String.Other), ('[^\\\\#' + bracecc + ']+', String.Other)]
            states['strings'].append(('%[qsw]' + lbrace, String.Other, name + '-string'))
            states[name + '-regex'] = [('\\\\[\\\\' + bracecc + ']', String.Regex), (lbrace, String.Regex, '#push'), (rbrace + '[mixounse]*', String.Regex, '#pop'), include('string-intp'), ('[\\\\#' + bracecc + ']', String.Regex), ('[^\\\\#' + bracecc + ']+', String.Regex)]
            states['strings'].append(('%r' + lbrace, String.Regex, name + '-regex'))
        states['strings'] += [('(%r([\\W_]))((?:\\\\\\2|(?!\\2).)*)(\\2[mixounse]*)', intp_regex_callback), ('%[qsw]([\\W_])((?:\\\\\\1|(?!\\1).)*)\\1', String.Other), ('(%[QWx]([\\W_]))((?:\\\\\\2|(?!\\2).)*)(\\2)', intp_string_callback), ('(?<=[-+/*%=<>&!^|~,(])(\\s*)(%([\\t ])(?:(?:\\\\\\3|(?!\\3).)*)\\3)', bygroups(Whitespace, String.Other, None)), ('^(\\s*)(%([\\t ])(?:(?:\\\\\\3|(?!\\3).)*)\\3)', bygroups(Whitespace, String.Other, None)), ('(%([^a-zA-Z0-9\\s]))((?:\\\\\\2|(?!\\2).)*)(\\2)', intp_string_callback)]
        return states
    tokens = {'root': [('\\A#!.+?$', Comment.Hashbang), ('#.*?$', Comment.Single), ('=begin\\s.*?\\n=end.*?$', Comment.Multiline), (words(('BEGIN', 'END', 'alias', 'begin', 'break', 'case', 'defined?', 'do', 'else', 'elsif', 'end', 'ensure', 'for', 'if', 'in', 'next', 'redo', 'rescue', 'raise', 'retry', 'return', 'super', 'then', 'undef', 'unless', 'until', 'when', 'while', 'yield'), suffix='\\b'), Keyword), ('(module)(\\s+)([a-zA-Z_]\\w*(?:::[a-zA-Z_]\\w*)*)', bygroups(Keyword, Whitespace, Name.Namespace)), ('(def)(\\s+)', bygroups(Keyword, Whitespace), 'funcname'), ('def(?=[*%&^`~+-/\\[<>=])', Keyword, 'funcname'), ('(class)(\\s+)', bygroups(Keyword, Whitespace), 'classname'), (words(('initialize', 'new', 'loop', 'include', 'extend', 'raise', 'attr_reader', 'attr_writer', 'attr_accessor', 'attr', 'catch', 'throw', 'private', 'module_function', 'public', 'protected', 'true', 'false', 'nil'), suffix='\\b'), Keyword.Pseudo), ('(not|and|or)\\b', Operator.Word), (words(('autoload', 'block_given', 'const_defined', 'eql', 'equal', 'frozen', 'include', 'instance_of', 'is_a', 'iterator', 'kind_of', 'method_defined', 'nil', 'private_method_defined', 'protected_method_defined', 'public_method_defined', 'respond_to', 'tainted'), suffix='\\?'), Name.Builtin), ('(chomp|chop|exit|gsub|sub)!', Name.Builtin), (words(('Array', 'Float', 'Integer', 'String', '__id__', '__send__', 'abort', 'ancestors', 'at_exit', 'autoload', 'binding', 'callcc', 'caller', 'catch', 'chomp', 'chop', 'class_eval', 'class_variables', 'clone', 'const_defined?', 'const_get', 'const_missing', 'const_set', 'constants', 'display', 'dup', 'eval', 'exec', 'exit', 'extend', 'fail', 'fork', 'format', 'freeze', 'getc', 'gets', 'global_variables', 'gsub', 'hash', 'id', 'included_modules', 'inspect', 'instance_eval', 'instance_method', 'instance_methods', 'instance_variable_get', 'instance_variable_set', 'instance_variables', 'lambda', 'load', 'local_variables', 'loop', 'method', 'method_missing', 'methods', 'module_eval', 'name', 'object_id', 'open', 'p', 'print', 'printf', 'private_class_method', 'private_instance_methods', 'private_methods', 'proc', 'protected_instance_methods', 'protected_methods', 'public_class_method', 'public_instance_methods', 'public_methods', 'putc', 'puts', 'raise', 'rand', 'readline', 'readlines', 'require', 'scan', 'select', 'self', 'send', 'set_trace_func', 'singleton_methods', 'sleep', 'split', 'sprintf', 'srand', 'sub', 'syscall', 'system', 'taint', 'test', 'throw', 'to_a', 'to_s', 'trace_var', 'trap', 'untaint', 'untrace_var', 'warn'), prefix='(?<!\\.)', suffix='\\b'), Name.Builtin), ('__(FILE|LINE)__\\b', Name.Builtin.Pseudo), ('(?<!\\w)(<<[-~]?)(["`\\\']?)([a-zA-Z_]\\w*)(\\2)(.*?\\n)', heredoc_callback), ('(<<[-~]?)("|\\\')()(\\2)(.*?\\n)', heredoc_callback), ('__END__', Comment.Preproc, 'end-part'), ('(?:^|(?<=[=<>~!:])|(?<=(?:\\s|;)when\\s)|(?<=(?:\\s|;)or\\s)|(?<=(?:\\s|;)and\\s)|(?<=\\.index\\s)|(?<=\\.scan\\s)|(?<=\\.sub\\s)|(?<=\\.sub!\\s)|(?<=\\.gsub\\s)|(?<=\\.gsub!\\s)|(?<=\\.match\\s)|(?<=(?:\\s|;)if\\s)|(?<=(?:\\s|;)elsif\\s)|(?<=^when\\s)|(?<=^index\\s)|(?<=^scan\\s)|(?<=^sub\\s)|(?<=^gsub\\s)|(?<=^sub!\\s)|(?<=^gsub!\\s)|(?<=^match\\s)|(?<=^if\\s)|(?<=^elsif\\s))(\\s*)(/)', bygroups(Text, String.Regex), 'multiline-regex'), ('(?<=\\(|,|\\[)/', String.Regex, 'multiline-regex'), ('(\\s+)(/)(?![\\s=])', bygroups(Whitespace, String.Regex), 'multiline-regex'), ('(0_?[0-7]+(?:_[0-7]+)*)(\\s*)([/?])?', bygroups(Number.Oct, Whitespace, Operator)), ('(0x[0-9A-Fa-f]+(?:_[0-9A-Fa-f]+)*)(\\s*)([/?])?', bygroups(Number.Hex, Whitespace, Operator)), ('(0b[01]+(?:_[01]+)*)(\\s*)([/?])?', bygroups(Number.Bin, Whitespace, Operator)), ('([\\d]+(?:_\\d+)*)(\\s*)([/?])?', bygroups(Number.Integer, Whitespace, Operator)), ('@@[a-zA-Z_]\\w*', Name.Variable.Class), ('@[a-zA-Z_]\\w*', Name.Variable.Instance), ('\\$\\w+', Name.Variable.Global), ('\\$[!@&`\\\'+~=/\\\\,;.<>_*$?:"^-]', Name.Variable.Global), ('\\$-[0adFiIlpvw]', Name.Variable.Global), ('::', Operator), include('strings'), ('\\?(\\\\[MC]-)*(\\\\([\\\\abefnrstv#"\\\']|x[a-fA-F0-9]{1,2}|[0-7]{1,3})|\\S)(?!\\w)', String.Char), ('[A-Z]\\w+', Name.Constant), (words(RUBY_OPERATORS, prefix='(\\.|::)'), bygroups(Operator, Name.Operator)), ('(\\.|::)([a-zA-Z_]\\w*[!?]?|[*%&^`~+\\-/\\[<>=])', bygroups(Operator, Name)), ('[a-zA-Z_]\\w*[!?]?', Name), ('(\\[|\\]|\\*\\*|<<?|>>?|>=|<=|<=>|=~|={3}|!~|&&?|\\|\\||\\.{1,3})', Operator), ('[-+/*%=<>&!^|~]=?', Operator), ('[(){};,/?:\\\\]', Punctuation), ('\\s+', Whitespace)], 'funcname': [('\\(', Punctuation, 'defexpr'), ('(?:([a-zA-Z_]\\w*)(\\.))?([a-zA-Z\\u0080-\\uffff][a-zA-Z0-9_\\u0080-\\uffff]*[!?=]?|!=|!~|=~|\\*\\*?|[-+!~]@?|[/%&|^]|<=>|<[<=]?|>[>=]?|===?|\\[\\]=?|`)', bygroups(Name.Class, Operator, Name.Function), '#pop'), default('#pop')], 'classname': [('\\(', Punctuation, 'defexpr'), ('<<', Operator, '#pop'), ('[A-Z_]\\w*', Name.Class, '#pop'), default('#pop')], 'defexpr': [('(\\))(\\.|::)?', bygroups(Punctuation, Operator), '#pop'), ('\\(', Operator, '#push'), include('root')], 'in-intp': [('\\{', String.Interpol, '#push'), ('\\}', String.Interpol, '#pop'), include('root')], 'string-intp': [('#\\{', String.Interpol, 'in-intp'), ('#@@?[a-zA-Z_]\\w*', String.Interpol), ('#\\$[a-zA-Z_]\\w*', String.Interpol)], 'string-intp-escaped': [include('string-intp'), ('\\\\([\\\\abefnrstv#"\\\']|x[a-fA-F0-9]{1,2}|[0-7]{1,3})', String.Escape)], 'interpolated-regex': [include('string-intp'), ('[\\\\#]', String.Regex), ('[^\\\\#]+', String.Regex)], 'interpolated-string': [include('string-intp'), ('[\\\\#]', String.Other), ('[^\\\\#]+', String.Other)], 'multiline-regex': [include('string-intp'), ('\\\\\\\\', String.Regex), ('\\\\/', String.Regex), ('[\\\\#]', String.Regex), ('[^\\\\/#]+', String.Regex), ('/[mixounse]*', String.Regex, '#pop')], 'end-part': [('.+', Comment.Preproc, '#pop')]}
    tokens.update(gen_rubystrings_rules())
    
    def analyse_text(text):
        return shebang_matches(text, 'ruby(1\\.\\d)?')



class RubyConsoleLexer(Lexer):
    """
    For Ruby interactive console (**irb**) output.
    """
    name = 'Ruby irb session'
    aliases = ['rbcon', 'irb']
    mimetypes = ['text/x-ruby-shellsession']
    url = 'https://www.ruby-lang.org'
    version_added = ''
    _example = 'rbcon/console'
    _prompt_re = re.compile('irb\\([a-zA-Z_]\\w*\\):\\d{3}:\\d+[>*"\\\'] |>> |\\?> ')
    
    def get_tokens_unprocessed(self, text):
        rblexer = RubyLexer(**self.options)
        curcode = ''
        insertions = []
        for match in line_re.finditer(text):
            line = match.group()
            m = self._prompt_re.match(line)
            if m is not None:
                end = m.end()
                insertions.append((len(curcode), [(0, Generic.Prompt, line[:end])]))
                curcode += line[end:]
            else:
                if curcode:
                    yield from do_insertions(insertions, rblexer.get_tokens_unprocessed(curcode))
                    curcode = ''
                    insertions = []
                yield (match.start(), Generic.Output, line)
        if curcode:
            yield from do_insertions(insertions, rblexer.get_tokens_unprocessed(curcode))



class FancyLexer(RegexLexer):
    """
    Pygments Lexer For Fancy.

    Fancy is a self-hosted, pure object-oriented, dynamic,
    class-based, concurrent general-purpose programming language
    running on Rubinius, the Ruby VM.
    """
    name = 'Fancy'
    url = 'https://github.com/bakkdoor/fancy'
    filenames = ['*.fy', '*.fancypack']
    aliases = ['fancy', 'fy']
    mimetypes = ['text/x-fancysrc']
    version_added = '1.5'
    tokens = {'balanced-regex': [('/(\\\\\\\\|\\\\[^\\\\]|[^/\\\\])*/[egimosx]*', String.Regex, '#pop'), ('!(\\\\\\\\|\\\\[^\\\\]|[^!\\\\])*![egimosx]*', String.Regex, '#pop'), ('\\\\(\\\\\\\\|[^\\\\])*\\\\[egimosx]*', String.Regex, '#pop'), ('\\{(\\\\\\\\|\\\\[^\\\\]|[^}\\\\])*\\}[egimosx]*', String.Regex, '#pop'), ('<(\\\\\\\\|\\\\[^\\\\]|[^>\\\\])*>[egimosx]*', String.Regex, '#pop'), ('\\[(\\\\\\\\|\\\\[^\\\\]|[^\\]\\\\])*\\][egimosx]*', String.Regex, '#pop'), ('\\((\\\\\\\\|\\\\[^\\\\]|[^)\\\\])*\\)[egimosx]*', String.Regex, '#pop'), ('@(\\\\\\\\|\\\\[^\\\\]|[^@\\\\])*@[egimosx]*', String.Regex, '#pop'), ('%(\\\\\\\\|\\\\[^\\\\]|[^%\\\\])*%[egimosx]*', String.Regex, '#pop'), ('\\$(\\\\\\\\|\\\\[^\\\\]|[^$\\\\])*\\$[egimosx]*', String.Regex, '#pop')], 'root': [('\\s+', Whitespace), ('s\\{(\\\\\\\\|\\\\[^\\\\]|[^}\\\\])*\\}\\s*', String.Regex, 'balanced-regex'), ('s<(\\\\\\\\|\\\\[^\\\\]|[^>\\\\])*>\\s*', String.Regex, 'balanced-regex'), ('s\\[(\\\\\\\\|\\\\[^\\\\]|[^\\]\\\\])*\\]\\s*', String.Regex, 'balanced-regex'), ('s\\((\\\\\\\\|\\\\[^\\\\]|[^)\\\\])*\\)\\s*', String.Regex, 'balanced-regex'), ('m?/(\\\\\\\\|\\\\[^\\\\]|[^///\\n])*/[gcimosx]*', String.Regex), ('m(?=[/!\\\\{<\\[(@%$])', String.Regex, 'balanced-regex'), ('#(.*?)\\n', Comment.Single), ("\\'([^\\'\\s\\[\\](){}]+|\\[\\])", String.Symbol), ('"""(\\\\\\\\|\\\\[^\\\\]|[^\\\\])*?"""', String), ('"(\\\\\\\\|\\\\[^\\\\]|[^"\\\\])*"', String), ('(def|class|try|catch|finally|retry|return|return_local|match|case|->|=>)\\b', Keyword), ('(self|super|nil|false|true)\\b', Name.Constant), ('[(){};,/?|:\\\\]', Punctuation), (words(('Object', 'Array', 'Hash', 'Directory', 'File', 'Class', 'String', 'Number', 'Enumerable', 'FancyEnumerable', 'Block', 'TrueClass', 'NilClass', 'FalseClass', 'Tuple', 'Symbol', 'Stack', 'Set', 'FancySpec', 'Method', 'Package', 'Range'), suffix='\\b'), Name.Builtin), ('[a-zA-Z](\\w|[-+?!=*/^><%])*:', Name.Function), ('[-+*/~,<>=&!?%^\\[\\].$]+', Operator), ('[A-Z]\\w*', Name.Constant), ('@[a-zA-Z_]\\w*', Name.Variable.Instance), ('@@[a-zA-Z_]\\w*', Name.Variable.Class), ('@@?', Operator), ('[a-zA-Z_]\\w*', Name), ('(0[oO]?[0-7]+(?:_[0-7]+)*)(\\s*)([/?])?', bygroups(Number.Oct, Whitespace, Operator)), ('(0[xX][0-9A-Fa-f]+(?:_[0-9A-Fa-f]+)*)(\\s*)([/?])?', bygroups(Number.Hex, Whitespace, Operator)), ('(0[bB][01]+(?:_[01]+)*)(\\s*)([/?])?', bygroups(Number.Bin, Whitespace, Operator)), ('([\\d]+(?:_\\d+)*)(\\s*)([/?])?', bygroups(Number.Integer, Whitespace, Operator)), ('\\d+([eE][+-]?[0-9]+)|\\d+\\.\\d+([eE][+-]?[0-9]+)?', Number.Float), ('\\d+', Number.Integer)]}


