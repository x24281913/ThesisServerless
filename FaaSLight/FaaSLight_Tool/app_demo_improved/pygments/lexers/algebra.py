"""
    pygments.lexers.algebra
    ~~~~~~~~~~~~~~~~~~~~~~~

    Lexers for computer algebra systems.

    :copyright: Copyright 2006-present by the Pygments team, see AUTHORS.
    :license: BSD, see LICENSE for details.
"""

import re
from pygments.lexer import Lexer, RegexLexer, bygroups, do_insertions, words
from pygments.token import Text, Comment, Operator, Keyword, Name, String, Number, Punctuation, Generic, Whitespace
__all__ = ['GAPLexer', 'GAPConsoleLexer', 'MathematicaLexer', 'MuPADLexer', 'BCLexer']


class GAPLexer(RegexLexer):
    """
    For GAP source code.
    """
    name = 'GAP'
    url = 'https://www.gap-system.org'
    aliases = ['gap']
    filenames = ['*.g', '*.gd', '*.gi', '*.gap']
    version_added = '2.0'
    tokens = {'root': [('#.*$', Comment.Single), ('"(?:[^"\\\\]|\\\\.)*"', String), ('\\(|\\)|\\[|\\]|\\{|\\}', Punctuation), ('(?x)\\b(?:\n                if|then|elif|else|fi|\n                for|while|do|od|\n                repeat|until|\n                break|continue|\n                function|local|return|end|\n                rec|\n                quit|QUIT|\n                IsBound|Unbind|\n                TryNextMethod|\n                Info|Assert\n              )\\b', Keyword), ('(?x)\\b(?:\n                true|false|fail|infinity\n              )\\b', Name.Constant), ('(?x)\\b(?:\n                (Declare|Install)([A-Z][A-Za-z]+)|\n                   BindGlobal|BIND_GLOBAL\n              )\\b', Name.Builtin), ('\\.|,|:=|;|=|\\+|-|\\*|/|\\^|>|<', Operator), ('(?x)\\b(?:\n                and|or|not|mod|in\n              )\\b', Operator.Word), ('(?x)\n              (?:\\w+|`[^`]*`)\n              (?:::\\w+|`[^`]*`)*', Name.Variable), ('[0-9]+(?:\\.[0-9]*)?(?:e[0-9]+)?', Number), ('\\.[0-9]+(?:e[0-9]+)?', Number), ('.', Text)]}
    
    def analyse_text(text):
        score = 0.0
        if re.search('(InstallTrueMethod|Declare(Attribute|Category|Filter|Operation' + '|GlobalFunction|Synonym|SynonymAttr|Property))', text):
            score += 0.7
        if re.search('(DeclareRepresentation|Install(GlobalFunction|Method|' + 'ImmediateMethod|OtherMethod)|New(Family|Type)|Objectify)', text):
            score += 0.7
        return min(score, 1.0)



class GAPConsoleLexer(Lexer):
    """
    For GAP console sessions. Modeled after JuliaConsoleLexer.
    """
    name = 'GAP session'
    aliases = ['gap-console', 'gap-repl']
    filenames = ['*.tst']
    url = 'https://www.gap-system.org'
    version_added = '2.14'
    _example = 'gap-repl/euclidean.tst'
    
    def get_tokens_unprocessed(self, text):
        gaplexer = GAPLexer(**self.options)
        start = 0
        curcode = ''
        insertions = []
        output = False
        error = False
        for line in text.splitlines(keepends=True):
            if (line.startswith('gap> ') or line.startswith('brk> ')):
                insertions.append((len(curcode), [(0, Generic.Prompt, line[:5])]))
                curcode += line[5:]
                output = False
                error = False
            elif (not output and line.startswith('> ')):
                insertions.append((len(curcode), [(0, Generic.Prompt, line[:2])]))
                curcode += line[2:]
            else:
                if curcode:
                    yield from do_insertions(insertions, gaplexer.get_tokens_unprocessed(curcode))
                    curcode = ''
                    insertions = []
                if (line.startswith('Error, ') or error):
                    yield (start, Generic.Error, line)
                    error = True
                else:
                    yield (start, Generic.Output, line)
                output = True
            start += len(line)
        if curcode:
            yield from do_insertions(insertions, gaplexer.get_tokens_unprocessed(curcode))
    
    def analyse_text(text):
        if re.search('^gap> ', text):
            return 0.9
        else:
            return 0.0



