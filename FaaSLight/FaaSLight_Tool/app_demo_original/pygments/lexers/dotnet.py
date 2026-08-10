"""
    pygments.lexers.dotnet
    ~~~~~~~~~~~~~~~~~~~~~~

    Lexers for .net languages.

    :copyright: Copyright 2006-present by the Pygments team, see AUTHORS.
    :license: BSD, see LICENSE for details.
"""

import re
from pygments.lexer import RegexLexer, DelegatingLexer, bygroups, include, using, this, default, words
from pygments.token import Punctuation, Text, Comment, Operator, Keyword, Name, String, Number, Literal, Other, Whitespace
from pygments.util import get_choice_opt
from pygments import unistring as uni
from pygments.lexers.html import XmlLexer
__all__ = ['CSharpLexer', 'NemerleLexer', 'BooLexer', 'VbNetLexer', 'CSharpAspxLexer', 'VbNetAspxLexer', 'FSharpLexer', 'XppLexer']


class CSharpLexer(RegexLexer):
    """
    For C# source code.

    Additional options accepted:

    `unicodelevel`
      Determines which Unicode characters this lexer allows for identifiers.
      The possible values are:

      * ``none`` -- only the ASCII letters and numbers are allowed. This
        is the fastest selection.
      * ``basic`` -- all Unicode characters from the specification except
        category ``Lo`` are allowed.
      * ``full`` -- all Unicode characters as specified in the C# specs
        are allowed.  Note that this means a considerable slowdown since the
        ``Lo`` category has more than 40,000 characters in it!

      The default value is ``basic``.

      .. versionadded:: 0.8
    """
    name = 'C#'
    url = 'https://docs.microsoft.com/en-us/dotnet/csharp/'
    aliases = ['csharp', 'c#', 'cs']
    filenames = ['*.cs']
    mimetypes = ['text/x-csharp']
    version_added = ''
    flags = re.MULTILINE | re.DOTALL
    levels = {'none': '@?[_a-zA-Z]\\w*', 'basic': '@?[_' + uni.combine('Lu', 'Ll', 'Lt', 'Lm', 'Nl') + ']' + '[' + uni.combine('Lu', 'Ll', 'Lt', 'Lm', 'Nl', 'Nd', 'Pc', 'Cf', 'Mn', 'Mc') + ']*', 'full': '@?(?:_|[^' + uni.allexcept('Lu', 'Ll', 'Lt', 'Lm', 'Lo', 'Nl') + '])' + '[^' + uni.allexcept('Lu', 'Ll', 'Lt', 'Lm', 'Lo', 'Nl', 'Nd', 'Pc', 'Cf', 'Mn', 'Mc') + ']*'}
    tokens = {}
    token_variants = True
    for (levelname, cs_ident) in levels.items():
        tokens[levelname] = {'root': [include('numbers'), ('^([ \\t]*)((?:' + cs_ident + '(?:\\[\\])?\\s+)+?)(' + cs_ident + ')(\\s*)(\\()', bygroups(Whitespace, using(this), Name.Function, Whitespace, Punctuation)), ('^(\\s*)(\\[.*?\\])', bygroups(Whitespace, Name.Attribute)), ('[^\\S\\n]+', Whitespace), ('(\\\\)(\\n)', bygroups(Text, Whitespace)), ('//.*?\\n', Comment.Single), ('/[*].*?[*]/', Comment.Multiline), ('\\n', Whitespace), (words(('>>>=', '>>=', '<<=', '<=', '>=', '+=', '-=', '*=', '/=', '%=', '&=', '|=', '^=', '??=', '=>', '??', '?.', '!=', '==', '&&', '||', '>>>', '>>', '<<', '++', '--', '+', '-', '*', '/', '%', '&', '|', '^', '<', '>', '?', '!', '~', '=')), Operator), ('=~|!=|==|<<|>>|[-+/*%=<>&^|]', Operator), ('[()\\[\\];:,.]', Punctuation), ('[{}]', Punctuation), ('@"(""|[^"])*"', String), ('\\$?"(\\\\\\\\|\\\\[^\\\\]|[^"\\\\\\n])*["\\n]', String), ("'\\\\.'|'[^\\\\]'", String.Char), ('[0-9]+(\\.[0-9]*)?([eE][+-][0-9]+)?[flFLdD]?|0[xX][0-9a-fA-F]+[Ll]?', Number), ('(#)([ \\t]*)(if|endif|else|elif|define|undef|line|error|warning|region|endregion|pragma)\\b(.*?)(\\n)', bygroups(Comment.Preproc, Whitespace, Comment.Preproc, Comment.Preproc, Whitespace)), ('\\b(extern)(\\s+)(alias)\\b', bygroups(Keyword, Whitespace, Keyword)), (words(('abstract', 'as', 'async', 'await', 'base', 'break', 'by', 'case', 'catch', 'checked', 'const', 'continue', 'default', 'delegate', 'do', 'else', 'enum', 'event', 'explicit', 'extern', 'false', 'finally', 'fixed', 'for', 'foreach', 'goto', 'if', 'implicit', 'in', 'interface', 'internal', 'is', 'let', 'lock', 'new', 'null', 'on', 'operator', 'out', 'override', 'params', 'private', 'protected', 'public', 'readonly', 'ref', 'return', 'sealed', 'sizeof', 'stackalloc', 'static', 'switch', 'this', 'throw', 'true', 'try', 'typeof', 'unchecked', 'unsafe', 'virtual', 'void', 'while', 'get', 'set', 'new', 'partial', 'yield', 'add', 'remove', 'value', 'alias', 'ascending', 'descending', 'from', 'group', 'into', 'orderby', 'select', 'thenby', 'where', 'join', 'equals', 'record', 'allows', 'and', 'init', 'managed', 'nameof', 'nint', 'not', 'notnull', 'nuint', 'or', 'scoped', 'unmanaged', 'when', 'with'), suffix='\\b'), Keyword), ('(file)(\\s+)(record|class|abstract|enum|new|sealed|static)\\b', bygroups(Keyword, Whitespace, Keyword)), ('(global)(::)', bygroups(Keyword, Punctuation)), ('(bool|byte|char|decimal|double|dynamic|float|int|long|object|sbyte|short|string|uint|ulong|ushort|var)\\b\\??', Keyword.Type), ('(class|struct)(\\s+)', bygroups(Keyword, Whitespace), 'class'), ('(namespace|using)(\\s+)', bygroups(Keyword, Whitespace), 'namespace'), (cs_ident, Name)], 'numbers_int': [('0[xX][0-9a-fA-F]+(([uU][lL]?)|[lL][uU]?)?', Number.Hex), ('0[bB][01]+(([uU][lL]?)|[lL][uU]?)?', Number.Bin), ('[0-9]+(([uU][lL]?)|[lL][uU]?)?', Number.Integer)], 'numbers_float': [('([0-9]+\\.[0-9]+([eE][+-]?[0-9]+)?[fFdDmM]?)|(\\.[0-9]+([eE][+-]?[0-9]+)?[fFdDmM]?)|([0-9]+([eE][+-]?[0-9]+)[fFdDmM]?)|([0-9]+[fFdDmM])', Number.Float)], 'numbers': [include('numbers_float'), include('numbers_int')], 'class': [(cs_ident, Name.Class, '#pop'), default('#pop')], 'namespace': [('(?=\\()', Text, '#pop'), ('(' + cs_ident + '|\\.)+', Name.Namespace, '#pop')]}
    
    def __init__(self, **options):
        level = get_choice_opt(options, 'unicodelevel', list(self.tokens), 'basic')
        if level not in self._all_tokens:
            self._tokens = self.__class__.process_tokendef(level)
        else:
            self._tokens = self._all_tokens[level]
        RegexLexer.__init__(self, **options)



