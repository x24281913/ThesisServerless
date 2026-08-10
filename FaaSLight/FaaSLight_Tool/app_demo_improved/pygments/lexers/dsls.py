"""
    pygments.lexers.dsls
    ~~~~~~~~~~~~~~~~~~~~

    Lexers for various domain-specific languages.

    :copyright: Copyright 2006-present by the Pygments team, see AUTHORS.
    :license: BSD, see LICENSE for details.
"""

import re
from pygments.lexer import ExtendedRegexLexer, RegexLexer, bygroups, words, include, default, this, using, combined
from pygments.token import Text, Comment, Operator, Keyword, Name, String, Number, Punctuation, Whitespace
__all__ = ['ProtoBufLexer', 'ZeekLexer', 'PuppetLexer', 'RslLexer', 'MscgenLexer', 'VGLLexer', 'AlloyLexer', 'PanLexer', 'CrmshLexer', 'ThriftLexer', 'FlatlineLexer', 'SnowballLexer']


class ProtoBufLexer(RegexLexer):
    """
    Lexer for Protocol Buffer definition files.
    """
    name = 'Protocol Buffer'
    url = 'https://developers.google.com/protocol-buffers/'
    aliases = ['protobuf', 'proto']
    filenames = ['*.proto']
    version_added = '1.4'
    tokens = {'root': [('[ \\t]+', Whitespace), ('[,;{}\\[\\]()<>]', Punctuation), ('/(\\\\\\n)?/(\\n|(.|\\n)*?[^\\\\]\\n)', Comment.Single), ('/(\\\\\\n)?\\*(.|\\n)*?\\*(\\\\\\n)?/', Comment.Multiline), (words(('import', 'option', 'optional', 'required', 'repeated', 'reserved', 'default', 'packed', 'ctype', 'extensions', 'to', 'max', 'rpc', 'returns', 'oneof', 'syntax'), prefix='\\b', suffix='\\b'), Keyword), (words(('int32', 'int64', 'uint32', 'uint64', 'sint32', 'sint64', 'fixed32', 'fixed64', 'sfixed32', 'sfixed64', 'float', 'double', 'bool', 'string', 'bytes'), suffix='\\b'), Keyword.Type), ('(true|false)\\b', Keyword.Constant), ('(package)(\\s+)', bygroups(Keyword.Namespace, Whitespace), 'package'), ('(message|extend)(\\s+)', bygroups(Keyword.Declaration, Whitespace), 'message'), ('(enum|group|service)(\\s+)', bygroups(Keyword.Declaration, Whitespace), 'type'), ('\\".*?\\"', String), ("\\'.*?\\'", String), ('(\\d+\\.\\d*|\\.\\d+|\\d+)[eE][+-]?\\d+[LlUu]*', Number.Float), ('(\\d+\\.\\d*|\\.\\d+|\\d+[fF])[fF]?', Number.Float), ('(\\-?(inf|nan))\\b', Number.Float), ('0x[0-9a-fA-F]+[LlUu]*', Number.Hex), ('0[0-7]+[LlUu]*', Number.Oct), ('\\d+[LlUu]*', Number.Integer), ('[+-=]', Operator), ('([a-zA-Z_][\\w.]*)([ \\t]*)(=)', bygroups(Name.Attribute, Whitespace, Operator)), ('[a-zA-Z_][\\w.]*', Name)], 'package': [('[a-zA-Z_][\\w\\.]*', Name.Namespace, '#pop'), default('#pop')], 'message': [('[a-zA-Z_]\\w*', Name.Class, '#pop'), default('#pop')], 'type': [('[a-zA-Z_]\\w*', Name, '#pop'), default('#pop')]}



