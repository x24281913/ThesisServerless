"""
    pygments.lexers.unicon
    ~~~~~~~~~~~~~~~~~~~~~~

    Lexers for the Icon and Unicon languages, including ucode VM.

    :copyright: Copyright 2006-present by the Pygments team, see AUTHORS.
    :license: BSD, see LICENSE for details.
"""

import re
from pygments.lexer import RegexLexer, include, bygroups, words, using, this
from pygments.token import Text, Comment, Operator, Keyword, Name, String, Number, Punctuation
__all__ = ['IconLexer', 'UcodeLexer', 'UniconLexer']


class UniconLexer(RegexLexer):
    """
    For Unicon source code.
    """
    name = 'Unicon'
    aliases = ['unicon']
    filenames = ['*.icn']
    mimetypes = ['text/unicon']
    url = 'https://www.unicon.org'
    version_added = '2.4'
    flags = re.MULTILINE
    tokens = {'root': [('[^\\S\\n]+', Text), ('#.*?\\n', Comment.Single), ('[^\\S\\n]+', Text), ('class|method|procedure', Keyword.Declaration, 'subprogram'), ('(record)(\\s+)(\\w+)', bygroups(Keyword.Declaration, Text, Keyword.Type), 'type_def'), ('(#line|\\$C|\\$Cend|\\$define|\\$else|\\$endif|\\$error|\\$ifdef|\\$ifndef|\\$include|\\$line|\\$undef)\\b', Keyword.PreProc), ('(&null|&fail)\\b', Keyword.Constant), ('&allocated|&ascii|&clock|&collections|&column|&col|&control|&cset|&current|&dateline|&date|&digits|&dump|&errno|&errornumber|&errortext|&errorvalue|&error|&errout|&eventcode|&eventvalue|&eventsource|&e|&features|&file|&host|&input|&interval|&lcase|&letters|&level|&line|&ldrag|&lpress|&lrelease|&main|&mdrag|&meta|&mpress|&mrelease|&now|&output|&phi|&pick|&pi|&pos|&progname|&random|&rdrag|&regions|&resize|&row|&rpress|&rrelease|&shift|&source|&storage|&subject|&time|&trace|&ucase|&version|&window|&x|&y', Keyword.Reserved), ('(by|of|not|to)\\b', Keyword.Reserved), ('(global|local|static|abstract)\\b', Keyword.Reserved), ('package|link|import', Keyword.Declaration), (words(('break', 'case', 'create', 'critical', 'default', 'end', 'all', 'do', 'else', 'every', 'fail', 'if', 'import', 'initial', 'initially', 'invocable', 'next', 'repeat', 'return', 'suspend', 'then', 'thread', 'until', 'while'), prefix='\\b', suffix='\\b'), Keyword.Reserved), (words(('Abort', 'abs', 'acos', 'Active', 'Alert', 'any', 'Any', 'Arb', 'Arbno', 'args', 'array', 'asin', 'atan', 'atanh', 'Attrib', 'Bal', 'bal', 'Bg', 'Break', 'Breakx', 'callout', 'center', 'char', 'chdir', 'chmod', 'chown', 'chroot', 'classname', 'Clip', 'Clone', 'close', 'cofail', 'collect', 'Color', 'ColorValue', 'condvar', 'constructor', 'copy', 'CopyArea', 'cos', 'Couple', 'crypt', 'cset', 'ctime', 'dbcolumns', 'dbdriver', 'dbkeys', 'dblimits', 'dbproduct', 'dbtables', 'delay', 'delete', 'detab', 'display', 'DrawArc', 'DrawCircle', 'DrawCube', 'DrawCurve', 'DrawCylinder', 'DrawDisk', 'DrawImage', 'DrawLine', 'DrawPoint', 'DrawPolygon', 'DrawRectangle', 'DrawSegment', 'DrawSphere', 'DrawString', 'DrawTorus', 'dtor', 'entab', 'EraseArea', 'errorclear', 'Event', 'eventmask', 'EvGet', 'EvSend', 'exec', 'exit', 'exp', 'Eye', 'Fail', 'fcntl', 'fdup', 'Fence', 'fetch', 'Fg', 'fieldnames', 'filepair', 'FillArc', 'FillCircle', 'FillPolygon', 'FillRectangle', 'find', 'flock', 'flush', 'Font', 'fork', 'FreeColor', 'FreeSpace', 'function', 'get', 'getch', 'getche', 'getegid', 'getenv', 'geteuid', 'getgid', 'getgr', 'gethost', 'getpgrp', 'getpid', 'getppid', 'getpw', 'getrusage', 'getserv', 'GetSpace', 'gettimeofday', 'getuid', 'globalnames', 'GotoRC', 'GotoXY', 'gtime', 'hardlink', 'iand', 'icom', 'IdentityMatrix', 'image', 'InPort', 'insert', 'Int86', 'integer', 'ioctl', 'ior', 'ishift', 'istate', 'ixor', 'kbhit', 'key', 'keyword', 'kill', 'left', 'Len', 'list', 'load', 'loadfunc', 'localnames', 'lock', 'log', 'Lower', 'lstat', 'many', 'map', 'match', 'MatrixMode', 'max', 'member', 'membernames', 'methodnames', 'methods', 'min', 'mkdir', 'move', 'MultMatrix', 'mutex', 'name', 'NewColor', 'Normals', 'NotAny', 'numeric', 'open', 'opencl', 'oprec', 'ord', 'OutPort', 'PaletteChars', 'PaletteColor', 'PaletteKey', 'paramnames', 'parent', 'Pattern', 'Peek', 'Pending', 'pipe', 'Pixel', 'PlayAudio', 'Poke', 'pop', 'PopMatrix', 'Pos', 'pos', 'proc', 'pull', 'push', 'PushMatrix', 'PushRotate', 'PushScale', 'PushTranslate', 'put', 'QueryPointer', 'Raise', 'read', 'ReadImage', 'readlink', 'reads', 'ready', 'real', 'receive', 'Refresh', 'Rem', 'remove', 'rename', 'repl', 'reverse', 'right', 'rmdir', 'Rotate', 'Rpos', 'Rtab', 'rtod', 'runerr', 'save', 'Scale', 'seek', 'select', 'send', 'seq', 'serial', 'set', 'setenv', 'setgid', 'setgrent', 'sethostent', 'setpgrp', 'setpwent', 'setservent', 'setuid', 'signal', 'sin', 'sort', 'sortf', 'Span', 'spawn', 'sql', 'sqrt', 'stat', 'staticnames', 'stop', 'StopAudio', 'string', 'structure', 'Succeed', 'Swi', 'symlink', 'sys_errstr', 'system', 'syswrite', 'Tab', 'tab', 'table', 'tan', 'Texcoord', 'Texture', 'TextWidth', 'Translate', 'trap', 'trim', 'truncate', 'trylock', 'type', 'umask', 'Uncouple', 'unlock', 'upto', 'utime', 'variable', 'VAttrib', 'wait', 'WAttrib', 'WDefault', 'WFlush', 'where', 'WinAssociate', 'WinButton', 'WinColorDialog', 'WindowContents', 'WinEditRegion', 'WinFontDialog', 'WinMenuBar', 'WinOpenDialog', 'WinPlayMedia', 'WinSaveDialog', 'WinScrollBar', 'WinSelectDialog', 'write', 'WriteImage', 'writes', 'WSection', 'WSync'), prefix='\\b', suffix='\\b'), Name.Function), include('numbers'), ('<@|<<@|>@|>>@|\\.>|->|===|~===|\\*\\*|\\+\\+|--|\\.|~==|~=|<=|>=|==|=|<<=|<<|>>=|>>|:=:|:=|->|<->|\\+:=|\\|', Operator), ('"(?:[^\\\\"]|\\\\.)*"', String), ("'(?:[^\\\\']|\\\\.)*'", String.Character), ('[*<>+=/&!?@~\\\\-]', Operator), ('\\^', Operator), ('(\\w+)(\\s*|[(,])', bygroups(Name, using(this))), ('[\\[\\]]', Punctuation), ("<>|=>|[()|:;,.'`{}%&?]", Punctuation), ('\\n+', Text)], 'numbers': [('\\b([+-]?([2-9]|[12][0-9]|3[0-6])[rR][0-9a-zA-Z]+)\\b', Number.Hex), ('[+-]?[0-9]*\\.([0-9]*)([Ee][+-]?[0-9]*)?', Number.Float), ('\\b([+-]?[0-9]+[KMGTPkmgtp]?)\\b', Number.Integer)], 'subprogram': [('\\(', Punctuation, ('#pop', 'formal_part')), (';', Punctuation, '#pop'), ('"[^"]+"|\\w+', Name.Function), include('root')], 'type_def': [('\\(', Punctuation, 'formal_part')], 'formal_part': [('\\)', Punctuation, '#pop'), ('\\w+', Name.Variable), (',', Punctuation), ('(:string|:integer|:real)\\b', Keyword.Reserved), include('root')]}