class NemerleLexer(RegexLexer):
    """
    For Nemerle source code.

    Additional options accepted:

    `unicodelevel`
      Determines which Unicode characters this lexer allows for identifiers.
      The possible values are:

      * ``none`` -- only the ASCII letters and numbers are allowed. This
        is the fastest selection.
      * ``basic`` -- all Unicode characters from the specification except
        category ``Lo`` are allowed.
      * ``full`` -- all Unicode characters as specified in the C# specs
        are allowed.  Note that this means a considerable slowdown since the
        ``Lo`` category has more than 40,000 characters in it!

      The default value is ``basic``.
    """
    name = 'Nemerle'
    url = 'http://nemerle.org'
    aliases = ['nemerle']
    filenames = ['*.n']
    mimetypes = ['text/x-nemerle']
    version_added = '1.5'
    flags = re.MULTILINE | re.DOTALL
    levels = {'none': '@?[_a-zA-Z]\\w*', 'basic': '@?[_' + uni.combine('Lu', 'Ll', 'Lt', 'Lm', 'Nl') + ']' + '[' + uni.combine('Lu', 'Ll', 'Lt', 'Lm', 'Nl', 'Nd', 'Pc', 'Cf', 'Mn', 'Mc') + ']*', 'full': '@?(?:_|[^' + uni.allexcept('Lu', 'Ll', 'Lt', 'Lm', 'Lo', 'Nl') + '])' + '[^' + uni.allexcept('Lu', 'Ll', 'Lt', 'Lm', 'Lo', 'Nl', 'Nd', 'Pc', 'Cf', 'Mn', 'Mc') + ']*'}
    tokens = {}
    token_variants = True
    for (levelname, cs_ident) in levels.items():
        tokens[levelname] = {'root': [('^([ \\t]*)((?:' + cs_ident + '(?:\\[\\])?\\s+)+?)(' + cs_ident + ')(\\s*)(\\()', bygroups(Whitespace, using(this), Name.Function, Whitespace, Punctuation)), ('^(\\s*)(\\[.*?\\])', bygroups(Whitespace, Name.Attribute)), ('[^\\S\\n]+', Whitespace), ('(\\\\)(\\n)', bygroups(Text, Whitespace)), ('//.*?\\n', Comment.Single), ('/[*].*?[*]/', Comment.Multiline), ('\\n', Whitespace), ('(\\$)(\\s*)(")', bygroups(String, Whitespace, String), 'splice-string'), ('(\\$)(\\s*)(<#)', bygroups(String, Whitespace, String), 'splice-string2'), ('<#', String, 'recursive-string'), ('(<\\[)(\\s*)(' + cs_ident + ':)?', bygroups(Keyword, Whitespace, Keyword)), ('\\]\\>', Keyword), ('\\$' + cs_ident, Name), ('(\\$)(\\()', bygroups(Name, Punctuation), 'splice-string-content'), ('[~!%^&*()+=|\\[\\]:;,.<>/?-]', Punctuation), ('[{}]', Punctuation), ('@"(""|[^"])*"', String), ('"(\\\\\\\\|\\\\[^\\\\]|[^"\\\\\\n])*["\\n]', String), ("'\\\\.'|'[^\\\\]'", String.Char), ('0[xX][0-9a-fA-F]+[Ll]?', Number), ('[0-9](\\.[0-9]*)?([eE][+-][0-9]+)?[flFLdD]?', Number), ('(#)([ \\t]*)(if|endif|else|elif|define|undef|line|error|warning|region|endregion|pragma)\\b', bygroups(Comment.Preproc, Whitespace, Comment.Preproc), 'preproc'), ('\\b(extern)(\\s+)(alias)\\b', bygroups(Keyword, Whitespace, Keyword)), ('(abstract|and|as|base|catch|def|delegate|enum|event|extern|false|finally|fun|implements|interface|internal|is|macro|match|matches|module|mutable|new|null|out|override|params|partial|private|protected|public|ref|sealed|static|syntax|this|throw|true|try|type|typeof|virtual|volatile|when|where|with|assert|assert2|async|break|checked|continue|do|else|ensures|for|foreach|if|late|lock|new|nolate|otherwise|regexp|repeat|requires|return|surroundwith|unchecked|unless|using|while|yield)\\b', Keyword), ('(global)(::)', bygroups(Keyword, Punctuation)), ('(bool|byte|char|decimal|double|float|int|long|object|sbyte|short|string|uint|ulong|ushort|void|array|list)\\b\\??', Keyword.Type), ('(:>?)(\\s*)(' + cs_ident + '\\??)', bygroups(Punctuation, Whitespace, Keyword.Type)), ('(class|struct|variant|module)(\\s+)', bygroups(Keyword, Whitespace), 'class'), ('(namespace|using)(\\s+)', bygroups(Keyword, Whitespace), 'namespace'), (cs_ident, Name)], 'class': [(cs_ident, Name.Class, '#pop')], 'preproc': [('\\w+', Comment.Preproc), ('[ \\t]+', Whitespace), ('\\n', Whitespace, '#pop')], 'namespace': [('(?=\\()', Text, '#pop'), ('(' + cs_ident + '|\\.)+', Name.Namespace, '#pop')], 'splice-string': [('[^"$]', String), ('\\$' + cs_ident, Name), ('(\\$)(\\()', bygroups(Name, Punctuation), 'splice-string-content'), ('\\\\"', String), ('"', String, '#pop')], 'splice-string2': [('[^#<>$]', String), ('\\$' + cs_ident, Name), ('(\\$)(\\()', bygroups(Name, Punctuation), 'splice-string-content'), ('<#', String, '#push'), ('#>', String, '#pop')], 'recursive-string': [('[^#<>]', String), ('<#', String, '#push'), ('#>', String, '#pop')], 'splice-string-content': [('if|match', Keyword), ('[~!%^&*+=|\\[\\]:;,.<>/?-\\\\"$ ]', Punctuation), (cs_ident, Name), ('\\d+', Number), ('\\(', Punctuation, '#push'), ('\\)', Punctuation, '#pop')]}
    
    def __init__(self, **options):
        level = get_choice_opt(options, 'unicodelevel', list(self.tokens), 'basic')
        if level not in self._all_tokens:
            self._tokens = self.__class__.process_tokendef(level)
        else:
            self._tokens = self._all_tokens[level]
        RegexLexer.__init__(self, **options)
    
    def analyse_text(text):
        """Nemerle is quite similar to Python, but @if is relatively uncommon
        elsewhere."""
        result = 0
        if '@if' in text:
            result += 0.1
        return result