class ThriftLexer(RegexLexer):
    """
    For Thrift interface definitions.
    """
    name = 'Thrift'
    url = 'https://thrift.apache.org/'
    aliases = ['thrift']
    filenames = ['*.thrift']
    mimetypes = ['application/x-thrift']
    version_added = '2.1'
    tokens = {'root': [include('whitespace'), include('comments'), ('"', String.Double, combined('stringescape', 'dqs')), ("\\'", String.Single, combined('stringescape', 'sqs')), ('(namespace)(\\s+)', bygroups(Keyword.Namespace, Whitespace), 'namespace'), ('(enum|union|struct|service|exception)(\\s+)', bygroups(Keyword.Declaration, Whitespace), 'class'), ('((?:(?:[^\\W\\d]|\\$)[\\w.\\[\\]$<>]*\\s+)+?)((?:[^\\W\\d]|\\$)[\\w$]*)(\\s*)(\\()', bygroups(using(this), Name.Function, Whitespace, Operator)), include('keywords'), include('numbers'), ('[&=]', Operator), ('[:;,{}()<>\\[\\]]', Punctuation), ('[a-zA-Z_](\\.\\w|\\w)*', Name)], 'whitespace': [('\\n', Whitespace), ('\\s+', Whitespace)], 'comments': [('#.*$', Comment), ('//.*?\\n', Comment), ('/\\*[\\w\\W]*?\\*/', Comment.Multiline)], 'stringescape': [('\\\\([\\\\nrt"\\\'])', String.Escape)], 'dqs': [('"', String.Double, '#pop'), ('[^\\\\"\\n]+', String.Double)], 'sqs': [("'", String.Single, '#pop'), ("[^\\\\\\'\\n]+", String.Single)], 'namespace': [('[a-z*](\\.\\w|\\w)*', Name.Namespace, '#pop'), default('#pop')], 'class': [('[a-zA-Z_]\\w*', Name.Class, '#pop'), default('#pop')], 'keywords': [('(async|oneway|extends|throws|required|optional)\\b', Keyword), ('(true|false)\\b', Keyword.Constant), ('(const|typedef)\\b', Keyword.Declaration), (words(('cpp_namespace', 'cpp_include', 'cpp_type', 'java_package', 'cocoa_prefix', 'csharp_namespace', 'delphi_namespace', 'php_namespace', 'py_module', 'perl_package', 'ruby_namespace', 'smalltalk_category', 'smalltalk_prefix', 'xsd_all', 'xsd_optional', 'xsd_nillable', 'xsd_namespace', 'xsd_attrs', 'include'), suffix='\\b'), Keyword.Namespace), (words(('void', 'bool', 'byte', 'i16', 'i32', 'i64', 'double', 'string', 'binary', 'map', 'list', 'set', 'slist', 'senum'), suffix='\\b'), Keyword.Type), (words(('BEGIN', 'END', '__CLASS__', '__DIR__', '__FILE__', '__FUNCTION__', '__LINE__', '__METHOD__', '__NAMESPACE__', 'abstract', 'alias', 'and', 'args', 'as', 'assert', 'begin', 'break', 'case', 'catch', 'class', 'clone', 'continue', 'declare', 'def', 'default', 'del', 'delete', 'do', 'dynamic', 'elif', 'else', 'elseif', 'elsif', 'end', 'enddeclare', 'endfor', 'endforeach', 'endif', 'endswitch', 'endwhile', 'ensure', 'except', 'exec', 'finally', 'float', 'for', 'foreach', 'function', 'global', 'goto', 'if', 'implements', 'import', 'in', 'inline', 'instanceof', 'interface', 'is', 'lambda', 'module', 'native', 'new', 'next', 'nil', 'not', 'or', 'pass', 'public', 'print', 'private', 'protected', 'raise', 'redo', 'rescue', 'retry', 'register', 'return', 'self', 'sizeof', 'static', 'super', 'switch', 'synchronized', 'then', 'this', 'throw', 'transient', 'try', 'undef', 'unless', 'unsigned', 'until', 'use', 'var', 'virtual', 'volatile', 'when', 'while', 'with', 'xor', 'yield'), prefix='\\b', suffix='\\b'), Keyword.Reserved)], 'numbers': [('[+-]?(\\d+\\.\\d+([eE][+-]?\\d+)?|\\.?\\d+[eE][+-]?\\d+)', Number.Float), ('[+-]?0x[0-9A-Fa-f]+', Number.Hex), ('[+-]?[0-9]+', Number.Integer)]}



