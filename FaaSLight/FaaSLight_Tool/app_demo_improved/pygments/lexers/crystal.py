"""
    pygments.lexers.crystal
    ~~~~~~~~~~~~~~~~~~~~~~~

    Lexer for Crystal.

    :copyright: Copyright 2006-present by the Pygments team, see AUTHORS.
    :license: BSD, see LICENSE for details.
"""

import re
from pygments.lexer import ExtendedRegexLexer, include, bygroups, default, words, line_re
from pygments.token import Comment, Operator, Keyword, Name, String, Number, Punctuation, Error, Whitespace
__all__ = ['CrystalLexer']
CRYSTAL_OPERATORS = ['!=', '!~', '!', '%', '&&', '&', '**', '*', '+', '-', '/', '<=>', '<<', '<=', '<', '===', '==', '=~', '=', '>=', '>>', '>', '[]=', '[]?', '[]', '^', '||', '|', '~']


class CrystalLexer(ExtendedRegexLexer):
    """
    For Crystal source code.
    """
    name = 'Crystal'
    url = 'https://crystal-lang.org'
    aliases = ['cr', 'crystal']
    filenames = ['*.cr']
    mimetypes = ['text/x-crystal']
    version_added = '2.2'
    flags = re.DOTALL | re.MULTILINE
    
    def heredoc_callback(self, match, ctx):
        start = match.start(1)
        yield (start, Operator, match.group(1))
        yield (match.start(2), String.Heredoc, match.group(2))
        yield (match.start(3), String.Delimiter, match.group(3))
        yield (match.start(4), String.Heredoc, match.group(4))
        heredocstack = ctx.__dict__.setdefault('heredocstack', [])
        outermost = not bool(heredocstack)
        heredocstack.append((match.group(1) == '<<-', match.group(3)))
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
    
    def gen_crystalstrings_rules():
        states = {}
        states['strings'] = [('\\:\\w+[!?]?', String.Symbol), (words(CRYSTAL_OPERATORS, prefix='\\:'), String.Symbol), (":'(\\\\\\\\|\\\\[^\\\\]|[^'\\\\])*'", String.Symbol), ("'(\\\\\\\\|\\\\'|[^']|\\\\[^'\\\\]+)'", String.Char), (':"', String.Symbol, 'simple-sym'), ('([a-zA-Z_]\\w*)(:)(?!:)', bygroups(String.Symbol, Punctuation)), ('"', String.Double, 'simple-string'), ('(?<!\\.)`', String.Backtick, 'simple-backtick')]
        for (name, ttype, end) in (('string', String.Double, '"'), ('sym', String.Symbol, '"'), ('backtick', String.Backtick, '`')):
            states['simple-' + name] = [include(('string-escaped' if name == 'sym' else 'string-intp-escaped')), (f'[^\\\\{end}#]+', ttype), ('[\\\\#]', ttype), (end, ttype, '#pop')]
        for (lbrace, rbrace, bracecc, name) in (('\\{', '\\}', '{}', 'cb'), ('\\[', '\\]', '\\[\\]', 'sb'), ('\\(', '\\)', '()', 'pa'), ('<', '>', '<>', 'ab'), ('\\|', '\\|', '\\|', 'pi')):
            states[name + '-intp-string'] = [('\\\\' + lbrace, String.Other)] + (lbrace != rbrace) * [(lbrace, String.Other, '#push')] + [(rbrace, String.Other, '#pop'), include('string-intp-escaped'), ('[\\\\#' + bracecc + ']', String.Other), ('[^\\\\#' + bracecc + ']+', String.Other)]
            states['strings'].append(('%Q?' + lbrace, String.Other, name + '-intp-string'))
            states[name + '-string'] = [('\\\\[\\\\' + bracecc + ']', String.Other)] + (lbrace != rbrace) * [(lbrace, String.Other, '#push')] + [(rbrace, String.Other, '#pop'), ('[\\\\#' + bracecc + ']', String.Other), ('[^\\\\#' + bracecc + ']+', String.Other)]
            states['strings'].append(('%[qwi]' + lbrace, String.Other, name + '-string'))
            states[name + '-regex'] = [('\\\\[\\\\' + bracecc + ']', String.Regex)] + (lbrace != rbrace) * [(lbrace, String.Regex, '#push')] + [(rbrace + '[imsx]*', String.Regex, '#pop'), include('string-intp'), ('[\\\\#' + bracecc + ']', String.Regex), ('[^\\\\#' + bracecc + ']+', String.Regex)]
            states['strings'].append(('%r' + lbrace, String.Regex, name + '-regex'))
        return states
    tokens = {'root': [('#.*?$', Comment.Single), (words('\n                abstract asm begin break case do else elsif end ensure extend if in\n                include next of private protected require rescue return select self super\n                then unless until when while with yield\n            '.split(), suffix='\\b'), Keyword), (words('\n                previous_def forall out uninitialized __DIR__ __FILE__ __LINE__\n                __END_LINE__\n            '.split(), prefix='(?<!\\.)', suffix='\\b'), Keyword.Pseudo), ('\\.(is_a\\?|nil\\?|responds_to\\?|as\\?|as\\b)', Keyword.Pseudo), (words(['true', 'false', 'nil'], suffix='\\b'), Keyword.Constant), ('(module|lib)(\\s+)([a-zA-Z_]\\w*(?:::[a-zA-Z_]\\w*)*)', bygroups(Keyword, Whitespace, Name.Namespace)), ('(def|fun|macro)(\\s+)((?:[a-zA-Z_]\\w*::)*)', bygroups(Keyword, Whitespace, Name.Namespace), 'funcname'), ('def(?=[*%&^`~+-/\\[<>=])', Keyword, 'funcname'), ('(annotation|class|struct|union|type|alias|enum)(\\s+)((?:[a-zA-Z_]\\w*::)*)', bygroups(Keyword, Whitespace, Name.Namespace), 'classname'), (words('\n                instance_sizeof offsetof pointerof sizeof typeof\n            '.split(), prefix='(?<!\\.)', suffix='\\b'), Keyword.Pseudo), ('(?<!\\.)(debugger\\b|p!|pp!|record\\b|spawn\\b)', Name.Builtin.Pseudo), (words('\n                abort at_exit caller exit gets loop main p pp print printf puts\n                raise rand read_line sleep spawn sprintf system\n            '.split(), prefix='(?<!\\.)', suffix='\\b'), Name.Builtin), ('(?<!\\.)(((class_)?((getter|property)\\b[!?]?|setter\\b))|(def_(clone|equals|equals_and_hash|hash)|delegate|forward_missing_to)\\b)', Name.Builtin.Pseudo), ('(?<!\\w)(<<-?)(["`\\\']?)([a-zA-Z_]\\w*)(\\2)(.*?\\n)', heredoc_callback), ('(<<-?)("|\\\')()(\\2)(.*?\\n)', heredoc_callback), ('__END__', Comment.Preproc, 'end-part'), ('(?:^|(?<=[=<>~!:])|(?<=(?:\\s|;)when\\s)|(?<=(?:\\s|;)or\\s)|(?<=(?:\\s|;)and\\s)|(?<=\\.index\\s)|(?<=\\.scan\\s)|(?<=\\.sub\\s)|(?<=\\.sub!\\s)|(?<=\\.gsub\\s)|(?<=\\.gsub!\\s)|(?<=\\.match\\s)|(?<=(?:\\s|;)if\\s)|(?<=(?:\\s|;)elsif\\s)|(?<=^when\\s)|(?<=^index\\s)|(?<=^scan\\s)|(?<=^sub\\s)|(?<=^gsub\\s)|(?<=^sub!\\s)|(?<=^gsub!\\s)|(?<=^match\\s)|(?<=^if\\s)|(?<=^elsif\\s))(\\s*)(/)', bygroups(Whitespace, String.Regex), 'multiline-regex'), ('(?<=\\(|,|\\[)/', String.Regex, 'multiline-regex'), ('(\\s+)(/)(?![\\s=])', bygroups(Whitespace, String.Regex), 'multiline-regex'), ('(0o[0-7]+(?:_[0-7]+)*(?:_?[iu][0-9]+)?)\\b(\\s*)([/?])?', bygroups(Number.Oct, Whitespace, Operator)), ('(0x[0-9A-Fa-f]+(?:_[0-9A-Fa-f]+)*(?:_?[iu][0-9]+)?)\\b(\\s*)([/?])?', bygroups(Number.Hex, Whitespace, Operator)), ('(0b[01]+(?:_[01]+)*(?:_?[iu][0-9]+)?)\\b(\\s*)([/?])?', bygroups(Number.Bin, Whitespace, Operator)), ('((?:0(?![0-9])|[1-9][\\d_]*)(?:\\.\\d[\\d_]*)(?:e[+-]?[0-9]+)?(?:_?f[0-9]+)?)(\\s*)([/?])?', bygroups(Number.Float, Whitespace, Operator)), ('((?:0(?![0-9])|[1-9][\\d_]*)(?:\\.\\d[\\d_]*)?(?:e[+-]?[0-9]+)(?:_?f[0-9]+)?)(\\s*)([/?])?', bygroups(Number.Float, Whitespace, Operator)), ('((?:0(?![0-9])|[1-9][\\d_]*)(?:\\.\\d[\\d_]*)?(?:e[+-]?[0-9]+)?(?:_?f[0-9]+))(\\s*)([/?])?', bygroups(Number.Float, Whitespace, Operator)), ('(0\\b|[1-9][\\d]*(?:_\\d+)*(?:_?[iu][0-9]+)?)\\b(\\s*)([/?])?', bygroups(Number.Integer, Whitespace, Operator)), ('@@[a-zA-Z_]\\w*', Name.Variable.Class), ('@[a-zA-Z_]\\w*', Name.Variable.Instance), ('\\$\\w+', Name.Variable.Global), ('\\$[!@&`\\\'+~=/\\\\,;.<>_*$?:"^-]', Name.Variable.Global), ('\\$-[0adFiIlpvw]', Name.Variable.Global), ('::', Operator), include('strings'), ('\\?(\\\\[MC]-)*(\\\\([\\\\abefnrtv#"\\\']|[0-7]{1,3}|x[a-fA-F0-9]{2}|u[a-fA-F0-9]{4}|u\\{[a-fA-F0-9 ]+\\})|\\S)(?!\\w)', String.Char), ('[A-Z][A-Z_]+\\b(?!::|\\.)', Name.Constant), ('\\{%', String.Interpol, 'in-macro-control'), ('\\{\\{', String.Interpol, 'in-macro-expr'), ('(@\\[)(\\s*)([A-Z]\\w*(::[A-Z]\\w*)*)', bygroups(Operator, Whitespace, Name.Decorator), 'in-annot'), (words(CRYSTAL_OPERATORS, prefix='(\\.|::)'), bygroups(Operator, Name.Operator)), ('(\\.|::)([a-zA-Z_]\\w*[!?]?|[*%&^`~+\\-/\\[<>=])', bygroups(Operator, Name)), ('[a-zA-Z_]\\w*(?:[!?](?!=))?', Name), ('(\\[|\\]\\??|\\*\\*|<=>?|>=|<<?|>>?|=~|===|!~|&&?|\\|\\||\\.{1,3})', Operator), ('[-+/*%=<>&!^|~]=?', Operator), ('[(){};,/?:\\\\]', Punctuation), ('\\s+', Whitespace)], 'funcname': [('(?:([a-zA-Z_]\\w*)(\\.))?([a-zA-Z_]\\w*[!?]?|\\*\\*?|[-+]@?|[/%&|^`~]|\\[\\]=?|<<|>>|<=?>|>=?|===?)', bygroups(Name.Class, Operator, Name.Function), '#pop'), default('#pop')], 'classname': [('[A-Z_]\\w*', Name.Class), ('(\\()(\\s*)([A-Z_]\\w*)(\\s*)(\\))', bygroups(Punctuation, Whitespace, Name.Class, Whitespace, Punctuation)), default('#pop')], 'in-intp': [('\\{', String.Interpol, '#push'), ('\\}', String.Interpol, '#pop'), include('root')], 'string-intp': [('#\\{', String.Interpol, 'in-intp')], 'string-escaped': [('\\\\([\\\\abefnrtv#"\\\']|[0-7]{1,3}|x[a-fA-F0-9]{2}|u[a-fA-F0-9]{4}|u\\{[a-fA-F0-9 ]+\\})', String.Escape)], 'string-intp-escaped': [include('string-intp'), include('string-escaped')], 'interpolated-regex': [include('string-intp'), ('[\\\\#]', String.Regex), ('[^\\\\#]+', String.Regex)], 'interpolated-string': [include('string-intp'), ('[\\\\#]', String.Other), ('[^\\\\#]+', String.Other)], 'multiline-regex': [include('string-intp'), ('\\\\\\\\', String.Regex), ('\\\\/', String.Regex), ('[\\\\#]', String.Regex), ('[^\\\\/#]+', String.Regex), ('/[imsx]*', String.Regex, '#pop')], 'end-part': [('.+', Comment.Preproc, '#pop')], 'in-macro-control': [('\\{%', String.Interpol, '#push'), ('%\\}', String.Interpol, '#pop'), ('(for|verbatim)\\b', Keyword), include('root')], 'in-macro-expr': [('\\{\\{', String.Interpol, '#push'), ('\\}\\}', String.Interpol, '#pop'), include('root')], 'in-annot': [('\\[', Operator, '#push'), ('\\]', Operator, '#pop'), include('root')]}
    tokens.update(gen_crystalstrings_rules())


