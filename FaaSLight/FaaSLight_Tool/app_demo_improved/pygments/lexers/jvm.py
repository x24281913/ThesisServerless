"""
    pygments.lexers.jvm
    ~~~~~~~~~~~~~~~~~~~

    Pygments lexers for JVM languages.

    :copyright: Copyright 2006-present by the Pygments team, see AUTHORS.
    :license: BSD, see LICENSE for details.
"""

import re
from pygments.lexer import Lexer, RegexLexer, include, bygroups, using, this, combined, default, words
from pygments.token import Text, Comment, Operator, Keyword, Name, String, Number, Punctuation, Whitespace
from pygments.util import shebang_matches
from pygments import unistring as uni
__all__ = ['JavaLexer', 'ScalaLexer', 'GosuLexer', 'GosuTemplateLexer', 'GroovyLexer', 'IokeLexer', 'ClojureLexer', 'ClojureScriptLexer', 'KotlinLexer', 'XtendLexer', 'AspectJLexer', 'CeylonLexer', 'PigLexer', 'GoloLexer', 'JasminLexer', 'SarlLexer']


class JavaLexer(RegexLexer):
    """
    For Java source code.
    """
    name = 'Java'
    url = 'https://www.oracle.com/technetwork/java/'
    aliases = ['java']
    filenames = ['*.java']
    mimetypes = ['text/x-java']
    version_added = ''
    flags = re.MULTILINE | re.DOTALL
    tokens = {'root': [('(^\\s*)((?:(?:public|private|protected|static|strictfp)(?:\\s+))*)(record)\\b', bygroups(Whitespace, using(this), Keyword.Declaration), 'class'), ('[^\\S\\n]+', Whitespace), ('(//.*?)(\\n)', bygroups(Comment.Single, Whitespace)), ('/\\*.*?\\*/', Comment.Multiline), ('(assert|break|case|catch|continue|default|do|else|finally|for|if|goto|instanceof|new|return|switch|this|throw|try|while)\\b', Keyword), ('((?:(?:[^\\W\\d]|\\$)[\\w.\\[\\]$<>?]*\\s+)+?)((?:[^\\W\\d]|\\$)[\\w$]*)(\\s*)(\\()', bygroups(using(this), Name.Function, Whitespace, Punctuation)), ('@[^\\W\\d][\\w.]*', Name.Decorator), ('(abstract|const|enum|exports|extends|final|implements|native|non-sealed|open|opens|permits|private|protected|provides|public|requires|sealed|static|strictfp|super|synchronized|throws|to|transient|transitive|uses|volatile|with|yield)\\b', Keyword.Declaration), ('(boolean|byte|char|double|float|int|long|short|void)\\b', Keyword.Type), ('(package)(\\s+)', bygroups(Keyword.Namespace, Whitespace), 'import'), ('(true|false|null)\\b', Keyword.Constant), ('(class|interface)\\b', Keyword.Declaration, 'class'), ('(module)\\b', Keyword.Declaration, 'module'), ('(var)(\\s+)', bygroups(Keyword.Declaration, Whitespace), 'var'), ('(import(?:\\s+(?:static|module))?)(\\s+)', bygroups(Keyword.Namespace, Whitespace), 'import'), ('"""\\n', String, 'multiline_string'), ('"', String, 'string'), ("'\\\\.'|'[^\\\\]'|'\\\\u[0-9a-fA-F]{4}'", String.Char), ('(\\.)((?:[^\\W\\d]|\\$)[\\w$]*)', bygroups(Punctuation, Name.Attribute)), ('^(\\s*)(default)(:)', bygroups(Whitespace, Keyword, Punctuation)), ('^(\\s*)((?:[^\\W\\d]|\\$)[\\w$]*)(:)', bygroups(Whitespace, Name.Label, Punctuation)), ('([^\\W\\d]|\\$)[\\w$]*', Name), ('([0-9][0-9_]*\\.([0-9][0-9_]*)?|\\.[0-9][0-9_]*)([eE][+\\-]?[0-9][0-9_]*)?[fFdD]?|[0-9][eE][+\\-]?[0-9][0-9_]*[fFdD]?|[0-9]([eE][+\\-]?[0-9][0-9_]*)?[fFdD]|0[xX]([0-9a-fA-F][0-9a-fA-F_]*\\.?|([0-9a-fA-F][0-9a-fA-F_]*)?\\.[0-9a-fA-F][0-9a-fA-F_]*)[pP][+\\-]?[0-9][0-9_]*[fFdD]?', Number.Float), ('0[xX][0-9a-fA-F][0-9a-fA-F_]*[lL]?', Number.Hex), ('0[bB][01][01_]*[lL]?', Number.Bin), ('0[0-7_]+[lL]?', Number.Oct), ('0|[1-9][0-9_]*[lL]?', Number.Integer), ('[~^*!%&\\[\\]<>|+=/?-]', Operator), ('[{}();:.,]', Punctuation), ('\\n', Whitespace)], 'class': [('\\s+', Text), ('([^\\W\\d]|\\$)[\\w$]*', Name.Class, '#pop')], 'module': [('\\s+', Text), ('([^\\W\\d]|\\$)[\\w$]*', Name.Class, '#pop')], 'var': [('([^\\W\\d]|\\$)[\\w$]*', Name, '#pop')], 'import': [('[\\w.]+\\*?', Name.Namespace, '#pop')], 'multiline_string': [('"""', String, '#pop'), ('"', String), include('string')], 'string': [('[^\\\\"]+', String), ('\\\\\\\\', String), ('\\\\"', String), ('\\\\', String), ('"', String, '#pop')]}



class AspectJLexer(JavaLexer):
    """
    For AspectJ source code.
    """
    name = 'AspectJ'
    url = 'http://www.eclipse.org/aspectj/'
    aliases = ['aspectj']
    filenames = ['*.aj']
    mimetypes = ['text/x-aspectj']
    version_added = '1.6'
    aj_keywords = {'aspect', 'pointcut', 'privileged', 'call', 'execution', 'initialization', 'preinitialization', 'handler', 'get', 'set', 'staticinitialization', 'target', 'args', 'within', 'withincode', 'cflow', 'cflowbelow', 'annotation', 'before', 'after', 'around', 'proceed', 'throwing', 'returning', 'adviceexecution', 'declare', 'parents', 'warning', 'error', 'soft', 'precedence', 'thisJoinPoint', 'thisJoinPointStaticPart', 'thisEnclosingJoinPointStaticPart', 'issingleton', 'perthis', 'pertarget', 'percflow', 'percflowbelow', 'pertypewithin', 'lock', 'unlock', 'thisAspectInstance'}
    aj_inter_type = {'parents:', 'warning:', 'error:', 'soft:', 'precedence:'}
    aj_inter_type_annotation = {'@type', '@method', '@constructor', '@field'}
    
    def get_tokens_unprocessed(self, text):
        for (index, token, value) in JavaLexer.get_tokens_unprocessed(self, text):
            if (token is Name and value in self.aj_keywords):
                yield (index, Keyword, value)
            elif (token is Name.Label and value in self.aj_inter_type):
                yield (index, Keyword, value[:-1])
                yield (index, Operator, value[-1])
            elif (token is Name.Decorator and value in self.aj_inter_type_annotation):
                yield (index, Keyword, value)
            else:
                yield (index, token, value)