class ZeekLexer(RegexLexer):
    """
    For Zeek scripts.
    """
    name = 'Zeek'
    url = 'https://www.zeek.org/'
    aliases = ['zeek', 'bro']
    filenames = ['*.zeek', '*.bro']
    version_added = '2.5'
    _hex = '[0-9a-fA-F]'
    _float = '((\\d*\\.?\\d+)|(\\d+\\.?\\d*))([eE][-+]?\\d+)?'
    _h = '[A-Za-z0-9][-A-Za-z0-9]*'
    tokens = {'root': [include('whitespace'), include('comments'), include('directives'), include('attributes'), include('types'), include('keywords'), include('literals'), include('operators'), include('punctuation'), ('((?:[A-Za-z_]\\w*)(?:::(?:[A-Za-z_]\\w*))*)(?=\\s*\\()', Name.Function), include('identifiers')], 'whitespace': [('\\n', Whitespace), ('\\s+', Whitespace), ('(\\\\)(\\n)', bygroups(Text, Whitespace))], 'comments': [('#.*$', Comment)], 'directives': [('@(load-plugin|load-sigs|load|unload)\\b.*$', Comment.Preproc), ('@(DEBUG|DIR|FILENAME|deprecated|if|ifdef|ifndef|else|endif)\\b', Comment.Preproc), ('(@prefixes)(\\s*)((\\+?=).*)$', bygroups(Comment.Preproc, Whitespace, Comment.Preproc))], 'attributes': [(words(('redef', 'priority', 'log', 'optional', 'default', 'add_func', 'delete_func', 'expire_func', 'read_expire', 'write_expire', 'create_expire', 'synchronized', 'persistent', 'rotate_interval', 'rotate_size', 'encrypt', 'raw_output', 'mergeable', 'error_handler', 'type_column', 'deprecated'), prefix='&', suffix='\\b'), Keyword.Pseudo)], 'types': [(words(('any', 'enum', 'record', 'set', 'table', 'vector', 'function', 'hook', 'event', 'addr', 'bool', 'count', 'double', 'file', 'int', 'interval', 'pattern', 'port', 'string', 'subnet', 'time'), suffix='\\b'), Keyword.Type), ('(opaque)(\\s+)(of)(\\s+)((?:[A-Za-z_]\\w*)(?:::(?:[A-Za-z_]\\w*))*)\\b', bygroups(Keyword.Type, Whitespace, Operator.Word, Whitespace, Keyword.Type)), ('(type)(\\s+)((?:[A-Za-z_]\\w*)(?:::(?:[A-Za-z_]\\w*))*)(\\s*)(:)(\\s*)\\b(record|enum)\\b', bygroups(Keyword, Whitespace, Name.Class, Whitespace, Operator, Whitespace, Keyword.Type)), ('(type)(\\s+)((?:[A-Za-z_]\\w*)(?:::(?:[A-Za-z_]\\w*))*)(\\s*)(:)', bygroups(Keyword, Whitespace, Name, Whitespace, Operator)), ('(redef)(\\s+)(record|enum)(\\s+)((?:[A-Za-z_]\\w*)(?:::(?:[A-Za-z_]\\w*))*)\\b', bygroups(Keyword, Whitespace, Keyword.Type, Whitespace, Name.Class))], 'keywords': [(words(('redef', 'export', 'if', 'else', 'for', 'while', 'return', 'break', 'next', 'continue', 'fallthrough', 'switch', 'default', 'case', 'add', 'delete', 'when', 'timeout', 'schedule'), suffix='\\b'), Keyword), ('(print)\\b', Keyword), ('(global|local|const|option)\\b', Keyword.Declaration), ('(module)(\\s+)(([A-Za-z_]\\w*)(?:::([A-Za-z_]\\w*))*)\\b', bygroups(Keyword.Namespace, Whitespace, Name.Namespace))], 'literals': [('"', String, 'string'), ('/(?=.*/)', String.Regex, 'regex'), ('(T|F)\\b', Keyword.Constant), ('\\d{1,5}/(udp|tcp|icmp|unknown)\\b', Number), ('(\\d{1,3}.){3}(\\d{1,3})\\b', Number), ('\\[([0-9a-fA-F]{0,4}:){2,7}([0-9a-fA-F]{0,4})?((\\d{1,3}.){3}(\\d{1,3}))?\\]', Number), ('0[xX]' + _hex + '+\\b', Number.Hex), (_float + '\\s*(day|hr|min|sec|msec|usec)s?\\b', Number.Float), (_float + '\\b', Number.Float), ('(\\d+)\\b', Number.Integer), (_h + '(\\.' + _h + ')+', String)], 'operators': [('[!%*/+<=>~|&^-]', Operator), ('([-+=&|]{2}|[+=!><-]=)', Operator), ('(in|as|is|of)\\b', Operator.Word), ('\\??\\$', Operator)], 'punctuation': [('[{}()\\[\\],;.]', Punctuation), ('[?:]', Punctuation)], 'identifiers': [('([a-zA-Z_]\\w*)(::)', bygroups(Name, Punctuation)), ('[a-zA-Z_]\\w*', Name)], 'string': [('\\\\.', String.Escape), ('%-?[0-9]*(\\.[0-9]+)?[DTd-gsx]', String.Escape), ('"', String, '#pop'), ('.', String)], 'regex': [('\\\\.', String.Escape), ('/', String.Regex, '#pop'), ('.', String.Regex)]}

BroLexer = ZeekLexer


