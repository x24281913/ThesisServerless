"""
    pygments.lexers.erlang
    ~~~~~~~~~~~~~~~~~~~~~~

    Lexers for Erlang.

    :copyright: Copyright 2006-present by the Pygments team, see AUTHORS.
    :license: BSD, see LICENSE for details.
"""

import re
from pygments.lexer import Lexer, RegexLexer, bygroups, words, do_insertions, include, default, line_re
from pygments.token import Comment, Operator, Keyword, Name, String, Number, Punctuation, Generic, Whitespace
__all__ = ['ErlangLexer', 'ErlangShellLexer', 'ElixirConsoleLexer', 'ElixirLexer']


class ErlangLexer(RegexLexer):
    """
    For the Erlang functional programming language.
    """
    name = 'Erlang'
    url = 'https://www.erlang.org/'
    aliases = ['erlang']
    filenames = ['*.erl', '*.hrl', '*.es', '*.escript']
    mimetypes = ['text/x-erlang']
    version_added = '0.9'
    keywords = ('after', 'begin', 'case', 'catch', 'cond', 'end', 'fun', 'if', 'let', 'of', 'query', 'receive', 'try', 'when')
    builtins = ('abs', 'append_element', 'apply', 'atom_to_list', 'binary_to_list', 'bitstring_to_list', 'binary_to_term', 'bit_size', 'bump_reductions', 'byte_size', 'cancel_timer', 'check_process_code', 'delete_module', 'demonitor', 'disconnect_node', 'display', 'element', 'erase', 'exit', 'float', 'float_to_list', 'fun_info', 'fun_to_list', 'function_exported', 'garbage_collect', 'get', 'get_keys', 'group_leader', 'hash', 'hd', 'integer_to_list', 'iolist_to_binary', 'iolist_size', 'is_atom', 'is_binary', 'is_bitstring', 'is_boolean', 'is_builtin', 'is_float', 'is_function', 'is_integer', 'is_list', 'is_number', 'is_pid', 'is_port', 'is_process_alive', 'is_record', 'is_reference', 'is_tuple', 'length', 'link', 'list_to_atom', 'list_to_binary', 'list_to_bitstring', 'list_to_existing_atom', 'list_to_float', 'list_to_integer', 'list_to_pid', 'list_to_tuple', 'load_module', 'localtime_to_universaltime', 'make_tuple', 'md5', 'md5_final', 'md5_update', 'memory', 'module_loaded', 'monitor', 'monitor_node', 'node', 'nodes', 'open_port', 'phash', 'phash2', 'pid_to_list', 'port_close', 'port_command', 'port_connect', 'port_control', 'port_call', 'port_info', 'port_to_list', 'process_display', 'process_flag', 'process_info', 'purge_module', 'put', 'read_timer', 'ref_to_list', 'register', 'resume_process', 'round', 'send', 'send_after', 'send_nosuspend', 'set_cookie', 'setelement', 'size', 'spawn', 'spawn_link', 'spawn_monitor', 'spawn_opt', 'split_binary', 'start_timer', 'statistics', 'suspend_process', 'system_flag', 'system_info', 'system_monitor', 'system_profile', 'term_to_binary', 'tl', 'trace', 'trace_delivered', 'trace_info', 'trace_pattern', 'trunc', 'tuple_size', 'tuple_to_list', 'universaltime_to_localtime', 'unlink', 'unregister', 'whereis')
    operators = '(\\+\\+?|--?|\\*|/|<|>|/=|=:=|=/=|=<|>=|==?|<-|!|\\?)'
    word_operators = ('and', 'andalso', 'band', 'bnot', 'bor', 'bsl', 'bsr', 'bxor', 'div', 'not', 'or', 'orelse', 'rem', 'xor')
    atom_re = "(?:[a-z]\\w*|'[^\\n']*[^\\\\]')"
    variable_re = '(?:[A-Z_]\\w*)'
    esc_char_re = '[bdefnrstv\\\'"\\\\]'
    esc_octal_re = '[0-7][0-7]?[0-7]?'
    esc_hex_re = '(?:x[0-9a-fA-F]{2}|x\\{[0-9a-fA-F]+\\})'
    esc_ctrl_re = '\\^[a-zA-Z]'
    escape_re = '(?:\\\\(?:' + esc_char_re + '|' + esc_octal_re + '|' + esc_hex_re + '|' + esc_ctrl_re + '))'
    macro_re = '(?:' + variable_re + '|' + atom_re + ')'
    base_re = '(?:[2-9]|[12][0-9]|3[0-6])'
    tokens = {'root': [('\\s+', Whitespace), ('(%.*)(\\n)', bygroups(Comment, Whitespace)), (words(keywords, suffix='\\b'), Keyword), (words(builtins, suffix='\\b'), Name.Builtin), (words(word_operators, suffix='\\b'), Operator.Word), ('^-', Punctuation, 'directive'), (operators, Operator), ('"', String, 'string'), ('<<', Name.Label), ('>>', Name.Label), ('(' + atom_re + ')(:)', bygroups(Name.Namespace, Punctuation)), ('(?:^|(?<=:))(' + atom_re + ')(\\s*)(\\()', bygroups(Name.Function, Whitespace, Punctuation)), ('[+-]?' + base_re + '#[0-9a-zA-Z]+', Number.Integer), ('[+-]?\\d+', Number.Integer), ('[+-]?\\d+.\\d+', Number.Float), ('[]\\[:_@\\".{}()|;,]', Punctuation), (variable_re, Name.Variable), (atom_re, Name), ('\\?' + macro_re, Name.Constant), ('\\$(?:' + escape_re + '|\\\\[ %]|[^\\\\])', String.Char), ('#' + atom_re + '(:?\\.' + atom_re + ')?', Name.Label), ('\\A#!.+\\n', Comment.Hashbang), ('#\\{', Punctuation, 'map_key')], 'string': [(escape_re, String.Escape), ('"', String, '#pop'), ('~[0-9.*]*[~#+BPWXb-ginpswx]', String.Interpol), ('[^"\\\\~]+', String), ('~', String)], 'directive': [('(define)(\\s*)(\\()(' + macro_re + ')', bygroups(Name.Entity, Whitespace, Punctuation, Name.Constant), '#pop'), ('(record)(\\s*)(\\()(' + macro_re + ')', bygroups(Name.Entity, Whitespace, Punctuation, Name.Label), '#pop'), (atom_re, Name.Entity, '#pop')], 'map_key': [include('root'), ('=>', Punctuation, 'map_val'), (':=', Punctuation, 'map_val'), ('\\}', Punctuation, '#pop')], 'map_val': [include('root'), (',', Punctuation, '#pop'), ('(?=\\})', Punctuation, '#pop')]}



