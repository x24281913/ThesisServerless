"""
    pygments.lexers.parsers
    ~~~~~~~~~~~~~~~~~~~~~~~

    Lexers for parser generators.

    :copyright: Copyright 2006-present by the Pygments team, see AUTHORS.
    :license: BSD, see LICENSE for details.
"""

import re
from pygments.lexer import RegexLexer, DelegatingLexer, include, bygroups, using
from pygments.token import Punctuation, Other, Text, Comment, Operator, Keyword, Name, String, Number, Whitespace
from pygments.lexers.jvm import JavaLexer
from pygments.lexers.c_cpp import CLexer, CppLexer
from pygments.lexers.objective import ObjectiveCLexer
from pygments.lexers.d import DLexer
from pygments.lexers.dotnet import CSharpLexer
from pygments.lexers.ruby import RubyLexer
from pygments.lexers.python import PythonLexer
from pygments.lexers.perl import PerlLexer
__all__ = ['RagelLexer', 'RagelEmbeddedLexer', 'RagelCLexer', 'RagelDLexer', 'RagelCppLexer', 'RagelObjectiveCLexer', 'RagelRubyLexer', 'RagelJavaLexer', 'AntlrLexer', 'AntlrPythonLexer', 'AntlrPerlLexer', 'AntlrRubyLexer', 'AntlrCppLexer', 'AntlrCSharpLexer', 'AntlrObjectiveCLexer', 'AntlrJavaLexer', 'AntlrActionScriptLexer', 'TreetopLexer', 'EbnfLexer']


class RagelLexer(RegexLexer):
    """A pure `Ragel <www.colm.net/open-source/ragel>`_ lexer.

    Use this for fragments of Ragel.  For ``.rl`` files, use
    :class:`RagelEmbeddedLexer` instead (or one of the language-specific
    subclasses).
    """
    name = 'Ragel'
    url = 'http://www.colm.net/open-source/ragel/'
    aliases = ['ragel']
    filenames = []
    version_added = '1.1'
    tokens = {'whitespace': [('\\s+', Whitespace)], 'comments': [('\\#.*$', Comment)], 'keywords': [('(access|action|alphtype)\\b', Keyword), ('(getkey|write|machine|include)\\b', Keyword), ('(any|ascii|extend|alpha|digit|alnum|lower|upper)\\b', Keyword), ('(xdigit|cntrl|graph|print|punct|space|zlen|empty)\\b', Keyword)], 'numbers': [('0x[0-9A-Fa-f]+', Number.Hex), ('[+-]?[0-9]+', Number.Integer)], 'literals': [('"(\\\\\\\\|\\\\[^\\\\]|[^"\\\\])*"', String.Double), ("'(\\\\\\\\|\\\\[^\\\\]|[^'\\\\])*'", String.Single), ('\\[(\\\\\\\\|\\\\[^\\\\]|[^\\\\\\]])*\\]', String), ('/(?!\\*)(\\\\\\\\|\\\\[^\\\\]|[^/\\\\])*/', String.Regex)], 'identifiers': [('[a-zA-Z_]\\w*', Name.Variable)], 'operators': [(',', Operator), ('\\||&|--?', Operator), ('\\.|<:|:>>?', Operator), (':', Operator), ('->', Operator), ('(>|\\$|%|<|@|<>)(/|eof\\b)', Operator), ('(>|\\$|%|<|@|<>)(!|err\\b)', Operator), ('(>|\\$|%|<|@|<>)(\\^|lerr\\b)', Operator), ('(>|\\$|%|<|@|<>)(~|to\\b)', Operator), ('(>|\\$|%|<|@|<>)(\\*|from\\b)', Operator), ('>|@|\\$|%', Operator), ('\\*|\\?|\\+|\\{[0-9]*,[0-9]*\\}', Operator), ('!|\\^', Operator), ('\\(|\\)', Operator)], 'root': [include('literals'), include('whitespace'), include('comments'), include('keywords'), include('numbers'), include('identifiers'), include('operators'), ('\\{', Punctuation, 'host'), ('=', Operator), (';', Punctuation)], 'host': [('(' + '|'.join(('[^{}\\\'"/#]+', '[^\\\\]\\\\[{}]', '"(\\\\\\\\|\\\\[^\\\\]|[^"\\\\])*"', "'(\\\\\\\\|\\\\[^\\\\]|[^'\\\\])*'", '//.*$\\n?', '/\\*(.|\\n)*?\\*/', '\\#.*$\\n?', '/(?!\\*)(\\\\\\\\|\\\\[^\\\\]|[^/\\\\])*/', '/')) + ')+', Other), ('\\{', Punctuation, '#push'), ('\\}', Punctuation, '#pop')]}