class BooLexer(RegexLexer):
    """
    For Boo source code.
    """
    name = 'Boo'
    url = 'https://github.com/boo-lang/boo'
    aliases = ['boo']
    filenames = ['*.boo']
    mimetypes = ['text/x-boo']
    version_added = ''
    tokens = {'root': [('\\s+', Whitespace), ('(#|//).*$', Comment.Single), ('/[*]', Comment.Multiline, 'comment'), ('[]{}:(),.;[]', Punctuation), ('(\\\\)(\\n)', bygroups(Text, Whitespace)), ('\\\\', Text), ('(in|is|and|or|not)\\b', Operator.Word), ('/(\\\\\\\\|\\\\[^\\\\]|[^/\\\\\\s])/', String.Regex), ('@/(\\\\\\\\|\\\\[^\\\\]|[^/\\\\])*/', String.Regex), ('=~|!=|==|<<|>>|[-+/*%=<>&^|]', Operator), ('(as|abstract|callable|constructor|destructor|do|import|enum|event|final|get|interface|internal|of|override|partial|private|protected|public|return|set|static|struct|transient|virtual|yield|super|and|break|cast|continue|elif|else|ensure|except|for|given|goto|if|in|is|isa|not|or|otherwise|pass|raise|ref|try|unless|when|while|from|as)\\b', Keyword), ('def(?=\\s+\\(.*?\\))', Keyword), ('(def)(\\s+)', bygroups(Keyword, Whitespace), 'funcname'), ('(class)(\\s+)', bygroups(Keyword, Whitespace), 'classname'), ('(namespace)(\\s+)', bygroups(Keyword, Whitespace), 'namespace'), ('(?<!\\.)(true|false|null|self|__eval__|__switch__|array|assert|checked|enumerate|filter|getter|len|lock|map|matrix|max|min|normalArrayIndexing|print|property|range|rawArrayIndexing|required|typeof|unchecked|using|yieldAll|zip)\\b', Name.Builtin), ('"""(\\\\\\\\|\\\\"|.*?)"""', String.Double), ('"(\\\\\\\\|\\\\[^\\\\]|[^"\\\\])*"', String.Double), ("'(\\\\\\\\|\\\\[^\\\\]|[^'\\\\])*'", String.Single), ('[a-zA-Z_]\\w*', Name), ('(\\d+\\.\\d*|\\d*\\.\\d+)([fF][+-]?[0-9]+)?', Number.Float), ('[0-9][0-9.]*(ms?|d|h|s)', Number), ('0\\d+', Number.Oct), ('0x[a-fA-F0-9]+', Number.Hex), ('\\d+L', Number.Integer.Long), ('\\d+', Number.Integer)], 'comment': [('/[*]', Comment.Multiline, '#push'), ('[*]/', Comment.Multiline, '#pop'), ('[^/*]', Comment.Multiline), ('[*/]', Comment.Multiline)], 'funcname': [('[a-zA-Z_]\\w*', Name.Function, '#pop')], 'classname': [('[a-zA-Z_]\\w*', Name.Class, '#pop')], 'namespace': [('[a-zA-Z_][\\w.]*', Name.Namespace, '#pop')]}