class ErlangShellLexer(Lexer):
    """
    Shell sessions in erl (for Erlang code).
    """
    name = 'Erlang erl session'
    aliases = ['erl']
    filenames = ['*.erl-sh']
    mimetypes = ['text/x-erl-shellsession']
    url = 'https://www.erlang.org/'
    version_added = '1.1'
    _prompt_re = re.compile('(?:\\([\\w@_.]+\\))?\\d+>(?=\\s|\\Z)')
    
    def get_tokens_unprocessed(self, text):
        erlexer = ErlangLexer(**self.options)
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
                    yield from do_insertions(insertions, erlexer.get_tokens_unprocessed(curcode))
                    curcode = ''
                    insertions = []
                if line.startswith('*'):
                    yield (match.start(), Generic.Traceback, line)
                else:
                    yield (match.start(), Generic.Output, line)
        if curcode:
            yield from do_insertions(insertions, erlexer.get_tokens_unprocessed(curcode))


def gen_elixir_string_rules(name, symbol, token):
    import custom_funtemplate
    return custom_funtemplate.rewrite_template('pygments.lexers.erlang.gen_elixir_string_rules', 'gen_elixir_string_rules(name, symbol, token)', {'include': include, 'bygroups': bygroups, 'name': name, 'symbol': symbol, 'token': token}, 1)

def gen_elixir_sigstr_rules(term, term_class, token, interpol=True):
    import custom_funtemplate
    return custom_funtemplate.rewrite_template('pygments.lexers.erlang.gen_elixir_sigstr_rules', 'gen_elixir_sigstr_rules(term, term_class, token, interpol=True)', {'include': include, 'term': term, 'term_class': term_class, 'token': token, 'interpol': interpol}, 1)