class RagelEmbeddedLexer(RegexLexer):
    """
    A lexer for Ragel embedded in a host language file.

    This will only highlight Ragel statements. If you want host language
    highlighting then call the language-specific Ragel lexer.
    """
    name = 'Embedded Ragel'
    aliases = ['ragel-em']
    filenames = ['*.rl']
    url = 'http://www.colm.net/open-source/ragel/'
    version_added = '1.1'
    tokens = {'root': [('(' + '|'.join(('[^%\\\'"/#]+', '%(?=[^%]|$)', '"(\\\\\\\\|\\\\[^\\\\]|[^"\\\\])*"', "'(\\\\\\\\|\\\\[^\\\\]|[^'\\\\])*'", '/\\*(.|\\n)*?\\*/', '//.*$\\n?', '\\#.*$\\n?', '/(?!\\*)(\\\\\\\\|\\\\[^\\\\]|[^/\\\\])*/', '/')) + ')+', Other), ('(%%)(?![{%])(.*)($|;)(\\n?)', bygroups(Punctuation, using(RagelLexer), Punctuation, Text)), ('(%%%%|%%)\\{', Punctuation, 'multi-line-fsm')], 'multi-line-fsm': [('(' + '|'.join(('(' + '|'.join(('[^}\\\'"\\[/#]', '\\}(?=[^%]|$)', '\\}%(?=[^%]|$)', '[^\\\\]\\\\[{}]', '(>|\\$|%|<|@|<>)/', '/(?!\\*)(\\\\\\\\|\\\\[^\\\\]|[^/\\\\])*/\\*', '/(?=[^/*]|$)')) + ')+', '"(\\\\\\\\|\\\\[^\\\\]|[^"\\\\])*"', "'(\\\\\\\\|\\\\[^\\\\]|[^'\\\\])*'", '\\[(\\\\\\\\|\\\\[^\\\\]|[^\\]\\\\])*\\]', '/\\*(.|\\n)*?\\*/', '//.*$\\n?', '\\#.*$\\n?')) + ')+', using(RagelLexer)), ('\\}%%', Punctuation, '#pop')]}
    
    def analyse_text(text):
        return '@LANG: indep' in text



class RagelRubyLexer(DelegatingLexer):
    """
    A lexer for Ragel in a Ruby host file.
    """
    name = 'Ragel in Ruby Host'
    aliases = ['ragel-ruby', 'ragel-rb']
    filenames = ['*.rl']
    url = 'http://www.colm.net/open-source/ragel/'
    version_added = '1.1'
    
    def __init__(self, **options):
        super().__init__(RubyLexer, RagelEmbeddedLexer, **options)
    
    def analyse_text(text):
        return '@LANG: ruby' in text



class RagelCLexer(DelegatingLexer):
    """
    A lexer for Ragel in a C host file.
    """
    name = 'Ragel in C Host'
    aliases = ['ragel-c']
    filenames = ['*.rl']
    url = 'http://www.colm.net/open-source/ragel/'
    version_added = '1.1'
    
    def __init__(self, **options):
        super().__init__(CLexer, RagelEmbeddedLexer, **options)
    
    def analyse_text(text):
        return '@LANG: c' in text



class RagelDLexer(DelegatingLexer):
    """
    A lexer for Ragel in a D host file.
    """
    name = 'Ragel in D Host'
    aliases = ['ragel-d']
    filenames = ['*.rl']
    url = 'http://www.colm.net/open-source/ragel/'
    version_added = '1.1'
    
    def __init__(self, **options):
        super().__init__(DLexer, RagelEmbeddedLexer, **options)
    
    def analyse_text(text):
        return '@LANG: d' in text



