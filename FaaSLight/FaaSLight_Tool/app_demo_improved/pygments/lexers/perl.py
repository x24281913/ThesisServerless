"""
    pygments.lexers.perl
    ~~~~~~~~~~~~~~~~~~~~

    Lexers for Perl, Raku and related languages.

    :copyright: Copyright 2006-present by the Pygments team, see AUTHORS.
    :license: BSD, see LICENSE for details.
"""

import re
from pygments.lexer import RegexLexer, ExtendedRegexLexer, include, bygroups, using, this, default, words
from pygments.token import Text, Comment, Operator, Keyword, Name, String, Number, Punctuation, Whitespace
from pygments.util import shebang_matches
__all__ = ['PerlLexer', 'Perl6Lexer']


class PerlLexer(RegexLexer):
    """
    For Perl source code.
    """
    name = 'Perl'
    url = 'https://www.perl.org'
    aliases = ['perl', 'pl']
    filenames = ['*.pl', '*.pm', '*.t', '*.perl']
    mimetypes = ['text/x-perl', 'application/x-perl']
    version_added = ''
    flags = re.DOTALL | re.MULTILINE
    tokens = {'balanced-regex': [('/(\\\\\\\\|\\\\[^\\\\]|[^\\\\/])*/[egimosx]*', String.Regex, '#pop'), ('!(\\\\\\\\|\\\\[^\\\\]|[^\\\\!])*![egimosx]*', String.Regex, '#pop'), ('\\\\(\\\\\\\\|[^\\\\])*\\\\[egimosx]*', String.Regex, '#pop'), ('\\{(\\\\\\\\|\\\\[^\\\\]|[^\\\\}])*\\}[egimosx]*', String.Regex, '#pop'), ('<(\\\\\\\\|\\\\[^\\\\]|[^\\\\>])*>[egimosx]*', String.Regex, '#pop'), ('\\[(\\\\\\\\|\\\\[^\\\\]|[^\\\\\\]])*\\][egimosx]*', String.Regex, '#pop'), ('\\((\\\\\\\\|\\\\[^\\\\]|[^\\\\)])*\\)[egimosx]*', String.Regex, '#pop'), ('@(\\\\\\\\|\\\\[^\\\\]|[^\\\\@])*@[egimosx]*', String.Regex, '#pop'), ('%(\\\\\\\\|\\\\[^\\\\]|[^\\\\%])*%[egimosx]*', String.Regex, '#pop'), ('\\$(\\\\\\\\|\\\\[^\\\\]|[^\\\\$])*\\$[egimosx]*', String.Regex, '#pop')], 'root': [('\\A\\#!.+?$', Comment.Hashbang), ('\\#.*?$', Comment.Single), ('^=[a-zA-Z0-9]+\\s+.*?\\n=cut', Comment.Multiline), (words(('case', 'continue', 'do', 'else', 'elsif', 'for', 'foreach', 'if', 'last', 'my', 'next', 'our', 'redo', 'reset', 'then', 'unless', 'until', 'while', 'print', 'new', 'BEGIN', 'CHECK', 'INIT', 'END', 'return'), suffix='\\b'), Keyword), ('(format)(\\s+)(\\w+)(\\s*)(=)(\\s*\\n)', bygroups(Keyword, Whitespace, Name, Whitespace, Punctuation, Whitespace), 'format'), ('(eq|lt|gt|le|ge|ne|not|and|or|cmp)\\b', Operator.Word), ('s/(\\\\\\\\|\\\\[^\\\\]|[^\\\\/])*/(\\\\\\\\|\\\\[^\\\\]|[^\\\\/])*/[egimosx]*', String.Regex), ('s!(\\\\\\\\|\\\\!|[^!])*!(\\\\\\\\|\\\\!|[^!])*![egimosx]*', String.Regex), ('s\\\\(\\\\\\\\|[^\\\\])*\\\\(\\\\\\\\|[^\\\\])*\\\\[egimosx]*', String.Regex), ('s@(\\\\\\\\|\\\\[^\\\\]|[^\\\\@])*@(\\\\\\\\|\\\\[^\\\\]|[^\\\\@])*@[egimosx]*', String.Regex), ('s%(\\\\\\\\|\\\\[^\\\\]|[^\\\\%])*%(\\\\\\\\|\\\\[^\\\\]|[^\\\\%])*%[egimosx]*', String.Regex), ('s\\{(\\\\\\\\|\\\\[^\\\\]|[^\\\\}])*\\}\\s*', String.Regex, 'balanced-regex'), ('s<(\\\\\\\\|\\\\[^\\\\]|[^\\\\>])*>\\s*', String.Regex, 'balanced-regex'), ('s\\[(\\\\\\\\|\\\\[^\\\\]|[^\\\\\\]])*\\]\\s*', String.Regex, 'balanced-regex'), ('s\\((\\\\\\\\|\\\\[^\\\\]|[^\\\\)])*\\)\\s*', String.Regex, 'balanced-regex'), ('m?/(\\\\\\\\|\\\\[^\\\\]|[^\\\\/\\n])*/[gcimosx]*', String.Regex), ('m(?=[/!\\\\{<\\[(@%$])', String.Regex, 'balanced-regex'), ('((?<==~)|(?<=\\())\\s*/(\\\\\\\\|\\\\[^\\\\]|[^\\\\/])*/[gcimosx]*', String.Regex), ('\\s+', Whitespace), (words(('abs', 'accept', 'alarm', 'atan2', 'bind', 'binmode', 'bless', 'caller', 'chdir', 'chmod', 'chomp', 'chop', 'chown', 'chr', 'chroot', 'close', 'closedir', 'connect', 'continue', 'cos', 'crypt', 'dbmclose', 'dbmopen', 'defined', 'delete', 'die', 'dump', 'each', 'endgrent', 'endhostent', 'endnetent', 'endprotoent', 'endpwent', 'endservent', 'eof', 'eval', 'exec', 'exists', 'exit', 'exp', 'fcntl', 'fileno', 'flock', 'fork', 'format', 'formline', 'getc', 'getgrent', 'getgrgid', 'getgrnam', 'gethostbyaddr', 'gethostbyname', 'gethostent', 'getlogin', 'getnetbyaddr', 'getnetbyname', 'getnetent', 'getpeername', 'getpgrp', 'getppid', 'getpriority', 'getprotobyname', 'getprotobynumber', 'getprotoent', 'getpwent', 'getpwnam', 'getpwuid', 'getservbyname', 'getservbyport', 'getservent', 'getsockname', 'getsockopt', 'glob', 'gmtime', 'goto', 'grep', 'hex', 'import', 'index', 'int', 'ioctl', 'join', 'keys', 'kill', 'last', 'lc', 'lcfirst', 'length', 'link', 'listen', 'local', 'localtime', 'log', 'lstat', 'map', 'mkdir', 'msgctl', 'msgget', 'msgrcv', 'msgsnd', 'my', 'next', 'oct', 'open', 'opendir', 'ord', 'our', 'pack', 'pipe', 'pop', 'pos', 'printf', 'prototype', 'push', 'quotemeta', 'rand', 'read', 'readdir', 'readline', 'readlink', 'readpipe', 'recv', 'redo', 'ref', 'rename', 'reverse', 'rewinddir', 'rindex', 'rmdir', 'scalar', 'seek', 'seekdir', 'select', 'semctl', 'semget', 'semop', 'send', 'setgrent', 'sethostent', 'setnetent', 'setpgrp', 'setpriority', 'setprotoent', 'setpwent', 'setservent', 'setsockopt', 'shift', 'shmctl', 'shmget', 'shmread', 'shmwrite', 'shutdown', 'sin', 'sleep', 'socket', 'socketpair', 'sort', 'splice', 'split', 'sprintf', 'sqrt', 'srand', 'stat', 'study', 'substr', 'symlink', 'syscall', 'sysopen', 'sysread', 'sysseek', 'system', 'syswrite', 'tell', 'telldir', 'tie', 'tied', 'time', 'times', 'tr', 'truncate', 'uc', 'ucfirst', 'umask', 'undef', 'unlink', 'unpack', 'unshift', 'untie', 'utime', 'values', 'vec', 'wait', 'waitpid', 'wantarray', 'warn', 'write'), suffix='\\b'), Name.Builtin), ('((__(DATA|DIE|WARN)__)|(STD(IN|OUT|ERR)))\\b', Name.Builtin.Pseudo), ('(<<)([\\\'"]?)([a-zA-Z_]\\w*)(\\2;?\\n.*?\\n)(\\3)(\\n)', bygroups(String, String, String.Delimiter, String, String.Delimiter, Whitespace)), ('__END__', Comment.Preproc, 'end-part'), ('\\$\\^[ADEFHILMOPSTWX]', Name.Variable.Global), ('\\$[\\\\\\"\\[\\]\'&`+*.,;=%~?@$!<>(^|/-](?!\\w)', Name.Variable.Global), ('[$@%#]+', Name.Variable, 'varname'), ('0_?[0-7]+(_[0-7]+)*', Number.Oct), ('0x[0-9A-Fa-f]+(_[0-9A-Fa-f]+)*', Number.Hex), ('0b[01]+(_[01]+)*', Number.Bin), ('(?i)(\\d*(_\\d*)*\\.\\d+(_\\d*)*|\\d+(_\\d*)*\\.\\d+(_\\d*)*)(e[+-]?\\d+)?', Number.Float), ('(?i)\\d+(_\\d*)*e[+-]?\\d+(_\\d*)*', Number.Float), ('\\d+(_\\d+)*', Number.Integer), ("'(\\\\\\\\|\\\\[^\\\\]|[^'\\\\])*'", String), ('"(\\\\\\\\|\\\\[^\\\\]|[^"\\\\])*"', String), ('`(\\\\\\\\|\\\\[^\\\\]|[^`\\\\])*`', String.Backtick), ('<([^\\s>]+)>', String.Regex), ('(q|qq|qw|qr|qx)\\{', String.Other, 'cb-string'), ('(q|qq|qw|qr|qx)\\(', String.Other, 'rb-string'), ('(q|qq|qw|qr|qx)\\[', String.Other, 'sb-string'), ('(q|qq|qw|qr|qx)\\<', String.Other, 'lt-string'), ('(q|qq|qw|qr|qx)([\\W_])(.|\\n)*?\\2', String.Other), ('(package)(\\s+)([a-zA-Z_]\\w*(?:::[a-zA-Z_]\\w*)*)', bygroups(Keyword, Whitespace, Name.Namespace)), ('(use|require|no)(\\s+)([a-zA-Z_]\\w*(?:::[a-zA-Z_]\\w*)*)', bygroups(Keyword, Whitespace, Name.Namespace)), ('(sub)(\\s+)', bygroups(Keyword, Whitespace), 'funcname'), (words(('no', 'package', 'require', 'use'), suffix='\\b'), Keyword), ('(\\[\\]|\\*\\*|::|<<|>>|>=|<=>|<=|={3}|!=|=~|!~|&&?|\\|\\||\\.{1,3})', Operator), ('[-+/*%=<>&^|!\\\\~]=?', Operator), ('[()\\[\\]:;,<>/?{}]', Punctuation), ('(?=\\w)', Name, 'name')], 'format': [('\\.\\n', String.Interpol, '#pop'), ('[^\\n]*\\n', String.Interpol)], 'varname': [('\\s+', Whitespace), ('\\{', Punctuation, '#pop'), ('\\)|,', Punctuation, '#pop'), ('\\w+::', Name.Namespace), ('[\\w:]+', Name.Variable, '#pop')], 'name': [('[a-zA-Z_]\\w*(::[a-zA-Z_]\\w*)*(::)?(?=\\s*->)', Name.Namespace, '#pop'), ('[a-zA-Z_]\\w*(::[a-zA-Z_]\\w*)*::', Name.Namespace, '#pop'), ('[\\w:]+', Name, '#pop'), ('[A-Z_]+(?=\\W)', Name.Constant, '#pop'), ('(?=\\W)', Text, '#pop')], 'funcname': [('[a-zA-Z_]\\w*[!?]?', Name.Function), ('\\s+', Whitespace), ('(\\([$@%]*\\))(\\s*)', bygroups(Punctuation, Whitespace)), (';', Punctuation, '#pop'), ('.*?\\{', Punctuation, '#pop')], 'cb-string': [('\\\\[{}\\\\]', String.Other), ('\\\\', String.Other), ('\\{', String.Other, 'cb-string'), ('\\}', String.Other, '#pop'), ('[^{}\\\\]+', String.Other)], 'rb-string': [('\\\\[()\\\\]', String.Other), ('\\\\', String.Other), ('\\(', String.Other, 'rb-string'), ('\\)', String.Other, '#pop'), ('[^()]+', String.Other)], 'sb-string': [('\\\\[\\[\\]\\\\]', String.Other), ('\\\\', String.Other), ('\\[', String.Other, 'sb-string'), ('\\]', String.Other, '#pop'), ('[^\\[\\]]+', String.Other)], 'lt-string': [('\\\\[<>\\\\]', String.Other), ('\\\\', String.Other), ('\\<', String.Other, 'lt-string'), ('\\>', String.Other, '#pop'), ('[^<>]+', String.Other)], 'end-part': [('.+', Comment.Preproc, '#pop')]}
    
    def analyse_text(text):
        if shebang_matches(text, 'perl'):
            return True
        result = 0
        if re.search('(?:my|our)\\s+[$@%(]', text):
            result += 0.9
        if ':=' in text:
            result /= 2
        return result