class ScalaLexer(RegexLexer):
    """
    For Scala source code.
    """
    name = 'Scala'
    url = 'http://www.scala-lang.org'
    aliases = ['scala']
    filenames = ['*.scala']
    mimetypes = ['text/x-scala']
    version_added = ''
    flags = re.MULTILINE | re.DOTALL
    opchar = '[!#%&*\\-\\/:?@^' + uni.combine('Sm', 'So') + ']'
    letter = '[_\\$' + uni.combine('Ll', 'Lu', 'Lo', 'Nl', 'Lt') + ']'
    upperLetter = '[' + uni.combine('Lu', 'Lt') + ']'
    letterOrDigit = f'(?:{letter}|[0-9])'
    letterOrDigitNoDollarSign = '(?:{}|[0-9])'.format(letter.replace('\\$', ''))
    alphaId = f'{letter}+'
    simpleInterpolatedVariable = f'{letter}{letterOrDigitNoDollarSign}*'
    idrest = f'{letter}{letterOrDigit}*(?:(?<=_){opchar}+)?'
    idUpper = f'{upperLetter}{letterOrDigit}*(?:(?<=_){opchar}+)?'
    plainid = f'(?:{idrest}|{opchar}+)'
    backQuotedId = '`[^`]+`'
    anyId = f'(?:{plainid}|{backQuotedId})'
    notStartOfComment = '(?!//|/\\*)'
    endOfLineMaybeWithComment = '(?=\\s*(//|$))'
    keywords = ('new', 'return', 'throw', 'classOf', 'isInstanceOf', 'asInstanceOf', 'else', 'if', 'then', 'do', 'while', 'for', 'yield', 'match', 'case', 'catch', 'finally', 'try')
    operators = ('<%', '=:=', '<:<', '<%<', '>:', '<:', '=', '==', '!=', '<=', '>=', '<>', '<', '>', '<-', '←', '->', '→', '=>', '⇒', '?', '@', '|', '-', '+', '*', '%', '~', '\\')
    storage_modifiers = ('private', 'protected', 'synchronized', '@volatile', 'abstract', 'final', 'lazy', 'sealed', 'implicit', 'override', '@transient', '@native')
    tokens = {'root': [include('whitespace'), include('comments'), include('script-header'), include('imports'), include('exports'), include('storage-modifiers'), include('annotations'), include('using'), include('declarations'), include('inheritance'), include('extension'), include('end'), include('constants'), include('strings'), include('symbols'), include('singleton-type'), include('inline'), include('quoted'), include('keywords'), include('operators'), include('punctuation'), include('names')], 'whitespace': [('\\s+', Whitespace)], 'comments': [('//.*?\\n', Comment.Single), ('/\\*', Comment.Multiline, 'comment')], 'script-header': [('^#!([^\\n]*)$', Comment.Hashbang)], 'imports': [('\\b(import)(\\s+)', bygroups(Keyword, Whitespace), 'import-path')], 'exports': [('\\b(export)(\\s+)(given)(\\s+)', bygroups(Keyword, Whitespace, Keyword, Whitespace), 'export-path'), ('\\b(export)(\\s+)', bygroups(Keyword, Whitespace), 'export-path')], 'storage-modifiers': [(words(storage_modifiers, prefix='\\b', suffix='\\b'), Keyword), ('\\b(transparent|opaque|infix|open|inline)\\b(?=[a-z\\s]*\\b(def|val|var|given|type|class|trait|object|enum)\\b)', Keyword)], 'annotations': [(f'@{idrest}', Name.Decorator)], 'using': [('(\\()(\\s*)(using)(\\s)', bygroups(Punctuation, Whitespace, Keyword, Whitespace))], 'declarations': [(f'\\b(def)\\b(\\s*){notStartOfComment}({anyId})?', bygroups(Keyword, Whitespace, Name.Function)), (f'\\b(trait)\\b(\\s*){notStartOfComment}({anyId})?', bygroups(Keyword, Whitespace, Name.Class)), (f'\\b(?:(case)(\\s+))?(class|object|enum)\\b(\\s*){notStartOfComment}({anyId})?', bygroups(Keyword, Whitespace, Keyword, Whitespace, Name.Class)), (f'(?<!\\.)\\b(type)\\b(\\s*){notStartOfComment}({anyId})?', bygroups(Keyword, Whitespace, Name.Class)), ('\\b(val|var)\\b', Keyword.Declaration), (f'\\b(package)(\\s+)(object)\\b(\\s*){notStartOfComment}({anyId})?', bygroups(Keyword, Whitespace, Keyword, Whitespace, Name.Namespace)), ('\\b(package)(\\s+)', bygroups(Keyword, Whitespace), 'package'), (f'\\b(given)\\b(\\s*)({idUpper})', bygroups(Keyword, Whitespace, Name.Class)), (f'\\b(given)\\b(\\s*)({anyId})?', bygroups(Keyword, Whitespace, Name))], 'inheritance': [(f'\\b(extends|with|derives)\\b(\\s*)({idUpper}|{backQuotedId}|(?=\\([^\\)]+=>)|(?={plainid})|(?="))?', bygroups(Keyword, Whitespace, Name.Class))], 'extension': [('\\b(extension)(\\s+)(?=[\\[\\(])', bygroups(Keyword, Whitespace))], 'end': [('\\b(end)(\\s+)(if|while|for|match|new|extension|val|var)\\b', bygroups(Keyword, Whitespace, Keyword)), (f'\\b(end)(\\s+)({idUpper}){endOfLineMaybeWithComment}', bygroups(Keyword, Whitespace, Name.Class)), (f'\\b(end)(\\s+)({backQuotedId}|{plainid})?{endOfLineMaybeWithComment}', bygroups(Keyword, Whitespace, Name.Namespace))], 'punctuation': [('[{}()\\[\\];,.]', Punctuation), ('(?<!:):(?!:)', Punctuation)], 'keywords': [(words(keywords, prefix='\\b', suffix='\\b'), Keyword)], 'operators': [(f'({opchar}{{2,}})(\\s+)', bygroups(Operator, Whitespace)), ('/(?![/*])', Operator), (words(operators), Operator), (f'(?<!{opchar})(!|&&|\\|\\|)(?!{opchar})', Operator)], 'constants': [('\\b(this|super)\\b', Name.Builtin.Pseudo), ('(true|false|null)\\b', Keyword.Constant), ('0[xX][0-9a-fA-F_]*', Number.Hex), ('([0-9][0-9_]*\\.[0-9][0-9_]*|\\.[0-9][0-9_]*)([eE][+-]?[0-9][0-9_]*)?[fFdD]?', Number.Float), ('[0-9]+([eE][+-]?[0-9]+)?[fFdD]', Number.Float), ('[0-9]+([eE][+-]?[0-9]+)[fFdD]?', Number.Float), ('[0-9]+[lL]', Number.Integer.Long), ('[0-9]+', Number.Integer), ('""".*?"""(?!")', String), ('"(\\\\\\\\|\\\\"|[^"])*"', String), ("(')(\\\\.)(')", bygroups(String.Char, String.Escape, String.Char)), ("'[^\\\\]'|'\\\\u[0-9a-fA-F]{4}'", String.Char)], 'strings': [('[fs]"""', String, 'interpolated-string-triple'), ('[fs]"', String, 'interpolated-string'), ('raw"(\\\\\\\\|\\\\"|[^"])*"', String)], 'symbols': [(f"('{plainid})(?!')", String.Symbol)], 'singleton-type': [('(\\.)(type)\\b', bygroups(Punctuation, Keyword))], 'inline': [(f'\\b(inline)(?=\\s+({plainid}|{backQuotedId})\\s*:)', Keyword), ('\\b(inline)\\b(?=(?:.(?!\\b(?:val|def|given)\\b))*\\b(if|match)\\b)', Keyword)], 'quoted': [("['$]\\{(?!')", Punctuation), ("'\\[(?!')", Punctuation)], 'names': [(idUpper, Name.Class), (anyId, Name)], 'comment': [('[^/*]+', Comment.Multiline), ('/\\*', Comment.Multiline, '#push'), ('\\*/', Comment.Multiline, '#pop'), ('[*/]', Comment.Multiline)], 'import-path': [('(?<=[\\n;:])', Text, '#pop'), include('comments'), ('\\b(given)\\b', Keyword), include('qualified-name'), ('\\{', Punctuation, 'import-path-curly-brace')], 'import-path-curly-brace': [include('whitespace'), include('comments'), ('\\b(given)\\b', Keyword), ('=>', Operator), ('\\}', Punctuation, '#pop'), (',', Punctuation), ('[\\[\\]]', Punctuation), include('qualified-name')], 'export-path': [('(?<=[\\n;:])', Text, '#pop'), include('comments'), include('qualified-name'), ('\\{', Punctuation, 'export-path-curly-brace')], 'export-path-curly-brace': [include('whitespace'), include('comments'), ('=>', Operator), ('\\}', Punctuation, '#pop'), (',', Punctuation), include('qualified-name')], 'package': [('(?<=[\\n;])', Text, '#pop'), (':', Punctuation, '#pop'), include('comments'), include('qualified-name')], 'interpolated-string-triple': [('"""(?!")', String, '#pop'), ('"', String), include('interpolated-string-common')], 'interpolated-string': [('"', String, '#pop'), include('interpolated-string-common')], 'interpolated-string-brace': [('\\}', String.Interpol, '#pop'), ('\\{', Punctuation, 'interpolated-string-nested-brace'), include('root')], 'interpolated-string-nested-brace': [('\\{', Punctuation, '#push'), ('\\}', Punctuation, '#pop'), include('root')], 'qualified-name': [(idUpper, Name.Class), (f'({anyId})(\\.)', bygroups(Name.Namespace, Punctuation)), ('\\.', Punctuation), (anyId, Name), ('[^\\S\\n]+', Whitespace)], 'interpolated-string-common': [('[^"$\\\\]+', String), ('\\$\\$', String.Escape), (f'(\\$)({simpleInterpolatedVariable})', bygroups(String.Interpol, Name)), ('\\$\\{', String.Interpol, 'interpolated-string-brace'), ('\\\\.', String)]}