class PuppetLexer(RegexLexer):
    """
    For Puppet configuration DSL.
    """
    name = 'Puppet'
    url = 'https://puppet.com/'
    aliases = ['puppet']
    filenames = ['*.pp']
    version_added = '1.6'
    tokens = {'root': [include('comments'), include('keywords'), include('names'), include('numbers'), include('operators'), include('strings'), ('[]{}:(),;[]', Punctuation), ('\\s+', Whitespace)], 'comments': [('(\\s*)(#.*)$', bygroups(Whitespace, Comment)), ('/(\\\\\\n)?[*](.|\\n)*?[*](\\\\\\n)?/', Comment.Multiline)], 'operators': [('(=>|\\?|<|>|=|\\+|-|/|\\*|~|!|\\|)', Operator), ('(in|and|or|not)\\b', Operator.Word)], 'names': [('[a-zA-Z_]\\w*', Name.Attribute), ('(\\$\\S+)(\\[)(\\S+)(\\])', bygroups(Name.Variable, Punctuation, String, Punctuation)), ('\\$\\S+', Name.Variable)], 'numbers': [('(\\d+\\.\\d*|\\d*\\.\\d+)([eE][+-]?[0-9]+)?j?', Number.Float), ('\\d+[eE][+-]?[0-9]+j?', Number.Float), ('0[0-7]+j?', Number.Oct), ('0[xX][a-fA-F0-9]+', Number.Hex), ('\\d+L', Number.Integer.Long), ('\\d+j?', Number.Integer)], 'keywords': [(words(('absent', 'alert', 'alias', 'audit', 'augeas', 'before', 'case', 'check', 'class', 'computer', 'configured', 'contained', 'create_resources', 'crit', 'cron', 'debug', 'default', 'define', 'defined', 'directory', 'else', 'elsif', 'emerg', 'err', 'exec', 'extlookup', 'fail', 'false', 'file', 'filebucket', 'fqdn_rand', 'generate', 'host', 'if', 'import', 'include', 'info', 'inherits', 'inline_template', 'installed', 'interface', 'k5login', 'latest', 'link', 'loglevel', 'macauthorization', 'mailalias', 'maillist', 'mcx', 'md5', 'mount', 'mounted', 'nagios_command', 'nagios_contact', 'nagios_contactgroup', 'nagios_host', 'nagios_hostdependency', 'nagios_hostescalation', 'nagios_hostextinfo', 'nagios_hostgroup', 'nagios_service', 'nagios_servicedependency', 'nagios_serviceescalation', 'nagios_serviceextinfo', 'nagios_servicegroup', 'nagios_timeperiod', 'node', 'noop', 'notice', 'notify', 'package', 'present', 'purged', 'realize', 'regsubst', 'resources', 'role', 'router', 'running', 'schedule', 'scheduled_task', 'search', 'selboolean', 'selmodule', 'service', 'sha1', 'shellquote', 'split', 'sprintf', 'ssh_authorized_key', 'sshkey', 'stage', 'stopped', 'subscribe', 'tag', 'tagged', 'template', 'tidy', 'true', 'undef', 'unmounted', 'user', 'versioncmp', 'vlan', 'warning', 'yumrepo', 'zfs', 'zone', 'zpool'), prefix='(?i)', suffix='\\b'), Keyword)], 'strings': [('"([^"])*"', String), ("'(\\\\'|[^'])*'", String)]}



class RslLexer(RegexLexer):
    """
    RSL is the formal specification
    language used in RAISE (Rigorous Approach to Industrial Software Engineering)
    method.
    """
    name = 'RSL'
    url = 'http://en.wikipedia.org/wiki/RAISE'
    aliases = ['rsl']
    filenames = ['*.rsl']
    mimetypes = ['text/rsl']
    version_added = '2.0'
    flags = re.MULTILINE | re.DOTALL
    tokens = {'root': [(words(('Bool', 'Char', 'Int', 'Nat', 'Real', 'Text', 'Unit', 'abs', 'all', 'always', 'any', 'as', 'axiom', 'card', 'case', 'channel', 'chaos', 'class', 'devt_relation', 'dom', 'elems', 'else', 'elif', 'end', 'exists', 'extend', 'false', 'for', 'hd', 'hide', 'if', 'in', 'is', 'inds', 'initialise', 'int', 'inter', 'isin', 'len', 'let', 'local', 'ltl_assertion', 'object', 'of', 'out', 'post', 'pre', 'read', 'real', 'rng', 'scheme', 'skip', 'stop', 'swap', 'then', 'theory', 'test_case', 'tl', 'transition_system', 'true', 'type', 'union', 'until', 'use', 'value', 'variable', 'while', 'with', 'write', '~isin', '-inflist', '-infset', '-list', '-set'), prefix='\\b', suffix='\\b'), Keyword), ('(variable|value)\\b', Keyword.Declaration), ('--.*?\\n', Comment), ('<:.*?:>', Comment), ('\\{!.*?!\\}', Comment), ('/\\*.*?\\*/', Comment), ('^([ \\t]*)([\\w]+)([ \\t]*)(:[^:])', bygroups(Whitespace, Name.Function, Whitespace, Name.Function)), ('(^[ \\t]*)([\\w]+)([ \\t]*)(\\([\\w\\s,]*\\))([ \\t]*)(is|as)', bygroups(Whitespace, Name.Function, Whitespace, Text, Whitespace, Keyword)), ('\\b[A-Z]\\w*\\b', Keyword.Type), ('(true|false)\\b', Keyword.Constant), ('".*"', String), ("\\'.\\'", String.Char), ('(><|->|-m->|/\\\\|<=|<<=|<\\.|\\|\\||\\|\\^\\||-~->|-~m->|\\\\/|>=|>>|\\.>|\\+\\+|-\\\\|<->|=>|:-|~=|\\*\\*|<<|>>=|\\+>|!!|\\|=\\||#)', Operator), ('[0-9]+\\.[0-9]+([eE][0-9]+)?[fd]?', Number.Float), ('0x[0-9a-f]+', Number.Hex), ('[0-9]+', Number.Integer), ('\\s+', Whitespace), ('.', Text)]}
    
    def analyse_text(text):
        """
        Check for the most common text in the beginning of a RSL file.
        """
        if re.search('scheme\\s*.*?=\\s*class\\s*type', text, re.I) is not None:
            return 1.0