class Perl6Lexer(ExtendedRegexLexer):
    """
    For Raku (a.k.a. Perl 6) source code.
    """
    name = 'Perl6'
    url = 'https://www.raku.org'
    aliases = ['perl6', 'pl6', 'raku']
    filenames = ['*.pl', '*.pm', '*.nqp', '*.p6', '*.6pl', '*.p6l', '*.pl6', '*.6pm', '*.p6m', '*.pm6', '*.t', '*.raku', '*.rakumod', '*.rakutest', '*.rakudoc']
    mimetypes = ['text/x-perl6', 'application/x-perl6']
    version_added = '2.0'
    flags = re.MULTILINE | re.DOTALL
    PERL6_IDENTIFIER_RANGE = "['\\w:-]"
    PERL6_KEYWORDS = ('BEGIN', 'CATCH', 'CHECK', 'CLOSE', 'CONTROL', 'DOC', 'END', 'ENTER', 'FIRST', 'INIT', 'KEEP', 'LAST', 'LEAVE', 'NEXT', 'POST', 'PRE', 'QUIT', 'UNDO', 'anon', 'augment', 'but', 'class', 'constant', 'default', 'does', 'else', 'elsif', 'enum', 'for', 'gather', 'given', 'grammar', 'has', 'if', 'import', 'is', 'let', 'loop', 'made', 'make', 'method', 'module', 'multi', 'my', 'need', 'orwith', 'our', 'proceed', 'proto', 'repeat', 'require', 'return', 'return-rw', 'returns', 'role', 'rule', 'state', 'sub', 'submethod', 'subset', 'succeed', 'supersede', 'token', 'try', 'unit', 'unless', 'until', 'use', 'when', 'while', 'with', 'without', 'export', 'native', 'repr', 'required', 'rw', 'symbol')
    PERL6_BUILTINS = ('ACCEPTS', 'abs', 'abs2rel', 'absolute', 'accept', 'accessed', 'acos', 'acosec', 'acosech', 'acosh', 'acotan', 'acotanh', 'acquire', 'act', 'action', 'actions', 'add', 'add_attribute', 'add_enum_value', 'add_fallback', 'add_method', 'add_parent', 'add_private_method', 'add_role', 'add_trustee', 'adverb', 'after', 'all', 'allocate', 'allof', 'allowed', 'alternative-names', 'annotations', 'antipair', 'antipairs', 'any', 'anyof', 'app_lifetime', 'append', 'arch', 'archname', 'args', 'arity', 'Array', 'asec', 'asech', 'asin', 'asinh', 'ASSIGN-KEY', 'ASSIGN-POS', 'assuming', 'ast', 'at', 'atan', 'atan2', 'atanh', 'AT-KEY', 'atomic-assign', 'atomic-dec-fetch', 'atomic-fetch', 'atomic-fetch-add', 'atomic-fetch-dec', 'atomic-fetch-inc', 'atomic-fetch-sub', 'atomic-inc-fetch', 'AT-POS', 'attributes', 'auth', 'await', 'backtrace', 'Bag', 'BagHash', 'bail-out', 'base', 'basename', 'base-repeating', 'batch', 'BIND-KEY', 'BIND-POS', 'bind-stderr', 'bind-stdin', 'bind-stdout', 'bind-udp', 'bits', 'bless', 'block', 'Bool', 'bool-only', 'bounds', 'break', 'Bridge', 'broken', 'BUILD', 'build-date', 'bytes', 'cache', 'callframe', 'calling-package', 'CALL-ME', 'callsame', 'callwith', 'can', 'cancel', 'candidates', 'cando', 'can-ok', 'canonpath', 'caps', 'caption', 'Capture', 'cas', 'catdir', 'categorize', 'categorize-list', 'catfile', 'catpath', 'cause', 'ceiling', 'cglobal', 'changed', 'Channel', 'chars', 'chdir', 'child', 'child-name', 'child-typename', 'chmod', 'chomp', 'chop', 'chr', 'chrs', 'chunks', 'cis', 'classify', 'classify-list', 'cleanup', 'clone', 'close', 'closed', 'close-stdin', 'cmp-ok', 'code', 'codes', 'collate', 'column', 'comb', 'combinations', 'command', 'comment', 'compiler', 'Complex', 'compose', 'compose_type', 'composer', 'condition', 'config', 'configure_destroy', 'configure_type_checking', 'conj', 'connect', 'constraints', 'construct', 'contains', 'contents', 'copy', 'cos', 'cosec', 'cosech', 'cosh', 'cotan', 'cotanh', 'count', 'count-only', 'cpu-cores', 'cpu-usage', 'CREATE', 'create_type', 'cross', 'cue', 'curdir', 'curupdir', 'd', 'Date', 'DateTime', 'day', 'daycount', 'day-of-month', 'day-of-week', 'day-of-year', 'days-in-month', 'declaration', 'decode', 'decoder', 'deepmap', 'default', 'defined', 'DEFINITE', 'delayed', 'DELETE-KEY', 'DELETE-POS', 'denominator', 'desc', 'DESTROY', 'destroyers', 'devnull', 'diag', 'did-you-mean', 'die', 'dies-ok', 'dir', 'dirname', 'dir-sep', 'DISTROnames', 'do', 'does', 'does-ok', 'done', 'done-testing', 'duckmap', 'dynamic', 'e', 'eager', 'earlier', 'elems', 'emit', 'enclosing', 'encode', 'encoder', 'encoding', 'end', 'ends-with', 'enum_from_value', 'enum_value_list', 'enum_values', 'enums', 'eof', 'EVAL', 'eval-dies-ok', 'EVALFILE', 'eval-lives-ok', 'exception', 'excludes-max', 'excludes-min', 'EXISTS-KEY', 'EXISTS-POS', 'exit', 'exitcode', 'exp', 'expected', 'explicitly-manage', 'expmod', 'extension', 'f', 'fail', 'fails-like', 'fc', 'feature', 'file', 'filename', 'find_method', 'find_method_qualified', 'finish', 'first', 'flat', 'flatmap', 'flip', 'floor', 'flunk', 'flush', 'fmt', 'format', 'formatter', 'freeze', 'from', 'from-list', 'from-loop', 'from-posix', 'full', 'full-barrier', 'get', 'get_value', 'getc', 'gist', 'got', 'grab', 'grabpairs', 'grep', 'handle', 'handled', 'handles', 'hardware', 'has_accessor', 'Hash', 'head', 'headers', 'hh-mm-ss', 'hidden', 'hides', 'hour', 'how', 'hyper', 'id', 'illegal', 'im', 'in', 'indent', 'index', 'indices', 'indir', 'infinite', 'infix', 'infix:<+>', 'infix:<->', 'install_method_cache', 'Instant', 'instead', 'Int', 'int-bounds', 'interval', 'in-timezone', 'invalid-str', 'invert', 'invocant', 'IO', 'IO::Notification.watch-path', 'is_trusted', 'is_type', 'isa', 'is-absolute', 'isa-ok', 'is-approx', 'is-deeply', 'is-hidden', 'is-initial-thread', 'is-int', 'is-lazy', 'is-leap-year', 'isNaN', 'isnt', 'is-prime', 'is-relative', 'is-routine', 'is-setting', 'is-win', 'item', 'iterator', 'join', 'keep', 'kept', 'KERNELnames', 'key', 'keyof', 'keys', 'kill', 'kv', 'kxxv', 'l', 'lang', 'last', 'lastcall', 'later', 'lazy', 'lc', 'leading', 'level', 'like', 'line', 'lines', 'link', 'List', 'listen', 'live', 'lives-ok', 'local', 'lock', 'log', 'log10', 'lookup', 'lsb', 'made', 'MAIN', 'make', 'Map', 'match', 'max', 'maxpairs', 'merge', 'message', 'method', 'method_table', 'methods', 'migrate', 'min', 'minmax', 'minpairs', 'minute', 'misplaced', 'Mix', 'MixHash', 'mkdir', 'mode', 'modified', 'month', 'move', 'mro', 'msb', 'multi', 'multiness', 'my', 'name', 'named', 'named_names', 'narrow', 'nativecast', 'native-descriptor', 'nativesizeof', 'new', 'new_type', 'new-from-daycount', 'new-from-pairs', 'next', 'nextcallee', 'next-handle', 'nextsame', 'nextwith', 'NFC', 'NFD', 'NFKC', 'NFKD', 'nl-in', 'nl-out', 'nodemap', 'nok', 'none', 'norm', 'not', 'note', 'now', 'nude', 'Num', 'numerator', 'Numeric', 'of', 'offset', 'offset-in-hours', 'offset-in-minutes', 'ok', 'old', 'on-close', 'one', 'on-switch', 'open', 'opened', 'operation', 'optional', 'ord', 'ords', 'orig', 'os-error', 'osname', 'out-buffer', 'pack', 'package', 'package-kind', 'package-name', 'packages', 'pair', 'pairs', 'pairup', 'parameter', 'params', 'parent', 'parent-name', 'parents', 'parse', 'parse-base', 'parsefile', 'parse-names', 'parts', 'pass', 'path', 'path-sep', 'payload', 'peer-host', 'peer-port', 'periods', 'perl', 'permutations', 'phaser', 'pick', 'pickpairs', 'pid', 'placeholder', 'plan', 'plus', 'polar', 'poll', 'polymod', 'pop', 'pos', 'positional', 'posix', 'postfix', 'postmatch', 'precomp-ext', 'precomp-target', 'pred', 'prefix', 'prematch', 'prepend', 'print', 'printf', 'print-nl', 'print-to', 'private', 'private_method_table', 'proc', 'produce', 'Promise', 'prompt', 'protect', 'pull-one', 'push', 'push-all', 'push-at-least', 'push-exactly', 'push-until-lazy', 'put', 'qualifier-type', 'quit', 'r', 'race', 'radix', 'rand', 'range', 'Rat', 'raw', 're', 'read', 'readchars', 'readonly', 'ready', 'Real', 'reallocate', 'reals', 'reason', 'rebless', 'receive', 'recv', 'redispatcher', 'redo', 'reduce', 'rel2abs', 'relative', 'release', 'rename', 'repeated', 'replacement', 'report', 'reserved', 'resolve', 'restore', 'result', 'resume', 'rethrow', 'reverse', 'right', 'rindex', 'rmdir', 'role', 'roles_to_compose', 'rolish', 'roll', 'rootdir', 'roots', 'rotate', 'rotor', 'round', 'roundrobin', 'routine-type', 'run', 'rwx', 's', 'samecase', 'samemark', 'samewith', 'say', 'schedule-on', 'scheduler', 'scope', 'sec', 'sech', 'second', 'seek', 'self', 'send', 'Set', 'set_hidden', 'set_name', 'set_package', 'set_rw', 'set_value', 'SetHash', 'set-instruments', 'setup_finalization', 'shape', 'share', 'shell', 'shift', 'sibling', 'sigil', 'sign', 'signal', 'signals', 'signature', 'sin', 'sinh', 'sink', 'sink-all', 'skip', 'skip-at-least', 'skip-at-least-pull-one', 'skip-one', 'skip-rest', 'sleep', 'sleep-timer', 'sleep-until', 'Slip', 'slurp', 'slurp-rest', 'slurpy', 'snap', 'snapper', 'so', 'socket-host', 'socket-port', 'sort', 'source', 'source-package', 'spawn', 'SPEC', 'splice', 'split', 'splitdir', 'splitpath', 'sprintf', 'spurt', 'sqrt', 'squish', 'srand', 'stable', 'start', 'started', 'starts-with', 'status', 'stderr', 'stdout', 'Str', 'sub_signature', 'subbuf', 'subbuf-rw', 'subname', 'subparse', 'subst', 'subst-mutate', 'substr', 'substr-eq', 'substr-rw', 'subtest', 'succ', 'sum', 'Supply', 'symlink', 't', 'tail', 'take', 'take-rw', 'tan', 'tanh', 'tap', 'target', 'target-name', 'tc', 'tclc', 'tell', 'then', 'throttle', 'throw', 'throws-like', 'timezone', 'tmpdir', 'to', 'today', 'todo', 'toggle', 'to-posix', 'total', 'trailing', 'trans', 'tree', 'trim', 'trim-leading', 'trim-trailing', 'truncate', 'truncated-to', 'trusts', 'try_acquire', 'trying', 'twigil', 'type', 'type_captures', 'typename', 'uc', 'udp', 'uncaught_handler', 'unimatch', 'uniname', 'uninames', 'uniparse', 'uniprop', 'uniprops', 'unique', 'unival', 'univals', 'unlike', 'unlink', 'unlock', 'unpack', 'unpolar', 'unshift', 'unwrap', 'updir', 'USAGE', 'use-ok', 'utc', 'val', 'value', 'values', 'VAR', 'variable', 'verbose-config', 'version', 'VMnames', 'volume', 'vow', 'w', 'wait', 'warn', 'watch', 'watch-path', 'week', 'weekday-of-month', 'week-number', 'week-year', 'WHAT', 'when', 'WHERE', 'WHEREFORE', 'WHICH', 'WHO', 'whole-second', 'WHY', 'wordcase', 'words', 'workaround', 'wrap', 'write', 'write-to', 'x', 'yada', 'year', 'yield', 'yyyy-mm-dd', 'z', 'zip', 'zip-latest')
    PERL6_BUILTIN_CLASSES = ('False', 'True', 'Any', 'Array', 'Associative', 'AST', 'atomicint', 'Attribute', 'Backtrace', 'Backtrace::Frame', 'Bag', 'Baggy', 'BagHash', 'Blob', 'Block', 'Bool', 'Buf', 'Callable', 'CallFrame', 'Cancellation', 'Capture', 'CArray', 'Channel', 'Code', 'compiler', 'Complex', 'ComplexStr', 'Cool', 'CurrentThreadScheduler', 'Cursor', 'Date', 'Dateish', 'DateTime', 'Distro', 'Duration', 'Encoding', 'Exception', 'Failure', 'FatRat', 'Grammar', 'Hash', 'HyperWhatever', 'Instant', 'Int', 'int16', 'int32', 'int64', 'int8', 'IntStr', 'IO', 'IO::ArgFiles', 'IO::CatHandle', 'IO::Handle', 'IO::Notification', 'IO::Path', 'IO::Path::Cygwin', 'IO::Path::QNX', 'IO::Path::Unix', 'IO::Path::Win32', 'IO::Pipe', 'IO::Socket', 'IO::Socket::Async', 'IO::Socket::INET', 'IO::Spec', 'IO::Spec::Cygwin', 'IO::Spec::QNX', 'IO::Spec::Unix', 'IO::Spec::Win32', 'IO::Special', 'Iterable', 'Iterator', 'Junction', 'Kernel', 'Label', 'List', 'Lock', 'Lock::Async', 'long', 'longlong', 'Macro', 'Map', 'Match', 'Metamodel::AttributeContainer', 'Metamodel::C3MRO', 'Metamodel::ClassHOW', 'Metamodel::EnumHOW', 'Metamodel::Finalization', 'Metamodel::MethodContainer', 'Metamodel::MROBasedMethodDispatch', 'Metamodel::MultipleInheritance', 'Metamodel::Naming', 'Metamodel::Primitives', 'Metamodel::PrivateMethodContainer', 'Metamodel::RoleContainer', 'Metamodel::Trusting', 'Method', 'Mix', 'MixHash', 'Mixy', 'Mu', 'NFC', 'NFD', 'NFKC', 'NFKD', 'Nil', 'Num', 'num32', 'num64', 'Numeric', 'NumStr', 'ObjAt', 'Order', 'Pair', 'Parameter', 'Perl', 'Pod::Block', 'Pod::Block::Code', 'Pod::Block::Comment', 'Pod::Block::Declarator', 'Pod::Block::Named', 'Pod::Block::Para', 'Pod::Block::Table', 'Pod::Heading', 'Pod::Item', 'Pointer', 'Positional', 'PositionalBindFailover', 'Proc', 'Proc::Async', 'Promise', 'Proxy', 'PseudoStash', 'QuantHash', 'Range', 'Rat', 'Rational', 'RatStr', 'Real', 'Regex', 'Routine', 'Scalar', 'Scheduler', 'Semaphore', 'Seq', 'Set', 'SetHash', 'Setty', 'Signature', 'size_t', 'Slip', 'Stash', 'Str', 'StrDistance', 'Stringy', 'Sub', 'Submethod', 'Supplier', 'Supplier::Preserving', 'Supply', 'Systemic', 'Tap', 'Telemetry', 'Telemetry::Instrument::Thread', 'Telemetry::Instrument::Usage', 'Telemetry::Period', 'Telemetry::Sampler', 'Thread', 'ThreadPoolScheduler', 'UInt', 'uint16', 'uint32', 'uint64', 'uint8', 'Uni', 'utf8', 'Variable', 'Version', 'VM', 'Whatever', 'WhateverCode', 'WrapHandle')
    PERL6_OPERATORS = ('X', 'Z', 'after', 'also', 'and', 'andthen', 'before', 'cmp', 'div', 'eq', 'eqv', 'extra', 'ff', 'fff', 'ge', 'gt', 'le', 'leg', 'lt', 'm', 'mm', 'mod', 'ne', 'or', 'orelse', 'rx', 's', 'tr', 'x', 'xor', 'xx', '++', '--', '**', '!', '+', '-', '~', '?', '|', '||', '+^', '~^', '?^', '^', '*', '/', '%', '%%', '+&', '+<', '+>', '~&', '~<', '~>', '?&', 'gcd', 'lcm', '+', '-', '+|', '+^', '~|', '~^', '?|', '?^', '~', '&', '^', 'but', 'does', '<=>', '..', '..^', '^..', '^..^', '!=', '==', '<', '<=', '>', '>=', '~~', '===', '!eqv', '&&', '||', '^^', '//', 'min', 'max', '??', '!!', 'ff', 'fff', 'so', 'not', '<==', '==>', '<<==', '==>>', 'unicmp')
    PERL6_BRACKETS = {'(': ')', '<': '>', '[': ']', '{': '}', '«': '»', '༺': '༻', '༼': '༽', '᚛': '᚜', '‘': '’', '‚': '’', '‛': '’', '“': '”', '„': '”', '‟': '”', '‹': '›', '⁅': '⁆', '⁽': '⁾', '₍': '₎', '∈': '∋', '∉': '∌', '∊': '∍', '∕': '⧵', '∼': '∽', '≃': '⋍', '≒': '≓', '≔': '≕', '≤': '≥', '≦': '≧', '≨': '≩', '≪': '≫', '≮': '≯', '≰': '≱', '≲': '≳', '≴': '≵', '≶': '≷', '≸': '≹', '≺': '≻', '≼': '≽', '≾': '≿', '⊀': '⊁', '⊂': '⊃', '⊄': '⊅', '⊆': '⊇', '⊈': '⊉', '⊊': '⊋', '⊏': '⊐', '⊑': '⊒', '⊘': '⦸', '⊢': '⊣', '⊦': '⫞', '⊨': '⫤', '⊩': '⫣', '⊫': '⫥', '⊰': '⊱', '⊲': '⊳', '⊴': '⊵', '⊶': '⊷', '⋉': '⋊', '⋋': '⋌', '⋐': '⋑', '⋖': '⋗', '⋘': '⋙', '⋚': '⋛', '⋜': '⋝', '⋞': '⋟', '⋠': '⋡', '⋢': '⋣', '⋤': '⋥', '⋦': '⋧', '⋨': '⋩', '⋪': '⋫', '⋬': '⋭', '⋰': '⋱', '⋲': '⋺', '⋳': '⋻', '⋴': '⋼', '⋶': '⋽', '⋷': '⋾', '⌈': '⌉', '⌊': '⌋', '〈': '〉', '⎴': '⎵', '❨': '❩', '❪': '❫', '❬': '❭', '❮': '❯', '❰': '❱', '❲': '❳', '❴': '❵', '⟃': '⟄', '⟅': '⟆', '⟕': '⟖', '⟝': '⟞', '⟢': '⟣', '⟤': '⟥', '⟦': '⟧', '⟨': '⟩', '⟪': '⟫', '⦃': '⦄', '⦅': '⦆', '⦇': '⦈', '⦉': '⦊', '⦋': '⦌', '⦍': '⦎', '⦏': '⦐', '⦑': '⦒', '⦓': '⦔', '⦕': '⦖', '⦗': '⦘', '⧀': '⧁', '⧄': '⧅', '⧏': '⧐', '⧑': '⧒', '⧔': '⧕', '⧘': '⧙', '⧚': '⧛', '⧸': '⧹', '⧼': '⧽', '⨫': '⨬', '⨭': '⨮', '⨴': '⨵', '⨼': '⨽', '⩤': '⩥', '⩹': '⩺', '⩽': '⩾', '⩿': '⪀', '⪁': '⪂', '⪃': '⪄', '⪋': '⪌', '⪑': '⪒', '⪓': '⪔', '⪕': '⪖', '⪗': '⪘', '⪙': '⪚', '⪛': '⪜', '⪡': '⪢', '⪦': '⪧', '⪨': '⪩', '⪪': '⪫', '⪬': '⪭', '⪯': '⪰', '⪳': '⪴', '⪻': '⪼', '⪽': '⪾', '⪿': '⫀', '⫁': '⫂', '⫃': '⫄', '⫅': '⫆', '⫍': '⫎', '⫏': '⫐', '⫑': '⫒', '⫓': '⫔', '⫕': '⫖', '⫬': '⫭', '⫷': '⫸', '⫹': '⫺', '⸂': '⸃', '⸄': '⸅', '⸉': '⸊', '⸌': '⸍', '⸜': '⸝', '⸠': '⸡', '〈': '〉', '《': '》', '「': '」', '『': '』', '【': '】', '〔': '〕', '〖': '〗', '〘': '〙', '〚': '〛', '〝': '〞', '﴾': '﴿', '︗': '︘', '︵': '︶', '︷': '︸', '︹': '︺', '︻': '︼', '︽': '︾', '︿': '﹀', '﹁': '﹂', '﹃': '﹄', '﹇': '﹈', '﹙': '﹚', '﹛': '﹜', '﹝': '﹞', '（': '）', '＜': '＞', '［': '］', '｛': '｝', '｟': '｠', '｢': '｣'}
    
    def _build_word_match(words, boundary_regex_fragment=None, prefix='', suffix=''):
        if boundary_regex_fragment is None:
            return '\\b(' + prefix + '|'.join((re.escape(x) for x in words)) + suffix + ')\\b'
        else:
            return '(?<!' + boundary_regex_fragment + ')' + prefix + '(' + '|'.join((re.escape(x) for x in words)) + ')' + suffix + '(?!' + boundary_regex_fragment + ')'
    
    def brackets_callback(token_class):
        
        def callback(lexer, match, context):
            groups = match.groupdict()
            opening_chars = groups['delimiter']
            n_chars = len(opening_chars)
            adverbs = groups.get('adverbs')
            closer = Perl6Lexer.PERL6_BRACKETS.get(opening_chars[0])
            text = context.text
            if closer is None:
                end_pos = text.find(opening_chars, match.start('delimiter') + n_chars)
            else:
                closing_chars = closer * n_chars
                nesting_level = 1
                search_pos = match.start('delimiter')
                while nesting_level > 0:
                    next_open_pos = text.find(opening_chars, search_pos + n_chars)
                    next_close_pos = text.find(closing_chars, search_pos + n_chars)
                    if next_close_pos == -1:
                        next_close_pos = len(text)
                        nesting_level = 0
                    elif (next_open_pos != -1 and next_open_pos < next_close_pos):
                        nesting_level += 1
                        search_pos = next_open_pos
                    else:
                        nesting_level -= 1
                        search_pos = next_close_pos
                end_pos = next_close_pos
            if end_pos < 0:
                end_pos = len(text)
            if (adverbs is not None and re.search(':to\\b', adverbs)):
                heredoc_terminator = text[match.start('delimiter') + n_chars:end_pos]
                end_heredoc = re.search('^\\s*' + re.escape(heredoc_terminator) + '\\s*$', text[end_pos:], re.MULTILINE)
                if end_heredoc:
                    end_pos += end_heredoc.end()
                else:
                    end_pos = len(text)
            yield (match.start(), token_class, text[match.start():end_pos + n_chars])
            context.pos = end_pos + n_chars
        return callback
    
    def opening_brace_callback(lexer, match, context):
        stack = context.stack
        yield (match.start(), Text, context.text[match.start():match.end()])
        context.pos = match.end()
        if (len(stack) > 2 and stack[-2] == 'token'):
            context.perl6_token_nesting_level += 1
    
    def closing_brace_callback(lexer, match, context):
        stack = context.stack
        yield (match.start(), Text, context.text[match.start():match.end()])
        context.pos = match.end()
        if (len(stack) > 2 and stack[-2] == 'token'):
            context.perl6_token_nesting_level -= 1
            if context.perl6_token_nesting_level == 0:
                stack.pop()
    
    def embedded_perl6_callback(lexer, match, context):
        context.perl6_token_nesting_level = 1
        yield (match.start(), Text, context.text[match.start():match.end()])
        context.pos = match.end()
        context.stack.append('root')
    tokens = {'common': [('#[`|=](?P<delimiter>(?P<first_char>[' + ''.join(PERL6_BRACKETS) + '])(?P=first_char)*)', brackets_callback(Comment.Multiline)), ('#[^\\n]*$', Comment.Single), ('^(\\s*)=begin\\s+(\\w+)\\b.*?^\\1=end\\s+\\2', Comment.Multiline), ('^(\\s*)=for.*?\\n\\s*?\\n', Comment.Multiline), ('^=.*?\\n\\s*?\\n', Comment.Multiline), ('(regex|token|rule)(\\s*' + PERL6_IDENTIFIER_RANGE + '+:sym)', bygroups(Keyword, Name), 'token-sym-brackets'), ('(regex|token|rule)(?!' + PERL6_IDENTIFIER_RANGE + ')(\\s*' + PERL6_IDENTIFIER_RANGE + '+)?', bygroups(Keyword, Name), 'pre-token'), ('(role)(\\s+)(q)(\\s*)', bygroups(Keyword, Whitespace, Name, Whitespace)), (_build_word_match(PERL6_KEYWORDS, PERL6_IDENTIFIER_RANGE), Keyword), (_build_word_match(PERL6_BUILTIN_CLASSES, PERL6_IDENTIFIER_RANGE, suffix='(?::[UD])?'), Name.Builtin), (_build_word_match(PERL6_BUILTINS, PERL6_IDENTIFIER_RANGE), Name.Builtin), ('[$@%&][.^:?=!~]?' + PERL6_IDENTIFIER_RANGE + '+(?:<<.*?>>|<.*?>|«.*?»)*', Name.Variable), ('\\$[!/](?:<<.*?>>|<.*?>|«.*?»)*', Name.Variable.Global), ('::\\?\\w+', Name.Variable.Global), ('[$@%&]\\*' + PERL6_IDENTIFIER_RANGE + '+(?:<<.*?>>|<.*?>|«.*?»)*', Name.Variable.Global), ('\\$(?:<.*?>)+', Name.Variable), ('(?:q|qq|Q)[a-zA-Z]?\\s*(?P<adverbs>:[\\w\\s:]+)?\\s*(?P<delimiter>(?P<first_char>[^0-9a-zA-Z:\\s])(?P=first_char)*)', brackets_callback(String)), ('0_?[0-7]+(_[0-7]+)*', Number.Oct), ('0x[0-9A-Fa-f]+(_[0-9A-Fa-f]+)*', Number.Hex), ('0b[01]+(_[01]+)*', Number.Bin), ('(?i)(\\d*(_\\d*)*\\.\\d+(_\\d*)*|\\d+(_\\d*)*\\.\\d+(_\\d*)*)(e[+-]?\\d+)?', Number.Float), ('(?i)\\d+(_\\d*)*e[+-]?\\d+(_\\d*)*', Number.Float), ('\\d+(_\\d+)*', Number.Integer), ('(?<=~~)\\s*/(?:\\\\\\\\|\\\\/|.)*?/', String.Regex), ('(?<=[=(,])\\s*/(?:\\\\\\\\|\\\\/|.)*?/', String.Regex), ('m\\w+(?=\\()', Name), ('(?:m|ms|rx)\\s*(?P<adverbs>:[\\w\\s:]+)?\\s*(?P<delimiter>(?P<first_char>[^\\w:\\s])(?P=first_char)*)', brackets_callback(String.Regex)), ('(?:s|ss|tr)\\s*(?::[\\w\\s:]+)?\\s*/(?:\\\\\\\\|\\\\/|.)*?/(?:\\\\\\\\|\\\\/|.)*?/', String.Regex), ('<[^\\s=].*?\\S>', String), (_build_word_match(PERL6_OPERATORS), Operator), ('\\w' + PERL6_IDENTIFIER_RANGE + '*', Name), ("'(\\\\\\\\|\\\\[^\\\\]|[^'\\\\])*'", String), ('"(\\\\\\\\|\\\\[^\\\\]|[^"\\\\])*"', String)], 'root': [include('common'), ('\\{', opening_brace_callback), ('\\}', closing_brace_callback), ('.+?', Text)], 'pre-token': [include('common'), ('\\{', Text, ('#pop', 'token')), ('.+?', Text)], 'token-sym-brackets': [('(?P<delimiter>(?P<first_char>[' + ''.join(PERL6_BRACKETS) + '])(?P=first_char)*)', brackets_callback(Name), ('#pop', 'pre-token')), default(('#pop', 'pre-token'))], 'token': [('\\}', Text, '#pop'), ('(?<=:)(?:my|our|state|constant|temp|let).*?;', using(this)), ('<(?:[-!?+.]\\s*)?\\[.*?\\]>', String.Regex), ("(?<!\\\\)'(\\\\\\\\|\\\\[^\\\\]|[^'\\\\])*'", String.Regex), ('(?<!\\\\)"(\\\\\\\\|\\\\[^\\\\]|[^"\\\\])*"', String.Regex), ('#.*?$', Comment.Single), ('\\{', embedded_perl6_callback), ('.+?', String.Regex)]}
    
    def analyse_text(text):
        
        def strip_pod(lines):
            in_pod = False
            stripped_lines = []
            for line in lines:
                if re.match('^=(?:end|cut)', line):
                    in_pod = False
                elif re.match('^=\\w+', line):
                    in_pod = True
                elif not in_pod:
                    stripped_lines.append(line)
            return stripped_lines
        lines = text.splitlines()
        lines = strip_pod(lines)
        text = '\n'.join(lines)
        if shebang_matches(text, 'perl6|rakudo|niecza|pugs'):
            return True
        saw_perl_decl = False
        rating = False
        if re.search('(?:my|our|has)\\s+(?:' + Perl6Lexer.PERL6_IDENTIFIER_RANGE + '+\\s+)?[$@%&(]', text):
            rating = 0.8
            saw_perl_decl = True
        for line in lines:
            line = re.sub('#.*', '', line)
            if re.match('^\\s*$', line):
                continue
            if re.match('^\\s*(?:use\\s+)?v6(?:\\.\\d(?:\\.\\d)?)?;', line):
                return True
            class_decl = re.match('^\\s*(?:(?P<scope>my|our)\\s+)?(?:module|class|role|enum|grammar)', line)
            if class_decl:
                if (saw_perl_decl or class_decl.group('scope') is not None):
                    return True
                rating = 0.05
                continue
            break
        if ':=' in text:
            rating /= 2
        return rating
    
    def __init__(self, **options):
        super().__init__(**options)
        self.encoding = options.get('encoding', 'utf-8')