class RagelCppLexer(DelegatingLexer):
    """
    A lexer for Ragel in a C++ host file.
    """
    name = 'Ragel in CPP Host'
    aliases = ['ragel-cpp']
    filenames = ['*.rl']
    url = 'http://www.colm.net/open-source/ragel/'
    version_added = '1.1'
    
    def __init__(self, **options):
        super().__init__(CppLexer, RagelEmbeddedLexer, **options)
    
    def analyse_text(text):
        return '@LANG: c++' in text



class RagelObjectiveCLexer(DelegatingLexer):
    """
    A lexer for Ragel in an Objective C host file.
    """
    name = 'Ragel in Objective C Host'
    aliases = ['ragel-objc']
    filenames = ['*.rl']
    url = 'http://www.colm.net/open-source/ragel/'
    version_added = '1.1'
    
    def __init__(self, **options):
        super().__init__(ObjectiveCLexer, RagelEmbeddedLexer, **options)
    
    def analyse_text(text):
        return '@LANG: objc' in text



class RagelJavaLexer(DelegatingLexer):
    """
    A lexer for Ragel in a Java host file.
    """
    name = 'Ragel in Java Host'
    aliases = ['ragel-java']
    filenames = ['*.rl']
    url = 'http://www.colm.net/open-source/ragel/'
    version_added = '1.1'
    
    def __init__(self, **options):
        super().__init__(JavaLexer, RagelEmbeddedLexer, **options)
    
    def analyse_text(text):
        return '@LANG: java' in text



