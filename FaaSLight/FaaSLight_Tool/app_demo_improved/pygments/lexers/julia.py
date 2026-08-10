"""
    pygments.lexers.julia
    ~~~~~~~~~~~~~~~~~~~~~

    Lexers for the Julia language.

    :copyright: Copyright 2006-present by the Pygments team, see AUTHORS.
    :license: BSD, see LICENSE for details.
"""

from pygments.lexer import Lexer, RegexLexer, bygroups, do_insertions, words, include
from pygments.token import Text, Comment, Operator, Keyword, Name, String, Number, Punctuation, Generic, Whitespace
from pygments.util import shebang_matches
from pygments.lexers._julia_builtins import OPERATORS_LIST, DOTTED_OPERATORS_LIST, KEYWORD_LIST, BUILTIN_LIST, LITERAL_LIST
__all__ = ['JuliaLexer', 'JuliaConsoleLexer']
allowed_variable = '(?:[a-zA-Z_¡-\U0010ffff][a-zA-Z_0-9!¡-\U0010ffff]*)'
operator_suffixes = '[²³¹ʰʲʳʷʸˡˢˣᴬᴮᴰᴱᴳᴴᴵᴶᴷᴸᴹᴺᴼᴾᴿᵀᵁᵂᵃᵇᵈᵉᵍᵏᵐᵒᵖᵗᵘᵛᵝᵞᵟᵠᵡᵢᵣᵤᵥᵦᵧᵨᵩᵪᶜᶠᶥᶦᶫᶰᶸᶻᶿ′″‴‵‶‷⁗⁰ⁱ⁴⁵⁶⁷⁸⁹⁺⁻⁼⁽⁾ⁿ₀₁₂₃₄₅₆₇₈₉₊₋₌₍₎ₐₑₒₓₕₖₗₘₙₚₛₜⱼⱽ]*'