class MscgenLexer(RegexLexer):
    """
    For Mscgen files.
    """
    name = 'Mscgen'
    url = 'http://www.mcternan.me.uk/mscgen/'
    aliases = ['mscgen', 'msc']
    filenames = ['*.msc']
    version_added = '1.6'
    _var = '(\\w+|"(?:\\\\"|[^"])*")'
    tokens = {'root': [('msc\\b', Keyword.Type), ('(hscale|HSCALE|width|WIDTH|wordwraparcs|WORDWRAPARCS|arcgradient|ARCGRADIENT)\\b', Name.Property), ('(abox|ABOX|rbox|RBOX|box|BOX|note|NOTE)\\b', Operator.Word), ('(\\.|-|\\|){3}', Keyword), ('(?:-|=|\\.|:){2}|<<=>>|<->|<=>|<<>>|<:>|->|=>>|>>|=>|:>|-x|-X|<-|<<=|<<|<=|<:|x-|X-|=', Operator), ('\\*', Name.Builtin), (_var, Name.Variable), ('\\[', Punctuation, 'attrs'), ('\\{|\\}|,|;', Punctuation), include('comments')], 'attrs': [('\\]', Punctuation, '#pop'), (_var + '(\\s*)(=)(\\s*)' + _var, bygroups(Name.Attribute, Whitespace, Operator, Whitespace, String)), (',', Punctuation), include('comments')], 'comments': [('(?://|#).*?\\n', Comment.Single), ('/\\*(?:.|\\n)*?\\*/', Comment.Multiline), ('[ \\t\\r\\n]+', Whitespace)]}



class VGLLexer(RegexLexer):
    """
    For SampleManager VGL source code.
    """
    name = 'VGL'
    url = 'http://www.thermoscientific.com/samplemanager'
    aliases = ['vgl']
    filenames = ['*.rpf']
    version_added = '1.6'
    flags = re.MULTILINE | re.DOTALL | re.IGNORECASE
    tokens = {'root': [('\\{[^}]*\\}', Comment.Multiline), ('declare', Keyword.Constant), ('(if|then|else|endif|while|do|endwhile|and|or|prompt|object|create|on|line|with|global|routine|value|endroutine|constant|global|set|join|library|compile_option|file|exists|create|copy|delete|enable|windows|name|notprotected)(?! *[=<>.,()])', Keyword), ('(true|false|null|empty|error|locked)', Keyword.Constant), ('[~^*#!%&\\[\\]()<>|+=:;,./?-]', Operator), ('"[^"]*"', String), ('(\\.)([a-z_$][\\w$]*)', bygroups(Operator, Name.Attribute)), ('[0-9][0-9]*(\\.[0-9]+(e[+\\-]?[0-9]+)?)?', Number), ('[a-z_$][\\w$]*', Name), ('[\\r\\n]+', Whitespace), ('\\s+', Whitespace)]}