class AntlrLexer(RegexLexer):
    """
    Generic ANTLR Lexer.
    Should not be called directly, instead
    use DelegatingLexer for your target language.
    """
    name = 'ANTLR'
    aliases = ['antlr']
    filenames = []
    url = 'https://www.antlr.org'
    version_added = '1.1'
    _id = '[A-Za-z]\\w*'
    _TOKEN_REF = '[A-Z]\\w*'
    _RULE_REF = '[a-z]\\w*'
    _STRING_LITERAL = "\\'(?:\\\\\\\\|\\\\\\'|[^\\']*)\\'"
    _INT = '[0-9]+'
    tokens = {'whitespace': [('\\s+', Whitespace)], 'comments': [('//.*$', Comment), ('/\\*(.|\\n)*?\\*/', Comment)], 'root': [include('whitespace'), include('comments'), ('(lexer|parser|tree)?(\\s*)(grammar\\b)(\\s*)(' + _id + ')(;)', bygroups(Keyword, Whitespace, Keyword, Whitespace, Name.Class, Punctuation)), ('options\\b', Keyword, 'options'), ('tokens\\b', Keyword, 'tokens'), ('(scope)(\\s*)(' + _id + ')(\\s*)(\\{)', bygroups(Keyword, Whitespace, Name.Variable, Whitespace, Punctuation), 'action'), ('(catch|finally)\\b', Keyword, 'exception'), ('(@' + _id + ')(\\s*)(::)?(\\s*)(' + _id + ')(\\s*)(\\{)', bygroups(Name.Label, Whitespace, Punctuation, Whitespace, Name.Label, Whitespace, Punctuation), 'action'), ('((?:protected|private|public|fragment)\\b)?(\\s*)(' + _id + ')(!)?', bygroups(Keyword, Whitespace, Name.Label, Punctuation), ('rule-alts', 'rule-prelims'))], 'exception': [('\\n', Whitespace, '#pop'), ('\\s', Whitespace), include('comments'), ('\\[', Punctuation, 'nested-arg-action'), ('\\{', Punctuation, 'action')], 'rule-prelims': [include('whitespace'), include('comments'), ('returns\\b', Keyword), ('\\[', Punctuation, 'nested-arg-action'), ('\\{', Punctuation, 'action'), ('(throws)(\\s+)(' + _id + ')', bygroups(Keyword, Whitespace, Name.Label)), ('(,)(\\s*)(' + _id + ')', bygroups(Punctuation, Whitespace, Name.Label)), ('options\\b', Keyword, 'options'), ('(scope)(\\s+)(\\{)', bygroups(Keyword, Whitespace, Punctuation), 'action'), ('(scope)(\\s+)(' + _id + ')(\\s*)(;)', bygroups(Keyword, Whitespace, Name.Label, Whitespace, Punctuation)), ('(@' + _id + ')(\\s*)(\\{)', bygroups(Name.Label, Whitespace, Punctuation), 'action'), (':', Punctuation, '#pop')], 'rule-alts': [include('whitespace'), include('comments'), ('options\\b', Keyword, 'options'), (':', Punctuation), ('"(\\\\\\\\|\\\\[^\\\\]|[^"\\\\])*"', String.Double), ("'(\\\\\\\\|\\\\[^\\\\]|[^'\\\\])*'", String.Single), ('<<([^>]|>[^>])>>', String), ('\\$?[A-Z_]\\w*', Name.Constant), ('\\$?[a-z_]\\w*', Name.Variable), ('(\\+|\\||->|=>|=|\\(|\\)|\\.\\.|\\.|\\?|\\*|\\^|!|\\#|~)', Operator), (',', Punctuation), ('\\[', Punctuation, 'nested-arg-action'), ('\\{', Punctuation, 'action'), (';', Punctuation, '#pop')], 'tokens': [include('whitespace'), include('comments'), ('\\{', Punctuation), ('(' + _TOKEN_REF + ')(\\s*)(=)?(\\s*)(' + _STRING_LITERAL + ')?(\\s*)(;)', bygroups(Name.Label, Whitespace, Punctuation, Whitespace, String, Whitespace, Punctuation)), ('\\}', Punctuation, '#pop')], 'options': [include('whitespace'), include('comments'), ('\\{', Punctuation), ('(' + _id + ')(\\s*)(=)(\\s*)(' + '|'.join((_id, _STRING_LITERAL, _INT, '\\*')) + ')(\\s*)(;)', bygroups(Name.Variable, Whitespace, Punctuation, Whitespace, Text, Whitespace, Punctuation)), ('\\}', Punctuation, '#pop')], 'action': [('(' + '|'.join(('[^${}\\\'"/\\\\]+', '"(\\\\\\\\|\\\\[^\\\\]|[^"\\\\])*"', "'(\\\\\\\\|\\\\[^\\\\]|[^'\\\\])*'", '//.*$\\n?', '/\\*(.|\\n)*?\\*/', '/(?!\\*)(\\\\\\\\|\\\\[^\\\\]|[^/\\\\])*/', '\\\\(?!%)', '/')) + ')+', Other), ('(\\\\)(%)', bygroups(Punctuation, Other)), ('(\\$[a-zA-Z]+)(\\.?)(text|value)?', bygroups(Name.Variable, Punctuation, Name.Property)), ('\\{', Punctuation, '#push'), ('\\}', Punctuation, '#pop')], 'nested-arg-action': [('(' + '|'.join(('[^$\\[\\]\\\'"/]+', '"(\\\\\\\\|\\\\[^\\\\]|[^"\\\\])*"', "'(\\\\\\\\|\\\\[^\\\\]|[^'\\\\])*'", '//.*$\\n?', '/\\*(.|\\n)*?\\*/', '/(?!\\*)(\\\\\\\\|\\\\[^\\\\]|[^/\\\\])*/', '/')) + ')+', Other), ('\\[', Punctuation, '#push'), ('\\]', Punctuation, '#pop'), ('(\\$[a-zA-Z]+)(\\.?)(text|value)?', bygroups(Name.Variable, Punctuation, Name.Property)), ('(\\\\\\\\|\\\\\\]|\\\\\\[|[^\\[\\]])+', Other)]}
    
    def analyse_text(text):
        return re.search('^\\s*grammar\\s+[a-zA-Z0-9]+\\s*;', text, re.M)



class AntlrCppLexer(DelegatingLexer):
    """
    ANTLR with C++ Target
    """
    name = 'ANTLR With CPP Target'
    aliases = ['antlr-cpp']
    filenames = ['*.G', '*.g']
    url = 'https://www.antlr.org'
    version_added = '1.1'
    
    def __init__(self, **options):
        super().__init__(CppLexer, AntlrLexer, **options)
    
    def analyse_text(text):
        return (AntlrLexer.analyse_text(text) and re.search('^\\s*language\\s*=\\s*C\\s*;', text, re.M))