class GosuLexer(RegexLexer):
    """
    For Gosu source code.
    """
    name = 'Gosu'
    aliases = ['gosu']
    filenames = ['*.gs', '*.gsx', '*.gsp', '*.vark']
    mimetypes = ['text/x-gosu']
    url = 'https://gosu-lang.github.io'
    version_added = '1.5'
    flags = re.MULTILINE | re.DOTALL
    tokens = {'root': [('^(\\s*(?:[a-zA-Z_][\\w.\\[\\]]*\\s+)+?)([a-zA-Z_]\\w*)(\\s*)(\\()', bygroups(using(this), Name.Function, Whitespace, Operator)), ('[^\\S\\n]+', Whitespace), ('//.*?\\n', Comment.Single), ('/\\*.*?\\*/', Comment.Multiline), ('@[a-zA-Z_][\\w.]*', Name.Decorator), ('(in|as|typeof|statictypeof|typeis|typeas|if|else|foreach|for|index|while|do|continue|break|return|try|catch|finally|this|throw|new|switch|case|default|eval|super|outer|classpath|using)\\b', Keyword), ('(var|delegate|construct|function|private|internal|protected|public|abstract|override|final|static|extends|transient|implements|represents|readonly)\\b', Keyword.Declaration), ('(property)(\\s+)(get|set)?', bygroups(Keyword.Declaration, Whitespace, Keyword.Declaration)), ('(boolean|byte|char|double|float|int|long|short|void|block)\\b', Keyword.Type), ('(package)(\\s+)', bygroups(Keyword.Namespace, Whitespace)), ('(true|false|null|NaN|Infinity)\\b', Keyword.Constant), ('(class|interface|enhancement|enum)(\\s+)([a-zA-Z_]\\w*)', bygroups(Keyword.Declaration, Whitespace, Name.Class)), ('(uses)(\\s+)([\\w.]+\\*?)', bygroups(Keyword.Namespace, Whitespace, Name.Namespace)), ('"', String, 'string'), ('(\\??[.#])([a-zA-Z_]\\w*)', bygroups(Operator, Name.Attribute)), ('(:)([a-zA-Z_]\\w*)', bygroups(Operator, Name.Attribute)), ('[a-zA-Z_$]\\w*', Name), ('and|or|not|[\\\\~^*!%&\\[\\](){}<>|+=:;,./?-]', Operator), ('[0-9][0-9]*\\.[0-9]+([eE][0-9]+)?[fd]?', Number.Float), ('[0-9]+', Number.Integer), ('\\n', Whitespace)], 'templateText': [('(\\\\<)|(\\\\\\$)', String), ('(<%@\\s+)(extends|params)', bygroups(Operator, Name.Decorator), 'stringTemplate'), ('<%!--.*?--%>', Comment.Multiline), ('(<%)|(<%=)', Operator, 'stringTemplate'), ('\\$\\{', Operator, 'stringTemplateShorthand'), ('.', String)], 'string': [('"', String, '#pop'), include('templateText')], 'stringTemplate': [('"', String, 'string'), ('%>', Operator, '#pop'), include('root')], 'stringTemplateShorthand': [('"', String, 'string'), ('\\{', Operator, 'stringTemplateShorthand'), ('\\}', Operator, '#pop'), include('root')]}



class GosuTemplateLexer(Lexer):
    """
    For Gosu templates.
    """
    name = 'Gosu Template'
    aliases = ['gst']
    filenames = ['*.gst']
    mimetypes = ['text/x-gosu-template']
    url = 'https://gosu-lang.github.io'
    version_added = '1.5'
    
    def get_tokens_unprocessed(self, text):
        lexer = GosuLexer()
        stack = ['templateText']
        yield from lexer.get_tokens_unprocessed(text, stack)



class GroovyLexer(RegexLexer):
    """
    For Groovy source code.
    """
    name = 'Groovy'
    url = 'https://groovy-lang.org/'
    aliases = ['groovy']
    filenames = ['*.groovy', '*.gradle']
    mimetypes = ['text/x-groovy']
    version_added = '1.5'
    flags = re.MULTILINE | re.DOTALL
    tokens = {'root': [('#!(.*?)$', Comment.Preproc, 'base'), default('base')], 'base': [('[^\\S\\n]+', Whitespace), ('(//.*?)(\\n)', bygroups(Comment.Single, Whitespace)), ('/\\*.*?\\*/', Comment.Multiline), ('(assert|break|case|catch|continue|default|do|else|finally|for|if|goto|instanceof|new|return|switch|this|throw|try|while|in|as)\\b', Keyword), ('^(\\s*(?:[a-zA-Z_][\\w.\\[\\]]*\\s+)+?)([a-zA-Z_]\\w*|"(?:\\\\\\\\|\\\\[^\\\\]|[^"\\\\])*"|\'(?:\\\\\\\\|\\\\[^\\\\]|[^\'\\\\])*\')(\\s*)(\\()', bygroups(using(this), Name.Function, Whitespace, Operator)), ('@[a-zA-Z_][\\w.]*', Name.Decorator), ('(abstract|const|enum|extends|final|implements|native|private|protected|public|static|strictfp|super|synchronized|throws|transient|volatile)\\b', Keyword.Declaration), ('(def|boolean|byte|char|double|float|int|long|short|void)\\b', Keyword.Type), ('(package)(\\s+)', bygroups(Keyword.Namespace, Whitespace)), ('(true|false|null)\\b', Keyword.Constant), ('(class|interface)(\\s+)', bygroups(Keyword.Declaration, Whitespace), 'class'), ('(import)(\\s+)', bygroups(Keyword.Namespace, Whitespace), 'import'), ('""".*?"""', String.Double), ("'''.*?'''", String.Single), ('"(\\\\\\\\|\\\\[^\\\\]|[^"\\\\])*"', String.Double), ("'(\\\\\\\\|\\\\[^\\\\]|[^'\\\\])*'", String.Single), ('\\$/((?!/\\$).)*/\\$', String), ('/(\\\\\\\\|\\\\[^\\\\]|[^/\\\\])*/', String), ("'\\\\.'|'[^\\\\]'|'\\\\u[0-9a-fA-F]{4}'", String.Char), ('(\\.)([a-zA-Z_]\\w*)', bygroups(Operator, Name.Attribute)), ('[a-zA-Z_]\\w*:', Name.Label), ('[a-zA-Z_$]\\w*', Name), ('[~^*!%&\\[\\](){}<>|+=:;,./?-]', Operator), ('[0-9][0-9]*\\.[0-9]+([eE][0-9]+)?[fd]?', Number.Float), ('0x[0-9a-fA-F]+', Number.Hex), ('[0-9]+L?', Number.Integer), ('\\n', Whitespace)], 'class': [('[a-zA-Z_]\\w*', Name.Class, '#pop')], 'import': [('[\\w.]+\\*?', Name.Namespace, '#pop')]}
    
    def analyse_text(text):
        return shebang_matches(text, 'groovy')