class AlloyLexer(RegexLexer):
    """
    For Alloy source code.
    """
    name = 'Alloy'
    url = 'http://alloy.mit.edu'
    aliases = ['alloy']
    filenames = ['*.als']
    mimetypes = ['text/x-alloy']
    version_added = '2.0'
    flags = re.MULTILINE | re.DOTALL
    iden_rex = '[a-zA-Z_][\\w]*"*'
    string_rex = '"\\b(\\\\\\\\|\\\\[^\\\\]|[^"\\\\])*"'
    text_tuple = ('[^\\S\\n]+', Whitespace)
    tokens = {'sig': [('(extends)\\b', Keyword, '#pop'), (iden_rex, Name), text_tuple, (',', Punctuation), ('\\{', Operator, '#pop')], 'module': [text_tuple, (iden_rex, Name, '#pop')], 'fun': [text_tuple, ('\\{', Operator, '#pop'), (iden_rex, Name, '#pop')], 'fact': [include('fun'), (string_rex, String, '#pop')], 'root': [('--.*?$', Comment.Single), ('//.*?$', Comment.Single), ('/\\*.*?\\*/', Comment.Multiline), text_tuple, ('(module|open)(\\s+)', bygroups(Keyword.Namespace, Whitespace), 'module'), ('(sig|enum)(\\s+)', bygroups(Keyword.Declaration, Whitespace), 'sig'), ('(iden|univ|none)\\b', Keyword.Constant), ('(int|Int)\\b', Keyword.Type), ('(var|this|abstract|extends|set|seq|one|lone|let)\\b', Keyword), ('(all|some|no|sum|disj|when|else)\\b', Keyword), ('(run|check|for|but|exactly|expect|as|steps)\\b', Keyword), ('(always|after|eventually|until|release)\\b', Keyword), ('(historically|before|once|since|triggered)\\b', Keyword), ('(and|or|implies|iff|in)\\b', Operator.Word), ('(fun|pred|assert)(\\s+)', bygroups(Keyword, Whitespace), 'fun'), ('(fact)(\\s+)', bygroups(Keyword, Whitespace), 'fact'), ('!|#|&&|\\+\\+|<<|>>|>=|<=>|<=|\\.\\.|\\.|->', Operator), ("[-+/*%=<>&!^|~{}\\[\\]().\\';]", Operator), (iden_rex, Name), ('[:,]', Punctuation), ('[0-9]+', Number.Integer), (string_rex, String), ('\\n', Whitespace)]}



class PanLexer(RegexLexer):
    """
    Lexer for pan source files.

    Based on tcsh lexer.
    """
    name = 'Pan'
    url = 'https://github.com/quattor/pan/'
    aliases = ['pan']
    filenames = ['*.pan']
    version_added = '2.0'
    tokens = {'root': [include('basic'), ('\\(', Keyword, 'paren'), ('\\{', Keyword, 'curly'), include('data')], 'basic': [(words(('if', 'for', 'with', 'else', 'type', 'bind', 'while', 'valid', 'final', 'prefix', 'unique', 'object', 'foreach', 'include', 'template', 'function', 'variable', 'structure', 'extensible', 'declaration'), prefix='\\b', suffix='\\b'), Keyword), (words(('file_contents', 'format', 'index', 'length', 'match', 'matches', 'replace', 'splice', 'split', 'substr', 'to_lowercase', 'to_uppercase', 'debug', 'error', 'traceback', 'deprecated', 'base64_decode', 'base64_encode', 'digest', 'escape', 'unescape', 'append', 'create', 'first', 'nlist', 'key', 'list', 'merge', 'next', 'prepend', 'is_boolean', 'is_defined', 'is_double', 'is_list', 'is_long', 'is_nlist', 'is_null', 'is_number', 'is_property', 'is_resource', 'is_string', 'to_boolean', 'to_double', 'to_long', 'to_string', 'clone', 'delete', 'exists', 'path_exists', 'if_exists', 'return', 'value'), prefix='\\b', suffix='\\b'), Name.Builtin), ('#.*', Comment), ('\\\\[\\w\\W]', String.Escape), ('(\\b\\w+)(\\s*)(=)', bygroups(Name.Variable, Whitespace, Operator)), ('[\\[\\]{}()=]+', Operator), ("<<\\s*(\\'?)\\\\?(\\w+)[\\w\\W]+?\\2", String), (';', Punctuation)], 'data': [('(?s)"(\\\\\\\\|\\\\[0-7]+|\\\\.|[^"\\\\])*"', String.Double), ("(?s)'(\\\\\\\\|\\\\[0-7]+|\\\\.|[^'\\\\])*'", String.Single), ('\\s+', Whitespace), ('[^=\\s\\[\\]{}()$"\\\'`\\\\;#]+', Text), ('\\d+(?= |\\Z)', Number)], 'curly': [('\\}', Keyword, '#pop'), (':-', Keyword), ('\\w+', Name.Variable), ('[^}:"\\\'`$]+', Punctuation), (':', Punctuation), include('root')], 'paren': [('\\)', Keyword, '#pop'), include('root')]}