class ElixirLexer(RegexLexer):
    """
    For the Elixir language.
    """
    name = 'Elixir'
    url = 'https://elixir-lang.org'
    aliases = ['elixir', 'ex', 'exs']
    filenames = ['*.ex', '*.eex', '*.exs', '*.leex']
    mimetypes = ['text/x-elixir']
    version_added = '1.5'
    KEYWORD = ('fn', 'do', 'end', 'after', 'else', 'rescue', 'catch')
    KEYWORD_OPERATOR = ('not', 'and', 'or', 'when', 'in')
    BUILTIN = ('case', 'cond', 'for', 'if', 'unless', 'try', 'receive', 'raise', 'quote', 'unquote', 'unquote_splicing', 'throw', 'super')
    BUILTIN_DECLARATION = ('def', 'defp', 'defmodule', 'defprotocol', 'defmacro', 'defmacrop', 'defdelegate', 'defexception', 'defstruct', 'defimpl', 'defcallback')
    BUILTIN_NAMESPACE = ('import', 'require', 'use', 'alias')
    CONSTANT = ('nil', 'true', 'false')
    PSEUDO_VAR = ('_', '__MODULE__', '__DIR__', '__ENV__', '__CALLER__')
    OPERATORS3 = ('<<<', '>>>', '|||', '&&&', '^^^', '~~~', '===', '!==', '~>>', '<~>', '|~>', '<|>')
    OPERATORS2 = ('==', '!=', '<=', '>=', '&&', '||', '<>', '++', '--', '|>', '=~', '->', '<-', '|', '.', '=', '~>', '<~')
    OPERATORS1 = ('<', '>', '+', '-', '*', '/', '!', '^', '&')
    PUNCTUATION = ('\\\\', '<<', '>>', '=>', '(', ')', ':', ';', ',', '[', ']')
    
    def get_tokens_unprocessed(self, text):
        for (index, token, value) in RegexLexer.get_tokens_unprocessed(self, text):
            if token is Name:
                if value in self.KEYWORD:
                    yield (index, Keyword, value)
                elif value in self.KEYWORD_OPERATOR:
                    yield (index, Operator.Word, value)
                elif value in self.BUILTIN:
                    yield (index, Keyword, value)
                elif value in self.BUILTIN_DECLARATION:
                    yield (index, Keyword.Declaration, value)
                elif value in self.BUILTIN_NAMESPACE:
                    yield (index, Keyword.Namespace, value)
                elif value in self.CONSTANT:
                    yield (index, Name.Constant, value)
                elif value in self.PSEUDO_VAR:
                    yield (index, Name.Builtin.Pseudo, value)
                else:
                    yield (index, token, value)
            else:
                yield (index, token, value)
    
    def gen_elixir_sigil_rules():
        terminators = [('\\{', '\\}', '}', 'cb'), ('\\[', '\\]', '\\]', 'sb'), ('\\(', '\\)', ')', 'pa'), ('<', '>', '>', 'ab'), ('/', '/', '/', 'slas'), ('\\|', '\\|', '|', 'pipe'), ('"', '"', '"', 'quot'), ("'", "'", "'", 'apos')]
        triquotes = [('"""', 'triquot'), ("'''", 'triapos')]
        token = String.Other
        states = {'sigils': []}
        for (term, name) in triquotes:
            states['sigils'] += [(f'(~[a-z])({term})', bygroups(token, String.Heredoc), (name + '-end', name + '-intp')), (f'(~[A-Z])({term})', bygroups(token, String.Heredoc), (name + '-end', name + '-no-intp'))]
            states[name + '-end'] = [('[a-zA-Z]+', token, '#pop'), default('#pop')]
            states[name + '-intp'] = [('^(\\s*)(' + term + ')', bygroups(Whitespace, String.Heredoc), '#pop'), include('heredoc_interpol')]
            states[name + '-no-intp'] = [('^(\\s*)(' + term + ')', bygroups(Whitespace, String.Heredoc), '#pop'), include('heredoc_no_interpol')]
        for (lterm, rterm, rterm_class, name) in terminators:
            states['sigils'] += [('~[a-z]' + lterm, token, name + '-intp'), ('~[A-Z]' + lterm, token, name + '-no-intp')]
            states[name + '-intp'] = gen_elixir_sigstr_rules(rterm, rterm_class, token)
            states[name + '-no-intp'] = gen_elixir_sigstr_rules(rterm, rterm_class, token, interpol=False)
        return states
    op3_re = '|'.join((re.escape(s) for s in OPERATORS3))
    op2_re = '|'.join((re.escape(s) for s in OPERATORS2))
    op1_re = '|'.join((re.escape(s) for s in OPERATORS1))
    ops_re = f'(?:{op3_re}|{op2_re}|{op1_re})'
    punctuation_re = '|'.join((re.escape(s) for s in PUNCTUATION))
    alnum = '\\w'
    name_re = f'(?:\\.\\.\\.|[a-z_]{alnum}*[!?]?)'
    modname_re = f'[A-Z]{alnum}*(?:\\.[A-Z]{alnum}*)*'
    complex_name_re = f'(?:{name_re}|{modname_re}|{ops_re})'
    special_atom_re = '(?:\\.\\.\\.|<<>>|%\\{\\}|%|\\{\\})'
    long_hex_char_re = '(\\\\x\\{)([\\da-fA-F]+)(\\})'
    hex_char_re = '(\\\\x[\\da-fA-F]{1,2})'
    escape_char_re = '(\\\\[abdefnrstv])'
    tokens = {'root': [('\\s+', Whitespace), ('#.*$', Comment.Single), ('(\\?)' + long_hex_char_re, bygroups(String.Char, String.Escape, Number.Hex, String.Escape)), ('(\\?)' + hex_char_re, bygroups(String.Char, String.Escape)), ('(\\?)' + escape_char_re, bygroups(String.Char, String.Escape)), ('\\?\\\\?.', String.Char), (':::', String.Symbol), ('::', Operator), (':' + special_atom_re, String.Symbol), (':' + complex_name_re, String.Symbol), (':"', String.Symbol, 'string_double_atom'), (":'", String.Symbol, 'string_single_atom'), (f'({special_atom_re}|{complex_name_re})(:)(?=\\s|\\n)', bygroups(String.Symbol, Punctuation)), ('@' + name_re, Name.Attribute), (name_re, Name), (f'(%?)({modname_re})', bygroups(Punctuation, Name.Class)), (op3_re, Operator), (op2_re, Operator), (punctuation_re, Punctuation), ('&\\d', Name.Entity), (op1_re, Operator), ('0b[01]+', Number.Bin), ('0o[0-7]+', Number.Oct), ('0x[\\da-fA-F]+', Number.Hex), ('\\d(_?\\d)*\\.\\d(_?\\d)*([eE][-+]?\\d(_?\\d)*)?', Number.Float), ('\\d(_?\\d)*', Number.Integer), ('(""")(\\s*)', bygroups(String.Heredoc, Whitespace), 'heredoc_double'), ("(''')(\\s*)$", bygroups(String.Heredoc, Whitespace), 'heredoc_single'), ('"', String.Double, 'string_double'), ("'", String.Single, 'string_single'), include('sigils'), ('%\\{', Punctuation, 'map_key'), ('\\{', Punctuation, 'tuple')], 'heredoc_double': [('^(\\s*)(""")', bygroups(Whitespace, String.Heredoc), '#pop'), include('heredoc_interpol')], 'heredoc_single': [("^\\s*'''", String.Heredoc, '#pop'), include('heredoc_interpol')], 'heredoc_interpol': [('[^#\\\\\\n]+', String.Heredoc), include('escapes'), ('\\\\.', String.Heredoc), ('\\n+', String.Heredoc), include('interpol')], 'heredoc_no_interpol': [('[^\\\\\\n]+', String.Heredoc), ('\\\\.', String.Heredoc), ('\\n+', Whitespace)], 'escapes': [(long_hex_char_re, bygroups(String.Escape, Number.Hex, String.Escape)), (hex_char_re, String.Escape), (escape_char_re, String.Escape)], 'interpol': [('#\\{', String.Interpol, 'interpol_string')], 'interpol_string': [('\\}', String.Interpol, '#pop'), include('root')], 'map_key': [include('root'), (':', Punctuation, 'map_val'), ('=>', Punctuation, 'map_val'), ('\\}', Punctuation, '#pop')], 'map_val': [include('root'), (',', Punctuation, '#pop'), ('(?=\\})', Punctuation, '#pop')], 'tuple': [include('root'), ('\\}', Punctuation, '#pop')]}
    tokens.update(gen_elixir_string_rules('double', '"', String.Double))
    tokens.update(gen_elixir_string_rules('single', "'", String.Single))
    tokens.update(gen_elixir_string_rules('double_atom', '"', String.Symbol))
    tokens.update(gen_elixir_string_rules('single_atom', "'", String.Symbol))
    tokens.update(gen_elixir_sigil_rules())