class AntlrObjectiveCLexer(DelegatingLexer):
    """
    ANTLR with Objective-C Target
    """
    name = 'ANTLR With ObjectiveC Target'
    aliases = ['antlr-objc']
    filenames = ['*.G', '*.g']
    url = 'https://www.antlr.org'
    version_added = '1.1'
    
    def __init__(self, **options):
        super().__init__(ObjectiveCLexer, AntlrLexer, **options)
    
    def analyse_text(text):
        return (AntlrLexer.analyse_text(text) and re.search('^\\s*language\\s*=\\s*ObjC\\s*;', text))



class AntlrCSharpLexer(DelegatingLexer):
    """
    ANTLR with C# Target
    """
    name = 'ANTLR With C# Target'
    aliases = ['antlr-csharp', 'antlr-c#']
    filenames = ['*.G', '*.g']
    url = 'https://www.antlr.org'
    version_added = '1.1'
    
    def __init__(self, **options):
        super().__init__(CSharpLexer, AntlrLexer, **options)
    
    def analyse_text(text):
        return (AntlrLexer.analyse_text(text) and re.search('^\\s*language\\s*=\\s*CSharp2\\s*;', text, re.M))



class AntlrPythonLexer(DelegatingLexer):
    """
    ANTLR with Python Target
    """
    name = 'ANTLR With Python Target'
    aliases = ['antlr-python']
    filenames = ['*.G', '*.g']
    url = 'https://www.antlr.org'
    version_added = '1.1'
    
    def __init__(self, **options):
        super().__init__(PythonLexer, AntlrLexer, **options)
    
    def analyse_text(text):
        return (AntlrLexer.analyse_text(text) and re.search('^\\s*language\\s*=\\s*Python\\s*;', text, re.M))



class AntlrJavaLexer(DelegatingLexer):
    """
    ANTLR with Java Target
    """
    name = 'ANTLR With Java Target'
    aliases = ['antlr-java']
    filenames = ['*.G', '*.g']
    url = 'https://www.antlr.org'
    version_added = '1.1'
    
    def __init__(self, **options):
        super().__init__(JavaLexer, AntlrLexer, **options)
    
    def analyse_text(text):
        return (AntlrLexer.analyse_text(text) and 0.9)



class AntlrRubyLexer(DelegatingLexer):
    """
    ANTLR with Ruby Target
    """
    name = 'ANTLR With Ruby Target'
    aliases = ['antlr-ruby', 'antlr-rb']
    filenames = ['*.G', '*.g']
    url = 'https://www.antlr.org'
    version_added = '1.1'
    
    def __init__(self, **options):
        super().__init__(RubyLexer, AntlrLexer, **options)
    
    def analyse_text(text):
        return (AntlrLexer.analyse_text(text) and re.search('^\\s*language\\s*=\\s*Ruby\\s*;', text, re.M))



class AntlrPerlLexer(DelegatingLexer):
    """
    ANTLR with Perl Target
    """
    name = 'ANTLR With Perl Target'
    aliases = ['antlr-perl']
    filenames = ['*.G', '*.g']
    url = 'https://www.antlr.org'
    version_added = '1.1'
    
    def __init__(self, **options):
        super().__init__(PerlLexer, AntlrLexer, **options)
    
    def analyse_text(text):
        return (AntlrLexer.analyse_text(text) and re.search('^\\s*language\\s*=\\s*Perl5\\s*;', text, re.M))



class AntlrActionScriptLexer(DelegatingLexer):
    """
    ANTLR with ActionScript Target
    """
    name = 'ANTLR With ActionScript Target'
    aliases = ['antlr-actionscript', 'antlr-as']
    filenames = ['*.G', '*.g']
    url = 'https://www.antlr.org'
    version_added = '1.1'
    
    def __init__(self, **options):
        from pygments.lexers.actionscript import ActionScriptLexer
        super().__init__(ActionScriptLexer, AntlrLexer, **options)
    
    def analyse_text(text):
        return (AntlrLexer.analyse_text(text) and re.search('^\\s*language\\s*=\\s*ActionScript\\s*;', text, re.M))