class IokeLexer(RegexLexer):
    """
    For Ioke (a strongly typed, dynamic,
    prototype based programming language) source.
    """
    name = 'Ioke'
    url = 'https://ioke.org/'
    filenames = ['*.ik']
    aliases = ['ioke', 'ik']
    mimetypes = ['text/x-iokesrc']
    version_added = '1.4'
    tokens = {'interpolatableText': [('(\\\\b|\\\\e|\\\\t|\\\\n|\\\\f|\\\\r|\\\\"|\\\\\\\\|\\\\#|\\\\\\Z|\\\\u[0-9a-fA-F]{1,4}|\\\\[0-3]?[0-7]?[0-7])', String.Escape), ('#\\{', Punctuation, 'textInterpolationRoot')], 'text': [('(?<!\\\\)"', String, '#pop'), include('interpolatableText'), ('[^"]', String)], 'documentation': [('(?<!\\\\)"', String.Doc, '#pop'), include('interpolatableText'), ('[^"]', String.Doc)], 'textInterpolationRoot': [('\\}', Punctuation, '#pop'), include('root')], 'slashRegexp': [('(?<!\\\\)/[im-psux]*', String.Regex, '#pop'), include('interpolatableText'), ('\\\\/', String.Regex), ('[^/]', String.Regex)], 'squareRegexp': [('(?<!\\\\)][im-psux]*', String.Regex, '#pop'), include('interpolatableText'), ('\\\\]', String.Regex), ('[^\\]]', String.Regex)], 'squareText': [('(?<!\\\\)]', String, '#pop'), include('interpolatableText'), ('[^\\]]', String)], 'root': [('\\n', Whitespace), ('\\s+', Whitespace), (';(.*?)\\n', Comment), ('\\A#!(.*?)\\n', Comment), ('#/', String.Regex, 'slashRegexp'), ('#r\\[', String.Regex, 'squareRegexp'), (':[\\w!:?]+', String.Symbol), ('[\\w!:?]+:(?![\\w!?])', String.Other), (':"(\\\\\\\\|\\\\[^\\\\]|[^"\\\\])*"', String.Symbol), ('((?<=fn\\()|(?<=fnx\\()|(?<=method\\()|(?<=macro\\()|(?<=lecro\\()|(?<=syntax\\()|(?<=dmacro\\()|(?<=dlecro\\()|(?<=dlecrox\\()|(?<=dsyntax\\())(\\s*)"', String.Doc, 'documentation'), ('"', String, 'text'), ('#\\[', String, 'squareText'), ('\\w[\\w!:?]+(?=\\s*=.*mimic\\s)', Name.Entity), ('[a-zA-Z_][\\w!:?]*(?=[\\s]*[+*/-]?=[^=].*($|\\.))', Name.Variable), ('(break|cond|continue|do|ensure|for|for:dict|for:set|if|let|loop|p:for|p:for:dict|p:for:set|return|unless|until|while|with)(?![\\w!:?])', Keyword.Reserved), ('(eval|mimic|print|println)(?![\\w!:?])', Keyword), ('(cell\\?|cellNames|cellOwner\\?|cellOwner|cells|cell|documentation|hash|identity|mimic|removeCell\\!|undefineCell\\!)(?![\\w!:?])', Keyword), ('(stackTraceAsText)(?![\\w!:?])', Keyword), ('(dict|list|message|set)(?![\\w!:?])', Keyword.Reserved), ('(case|case:and|case:else|case:nand|case:nor|case:not|case:or|case:otherwise|case:xor)(?![\\w!:?])', Keyword.Reserved), ('(asText|become\\!|derive|freeze\\!|frozen\\?|in\\?|is\\?|kind\\?|mimic\\!|mimics|mimics\\?|prependMimic\\!|removeAllMimics\\!|removeMimic\\!|same\\?|send|thaw\\!|uniqueHexId)(?![\\w!:?])', Keyword), ('(after|around|before)(?![\\w!:?])', Keyword.Reserved), ('(kind|cellDescriptionDict|cellSummary|genSym|inspect|notice)(?![\\w!:?])', Keyword), ('(use|destructuring)', Keyword.Reserved), ('(cell\\?|cellOwner\\?|cellOwner|cellNames|cells|cell|documentation|identity|removeCell!|undefineCell)(?![\\w!:?])', Keyword), ('(internal:compositeRegexp|internal:concatenateText|internal:createDecimal|internal:createNumber|internal:createRegexp|internal:createText)(?![\\w!:?])', Keyword.Reserved), ('(availableRestarts|bind|error\\!|findRestart|handle|invokeRestart|rescue|restart|signal\\!|warn\\!)(?![\\w!:?])', Keyword.Reserved), ('(nil|false|true)(?![\\w!:?])', Name.Constant), ('(Arity|Base|Call|Condition|DateTime|Aspects|Pointcut|Assignment|BaseBehavior|Boolean|Case|AndCombiner|Else|NAndCombiner|NOrCombiner|NotCombiner|OrCombiner|XOrCombiner|Conditions|Definitions|FlowControl|Internal|Literals|Reflection|DefaultMacro|DefaultMethod|DefaultSyntax|Dict|FileSystem|Ground|Handler|Hook|IO|IokeGround|Struct|LexicalBlock|LexicalMacro|List|Message|Method|Mixins|NativeMethod|Number|Origin|Pair|Range|Reflector|Regexp Match|Regexp|Rescue|Restart|Runtime|Sequence|Set|Symbol|System|Text|Tuple)(?![\\w!:?])', Name.Builtin), ('(generateMatchMethod|aliasMethod|λ|ʎ|fnx|fn|method|dmacro|dlecro|syntax|macro|dlecrox|lecrox|lecro|syntax)(?![\\w!:?])', Name.Function), ('-?0[xX][0-9a-fA-F]+', Number.Hex), ('-?(\\d+\\.?\\d*|\\d*\\.\\d+)([eE][+-]?[0-9]+)?', Number.Float), ('-?\\d+', Number.Integer), ('#\\(', Punctuation), ('(&&>>|\\|\\|>>|\\*\\*>>|:::|::|\\.\\.\\.|===|\\*\\*>|\\*\\*=|&&>|&&=|\\|\\|>|\\|\\|=|\\->>|\\+>>|!>>|<>>>|<>>|&>>|%>>|#>>|@>>|/>>|\\*>>|\\?>>|\\|>>|\\^>>|~>>|\\$>>|=>>|<<=|>>=|<=>|<\\->|=~|!~|=>|\\+\\+|\\-\\-|<=|>=|==|!=|&&|\\.\\.|\\+=|\\-=|\\*=|\\/=|%=|&=|\\^=|\\|=|<\\-|\\+>|!>|<>|&>|%>|#>|\\@>|\\/>|\\*>|\\?>|\\|>|\\^>|~>|\\$>|<\\->|\\->|<<|>>|\\*\\*|\\?\\||\\?&|\\|\\||>|<|\\*|\\/|%|\\+|\\-|&|\\^|\\||=|\\$|!|~|\\?|#|\\u2260|\\u2218|\\u2208|\\u2209)', Operator), ('(and|nand|or|xor|nor|return|import)(?![\\w!?])', Operator), ("(\\`\\`|\\`|\\'\\'|\\'|\\.|\\,|@@|@|\\[|\\]|\\(|\\)|\\{|\\})", Punctuation), ('[A-Z][\\w!:?]*', Name.Class), ('[a-z_][\\w!:?]*', Name)]}



class ClojureLexer(RegexLexer):
    """
    Lexer for Clojure source code.
    """
    name = 'Clojure'
    url = 'http://clojure.org/'
    aliases = ['clojure', 'clj']
    filenames = ['*.clj', '*.cljc']
    mimetypes = ['text/x-clojure', 'application/x-clojure']
    version_added = '0.11'
    special_forms = ('.', 'def', 'do', 'fn', 'if', 'let', 'new', 'quote', 'var', 'loop')
    declarations = ('def-', 'defn', 'defn-', 'defmacro', 'defmulti', 'defmethod', 'defstruct', 'defonce', 'declare', 'definline', 'definterface', 'defprotocol', 'defrecord', 'deftype', 'defproject', 'ns')
    builtins = ('*', '+', '-', '->', '/', '<', '<=', '=', '==', '>', '>=', '..', 'accessor', 'agent', 'agent-errors', 'aget', 'alength', 'all-ns', 'alter', 'and', 'append-child', 'apply', 'array-map', 'aset', 'aset-boolean', 'aset-byte', 'aset-char', 'aset-double', 'aset-float', 'aset-int', 'aset-long', 'aset-short', 'assert', 'assoc', 'await', 'await-for', 'bean', 'binding', 'bit-and', 'bit-not', 'bit-or', 'bit-shift-left', 'bit-shift-right', 'bit-xor', 'boolean', 'branch?', 'butlast', 'byte', 'cast', 'char', 'children', 'class', 'clear-agent-errors', 'comment', 'commute', 'comp', 'comparator', 'complement', 'concat', 'conj', 'cons', 'constantly', 'cond', 'if-not', 'construct-proxy', 'contains?', 'count', 'create-ns', 'create-struct', 'cycle', 'dec', 'deref', 'difference', 'disj', 'dissoc', 'distinct', 'doall', 'doc', 'dorun', 'doseq', 'dosync', 'dotimes', 'doto', 'double', 'down', 'drop', 'drop-while', 'edit', 'end?', 'ensure', 'eval', 'every?', 'false?', 'ffirst', 'file-seq', 'filter', 'find', 'find-doc', 'find-ns', 'find-var', 'first', 'float', 'flush', 'for', 'fnseq', 'frest', 'gensym', 'get-proxy-class', 'get', 'hash-map', 'hash-set', 'identical?', 'identity', 'if-let', 'import', 'in-ns', 'inc', 'index', 'insert-child', 'insert-left', 'insert-right', 'inspect-table', 'inspect-tree', 'instance?', 'int', 'interleave', 'intersection', 'into', 'into-array', 'iterate', 'join', 'key', 'keys', 'keyword', 'keyword?', 'last', 'lazy-cat', 'lazy-cons', 'left', 'lefts', 'line-seq', 'list*', 'list', 'load', 'load-file', 'locking', 'long', 'loop', 'macroexpand', 'macroexpand-1', 'make-array', 'make-node', 'map', 'map-invert', 'map?', 'mapcat', 'max', 'max-key', 'memfn', 'merge', 'merge-with', 'meta', 'min', 'min-key', 'name', 'namespace', 'neg?', 'new', 'newline', 'next', 'nil?', 'node', 'not', 'not-any?', 'not-every?', 'not=', 'ns-imports', 'ns-interns', 'ns-map', 'ns-name', 'ns-publics', 'ns-refers', 'ns-resolve', 'ns-unmap', 'nth', 'nthrest', 'or', 'parse', 'partial', 'path', 'peek', 'pop', 'pos?', 'pr', 'pr-str', 'print', 'print-str', 'println', 'println-str', 'prn', 'prn-str', 'project', 'proxy', 'proxy-mappings', 'quot', 'rand', 'rand-int', 'range', 're-find', 're-groups', 're-matcher', 're-matches', 're-pattern', 're-seq', 'read', 'read-line', 'reduce', 'ref', 'ref-set', 'refer', 'rem', 'remove', 'remove-method', 'remove-ns', 'rename', 'rename-keys', 'repeat', 'replace', 'replicate', 'resolve', 'rest', 'resultset-seq', 'reverse', 'rfirst', 'right', 'rights', 'root', 'rrest', 'rseq', 'second', 'select', 'select-keys', 'send', 'send-off', 'seq', 'seq-zip', 'seq?', 'set', 'short', 'slurp', 'some', 'sort', 'sort-by', 'sorted-map', 'sorted-map-by', 'sorted-set', 'special-symbol?', 'split-at', 'split-with', 'str', 'string?', 'struct', 'struct-map', 'subs', 'subvec', 'symbol', 'symbol?', 'sync', 'take', 'take-nth', 'take-while', 'test', 'time', 'to-array', 'to-array-2d', 'tree-seq', 'true?', 'union', 'up', 'update-proxy', 'val', 'vals', 'var-get', 'var-set', 'var?', 'vector', 'vector-zip', 'vector?', 'when', 'when-first', 'when-let', 'when-not', 'with-local-vars', 'with-meta', 'with-open', 'with-out-str', 'xml-seq', 'xml-zip', 'zero?', 'zipmap', 'zipper')
    valid_name = '(?!#)[\\w!$%*+<=>?/.#|-]+'
    tokens = {'root': [(';.*$', Comment.Single), (',+', Text), ('\\s+', Whitespace), ('-?\\d+\\.\\d+', Number.Float), ('-?\\d+/\\d+', Number), ('-?\\d+', Number.Integer), ('0x-?[abcdef\\d]+', Number.Hex), ('"(\\\\\\\\|\\\\[^\\\\]|[^"\\\\])*"', String), ("'" + valid_name, String.Symbol), ('\\\\(.|[a-z]+)', String.Char), ('::?#?' + valid_name, String.Symbol), ("~@|[`\\'#^~&@]", Operator), (words(special_forms, suffix=' '), Keyword), (words(declarations, suffix=' '), Keyword.Declaration), (words(builtins, suffix=' '), Name.Builtin), ('(?<=\\()' + valid_name, Name.Function), (valid_name, Name.Variable), ('(\\[|\\])', Punctuation), ('(\\{|\\})', Punctuation), ('(\\(|\\))', Punctuation)]}