class MathematicaLexer(RegexLexer):
    """
    Lexer for Mathematica source code.
    """
    name = 'Mathematica'
    url = 'https://www.wolfram.com/language/'
    aliases = ['mathematica', 'mma', 'nb', 'wl', 'wolfram']
    filenames = ['*.nb', '*.cdf', '*.nbp', '*.ma', '*.wl', '*.wls']
    mimetypes = ['application/mathematica', 'application/vnd.wolfram.mathematica', 'application/vnd.wolfram.mathematica.package', 'application/vnd.wolfram.cdf', 'application/vnd.wolfram.wl']
    version_added = '2.0'
    operators = (';;', '=', '=.', '!===', ':=', '->', ':>', '/.', '+', '-', '*', '/', '^', '&&', '||', '!', '<>', '|', '/;', '?', '@', '//', '/@', '@@', '@@@', '~~', '===', '&', '<', '>', '<=', '>=')
    punctuation = (',', ';', '(', ')', '[', ']', '{', '}')
    
    def _multi_escape(entries):
        return '({})'.format('|'.join((re.escape(entry) for entry in entries)))
    tokens = {'root': [('(?s)\\(\\*.*?\\*\\)', Comment), ('([a-zA-Z]+[A-Za-z0-9]*`)', Name.Namespace), ('([A-Za-z0-9]*_+[A-Za-z0-9]*)', Name.Variable), ('#\\d*', Name.Variable), ('([a-zA-Z]+[a-zA-Z0-9]*)', Name), ('-?\\d+\\.\\d*', Number.Float), ('-?\\d*\\.\\d+', Number.Float), ('-?\\d+', Number.Integer), (words(operators), Operator), (words(punctuation), Punctuation), ('".*?"', String), ('\\s+', Text.Whitespace)]}



class MuPADLexer(RegexLexer):
    """
    A MuPAD lexer.
    Contributed by Christopher Creutzig <christopher@creutzig.de>.
    """
    name = 'MuPAD'
    url = 'http://www.mupad.com'
    aliases = ['mupad']
    filenames = ['*.mu']
    version_added = '0.8'
    tokens = {'root': [('//.*?$', Comment.Single), ('/\\*', Comment.Multiline, 'comment'), ('"(?:[^"\\\\]|\\\\.)*"', String), ('\\(|\\)|\\[|\\]|\\{|\\}', Punctuation), ('(?x)\\b(?:\n                next|break|end|\n                axiom|end_axiom|category|end_category|domain|end_domain|inherits|\n                if|%if|then|elif|else|end_if|\n                case|of|do|otherwise|end_case|\n                while|end_while|\n                repeat|until|end_repeat|\n                for|from|to|downto|step|end_for|\n                proc|local|option|save|begin|end_proc|\n                delete|frame\n              )\\b', Keyword), ('(?x)\\b(?:\n                DOM_ARRAY|DOM_BOOL|DOM_COMPLEX|DOM_DOMAIN|DOM_EXEC|DOM_EXPR|\n                DOM_FAIL|DOM_FLOAT|DOM_FRAME|DOM_FUNC_ENV|DOM_HFARRAY|DOM_IDENT|\n                DOM_INT|DOM_INTERVAL|DOM_LIST|DOM_NIL|DOM_NULL|DOM_POLY|DOM_PROC|\n                DOM_PROC_ENV|DOM_RAT|DOM_SET|DOM_STRING|DOM_TABLE|DOM_VAR\n              )\\b', Name.Class), ('(?x)\\b(?:\n                PI|EULER|E|CATALAN|\n                NIL|FAIL|undefined|infinity|\n                TRUE|FALSE|UNKNOWN\n              )\\b', Name.Constant), ('\\b(?:dom|procname)\\b', Name.Builtin.Pseudo), ("\\.|,|:|;|=|\\+|-|\\*|/|\\^|@|>|<|\\$|\\||!|\\'|%|~=", Operator), ('(?x)\\b(?:\n                and|or|not|xor|\n                assuming|\n                div|mod|\n                union|minus|intersect|in|subset\n              )\\b', Operator.Word), ('\\b(?:I|RDN_INF|RD_NINF|RD_NAN)\\b', Number), ('(?x)\n              ((?:[a-zA-Z_#][\\w#]*|`[^`]*`)\n              (?:::[a-zA-Z_#][\\w#]*|`[^`]*`)*)(\\s*)([(])', bygroups(Name.Function, Text, Punctuation)), ('(?x)\n              (?:[a-zA-Z_#][\\w#]*|`[^`]*`)\n              (?:::[a-zA-Z_#][\\w#]*|`[^`]*`)*', Name.Variable), ('[0-9]+(?:\\.[0-9]*)?(?:e[0-9]+)?', Number), ('\\.[0-9]+(?:e[0-9]+)?', Number), ('\\s+', Whitespace), ('.', Text)], 'comment': [('[^/*]+', Comment.Multiline), ('/\\*', Comment.Multiline, '#push'), ('\\*/', Comment.Multiline, '#pop'), ('[*/]', Comment.Multiline)]}



class BCLexer(RegexLexer):
    """
    A BC lexer.
    """
    name = 'BC'
    url = 'https://www.gnu.org/software/bc/'
    aliases = ['bc']
    filenames = ['*.bc']
    version_added = '2.1'
    tokens = {'root': [('/\\*', Comment.Multiline, 'comment'), ('"(?:[^"\\\\]|\\\\.)*"', String), ('[{}();,]', Punctuation), (words(('if', 'else', 'while', 'for', 'break', 'continue', 'halt', 'return', 'define', 'auto', 'print', 'read', 'length', 'scale', 'sqrt', 'limits', 'quit', 'warranty'), suffix='\\b'), Keyword), ('\\+\\+|--|\\|\\||&&|([-<>+*%\\^/!=])=?', Operator), ('[0-9]+(\\.[0-9]*)?', Number), ('\\.[0-9]+', Number), ('.', Text)], 'comment': [('[^*/]+', Comment.Multiline), ('\\*/', Comment.Multiline, '#pop'), ('[*/]', Comment.Multiline)]}