class CrmshLexer(RegexLexer):
    """
    Lexer for crmsh configuration files for Pacemaker clusters.
    """
    name = 'Crmsh'
    url = 'http://crmsh.github.io/'
    aliases = ['crmsh', 'pcmk']
    filenames = ['*.crmsh', '*.pcmk']
    mimetypes = []
    version_added = '2.1'
    elem = words(('node', 'primitive', 'group', 'clone', 'ms', 'location', 'colocation', 'order', 'fencing_topology', 'rsc_ticket', 'rsc_template', 'property', 'rsc_defaults', 'op_defaults', 'acl_target', 'acl_group', 'user', 'role', 'tag'), suffix='(?![\\w#$-])')
    sub = words(('params', 'meta', 'operations', 'op', 'rule', 'attributes', 'utilization'), suffix='(?![\\w#$-])')
    acl = words(('read', 'write', 'deny'), suffix='(?![\\w#$-])')
    bin_rel = words(('and', 'or'), suffix='(?![\\w#$-])')
    un_ops = words(('defined', 'not_defined'), suffix='(?![\\w#$-])')
    date_exp = words(('in_range', 'date', 'spec', 'in'), suffix='(?![\\w#$-])')
    acl_mod = '(?:tag|ref|reference|attribute|type|xpath)'
    bin_ops = '(?:lt|gt|lte|gte|eq|ne)'
    val_qual = '(?:string|version|number)'
    rsc_role_action = '(?:Master|Started|Slave|Stopped|start|promote|demote|stop)'
    tokens = {'root': [('^(#.*)(\\n)?', bygroups(Comment, Whitespace)), ('([\\w#$-]+)(=)("(?:""|[^"])*"|\\S+)', bygroups(Name.Attribute, Punctuation, String)), ('(node)(\\s+)([\\w#$-]+)(:)', bygroups(Keyword, Whitespace, Name, Punctuation)), ('([+-]?([0-9]+|inf)):', Number), (elem, Keyword), (sub, Keyword), (acl, Keyword), (f'(?:{val_qual}:)?({bin_ops})(?![\\w#$-])', Operator.Word), (bin_rel, Operator.Word), (un_ops, Operator.Word), (date_exp, Operator.Word), ('#[a-z]+(?![\\w#$-])', Name.Builtin), (f'({acl_mod})(:)("(?:""|[^"])*"|\\S+)', bygroups(Keyword, Punctuation, Name)), (f'([\\w#$-]+)(?:(:)({rsc_role_action}))?(?![\\w#$-])', bygroups(Name, Punctuation, Operator.Word)), ('(\\\\(?=\\n)|[\\[\\](){}/:@])', Punctuation), ('\\s+|\\n', Whitespace)]}



class FlatlineLexer(RegexLexer):
    """
    Lexer for Flatline expressions.
    """
    name = 'Flatline'
    url = 'https://github.com/bigmlcom/flatline'
    aliases = ['flatline']
    filenames = []
    mimetypes = ['text/x-flatline']
    version_added = '2.2'
    special_forms = ('let', )
    builtins = ('!=', '*', '+', '-', '<', '<=', '=', '>', '>=', 'abs', 'acos', 'all', 'all-but', 'all-with-defaults', 'all-with-numeric-default', 'and', 'asin', 'atan', 'avg', 'avg-window', 'bin-center', 'bin-count', 'call', 'category-count', 'ceil', 'cond', 'cond-window', 'cons', 'cos', 'cosh', 'count', 'diff-window', 'div', 'ensure-value', 'ensure-weighted-value', 'epoch', 'epoch-day', 'epoch-fields', 'epoch-hour', 'epoch-millisecond', 'epoch-minute', 'epoch-month', 'epoch-second', 'epoch-weekday', 'epoch-year', 'exp', 'f', 'field', 'field-prop', 'fields', 'filter', 'first', 'floor', 'head', 'if', 'in', 'integer', 'language', 'length', 'levenshtein', 'linear-regression', 'list', 'ln', 'log', 'log10', 'map', 'matches', 'matches?', 'max', 'maximum', 'md5', 'mean', 'median', 'min', 'minimum', 'missing', 'missing-count', 'missing?', 'missing_count', 'mod', 'mode', 'normalize', 'not', 'nth', 'occurrences', 'or', 'percentile', 'percentile-label', 'population', 'population-fraction', 'pow', 'preferred', 'preferred?', 'quantile-label', 'rand', 'rand-int', 'random-value', 're-quote', 'real', 'replace', 'replace-first', 'rest', 'round', 'row-number', 'segment-label', 'sha1', 'sha256', 'sin', 'sinh', 'sqrt', 'square', 'standard-deviation', 'standard_deviation', 'str', 'subs', 'sum', 'sum-squares', 'sum-window', 'sum_squares', 'summary', 'summary-no', 'summary-str', 'tail', 'tan', 'tanh', 'to-degrees', 'to-radians', 'variance', 'vectorize', 'weighted-random-value', 'window', 'winnow', 'within-percentiles?', 'z-score')
    valid_name = '(?!#)[\\w!$%*+<=>?/.#-]+'
    tokens = {'root': [('[,]+', Text), ('\\s+', Whitespace), ('-?\\d+\\.\\d+', Number.Float), ('-?\\d+', Number.Integer), ('0x-?[a-f\\d]+', Number.Hex), ('"(\\\\\\\\|\\\\[^\\\\]|[^"\\\\])*"', String), ('\\\\(.|[a-z]+)', String.Char), ('_', String.Symbol), (words(special_forms, suffix=' '), Keyword), (words(builtins, suffix=' '), Name.Builtin), ('(?<=\\()' + valid_name, Name.Function), (valid_name, Name.Variable), ('(\\(|\\))', Punctuation)]}