class ClojureScriptLexer(ClojureLexer):
    """
    Lexer for ClojureScript source code.
    """
    name = 'ClojureScript'
    url = 'http://clojure.org/clojurescript'
    aliases = ['clojurescript', 'cljs']
    filenames = ['*.cljs']
    mimetypes = ['text/x-clojurescript', 'application/x-clojurescript']
    version_added = '2.0'



class TeaLangLexer(RegexLexer):
    """
    For Tea source code. Only used within a
    TeaTemplateLexer.

    .. versionadded:: 1.5
    """
    flags = re.MULTILINE | re.DOTALL
    tokens = {'root': [('^(\\s*(?:[a-zA-Z_][\\w\\.\\[\\]]*\\s+)+?)([a-zA-Z_]\\w*)(\\s*)(\\()', bygroups(using(this), Name.Function, Whitespace, Operator)), ('[^\\S\\n]+', Whitespace), ('(//.*?)(\\n)', bygroups(Comment.Single, Whitespace)), ('/\\*.*?\\*/', Comment.Multiline), ('@[a-zA-Z_][\\w\\.]*', Name.Decorator), ('(and|break|else|foreach|if|in|not|or|reverse)\\b', Keyword), ('(as|call|define)\\b', Keyword.Declaration), ('(true|false|null)\\b', Keyword.Constant), ('(template)(\\s+)', bygroups(Keyword.Declaration, Whitespace), 'template'), ('(import)(\\s+)', bygroups(Keyword.Namespace, Whitespace), 'import'), ('"(\\\\\\\\|\\\\[^\\\\]|[^"\\\\])*"', String.Double), ("'(\\\\\\\\|\\\\[^\\\\]|[^'\\\\])*'", String.Single), ('(\\.)([a-zA-Z_]\\w*)', bygroups(Operator, Name.Attribute)), ('[a-zA-Z_]\\w*:', Name.Label), ('[a-zA-Z_\\$]\\w*', Name), ('(isa|[.]{3}|[.]{2}|[=#!<>+-/%&;,.\\*\\\\\\(\\)\\[\\]\\{\\}])', Operator), ('[0-9][0-9]*\\.[0-9]+([eE][0-9]+)?[fd]?', Number.Float), ('0x[0-9a-fA-F]+', Number.Hex), ('[0-9]+L?', Number.Integer), ('\\n', Whitespace)], 'template': [('[a-zA-Z_]\\w*', Name.Class, '#pop')], 'import': [('[\\w.]+\\*?', Name.Namespace, '#pop')]}



class CeylonLexer(RegexLexer):
    """
    For Ceylon source code.
    """
    name = 'Ceylon'
    url = 'http://ceylon-lang.org/'
    aliases = ['ceylon']
    filenames = ['*.ceylon']
    mimetypes = ['text/x-ceylon']
    version_added = '1.6'
    flags = re.MULTILINE | re.DOTALL
    _ws = '(?:\\s|//.*?\\n|/[*].*?[*]/)+'
    tokens = {'root': [('^(\\s*(?:[a-zA-Z_][\\w.\\[\\]]*\\s+)+?)([a-zA-Z_]\\w*)(\\s*)(\\()', bygroups(using(this), Name.Function, Whitespace, Operator)), ('[^\\S\\n]+', Whitespace), ('(//.*?)(\\n)', bygroups(Comment.Single, Whitespace)), ('/\\*', Comment.Multiline, 'comment'), ('(shared|abstract|formal|default|actual|variable|deprecated|small|late|literal|doc|by|see|throws|optional|license|tagged|final|native|annotation|sealed)\\b', Name.Decorator), ('(break|case|catch|continue|else|finally|for|in|if|return|switch|this|throw|try|while|is|exists|dynamic|nonempty|then|outer|assert|let)\\b', Keyword), ('(abstracts|extends|satisfies|super|given|of|out|assign)\\b', Keyword.Declaration), ('(function|value|void|new)\\b', Keyword.Type), ('(assembly|module|package)(\\s+)', bygroups(Keyword.Namespace, Whitespace)), ('(true|false|null)\\b', Keyword.Constant), ('(class|interface|object|alias)(\\s+)', bygroups(Keyword.Declaration, Whitespace), 'class'), ('(import)(\\s+)', bygroups(Keyword.Namespace, Whitespace), 'import'), ('"(\\\\\\\\|\\\\[^\\\\]|[^"\\\\])*"', String), ("'\\\\.'|'[^\\\\]'|'\\\\\\{#[0-9a-fA-F]{4}\\}'", String.Char), ('(\\.)([a-z_]\\w*)', bygroups(Operator, Name.Attribute)), ('[a-zA-Z_]\\w*:', Name.Label), ('[a-zA-Z_]\\w*', Name), ('[~^*!%&\\[\\](){}<>|+=:;,./?-]', Operator), ('\\d{1,3}(_\\d{3})+\\.\\d{1,3}(_\\d{3})+[kMGTPmunpf]?', Number.Float), ('\\d{1,3}(_\\d{3})+\\.[0-9]+([eE][+-]?[0-9]+)?[kMGTPmunpf]?', Number.Float), ('[0-9][0-9]*\\.\\d{1,3}(_\\d{3})+[kMGTPmunpf]?', Number.Float), ('[0-9][0-9]*\\.[0-9]+([eE][+-]?[0-9]+)?[kMGTPmunpf]?', Number.Float), ('#([0-9a-fA-F]{4})(_[0-9a-fA-F]{4})+', Number.Hex), ('#[0-9a-fA-F]+', Number.Hex), ('\\$([01]{4})(_[01]{4})+', Number.Bin), ('\\$[01]+', Number.Bin), ('\\d{1,3}(_\\d{3})+[kMGTP]?', Number.Integer), ('[0-9]+[kMGTP]?', Number.Integer), ('\\n', Whitespace)], 'class': [('[A-Za-z_]\\w*', Name.Class, '#pop')], 'import': [('[a-z][\\w.]*', Name.Namespace, '#pop')], 'comment': [('[^*/]', Comment.Multiline), ('/\\*', Comment.Multiline, '#push'), ('\\*/', Comment.Multiline, '#pop'), ('[*/]', Comment.Multiline)]}