class IconLexer(RegexLexer):
    """
    Lexer for Icon.
    """
    name = 'Icon'
    aliases = ['icon']
    filenames = ['*.icon', '*.ICON']
    mimetypes = []
    url = 'https://www2.cs.arizona.edu/icon'
    version_added = '1.6'
    flags = re.MULTILINE
    tokens = {'root': [('[^\\S\\n]+', Text), ('#.*?\\n', Comment.Single), ('[^\\S\\n]+', Text), ('class|method|procedure', Keyword.Declaration, 'subprogram'), ('(record)(\\s+)(\\w+)', bygroups(Keyword.Declaration, Text, Keyword.Type), 'type_def'), ('(#line|\\$C|\\$Cend|\\$define|\\$else|\\$endif|\\$error|\\$ifdef|\\$ifndef|\\$include|\\$line|\\$undef)\\b', Keyword.PreProc), ('(&null|&fail)\\b', Keyword.Constant), ('&allocated|&ascii|&clock|&collections|&column|&col|&control|&cset|&current|&dateline|&date|&digits|&dump|&errno|&errornumber|&errortext|&errorvalue|&error|&errout|&eventcode|&eventvalue|&eventsource|&e|&features|&file|&host|&input|&interval|&lcase|&letters|&level|&line|&ldrag|&lpress|&lrelease|&main|&mdrag|&meta|&mpress|&mrelease|&now|&output|&phi|&pick|&pi|&pos|&progname|&random|&rdrag|&regions|&resize|&row|&rpress|&rrelease|&shift|&source|&storage|&subject|&time|&trace|&ucase|&version|&window|&x|&y', Keyword.Reserved), ('(by|of|not|to)\\b', Keyword.Reserved), ('(global|local|static)\\b', Keyword.Reserved), ('link', Keyword.Declaration), (words(('break', 'case', 'create', 'default', 'end', 'all', 'do', 'else', 'every', 'fail', 'if', 'initial', 'invocable', 'next', 'repeat', 'return', 'suspend', 'then', 'until', 'while'), prefix='\\b', suffix='\\b'), Keyword.Reserved), (words(('abs', 'acos', 'Active', 'Alert', 'any', 'args', 'array', 'asin', 'atan', 'atanh', 'Attrib', 'bal', 'Bg', 'callout', 'center', 'char', 'chdir', 'chmod', 'chown', 'chroot', 'Clip', 'Clone', 'close', 'cofail', 'collect', 'Color', 'ColorValue', 'condvar', 'copy', 'CopyArea', 'cos', 'Couple', 'crypt', 'cset', 'ctime', 'delay', 'delete', 'detab', 'display', 'DrawArc', 'DrawCircle', 'DrawCube', 'DrawCurve', 'DrawCylinder', 'DrawDisk', 'DrawImage', 'DrawLine', 'DrawPoint', 'DrawPolygon', 'DrawRectangle', 'DrawSegment', 'DrawSphere', 'DrawString', 'DrawTorus', 'dtor', 'entab', 'EraseArea', 'errorclear', 'Event', 'eventmask', 'EvGet', 'EvSend', 'exec', 'exit', 'exp', 'Eye', 'fcntl', 'fdup', 'fetch', 'Fg', 'fieldnames', 'FillArc', 'FillCircle', 'FillPolygon', 'FillRectangle', 'find', 'flock', 'flush', 'Font', 'FreeColor', 'FreeSpace', 'function', 'get', 'getch', 'getche', 'getenv', 'GetSpace', 'gettimeofday', 'getuid', 'globalnames', 'GotoRC', 'GotoXY', 'gtime', 'hardlink', 'iand', 'icom', 'IdentityMatrix', 'image', 'InPort', 'insert', 'Int86', 'integer', 'ioctl', 'ior', 'ishift', 'istate', 'ixor', 'kbhit', 'key', 'keyword', 'kill', 'left', 'Len', 'list', 'load', 'loadfunc', 'localnames', 'lock', 'log', 'Lower', 'lstat', 'many', 'map', 'match', 'MatrixMode', 'max', 'member', 'membernames', 'methodnames', 'methods', 'min', 'mkdir', 'move', 'MultMatrix', 'mutex', 'name', 'NewColor', 'Normals', 'numeric', 'open', 'opencl', 'oprec', 'ord', 'OutPort', 'PaletteChars', 'PaletteColor', 'PaletteKey', 'paramnames', 'parent', 'Pattern', 'Peek', 'Pending', 'pipe', 'Pixel', 'Poke', 'pop', 'PopMatrix', 'Pos', 'pos', 'proc', 'pull', 'push', 'PushMatrix', 'PushRotate', 'PushScale', 'PushTranslate', 'put', 'QueryPointer', 'Raise', 'read', 'ReadImage', 'readlink', 'reads', 'ready', 'real', 'receive', 'Refresh', 'Rem', 'remove', 'rename', 'repl', 'reverse', 'right', 'rmdir', 'Rotate', 'Rpos', 'rtod', 'runerr', 'save', 'Scale', 'seek', 'select', 'send', 'seq', 'serial', 'set', 'setenv', 'setuid', 'signal', 'sin', 'sort', 'sortf', 'spawn', 'sql', 'sqrt', 'stat', 'staticnames', 'stop', 'string', 'structure', 'Swi', 'symlink', 'sys_errstr', 'system', 'syswrite', 'tab', 'table', 'tan', 'Texcoord', 'Texture', 'TextWidth', 'Translate', 'trap', 'trim', 'truncate', 'trylock', 'type', 'umask', 'Uncouple', 'unlock', 'upto', 'utime', 'variable', 'wait', 'WAttrib', 'WDefault', 'WFlush', 'where', 'WinAssociate', 'WinButton', 'WinColorDialog', 'WindowContents', 'WinEditRegion', 'WinFontDialog', 'WinMenuBar', 'WinOpenDialog', 'WinPlayMedia', 'WinSaveDialog', 'WinScrollBar', 'WinSelectDialog', 'write', 'WriteImage', 'writes', 'WSection', 'WSync'), prefix='\\b', suffix='\\b'), Name.Function), include('numbers'), ('===|~===|\\*\\*|\\+\\+|--|\\.|==|~==|<=|>=|=|~=|<<=|<<|>>=|>>|:=:|:=|<->|<-|\\+:=|\\|\\||\\|', Operator), ('"(?:[^\\\\"]|\\\\.)*"', String), ("'(?:[^\\\\']|\\\\.)*'", String.Character), ('[*<>+=/&!?@~\\\\-]', Operator), ('(\\w+)(\\s*|[(,])', bygroups(Name, using(this))), ('[\\[\\]]', Punctuation), ("<>|=>|[()|:;,.'`{}%\\^&?]", Punctuation), ('\\n+', Text)], 'numbers': [('\\b([+-]?([2-9]|[12][0-9]|3[0-6])[rR][0-9a-zA-Z]+)\\b', Number.Hex), ('[+-]?[0-9]*\\.([0-9]*)([Ee][+-]?[0-9]*)?', Number.Float), ('\\b([+-]?[0-9]+[KMGTPkmgtp]?)\\b', Number.Integer)], 'subprogram': [('\\(', Punctuation, ('#pop', 'formal_part')), (';', Punctuation, '#pop'), ('"[^"]+"|\\w+', Name.Function), include('root')], 'type_def': [('\\(', Punctuation, 'formal_part')], 'formal_part': [('\\)', Punctuation, '#pop'), ('\\w+', Name.Variable), (',', Punctuation), ('(:string|:integer|:real)\\b', Keyword.Reserved), include('root')]}