class VbNetLexer(RegexLexer):
    """
    For Visual Basic.NET source code.
    Also LibreOffice Basic, OpenOffice Basic, and StarOffice Basic.
    """
    name = 'VB.net'
    url = 'https://docs.microsoft.com/en-us/dotnet/visual-basic/'
    aliases = ['vb.net', 'vbnet', 'lobas', 'oobas', 'sobas', 'visual-basic', 'visualbasic']
    filenames = ['*.vb', '*.bas']
    mimetypes = ['text/x-vbnet', 'text/x-vba']
    version_added = ''
    uni_name = '[_' + uni.combine('Ll', 'Lt', 'Lm', 'Nl') + ']' + '[' + uni.combine('Ll', 'Lt', 'Lm', 'Nl', 'Nd', 'Pc', 'Cf', 'Mn', 'Mc') + ']*'
    flags = re.MULTILINE | re.IGNORECASE
    tokens = {'root': [('^\\s*<.*?>', Name.Attribute), ('\\s+', Whitespace), ('\\n', Whitespace), ('(rem\\b.*?)(\\n)', bygroups(Comment, Whitespace)), ("('.*?)(\\n)", bygroups(Comment, Whitespace)), ('#If\\s.*?\\sThen|#ElseIf\\s.*?\\sThen|#Else|#End\\s+If|#Const|#ExternalSource.*?\\n|#End\\s+ExternalSource|#Region.*?\\n|#End\\s+Region|#ExternalChecksum', Comment.Preproc), ('[(){}!#,.:]', Punctuation), ('(Option)(\\s+)(Strict|Explicit|Compare)(\\s+)(On|Off|Binary|Text)', bygroups(Keyword.Declaration, Whitespace, Keyword.Declaration, Whitespace, Keyword.Declaration)), (words(('AddHandler', 'Alias', 'ByRef', 'ByVal', 'Call', 'Case', 'Catch', 'CBool', 'CByte', 'CChar', 'CDate', 'CDec', 'CDbl', 'CInt', 'CLng', 'CObj', 'Continue', 'CSByte', 'CShort', 'CSng', 'CStr', 'CType', 'CUInt', 'CULng', 'CUShort', 'Declare', 'Default', 'Delegate', 'DirectCast', 'Do', 'Each', 'Else', 'ElseIf', 'EndIf', 'Erase', 'Error', 'Event', 'Exit', 'False', 'Finally', 'For', 'Friend', 'Get', 'Global', 'GoSub', 'GoTo', 'Handles', 'If', 'Implements', 'Inherits', 'Interface', 'Let', 'Lib', 'Loop', 'Me', 'MustInherit', 'MustOverride', 'MyBase', 'MyClass', 'Narrowing', 'New', 'Next', 'Not', 'Nothing', 'NotInheritable', 'NotOverridable', 'Of', 'On', 'Operator', 'Option', 'Optional', 'Overloads', 'Overridable', 'Overrides', 'ParamArray', 'Partial', 'Private', 'Protected', 'Public', 'RaiseEvent', 'ReadOnly', 'ReDim', 'RemoveHandler', 'Resume', 'Return', 'Select', 'Set', 'Shadows', 'Shared', 'Single', 'Static', 'Step', 'Stop', 'SyncLock', 'Then', 'Throw', 'To', 'True', 'Try', 'TryCast', 'Wend', 'Using', 'When', 'While', 'Widening', 'With', 'WithEvents', 'WriteOnly'), prefix='(?<!\\.)', suffix='\\b'), Keyword), ('(?<!\\.)End\\b', Keyword, 'end'), ('(?<!\\.)(Dim|Const)\\b', Keyword, 'dim'), ('(?<!\\.)(Function|Sub|Property)(\\s+)', bygroups(Keyword, Whitespace), 'funcname'), ('(?<!\\.)(Class|Structure|Enum)(\\s+)', bygroups(Keyword, Whitespace), 'classname'), ('(?<!\\.)(Module|Namespace|Imports)(\\s+)', bygroups(Keyword, Whitespace), 'namespace'), ('(?<!\\.)(Boolean|Byte|Char|Date|Decimal|Double|Integer|Long|Object|SByte|Short|Single|String|Variant|UInteger|ULong|UShort)\\b', Keyword.Type), ('(?<!\\.)(AddressOf|And|AndAlso|As|GetType|In|Is|IsNot|Like|Mod|Or|OrElse|TypeOf|Xor)\\b', Operator.Word), ('&=|[*]=|/=|\\\\=|\\^=|\\+=|-=|<<=|>>=|<<|>>|:=|<=|>=|<>|[-&*/\\\\^+=<>\\[\\]]', Operator), ('"', String, 'string'), ('(_)(\\n)', bygroups(Text, Whitespace)), (uni_name + '[%&@!#$]?', Name), ('#.*?#', Literal.Date), ('(\\d+\\.\\d*|\\d*\\.\\d+)(F[+-]?[0-9]+)?', Number.Float), ('\\d+([SILDFR]|US|UI|UL)?', Number.Integer), ('&H[0-9a-f]+([SILDFR]|US|UI|UL)?', Number.Integer), ('&O[0-7]+([SILDFR]|US|UI|UL)?', Number.Integer)], 'string': [('""', String), ('"C?', String, '#pop'), ('[^"]+', String)], 'dim': [(uni_name, Name.Variable, '#pop'), default('#pop')], 'funcname': [(uni_name, Name.Function, '#pop')], 'classname': [(uni_name, Name.Class, '#pop')], 'namespace': [(uni_name, Name.Namespace), ('\\.', Name.Namespace), default('#pop')], 'end': [('\\s+', Whitespace), ('(Function|Sub|Property|Class|Structure|Enum|Module|Namespace)\\b', Keyword, '#pop'), default('#pop')]}
    
    def analyse_text(text):
        if re.search('^\\s*(#If|Module|Namespace)', text, re.MULTILINE):
            return 0.5