class KotlinLexer(RegexLexer):
    """
    For Kotlin source code.
    """
    name = 'Kotlin'
    url = 'http://kotlinlang.org/'
    aliases = ['kotlin']
    filenames = ['*.kt', '*.kts']
    mimetypes = ['text/x-kotlin']
    version_added = '1.5'
    flags = re.MULTILINE | re.DOTALL
    kt_name = '@?[_' + uni.combine('Lu', 'Ll', 'Lt', 'Lm', 'Nl') + ']' + '[' + uni.combine('Lu', 'Ll', 'Lt', 'Lm', 'Nl', 'Nd', 'Pc', 'Cf', 'Mn', 'Mc') + ']*'
    kt_space_name = '@?[_' + uni.combine('Lu', 'Ll', 'Lt', 'Lm', 'Nl') + ']' + '[' + uni.combine('Lu', 'Ll', 'Lt', 'Lm', 'Nl', 'Nd', 'Pc', 'Cf', 'Mn', 'Mc', 'Zs') + "\\'~!%^&*()+=|\\[\\]:;,.<>/\\?-]*"
    kt_id = '(' + kt_name + '|`' + kt_space_name + '`)'
    modifiers = 'actual|abstract|annotation|companion|const|crossinline|data|enum|expect|external|final|infix|inline|inner|internal|lateinit|noinline|open|operator|override|private|protected|public|sealed|suspend|tailrec|value'
    tokens = {'root': [('[^\\S\\n]+', Whitespace), ('\\s+', Whitespace), ('\\\\$', String.Escape), ('\\n', Whitespace), ('(//.*?)(\\n)', bygroups(Comment.Single, Whitespace)), ('^(#!/.+?)(\\n)', bygroups(Comment.Single, Whitespace)), ('/[*].*?[*]/', Comment.Multiline), ('as\\?', Keyword), ('(as|break|by|catch|constructor|continue|do|dynamic|else|finally|get|for|if|init|[!]*in|[!]*is|out|reified|return|set|super|this|throw|try|typealias|typeof|vararg|when|where|while)\\b', Keyword), ('it\\b', Name.Builtin), (words(('Boolean?', 'Byte?', 'Char?', 'Double?', 'Float?', 'Int?', 'Long?', 'Short?', 'String?', 'Any?', 'Unit?')), Keyword.Type), (words(('Boolean', 'Byte', 'Char', 'Double', 'Float', 'Int', 'Long', 'Short', 'String', 'Any', 'Unit'), suffix='\\b'), Keyword.Type), ('(true|false|null)\\b', Keyword.Constant), ('(package|import)(\\s+)(\\S+)', bygroups(Keyword, Whitespace, Name.Namespace)), ('(\\?\\.)((?:[^\\W\\d]|\\$)[\\w$]*)', bygroups(Operator, Name.Attribute)), ('(\\.)((?:[^\\W\\d]|\\$)[\\w$]*)', bygroups(Punctuation, Name.Attribute)), ('@[^\\W\\d][\\w.]*', Name.Decorator), ('[^\\W\\d][\\w.]+@', Name.Decorator), ('(object)(\\s+)(:)(\\s+)', bygroups(Keyword, Whitespace, Punctuation, Whitespace), 'class'), ('((?:(?:' + modifiers + '|fun)\\s+)*)(class|interface|object)(\\s+)', bygroups(using(this, state='modifiers'), Keyword.Declaration, Whitespace), 'class'), ('(var|val)(\\s+)(\\()', bygroups(Keyword.Declaration, Whitespace, Punctuation), 'destructuring_assignment'), ('((?:(?:' + modifiers + ')\\s+)*)(var|val)(\\s+)', bygroups(using(this, state='modifiers'), Keyword.Declaration, Whitespace), 'variable'), ('((?:(?:' + modifiers + ')\\s+)*)(fun)(\\s+)', bygroups(using(this, state='modifiers'), Keyword.Declaration, Whitespace), 'function'), ('::|!!|\\?[:.]', Operator), ('[~^*!%&\\[\\]<>|+=/?-]', Operator), ('[{}();:.,]', Punctuation), ('"""', String, 'multiline_string'), ('"', String, 'string'), ("'\\\\.'|'[^\\\\]'", String.Char), ('[0-9](\\.[0-9]*)?([eE][+-][0-9]+)?[flFL]?|0[xX][0-9a-fA-F]+[Ll]?', Number), ('' + kt_id + '((\\?[^.])?)', Name)], 'class': [(kt_id, Name.Class, '#pop')], 'variable': [(kt_id, Name.Variable, '#pop')], 'destructuring_assignment': [(',', Punctuation), ('\\s+', Whitespace), (kt_id, Name.Variable), ('(:)(\\s+)(' + kt_id + ')', bygroups(Punctuation, Whitespace, Name)), ('<', Operator, 'generic'), ('\\)', Punctuation, '#pop')], 'function': [('<', Operator, 'generic'), ('' + kt_id + '(\\.)' + kt_id, bygroups(Name, Punctuation, Name.Function), '#pop'), (kt_id, Name.Function, '#pop')], 'generic': [('(>)(\\s*)', bygroups(Operator, Whitespace), '#pop'), (':', Punctuation), ('(reified|out|in)\\b', Keyword), (',', Punctuation), ('\\s+', Whitespace), (kt_id, Name)], 'modifiers': [('\\w+', Keyword.Declaration), ('\\s+', Whitespace), default('#pop')], 'string': [('"', String, '#pop'), include('string_common')], 'multiline_string': [('"""', String, '#pop'), ('"', String), include('string_common')], 'string_common': [('\\\\\\\\', String), ('\\\\"', String), ('\\\\', String), ('\\$\\{', String.Interpol, 'interpolation'), ('(\\$)(\\w+)', bygroups(String.Interpol, Name)), ('[^\\\\"$]+', String)], 'interpolation': [('"', String), ('\\$\\{', String.Interpol, 'interpolation'), ('\\{', Punctuation, 'scope'), ('\\}', String.Interpol, '#pop'), include('root')], 'scope': [('\\{', Punctuation, 'scope'), ('\\}', Punctuation, '#pop'), include('root')]}



class XtendLexer(RegexLexer):
    """
    For Xtend source code.
    """
    name = 'Xtend'
    url = 'https://www.eclipse.org/xtend/'
    aliases = ['xtend']
    filenames = ['*.xtend']
    mimetypes = ['text/x-xtend']
    version_added = '1.6'
    flags = re.MULTILINE | re.DOTALL
    tokens = {'root': [('^(\\s*(?:[a-zA-Z_][\\w.\\[\\]]*\\s+)+?)([a-zA-Z_$][\\w$]*)(\\s*)(\\()', bygroups(using(this), Name.Function, Whitespace, Operator)), ('[^\\S\\n]+', Whitespace), ('(//.*?)(\\n)', bygroups(Comment.Single, Whitespace)), ('/\\*.*?\\*/', Comment.Multiline), ('@[a-zA-Z_][\\w.]*', Name.Decorator), ('(assert|break|case|catch|continue|default|do|else|finally|for|if|goto|instanceof|new|return|switch|this|throw|try|while|IF|ELSE|ELSEIF|ENDIF|FOR|ENDFOR|SEPARATOR|BEFORE|AFTER)\\b', Keyword), ('(def|abstract|const|enum|extends|final|implements|native|private|protected|public|static|strictfp|super|synchronized|throws|transient|volatile|val|var)\\b', Keyword.Declaration), ('(boolean|byte|char|double|float|int|long|short|void)\\b', Keyword.Type), ('(package)(\\s+)', bygroups(Keyword.Namespace, Whitespace)), ('(true|false|null)\\b', Keyword.Constant), ('(class|interface)(\\s+)', bygroups(Keyword.Declaration, Whitespace), 'class'), ('(import)(\\s+)', bygroups(Keyword.Namespace, Whitespace), 'import'), ("(''')", String, 'template'), ('(\\u00BB)', String, 'template'), ('"(\\\\\\\\|\\\\[^\\\\]|[^"\\\\])*"', String.Double), ("'(\\\\\\\\|\\\\[^\\\\]|[^'\\\\])*'", String.Single), ('[a-zA-Z_]\\w*:', Name.Label), ('[a-zA-Z_$]\\w*', Name), ('[~^*!%&\\[\\](){}<>\\|+=:;,./?-]', Operator), ('[0-9][0-9]*\\.[0-9]+([eE][0-9]+)?[fd]?', Number.Float), ('0x[0-9a-fA-F]+', Number.Hex), ('[0-9]+L?', Number.Integer), ('\\n', Whitespace)], 'class': [('[a-zA-Z_]\\w*', Name.Class, '#pop')], 'import': [('[\\w.]+\\*?', Name.Namespace, '#pop')], 'template': [("'''", String, '#pop'), ('\\u00AB', String, '#pop'), ('.', String)]}



class PigLexer(RegexLexer):
    """
    For Pig Latin source code.
    """
    name = 'Pig'
    url = 'https://pig.apache.org/'
    aliases = ['pig']
    filenames = ['*.pig']
    mimetypes = ['text/x-pig']
    version_added = '2.0'
    flags = re.MULTILINE | re.IGNORECASE
    tokens = {'root': [('\\s+', Whitespace), ('--.*', Comment), ('/\\*[\\w\\W]*?\\*/', Comment.Multiline), ('\\\\$', String.Escape), ('\\\\', Text), ("\\'(?:\\\\[ntbrf\\\\\\']|\\\\u[0-9a-f]{4}|[^\\'\\\\\\n\\r])*\\'", String), include('keywords'), include('types'), include('builtins'), include('punct'), include('operators'), ('[0-9]*\\.[0-9]+(e[0-9]+)?[fd]?', Number.Float), ('0x[0-9a-f]+', Number.Hex), ('[0-9]+L?', Number.Integer), ('\\n', Whitespace), ('([a-z_]\\w*)(\\s*)(\\()', bygroups(Name.Function, Whitespace, Punctuation)), ('[()#:]', Text), ('[^(:#\\\'")\\s]+', Text), ('\\S+\\s+', Text)], 'keywords': [('(assert|and|any|all|arrange|as|asc|bag|by|cache|CASE|cat|cd|cp|%declare|%default|define|dense|desc|describe|distinct|du|dump|eval|exex|explain|filter|flatten|foreach|full|generate|group|help|if|illustrate|import|inner|input|into|is|join|kill|left|limit|load|ls|map|matches|mkdir|mv|not|null|onschema|or|order|outer|output|parallel|pig|pwd|quit|register|returns|right|rm|rmf|rollup|run|sample|set|ship|split|stderr|stdin|stdout|store|stream|through|union|using|void)\\b', Keyword)], 'builtins': [('(AVG|BinStorage|cogroup|CONCAT|copyFromLocal|copyToLocal|COUNT|cross|DIFF|MAX|MIN|PigDump|PigStorage|SIZE|SUM|TextLoader|TOKENIZE)\\b', Name.Builtin)], 'types': [('(bytearray|BIGINTEGER|BIGDECIMAL|chararray|datetime|double|float|int|long|tuple)\\b', Keyword.Type)], 'punct': [('[;(){}\\[\\]]', Punctuation)], 'operators': [('[#=,./%+\\-?]', Operator), ('(eq|gt|lt|gte|lte|neq|matches)\\b', Operator), ('(==|<=|<|>=|>|!=)', Operator)]}