class ElixirConsoleLexer(Lexer):
    """
    For Elixir interactive console (iex) output like:

    .. sourcecode:: iex

        iex> [head | tail] = [1,2,3]
        [1,2,3]
        iex> head
        1
        iex> tail
        [2,3]
        iex> [head | tail]
        [1,2,3]
        iex> length [head | tail]
        3
    """
    name = 'Elixir iex session'
    aliases = ['iex']
    mimetypes = ['text/x-elixir-shellsession']
    url = 'https://elixir-lang.org'
    version_added = '1.5'
    _prompt_re = re.compile('(iex|\\.{3})((?:\\([\\w@_.]+\\))?\\d+|\\(\\d+\\))?> ')
    
    def get_tokens_unprocessed(self, text):
        exlexer = ElixirLexer(**self.options)
        curcode = ''
        in_error = False
        insertions = []
        for match in line_re.finditer(text):
            line = match.group()
            if line.startswith('** '):
                in_error = True
                insertions.append((len(curcode), [(0, Generic.Error, line[:-1])]))
                curcode += line[-1:]
            else:
                m = self._prompt_re.match(line)
                if m is not None:
                    in_error = False
                    end = m.end()
                    insertions.append((len(curcode), [(0, Generic.Prompt, line[:end])]))
                    curcode += line[end:]
                else:
                    if curcode:
                        yield from do_insertions(insertions, exlexer.get_tokens_unprocessed(curcode))
                        curcode = ''
                        insertions = []
                    token = (Generic.Error if in_error else Generic.Output)
                    yield (match.start(), token, line)
        if curcode:
            yield from do_insertions(insertions, exlexer.get_tokens_unprocessed(curcode))