class JuliaLexer(RegexLexer):
    """
    For Julia source code.
    """
    name = 'Julia'
    url = 'https://julialang.org/'
    aliases = ['julia', 'jl']
    filenames = ['*.jl']
    mimetypes = ['text/x-julia', 'application/x-julia']
    version_added = '1.6'
    tokens = {'root': [('\\n', Whitespace), ('[^\\S\\n]+', Whitespace), ('#=', Comment.Multiline, 'blockcomment'), ('#.*$', Comment), ('[\\[\\](),;]', Punctuation), ('(' + allowed_variable + ')(\\s*)(:)(' + allowed_variable + ')', bygroups(Name, Whitespace, Operator, Name)), ('(?<![\\]):<>\\d.])(:' + allowed_variable + ')', String.Symbol), ('(?<=::)(\\s*)(' + allowed_variable + ')\\b(?![(\\[])', bygroups(Whitespace, Keyword.Type)), ('(' + allowed_variable + ')(\\s*)([<>]:)(\\s*)(' + allowed_variable + ')\\b(?![(\\[])', bygroups(Keyword.Type, Whitespace, Operator, Whitespace, Keyword.Type)), ('([<>]:)(\\s*)(' + allowed_variable + ')\\b(?![(\\[])', bygroups(Operator, Whitespace, Keyword.Type)), ('\\b(' + allowed_variable + ')(\\s*)([<>]:)', bygroups(Keyword.Type, Whitespace, Operator)), (words([*OPERATORS_LIST, *DOTTED_OPERATORS_LIST], suffix=operator_suffixes), Operator), (words(['.' + o for o in DOTTED_OPERATORS_LIST], suffix=operator_suffixes), Operator), (words(['...', '..']), Operator), ("'(\\\\.|\\\\[0-7]{1,3}|\\\\x[a-fA-F0-9]{1,3}|\\\\u[a-fA-F0-9]{1,4}|\\\\U[a-fA-F0-9]{1,6}|[^\\\\\\'\\n])'", String.Char), ("(?<=[.\\w)\\]])(\\'" + operator_suffixes + ')+', Operator), ('(raw)(""")', bygroups(String.Affix, String), 'tqrawstring'), ('(raw)(")', bygroups(String.Affix, String), 'rawstring'), ('(r)(""")', bygroups(String.Affix, String.Regex), 'tqregex'), ('(r)(")', bygroups(String.Affix, String.Regex), 'regex'), ('(' + allowed_variable + ')?(""")', bygroups(String.Affix, String), 'tqstring'), ('(' + allowed_variable + ')?(")', bygroups(String.Affix, String), 'string'), ('(' + allowed_variable + ')?(```)', bygroups(String.Affix, String.Backtick), 'tqcommand'), ('(' + allowed_variable + ')?(`)', bygroups(String.Affix, String.Backtick), 'command'), ('(' + allowed_variable + ')(\\{)', bygroups(Keyword.Type, Punctuation), 'curly'), ('(where)(\\s+)(' + allowed_variable + ')', bygroups(Keyword, Whitespace, Keyword.Type)), ('(\\{)', Punctuation, 'curly'), ('(abstract|primitive)([ \\t]+)(type\\b)([\\s()]+)(' + allowed_variable + ')', bygroups(Keyword, Whitespace, Keyword, Text, Keyword.Type)), ('(mutable(?=[ \\t]))?([ \\t]+)?(struct\\b)([\\s()]+)(' + allowed_variable + ')', bygroups(Keyword, Whitespace, Keyword, Text, Keyword.Type)), ('@' + allowed_variable, Name.Decorator), (words([*OPERATORS_LIST, '..', '.', *DOTTED_OPERATORS_LIST], prefix='@', suffix=operator_suffixes), Name.Decorator), (words(KEYWORD_LIST, suffix='\\b'), Keyword), (words(BUILTIN_LIST, suffix='\\b'), Keyword.Type), (words(LITERAL_LIST, suffix='\\b'), Name.Builtin), (allowed_variable, Name), ('(\\d+((_\\d+)+)?\\.(?!\\.)(\\d+((_\\d+)+)?)?|\\.\\d+((_\\d+)+)?)([eEf][+-]?[0-9]+)?', Number.Float), ('\\d+((_\\d+)+)?[eEf][+-]?[0-9]+', Number.Float), ('0x[a-fA-F0-9]+((_[a-fA-F0-9]+)+)?(\\.([a-fA-F0-9]+((_[a-fA-F0-9]+)+)?)?)?p[+-]?\\d+', Number.Float), ('0b[01]+((_[01]+)+)?', Number.Bin), ('0o[0-7]+((_[0-7]+)+)?', Number.Oct), ('0x[a-fA-F0-9]+((_[a-fA-F0-9]+)+)?', Number.Hex), ('\\d+((_\\d+)+)?', Number.Integer), (words(['.']), Operator)], 'blockcomment': [('[^=#]', Comment.Multiline), ('#=', Comment.Multiline, '#push'), ('=#', Comment.Multiline, '#pop'), ('[=#]', Comment.Multiline)], 'curly': [('\\{', Punctuation, '#push'), ('\\}', Punctuation, '#pop'), (allowed_variable, Keyword.Type), include('root')], 'tqrawstring': [('"""', String, '#pop'), ('([^"]|"[^"][^"])+', String)], 'rawstring': [('"', String, '#pop'), ('\\\\"', String.Escape), ('([^"\\\\]|\\\\[^"])+', String)], 'interp': [('\\$' + allowed_variable, String.Interpol), ('(\\$)(\\()', bygroups(String.Interpol, Punctuation), 'in-intp')], 'in-intp': [('\\(', Punctuation, '#push'), ('\\)', Punctuation, '#pop'), include('root')], 'string': [('(")(' + allowed_variable + '|\\d+)?', bygroups(String, String.Affix), '#pop'), ('\\\\([\\\\"\\\'$nrbtfav]|(x|u|U)[a-fA-F0-9]+|\\d+)', String.Escape), include('interp'), ('%[-#0 +]*([0-9]+|[*])?(\\.([0-9]+|[*]))?[hlL]?[E-GXc-giorsux%]', String.Interpol), ('[^"$%\\\\]+', String), ('.', String)], 'tqstring': [('(""")(' + allowed_variable + '|\\d+)?', bygroups(String, String.Affix), '#pop'), ('\\\\([\\\\"\\\'$nrbtfav]|(x|u|U)[a-fA-F0-9]+|\\d+)', String.Escape), include('interp'), ('[^"$%\\\\]+', String), ('.', String)], 'regex': [('(")([imsxa]*)?', bygroups(String.Regex, String.Affix), '#pop'), ('\\\\"', String.Regex), ('[^\\\\"]+', String.Regex)], 'tqregex': [('(""")([imsxa]*)?', bygroups(String.Regex, String.Affix), '#pop'), ('[^"]+', String.Regex)], 'command': [('(`)(' + allowed_variable + '|\\d+)?', bygroups(String.Backtick, String.Affix), '#pop'), ('\\\\[`$]', String.Escape), include('interp'), ('[^\\\\`$]+', String.Backtick), ('.', String.Backtick)], 'tqcommand': [('(```)(' + allowed_variable + '|\\d+)?', bygroups(String.Backtick, String.Affix), '#pop'), ('\\\\\\$', String.Escape), include('interp'), ('[^\\\\`$]+', String.Backtick), ('.', String.Backtick)]}
    
    def analyse_text(text):
        return shebang_matches(text, 'julia')



class JuliaConsoleLexer(Lexer):
    """
    For Julia console sessions. Modeled after MatlabSessionLexer.
    """
    name = 'Julia console'
    aliases = ['jlcon', 'julia-repl']
    url = 'https://julialang.org/'
    version_added = '1.6'
    _example = 'jlcon/console'
    
    def get_tokens_unprocessed(self, text):
        jllexer = JuliaLexer(**self.options)
        start = 0
        curcode = ''
        insertions = []
        output = False
        error = False
        for line in text.splitlines(keepends=True):
            if line.startswith('julia>'):
                insertions.append((len(curcode), [(0, Generic.Prompt, line[:6])]))
                curcode += line[6:]
                output = False
                error = False
            elif (line.startswith('help?>') or line.startswith('shell>')):
                yield (start, Generic.Prompt, line[:6])
                yield (start + 6, Text, line[6:])
                output = False
                error = False
            elif (line.startswith('      ') and not output):
                insertions.append((len(curcode), [(0, Whitespace, line[:6])]))
                curcode += line[6:]
            else:
                if curcode:
                    yield from do_insertions(insertions, jllexer.get_tokens_unprocessed(curcode))
                    curcode = ''
                    insertions = []
                if (line.startswith('ERROR: ') or error):
                    yield (start, Generic.Error, line)
                    error = True
                else:
                    yield (start, Generic.Output, line)
                output = True
            start += len(line)
        if curcode:
            yield from do_insertions(insertions, jllexer.get_tokens_unprocessed(curcode))