class GenericAspxLexer(RegexLexer):
    """
    Lexer for ASP.NET pages.
    """
    name = 'aspx-gen'
    filenames = []
    mimetypes = []
    url = 'https://dotnet.microsoft.com/en-us/apps/aspnet'
    flags = re.DOTALL
    tokens = {'root': [('(<%[@=#]?)(.*?)(%>)', bygroups(Name.Tag, Other, Name.Tag)), ('(<script.*?>)(.*?)(</script>)', bygroups(using(XmlLexer), Other, using(XmlLexer))), ('(.+?)(?=<)', using(XmlLexer)), ('.+', using(XmlLexer))]}



class CSharpAspxLexer(DelegatingLexer):
    """
    Lexer for highlighting C# within ASP.NET pages.
    """
    name = 'aspx-cs'
    aliases = ['aspx-cs']
    filenames = ['*.aspx', '*.asax', '*.ascx', '*.ashx', '*.asmx', '*.axd']
    mimetypes = []
    url = 'https://dotnet.microsoft.com/en-us/apps/aspnet'
    version_added = ''
    
    def __init__(self, **options):
        super().__init__(CSharpLexer, GenericAspxLexer, **options)
    
    def analyse_text(text):
        if re.search('Page\\s*Language="C#"', text, re.I) is not None:
            return 0.2
        elif re.search('script[^>]+language=["\\\']C#', text, re.I) is not None:
            return 0.15



class VbNetAspxLexer(DelegatingLexer):
    """
    Lexer for highlighting Visual Basic.net within ASP.NET pages.
    """
    name = 'aspx-vb'
    aliases = ['aspx-vb']
    filenames = ['*.aspx', '*.asax', '*.ascx', '*.ashx', '*.asmx', '*.axd']
    mimetypes = []
    url = 'https://dotnet.microsoft.com/en-us/apps/aspnet'
    version_added = ''
    
    def __init__(self, **options):
        super().__init__(VbNetLexer, GenericAspxLexer, **options)
    
    def analyse_text(text):
        if re.search('Page\\s*Language="Vb"', text, re.I) is not None:
            return 0.2
        elif re.search('script[^>]+language=["\\\']vb', text, re.I) is not None:
            return 0.15