class TreetopBaseLexer(RegexLexer):
    """
    A base lexer for `Treetop <http://treetop.rubyforge.org/>`_ grammars.
    Not for direct use; use :class:`TreetopLexer` instead.

    .. versionadded:: 1.6
    """
    tokens = {'root': [include('space'), ('require[ \\t]+[^\\n\\r]+[\\n\\r]', Other), ('module\\b', Keyword.Namespace, 'module'), ('grammar\\b', Keyword, 'grammar')], 'module': [include('space'), include('end'), ('module\\b', Keyword, '#push'), ('grammar\\b', Keyword, 'grammar'), ('[A-Z]\\w*(?:::[A-Z]\\w*)*', Name.Namespace)], 'grammar': [include('space'), include('end'), ('rule\\b', Keyword, 'rule'), ('include\\b', Keyword, 'include'), ('[A-Z]\\w*', Name)], 'include': [include('space'), ('[A-Z]\\w*(?:::[A-Z]\\w*)*', Name.Class, '#pop')], 'rule': [include('space'), include('end'), ('"(\\\\\\\\|\\\\[^\\\\]|[^"\\\\])*"', String.Double), ("'(\\\\\\\\|\\\\[^\\\\]|[^'\\\\])*'", String.Single), ('([A-Za-z_]\\w*)(:)', bygroups(Name.Label, Punctuation)), ('[A-Za-z_]\\w*', Name), ('[()]', Punctuation), ('[?+*/&!~]', Operator), ('\\[(?:\\\\.|\\[:\\^?[a-z]+:\\]|[^\\\\\\]])+\\]', String.Regex), ('([0-9]*)(\\.\\.)([0-9]*)', bygroups(Number.Integer, Operator, Number.Integer)), ('(<)([^>]+)(>)', bygroups(Punctuation, Name.Class, Punctuation)), ('\\{', Punctuation, 'inline_module'), ('\\.', String.Regex)], 'inline_module': [('\\{', Other, 'ruby'), ('\\}', Punctuation, '#pop'), ('[^{}]+', Other)], 'ruby': [('\\{', Other, '#push'), ('\\}', Other, '#pop'), ('[^{}]+', Other)], 'space': [('[ \\t\\n\\r]+', Whitespace), ('#[^\\n]*', Comment.Single)], 'end': [('end\\b', Keyword, '#pop')]}



class TreetopLexer(DelegatingLexer):
    """
    A lexer for Treetop grammars.
    """
    name = 'Treetop'
    aliases = ['treetop']
    filenames = ['*.treetop', '*.tt']
    url = 'https://cjheath.github.io/treetop'
    version_added = '1.6'
    
    def __init__(self, **options):
        super().__init__(RubyLexer, TreetopBaseLexer, **options)



class EbnfLexer(RegexLexer):
    """
    Lexer for `ISO/IEC 14977 EBNF
    <https://en.wikipedia.org/wiki/Extended_Backus%E2%80%93Naur_Form>`_
    grammars.
    """
    name = 'EBNF'
    aliases = ['ebnf']
    filenames = ['*.ebnf']
    mimetypes = ['text/x-ebnf']
    url = 'https://en.wikipedia.org/wiki/Extended_Backus%E2%80%93Naur_Form'
    version_added = '2.0'
    tokens = {'root': [include('whitespace'), include('comment_start'), include('identifier'), ('=', Operator, 'production')], 'production': [include('whitespace'), include('comment_start'), include('identifier'), ('"[^"]*"', String.Double), ("'[^']*'", String.Single), ('(\\?[^?]*\\?)', Name.Entity), ('[\\[\\]{}(),|]', Punctuation), ('-', Operator), (';', Punctuation, '#pop'), ('\\.', Punctuation, '#pop')], 'whitespace': [('\\s+', Text)], 'comment_start': [('\\(\\*', Comment.Multiline, 'comment')], 'comment': [('[^*)]', Comment.Multiline), include('comment_start'), ('\\*\\)', Comment.Multiline, '#pop'), ('[*)]', Comment.Multiline)], 'identifier': [('([a-zA-Z][\\w \\-]*)', Keyword)]}