class SnowballLexer(ExtendedRegexLexer):
    """
    Lexer for Snowball source code.
    """
    name = 'Snowball'
    url = 'https://snowballstem.org/'
    aliases = ['snowball']
    filenames = ['*.sbl']
    version_added = '2.2'
    _ws = '\\n\\r\\t '
    
    def __init__(self, **options):
        self._reset_stringescapes()
        ExtendedRegexLexer.__init__(self, **options)
    
    def _reset_stringescapes(self):
        self._start = "'"
        self._end = "'"
    
    def _string(do_string_first):
        
        def callback(lexer, match, ctx):
            s = match.start()
            text = match.group()
            string = re.compile(f'([^{re.escape(lexer._start)}]*)(.)').match
            escape = re.compile(f'([^{re.escape(lexer._end)}]*)(.)').match
            pos = 0
            do_string = do_string_first
            while pos < len(text):
                if do_string:
                    match = string(text, pos)
                    yield (s + match.start(1), String.Single, match.group(1))
                    if match.group(2) == "'":
                        yield (s + match.start(2), String.Single, match.group(2))
                        ctx.stack.pop()
                        break
                    yield (s + match.start(2), String.Escape, match.group(2))
                    pos = match.end()
                match = escape(text, pos)
                yield (s + match.start(), String.Escape, match.group())
                if match.group(2) != lexer._end:
                    ctx.stack[-1] = 'escape'
                    break
                pos = match.end()
                do_string = True
            ctx.pos = s + match.end()
        return callback
    
    def _stringescapes(lexer, match, ctx):
        lexer._start = match.group(3)
        lexer._end = match.group(5)
        return bygroups(Keyword.Reserved, Whitespace, String.Escape, Whitespace, String.Escape)(lexer, match, ctx)
    tokens = {'root': [('len\\b', Name.Builtin), ('lenof\\b', Operator.Word), include('root1')], 'root1': [(f'[{_ws}]+', Whitespace), ('\\d+', Number.Integer), ("'", String.Single, 'string'), ('[()]', Punctuation), ('/\\*[\\w\\W]*?\\*/', Comment.Multiline), ('//.*', Comment.Single), ('[!*+\\-/<=>]=|[-=]>|<[+-]|[$*+\\-/<=>?\\[\\]]', Operator), (words(('as', 'get', 'hex', 'among', 'define', 'decimal', 'backwardmode'), suffix='\\b'), Keyword.Reserved), (words(('strings', 'booleans', 'integers', 'routines', 'externals', 'groupings'), suffix='\\b'), Keyword.Reserved, 'declaration'), (words(('do', 'or', 'and', 'for', 'hop', 'non', 'not', 'set', 'try', 'fail', 'goto', 'loop', 'next', 'test', 'true', 'false', 'unset', 'atmark', 'attach', 'delete', 'gopast', 'insert', 'repeat', 'sizeof', 'tomark', 'atleast', 'atlimit', 'reverse', 'setmark', 'tolimit', 'setlimit', 'backwards', 'substring'), suffix='\\b'), Operator.Word), (words(('size', 'limit', 'cursor', 'maxint', 'minint'), suffix='\\b'), Name.Builtin), (f'(stringdef\\b)([{_ws}]*)([^{_ws}]+)', bygroups(Keyword.Reserved, Whitespace, String.Escape)), (f'(stringescapes\\b)([{_ws}]*)(.)([{_ws}]*)(.)', _stringescapes), ('[A-Za-z]\\w*', Name)], 'declaration': [('\\)', Punctuation, '#pop'), (words(('len', 'lenof'), suffix='\\b'), Name, ('root1', 'declaration')), include('root1')], 'string': [("[^']*'", _string(True))], 'escape': [("[^']*'", _string(False))]}
    
    def get_tokens_unprocessed(self, text=None, context=None):
        self._reset_stringescapes()
        return ExtendedRegexLexer.get_tokens_unprocessed(self, text, context)