class GoloLexer(RegexLexer):
    """
    For Golo source code.
    """
    name = 'Golo'
    url = 'http://golo-lang.org/'
    filenames = ['*.golo']
    aliases = ['golo']
    version_added = '2.0'
    tokens = {'root': [('[^\\S\\n]+', Whitespace), ('#.*$', Comment), ('(\\^|\\.\\.\\.|:|\\?:|->|==|!=|=|\\+|\\*|%|/|<=|<|>=|>|=|\\.)', Operator), ('(?<=[^-])(-)(?=[^-])', Operator), ('(?<=[^`])(is|isnt|and|or|not|oftype|in|orIfNull)\\b', Operator.Word), ('[]{}|(),[]', Punctuation), ('(module|import)(\\s+)', bygroups(Keyword.Namespace, Whitespace), 'modname'), ('\\b([a-zA-Z_][\\w$.]*)(::)', bygroups(Name.Namespace, Punctuation)), ('\\b([a-zA-Z_][\\w$]*(?:\\.[a-zA-Z_][\\w$]*)+)\\b', Name.Namespace), ('(let|var)(\\s+)', bygroups(Keyword.Declaration, Whitespace), 'varname'), ('(struct)(\\s+)', bygroups(Keyword.Declaration, Whitespace), 'structname'), ('(function)(\\s+)', bygroups(Keyword.Declaration, Whitespace), 'funcname'), ('(null|true|false)\\b', Keyword.Constant), ('(augment|pimp|if|else|case|match|return|case|when|then|otherwise|while|for|foreach|try|catch|finally|throw|local|continue|break)\\b', Keyword), ('(map|array|list|set|vector|tuple)(\\[)', bygroups(Name.Builtin, Punctuation)), ('(print|println|readln|raise|fun|asInterfaceInstance)\\b', Name.Builtin), ('(`?[a-zA-Z_][\\w$]*)(\\()', bygroups(Name.Function, Punctuation)), ('-?[\\d_]*\\.[\\d_]*([eE][+-]?\\d[\\d_]*)?F?', Number.Float), ('0[0-7]+j?', Number.Oct), ('0[xX][a-fA-F0-9]+', Number.Hex), ('-?\\d[\\d_]*L', Number.Integer.Long), ('-?\\d[\\d_]*', Number.Integer), ('`?[a-zA-Z_][\\w$]*', Name), ('@[a-zA-Z_][\\w$.]*', Name.Decorator), ('"""', String, combined('stringescape', 'triplestring')), ('"', String, combined('stringescape', 'doublestring')), ("'", String, combined('stringescape', 'singlestring')), ('----((.|\\n)*?)----', String.Doc)], 'funcname': [('`?[a-zA-Z_][\\w$]*', Name.Function, '#pop')], 'modname': [('[a-zA-Z_][\\w$.]*\\*?', Name.Namespace, '#pop')], 'structname': [('`?[\\w.]+\\*?', Name.Class, '#pop')], 'varname': [('`?[a-zA-Z_][\\w$]*', Name.Variable, '#pop')], 'string': [('[^\\\\\\\'"\\n]+', String), ('[\\\'"\\\\]', String)], 'stringescape': [('\\\\([\\\\abfnrtv"\\\']|\\n|N\\{.*?\\}|u[a-fA-F0-9]{4}|U[a-fA-F0-9]{8}|x[a-fA-F0-9]{2}|[0-7]{1,3})', String.Escape)], 'triplestring': [('"""', String, '#pop'), include('string'), ('\\n', String)], 'doublestring': [('"', String.Double, '#pop'), include('string')], 'singlestring': [("'", String, '#pop'), include('string')], 'operators': [('[#=,./%+\\-?]', Operator), ('(eq|gt|lt|gte|lte|neq|matches)\\b', Operator), ('(==|<=|<|>=|>|!=)', Operator)]}