class UcodeLexer(RegexLexer):
    """
    Lexer for Icon ucode files.
    """
    name = 'ucode'
    aliases = ['ucode']
    filenames = ['*.u', '*.u1', '*.u2']
    mimetypes = []
    url = 'http://www.unicon.org'
    version_added = '2.4'
    flags = re.MULTILINE
    tokens = {'root': [('(#.*\\n)', Comment), (words(('con', 'declend', 'end', 'global', 'impl', 'invocable', 'lab', 'link', 'local', 'record', 'uid', 'unions', 'version'), prefix='\\b', suffix='\\b'), Name.Function), (words(('colm', 'filen', 'line', 'synt'), prefix='\\b', suffix='\\b'), Comment), (words(('asgn', 'bang', 'bscan', 'cat', 'ccase', 'chfail', 'coact', 'cofail', 'compl', 'coret', 'create', 'cset', 'diff', 'div', 'dup', 'efail', 'einit', 'end', 'eqv', 'eret', 'error', 'escan', 'esusp', 'field', 'goto', 'init', 'int', 'inter', 'invoke', 'keywd', 'lconcat', 'lexeq', 'lexge', 'lexgt', 'lexle', 'lexlt', 'lexne', 'limit', 'llist', 'lsusp', 'mark', 'mark0', 'minus', 'mod', 'mult', 'neg', 'neqv', 'nonnull', 'noop', 'null', 'number', 'numeq', 'numge', 'numgt', 'numle', 'numlt', 'numne', 'pfail', 'plus', 'pnull', 'pop', 'power', 'pret', 'proc', 'psusp', 'push1', 'pushn1', 'random', 'rasgn', 'rcv', 'rcvbk', 'real', 'refresh', 'rswap', 'sdup', 'sect', 'size', 'snd', 'sndbk', 'str', 'subsc', 'swap', 'tabmat', 'tally', 'toby', 'trace', 'unmark', 'value', 'var'), prefix='\\b', suffix='\\b'), Keyword.Declaration), (words(('any', 'case', 'endcase', 'endevery', 'endif', 'endifelse', 'endrepeat', 'endsuspend', 'enduntil', 'endwhile', 'every', 'if', 'ifelse', 'repeat', 'suspend', 'until', 'while'), prefix='\\b', suffix='\\b'), Name.Constant), ('\\d+(\\s*|\\.$|$)', Number.Integer), ('[+-]?\\d*\\.\\d+(E[-+]?\\d+)?', Number.Float), ('[+-]?\\d+\\.\\d*(E[-+]?\\d+)?', Number.Float), ("(<>|=>|[()|:;,.'`]|[{}]|[%^]|[&?])", Punctuation), ('\\s+\\b', Text), ('[\\w-]+', Text)]}
    
    def analyse_text(text):
        """endsuspend and endrepeat are unique to this language, and
        \self, /self doesn't seem to get used anywhere else either."""
        result = 0
        if 'endsuspend' in text:
            result += 0.1
        if 'endrepeat' in text:
            result += 0.1
        if ':=' in text:
            result += 0.01
        if ('procedure' in text and 'end' in text):
            result += 0.01
        if ('\\self' in text and '/self' in text):
            result += 0.5
        return result