class FSharpLexer(RegexLexer):
    """
    For the F# language (version 3.0).
    """
    name = 'F#'
    url = 'https://fsharp.org/'
    aliases = ['fsharp', 'f#']
    filenames = ['*.fs', '*.fsi', '*.fsx']
    mimetypes = ['text/x-fsharp']
    version_added = '1.5'
    keywords = ['abstract', 'as', 'assert', 'base', 'begin', 'class', 'default', 'delegate', 'do!', 'do', 'done', 'downcast', 'downto', 'elif', 'else', 'end', 'exception', 'extern', 'false', 'finally', 'for', 'function', 'fun', 'global', 'if', 'inherit', 'inline', 'interface', 'internal', 'in', 'lazy', 'let!', 'let', 'match', 'member', 'module', 'mutable', 'namespace', 'new', 'null', 'of', 'open', 'override', 'private', 'public', 'rec', 'return!', 'return', 'select', 'static', 'struct', 'then', 'to', 'true', 'try', 'type', 'upcast', 'use!', 'use', 'val', 'void', 'when', 'while', 'with', 'yield!', 'yield']
    keywords += ['atomic', 'break', 'checked', 'component', 'const', 'constraint', 'constructor', 'continue', 'eager', 'event', 'external', 'fixed', 'functor', 'include', 'method', 'mixin', 'object', 'parallel', 'process', 'protected', 'pure', 'sealed', 'tailcall', 'trait', 'virtual', 'volatile']
    keyopts = ['!=', '#', '&&', '&', '\\(', '\\)', '\\*', '\\+', ',', '-\\.', '->', '-', '\\.\\.', '\\.', '::', ':=', ':>', ':', ';;', ';', '<-', '<\\]', '<', '>\\]', '>', '\\?\\?', '\\?', '\\[<', '\\[\\|', '\\[', '\\]', '_', '`', '\\{', '\\|\\]', '\\|', '\\}', '~', '<@@', '<@', '=', '@>', '@@>']
    operators = '[!$%&*+\\./:<=>?@^|~-]'
    word_operators = ['and', 'or', 'not']
    prefix_syms = '[!?~]'
    infix_syms = '[=<>@^|&+\\*/$%-]'
    primitives = ['sbyte', 'byte', 'char', 'nativeint', 'unativeint', 'float32', 'single', 'float', 'double', 'int8', 'uint8', 'int16', 'uint16', 'int32', 'uint32', 'int64', 'uint64', 'decimal', 'unit', 'bool', 'string', 'list', 'exn', 'obj', 'enum']
    tokens = {'escape-sequence': [('\\\\[\\\\"\\\'ntbrafv]', String.Escape), ('\\\\[0-9]{3}', String.Escape), ('\\\\u[0-9a-fA-F]{4}', String.Escape), ('\\\\U[0-9a-fA-F]{8}', String.Escape)], 'root': [('\\s+', Whitespace), ('\\(\\)|\\[\\]', Name.Builtin.Pseudo), ("\\b(?<!\\.)([A-Z][\\w\\']*)(?=\\s*\\.)", Name.Namespace, 'dotted'), ("\\b([A-Z][\\w\\']*)", Name), ('(///.*?)(\\n)', bygroups(String.Doc, Whitespace)), ('(//.*?)(\\n)', bygroups(Comment.Single, Whitespace)), ('\\(\\*(?!\\))', Comment, 'comment'), ('@"', String, 'lstring'), ('"""', String, 'tqs'), ('"', String, 'string'), ('\\b(open|module)(\\s+)([\\w.]+)', bygroups(Keyword, Whitespace, Name.Namespace)), ('\\b(let!?)(\\s+)(\\w+)', bygroups(Keyword, Whitespace, Name.Variable)), ('\\b(type)(\\s+)(\\w+)', bygroups(Keyword, Whitespace, Name.Class)), ('\\b(member|override)(\\s+)(\\w+)(\\.)(\\w+)', bygroups(Keyword, Whitespace, Name, Punctuation, Name.Function)), ('\\b({})\\b'.format('|'.join(keywords)), Keyword), ('``([^`\\n\\r\\t]|`[^`\\n\\r\\t])+``', Name), ('({})'.format('|'.join(keyopts)), Operator), (f'({infix_syms}|{prefix_syms})?{operators}', Operator), ('\\b({})\\b'.format('|'.join(word_operators)), Operator.Word), ('\\b({})\\b'.format('|'.join(primitives)), Keyword.Type), ('(#)([ \\t]*)(if|endif|else|line|nowarn|light|\\d+)\\b(.*?)(\\n)', bygroups(Comment.Preproc, Whitespace, Comment.Preproc, Comment.Preproc, Whitespace)), ("[^\\W\\d][\\w']*", Name), ('\\d[\\d_]*[uU]?[yslLnQRZINGmM]?', Number.Integer), ('0[xX][\\da-fA-F][\\da-fA-F_]*[uU]?[yslLn]?[fF]?', Number.Hex), ('0[oO][0-7][0-7_]*[uU]?[yslLn]?', Number.Oct), ('0[bB][01][01_]*[uU]?[yslLn]?', Number.Bin), ('-?\\d[\\d_]*(.[\\d_]*)?([eE][+\\-]?\\d[\\d_]*)[fFmM]?', Number.Float), ('\'(?:(\\\\[\\\\\\"\'ntbr ])|(\\\\[0-9]{3})|(\\\\x[0-9a-fA-F]{2}))\'B?', String.Char), ("'.'", String.Char), ("'", Keyword), ('@?"', String.Double, 'string'), ("[~?][a-z][\\w\\']*:", Name.Variable)], 'dotted': [('\\s+', Whitespace), ('\\.', Punctuation), ("[A-Z][\\w\\']*(?=\\s*\\.)", Name.Namespace), ("[A-Z][\\w\\']*", Name, '#pop'), ("[a-z_][\\w\\']*", Name, '#pop'), default('#pop')], 'comment': [('[^(*)@"]+', Comment), ('\\(\\*', Comment, '#push'), ('\\*\\)', Comment, '#pop'), ('@"', String, 'lstring'), ('"""', String, 'tqs'), ('"', String, 'string'), ('[(*)@]', Comment)], 'string': [('[^\\\\"]+', String), include('escape-sequence'), ('\\\\\\n', String), ('\\n', String), ('"B?', String, '#pop')], 'lstring': [('[^"]+', String), ('\\n', String), ('""', String), ('"B?', String, '#pop')], 'tqs': [('[^"]+', String), ('\\n', String), ('"""B?', String, '#pop'), ('"', String)]}
    
    def analyse_text(text):
        """F# doesn't have that many unique features -- |> and <| are weak
        indicators."""
        result = 0
        if '|>' in text:
            result += 0.05
        if '<|' in text:
            result += 0.05
        return result