class JasminLexer(RegexLexer):
    """
    For Jasmin assembly code.
    """
    name = 'Jasmin'
    url = 'http://jasmin.sourceforge.net/'
    aliases = ['jasmin', 'jasminxt']
    filenames = ['*.j']
    version_added = '2.0'
    _whitespace = ' \\n\\t\\r'
    _ws = f'(?:[{_whitespace}]+)'
    _separator = f'{_whitespace}:='
    _break = f'(?=[{_separator}]|$)'
    _name = f'[^{_separator}]+'
    _unqualified_name = f'(?:[^{_separator}.;\\[/]+)'
    tokens = {'default': [('\\n', Whitespace, '#pop'), ("'", String.Single, ('#pop', 'quote')), ('"', String.Double, 'string'), ('=', Punctuation), (':', Punctuation, 'label'), (_ws, Whitespace), (';.*', Comment.Single), (f'(\\$[-+])?0x-?[\\da-fA-F]+{_break}', Number.Hex), (f'(\\$[-+]|\\+)?-?\\d+{_break}', Number.Integer), (f'-?(\\d+\\.\\d*|\\.\\d+)([eE][-+]?\\d+)?[fFdD]?[\\x00-\\x08\\x0b\\x0c\\x0e-\\x1f]*{_break}', Number.Float), (f'\\${_name}', Name.Variable), (f'\\.annotation{_break}', Keyword.Reserved, 'annotation'), (f'(\\.attribute|\\.bytecode|\\.debug|\\.deprecated|\\.enclosing|\\.interface|\\.line|\\.signature|\\.source|\\.stack|\\.var|abstract|annotation|bridge|class|default|enum|field|final|fpstrict|interface|native|private|protected|public|signature|static|synchronized|synthetic|transient|varargs|volatile){_break}', Keyword.Reserved), (f'\\.catch{_break}', Keyword.Reserved, 'caught-exception'), (f'(\\.class|\\.implements|\\.inner|\\.super|inner|invisible|invisibleparam|outer|visible|visibleparam){_break}', Keyword.Reserved, 'class/convert-dots'), (f'\\.field{_break}', Keyword.Reserved, ('descriptor/convert-dots', 'field')), (f'(\\.end|\\.limit|use){_break}', Keyword.Reserved, 'no-verification'), (f'\\.method{_break}', Keyword.Reserved, 'method'), (f'\\.set{_break}', Keyword.Reserved, 'var'), (f'\\.throws{_break}', Keyword.Reserved, 'exception'), (f'(from|offset|to|using){_break}', Keyword.Reserved, 'label'), (f'is{_break}', Keyword.Reserved, ('descriptor/convert-dots', 'var')), (f'(locals|stack){_break}', Keyword.Reserved, 'verification'), (f'method{_break}', Keyword.Reserved, 'enclosing-method'), (words(('aaload', 'aastore', 'aconst_null', 'aload', 'aload_0', 'aload_1', 'aload_2', 'aload_3', 'aload_w', 'areturn', 'arraylength', 'astore', 'astore_0', 'astore_1', 'astore_2', 'astore_3', 'astore_w', 'athrow', 'baload', 'bastore', 'bipush', 'breakpoint', 'caload', 'castore', 'd2f', 'd2i', 'd2l', 'dadd', 'daload', 'dastore', 'dcmpg', 'dcmpl', 'dconst_0', 'dconst_1', 'ddiv', 'dload', 'dload_0', 'dload_1', 'dload_2', 'dload_3', 'dload_w', 'dmul', 'dneg', 'drem', 'dreturn', 'dstore', 'dstore_0', 'dstore_1', 'dstore_2', 'dstore_3', 'dstore_w', 'dsub', 'dup', 'dup2', 'dup2_x1', 'dup2_x2', 'dup_x1', 'dup_x2', 'f2d', 'f2i', 'f2l', 'fadd', 'faload', 'fastore', 'fcmpg', 'fcmpl', 'fconst_0', 'fconst_1', 'fconst_2', 'fdiv', 'fload', 'fload_0', 'fload_1', 'fload_2', 'fload_3', 'fload_w', 'fmul', 'fneg', 'frem', 'freturn', 'fstore', 'fstore_0', 'fstore_1', 'fstore_2', 'fstore_3', 'fstore_w', 'fsub', 'i2b', 'i2c', 'i2d', 'i2f', 'i2l', 'i2s', 'iadd', 'iaload', 'iand', 'iastore', 'iconst_0', 'iconst_1', 'iconst_2', 'iconst_3', 'iconst_4', 'iconst_5', 'iconst_m1', 'idiv', 'iinc', 'iinc_w', 'iload', 'iload_0', 'iload_1', 'iload_2', 'iload_3', 'iload_w', 'imul', 'ineg', 'int2byte', 'int2char', 'int2short', 'ior', 'irem', 'ireturn', 'ishl', 'ishr', 'istore', 'istore_0', 'istore_1', 'istore_2', 'istore_3', 'istore_w', 'isub', 'iushr', 'ixor', 'l2d', 'l2f', 'l2i', 'ladd', 'laload', 'land', 'lastore', 'lcmp', 'lconst_0', 'lconst_1', 'ldc2_w', 'ldiv', 'lload', 'lload_0', 'lload_1', 'lload_2', 'lload_3', 'lload_w', 'lmul', 'lneg', 'lookupswitch', 'lor', 'lrem', 'lreturn', 'lshl', 'lshr', 'lstore', 'lstore_0', 'lstore_1', 'lstore_2', 'lstore_3', 'lstore_w', 'lsub', 'lushr', 'lxor', 'monitorenter', 'monitorexit', 'nop', 'pop', 'pop2', 'ret', 'ret_w', 'return', 'saload', 'sastore', 'sipush', 'swap'), suffix=_break), Keyword.Reserved), (f'(anewarray|checkcast|instanceof|ldc|ldc_w|new){_break}', Keyword.Reserved, 'class/no-dots'), (f'invoke(dynamic|interface|nonvirtual|special|static|virtual){_break}', Keyword.Reserved, 'invocation'), (f'(getfield|putfield){_break}', Keyword.Reserved, ('descriptor/no-dots', 'field')), (f'(getstatic|putstatic){_break}', Keyword.Reserved, ('descriptor/no-dots', 'static')), (words(('goto', 'goto_w', 'if_acmpeq', 'if_acmpne', 'if_icmpeq', 'if_icmpge', 'if_icmpgt', 'if_icmple', 'if_icmplt', 'if_icmpne', 'ifeq', 'ifge', 'ifgt', 'ifle', 'iflt', 'ifne', 'ifnonnull', 'ifnull', 'jsr', 'jsr_w'), suffix=_break), Keyword.Reserved, 'label'), (f'(multianewarray|newarray){_break}', Keyword.Reserved, 'descriptor/convert-dots'), (f'tableswitch{_break}', Keyword.Reserved, 'table')], 'quote': [("'", String.Single, '#pop'), ('\\\\u[\\da-fA-F]{4}', String.Escape), ("[^'\\\\]+", String.Single)], 'string': [('"', String.Double, '#pop'), ('\\\\([nrtfb"\\\'\\\\]|u[\\da-fA-F]{4}|[0-3]?[0-7]{1,2})', String.Escape), ('[^"\\\\]+', String.Double)], 'root': [('\\n+', Whitespace), ("'", String.Single, 'quote'), include('default'), (f'({_name})([ \\t\\r]*)(:)', bygroups(Name.Label, Whitespace, Punctuation)), (_name, String.Other)], 'annotation': [('\\n', Whitespace, ('#pop', 'annotation-body')), (f'default{_break}', Keyword.Reserved, ('#pop', 'annotation-default')), include('default')], 'annotation-body': [('\\n+', Whitespace), (f'\\.end{_break}', Keyword.Reserved, '#pop'), include('default'), (_name, String.Other, ('annotation-items', 'descriptor/no-dots'))], 'annotation-default': [('\\n+', Whitespace), (f'\\.end{_break}', Keyword.Reserved, '#pop'), include('default'), default(('annotation-items', 'descriptor/no-dots'))], 'annotation-items': [("'", String.Single, 'quote'), include('default'), (_name, String.Other)], 'caught-exception': [(f'all{_break}', Keyword, '#pop'), include('exception')], 'class/convert-dots': [include('default'), (f'(L)((?:{_unqualified_name}[/.])*)({_name})(;)', bygroups(Keyword.Type, Name.Namespace, Name.Class, Punctuation), '#pop'), (f'((?:{_unqualified_name}[/.])*)({_name})', bygroups(Name.Namespace, Name.Class), '#pop')], 'class/no-dots': [include('default'), ('\\[+', Punctuation, ('#pop', 'descriptor/no-dots')), (f'(L)((?:{_unqualified_name}/)*)({_name})(;)', bygroups(Keyword.Type, Name.Namespace, Name.Class, Punctuation), '#pop'), (f'((?:{_unqualified_name}/)*)({_name})', bygroups(Name.Namespace, Name.Class), '#pop')], 'descriptor/convert-dots': [include('default'), ('\\[+', Punctuation), (f'(L)((?:{_unqualified_name}[/.])*)({_name}?)(;)', bygroups(Keyword.Type, Name.Namespace, Name.Class, Punctuation), '#pop'), (f'[^{_separator}\\[)L]+', Keyword.Type, '#pop'), default('#pop')], 'descriptor/no-dots': [include('default'), ('\\[+', Punctuation), (f'(L)((?:{_unqualified_name}/)*)({_name})(;)', bygroups(Keyword.Type, Name.Namespace, Name.Class, Punctuation), '#pop'), (f'[^{_separator}\\[)L]+', Keyword.Type, '#pop'), default('#pop')], 'descriptors/convert-dots': [('\\)', Punctuation, '#pop'), default('descriptor/convert-dots')], 'enclosing-method': [(_ws, Whitespace), (f'(?=[^{_separator}]*\\()', Text, ('#pop', 'invocation')), default(('#pop', 'class/convert-dots'))], 'exception': [include('default'), (f'((?:{_unqualified_name}[/.])*)({_name})', bygroups(Name.Namespace, Name.Exception), '#pop')], 'field': [(f'static{_break}', Keyword.Reserved, ('#pop', 'static')), include('default'), (f'((?:{_unqualified_name}[/.](?=[^{_separator}]*[/.]))*)({_unqualified_name}[/.])?({_name})', bygroups(Name.Namespace, Name.Class, Name.Variable.Instance), '#pop')], 'invocation': [include('default'), (f'((?:{_unqualified_name}[/.](?=[^{_separator}(]*[/.]))*)({_unqualified_name}[/.])?({_name})(\\()', bygroups(Name.Namespace, Name.Class, Name.Function, Punctuation), ('#pop', 'descriptor/convert-dots', 'descriptors/convert-dots', 'descriptor/convert-dots'))], 'label': [include('default'), (_name, Name.Label, '#pop')], 'method': [include('default'), (f'({_name})(\\()', bygroups(Name.Function, Punctuation), ('#pop', 'descriptor/convert-dots', 'descriptors/convert-dots', 'descriptor/convert-dots'))], 'no-verification': [(f'(locals|method|stack){_break}', Keyword.Reserved, '#pop'), include('default')], 'static': [include('default'), (f'((?:{_unqualified_name}[/.](?=[^{_separator}]*[/.]))*)({_unqualified_name}[/.])?({_name})', bygroups(Name.Namespace, Name.Class, Name.Variable.Class), '#pop')], 'table': [('\\n+', Whitespace), (f'default{_break}', Keyword.Reserved, '#pop'), include('default'), (_name, Name.Label)], 'var': [include('default'), (_name, Name.Variable, '#pop')], 'verification': [include('default'), (f'(Double|Float|Integer|Long|Null|Top|UninitializedThis){_break}', Keyword, '#pop'), (f'Object{_break}', Keyword, ('#pop', 'class/no-dots')), (f'Uninitialized{_break}', Keyword, ('#pop', 'label'))]}
    
    def analyse_text(text):
        score = 0
        if re.search('^\\s*\\.class\\s', text, re.MULTILINE):
            score += 0.5
            if re.search('^\\s*[a-z]+_[a-z]+\\b', text, re.MULTILINE):
                score += 0.3
        if re.search('^\\s*\\.(attribute|bytecode|debug|deprecated|enclosing|inner|interface|limit|set|signature|stack)\\b', text, re.MULTILINE):
            score += 0.6
        return min(score, 1.0)



class SarlLexer(RegexLexer):
    """
    For SARL source code.
    """
    name = 'SARL'
    url = 'http://www.sarl.io'
    aliases = ['sarl']
    filenames = ['*.sarl']
    mimetypes = ['text/x-sarl']
    version_added = '2.4'
    flags = re.MULTILINE | re.DOTALL
    tokens = {'root': [('^(\\s*(?:[a-zA-Z_][\\w.\\[\\]]*\\s+)+?)([a-zA-Z_$][\\w$]*)(\\s*)(\\()', bygroups(using(this), Name.Function, Whitespace, Operator)), ('[^\\S\\n]+', Whitespace), ('(//.*?)(\\n)', bygroups(Comment.Single, Whitespace)), ('/\\*.*?\\*/', Comment.Multiline), ('@[a-zA-Z_][\\w.]*', Name.Decorator), ('(as|break|case|catch|default|do|else|extends|extension|finally|fires|for|if|implements|instanceof|new|on|requires|return|super|switch|throw|throws|try|typeof|uses|while|with)\\b', Keyword), ('(abstract|def|dispatch|final|native|override|private|protected|public|static|strictfp|synchronized|transient|val|var|volatile)\\b', Keyword.Declaration), ('(boolean|byte|char|double|float|int|long|short|void)\\b', Keyword.Type), ('(package)(\\s+)', bygroups(Keyword.Namespace, Whitespace)), ('(false|it|null|occurrence|this|true|void)\\b', Keyword.Constant), ('(agent|annotation|artifact|behavior|capacity|class|enum|event|interface|skill|space)(\\s+)', bygroups(Keyword.Declaration, Whitespace), 'class'), ('(import)(\\s+)', bygroups(Keyword.Namespace, Whitespace), 'import'), ('"(\\\\\\\\|\\\\[^\\\\]|[^"\\\\])*"', String.Double), ("'(\\\\\\\\|\\\\[^\\\\]|[^'\\\\])*'", String.Single), ('[a-zA-Z_]\\w*:', Name.Label), ('[a-zA-Z_$]\\w*', Name), ('[~^*!%&\\[\\](){}<>\\|+=:;,./?-]', Operator), ('[0-9][0-9]*\\.[0-9]+([eE][0-9]+)?[fd]?', Number.Float), ('0x[0-9a-fA-F]+', Number.Hex), ('[0-9]+L?', Number.Integer), ('\\n', Whitespace)], 'class': [('[a-zA-Z_]\\w*', Name.Class, '#pop')], 'import': [('[\\w.]+\\*?', Name.Namespace, '#pop')]}