class XppLexer(RegexLexer):
    """
    For X++ source code. This is based loosely on the CSharpLexer
    """
    name = 'X++'
    url = 'https://learn.microsoft.com/en-us/dynamics365/fin-ops-core/dev-itpro/dev-ref/xpp-language-reference'
    aliases = ['xpp', 'x++']
    filenames = ['*.xpp']
    version_added = '2.15'
    flags = re.MULTILINE
    XPP_CHARS = '@?(?:_|[^' + uni.allexcept('Lu', 'Ll', 'Lt', 'Lm', 'Lo', 'Nl') + '])' + '[^' + uni.allexcept('Lu', 'Ll', 'Lt', 'Lm', 'Lo', 'Nl', 'Nd', 'Pc', 'Cf', 'Mn', 'Mc') + ']*'
    XPP_CHARS = XPP_CHARS.replace('\x00', '\x01')
    OPERATORS = ('<=', '>=', '+=', '-=', '*=', '/=', '!=', '==', '&&', '||', '>>', '<<', '++', '--', '+', '-', '*', '/', '%', '&', '|', '^', '<', '>', '?', '!', '~', '=')
    KEYWORDS = ('abstract', 'anytype', 'as', 'async', 'asc', 'at', 'avg', 'break', 'breakpoint', 'by', 'byref', 'case', 'catch', 'changecompany', 'client', 'container', 'continue', 'count', 'crosscompany', 'default', 'delegate', 'delete_from', 'desc', 'display', 'div', 'do', 'edit', 'else', 'element', 'eventhandler', 'exists', 'false', 'final', 'firstfast', 'firstonly', 'firstonly10', 'firstonly100', 'firstonly1000', 'flush', 'for', 'forceliterals', 'forcenestedloop', 'forceplaceholders', 'forceselectorder', 'forupdate', 'from', 'group', 'if', 'insert_recordset', 'interface', 'is', 'join', 'like', 'maxof', 'minof', 'mod', 'new', 'next', 'nofetch', 'notexists', 'null', 'optimisticlock', 'order', 'outer', 'pause', 'pessimisticlock', 'print', 'private', 'protected', 'public', 'repeatableread', 'retry', 'return', 'reverse', 'select', 'server', 'setting', 'static', 'sum', 'super', 'switch', 'tablelock', 'this', 'throw', 'true', 'try', 'ttsabort', 'ttsbegin', 'ttscommit', 'update_recordset', 'validtimestate', 'void', 'where', 'while', 'window')
    RUNTIME_FUNCTIONS = ('_duration', 'abs', 'acos', 'any2Date', 'any2Enum', 'any2Guid', 'any2Int', 'any2Int64', 'any2Real', 'any2Str', 'anytodate', 'anytoenum', 'anytoguid', 'anytoint', 'anytoint64', 'anytoreal', 'anytostr', 'asin', 'atan', 'beep', 'cTerm', 'char2Num', 'classIdGet', 'corrFlagGet', 'corrFlagSet', 'cos', 'cosh', 'curExt', 'curUserId', 'date2Num', 'date2Str', 'datetime2Str', 'dayName', 'dayOfMth', 'dayOfWk', 'dayOfYr', 'ddb', 'decRound', 'dg', 'dimOf', 'endMth', 'enum2str', 'exp', 'exp10', 'fV', 'fieldId2Name', 'fieldId2PName', 'fieldName2Id', 'frac', 'funcName', 'getCurrentPartition', 'getCurrentPartitionRecId', 'getPrefix', 'guid2Str', 'idg', 'indexId2Name', 'indexName2Id', 'int2Str', 'int642Str', 'intvMax', 'intvName', 'intvNo', 'intvNorm', 'log10', 'logN', 'match', 'max', 'min', 'mkDate', 'mthName', 'mthOfYr', 'newGuid', 'nextMth', 'nextQtr', 'nextYr', 'num2Char', 'num2Date', 'num2Str', 'pmt', 'power', 'prevMth', 'prevQtr', 'prevYr', 'prmIsDefault', 'pt', 'pv', 'rate', 'refPrintAll', 'round', 'runAs', 'sessionId', 'setPrefix', 'sin', 'sinh', 'sleep', 'sln', 'str2Date', 'str2Datetime', 'str2Enum', 'str2Guid', 'str2Int', 'str2Int64', 'str2Num', 'str2Time', 'strAlpha', 'strCmp', 'strColSeq', 'strDel', 'strFind', 'strFmt', 'strIns', 'strKeep', 'strLTrim', 'strLen', 'strLine', 'strLwr', 'strNFind', 'strPoke', 'strPrompt', 'strRTrim', 'strRem', 'strRep', 'strScan', 'strUpr', 'subStr', 'syd', 'systemDateGet', 'systemDateSet', 'tableId2Name', 'tableId2PName', 'tableName2Id', 'tan', 'tanh', 'term', 'time2Str', 'timeNow', 'today', 'trunc', 'typeOf', 'uint2Str', 'wkOfYr', 'year')
    COMPILE_FUNCTIONS = ('attributeStr', 'classNum', 'classStr', 'configurationKeyNum', 'configurationKeyStr', 'dataEntityDataSourceStr', 'delegateStr', 'dimensionHierarchyLevelStr', 'dimensionHierarchyStr', 'dimensionReferenceStr', 'dutyStr', 'enumCnt', 'enumLiteralStr', 'enumNum', 'enumStr', 'extendedTypeNum', 'extendedTypeStr', 'fieldNum', 'fieldPName', 'fieldStr', 'formControlStr', 'formDataFieldStr', 'formDataSourceStr', 'formMethodStr', 'formStr', 'identifierStr', 'indexNum', 'indexStr', 'licenseCodeNum', 'licenseCodeStr', 'literalStr', 'maxDate', 'maxInt', 'measureStr', 'measurementStr', 'menuItemActionStr', 'menuItemDisplayStr', 'menuItemOutputStr', 'menuStr', 'methodStr', 'minInt', 'privilegeStr', 'queryDatasourceStr', 'queryMethodStr', 'queryStr', 'reportStr', 'resourceStr', 'roleStr', 'ssrsReportStr', 'staticDelegateStr', 'staticMethodStr', 'tableCollectionStr', 'tableFieldGroupStr', 'tableMethodStr', 'tableNum', 'tablePName', 'tableStaticMethodStr', 'tableStr', 'tileStr', 'varStr', 'webActionItemStr', 'webDisplayContentItemStr', 'webFormStr', 'webMenuStr', 'webOutputContentItemStr', 'webReportStr', 'webSiteTempStr', 'webStaticFileStr', 'webUrlItemStr', 'webWebPartStr', 'webletItemStr', 'webpageDefStr', 'websiteDefStr', 'workflowApprovalStr', 'workflowCategoryStr', 'workflowTaskStr', 'workflowTypeStr')
    tokens = {}
    tokens = {'root': [('(\\s*)\\b(else|if)\\b([^\\n])', bygroups(Whitespace, Keyword, using(this))), ('^([ \\t]*)((?:' + XPP_CHARS + '(?:\\[\\])?\\s+)+?)(' + XPP_CHARS + ')(\\s*)(\\()', bygroups(Whitespace, using(this), Name.Function, Whitespace, Punctuation)), ('^(\\s*)(\\[)([^\\n]*?)(\\])', bygroups(Whitespace, Name.Attribute, Name.Variable.Class, Name.Attribute)), ('[^\\S\\n]+', Whitespace), ('(\\\\)(\\n)', bygroups(Text, Whitespace)), ('//[^\\n]*?\\n', Comment.Single), ('/[*][^\\n]*?[*]/', Comment.Multiline), ('\\n', Whitespace), (words(OPERATORS), Operator), ('=~|!=|==|<<|>>|[-+/*%=<>&^|]', Operator), ('[()\\[\\];:,.#@]', Punctuation), ('[{}]', Punctuation), ('@"(""|[^"])*"', String), ('\\$?"(\\\\\\\\|\\\\[^\\\\]|[^"\\\\\\n])*["\\n]', String), ("'\\\\.'|'[^\\\\]'", String.Char), ('[0-9]+(\\.[0-9]*)?([eE][+-][0-9]+)?[flFLdD]?|0[xX][0-9a-fA-F]+[Ll]?', Number), (words(KEYWORDS, suffix='\\b'), Keyword), ('(boolean|int|int64|str|real|guid|date)\\b\\??', Keyword.Type), ('(class|struct|extends|implements)(\\s+)', bygroups(Keyword, Whitespace), 'class'), ('(' + XPP_CHARS + ')(::)', bygroups(Name.Variable.Class, Punctuation)), ('(\\s*)(\\w+)(\\s+\\w+(,|=)?[^\\n]*;)', bygroups(Whitespace, Name.Variable.Class, using(this))), ('(fieldNum\\()(' + XPP_CHARS + ')(\\s*,\\s*)(' + XPP_CHARS + ')(\\s*\\))', bygroups(using(this), Name.Variable.Class, using(this), Name.Property, using(this))), ('(tableNum\\()(' + XPP_CHARS + ')(\\s*\\))', bygroups(using(this), Name.Variable.Class, using(this))), (words(RUNTIME_FUNCTIONS, suffix='(?=\\()'), Name.Function.Magic), (words(COMPILE_FUNCTIONS, suffix='(?=\\()'), Name.Function.Magic), (XPP_CHARS, Name)], 'class': [(XPP_CHARS, Name.Class, '#pop'), default('#pop')], 'namespace': [('(?=\\()', Text, '#pop'), ('(' + XPP_CHARS + '|\\.)+', Name.Namespace, '#pop')]}


