"""
    pygments.lexers.rdf
    ~~~~~~~~~~~~~~~~~~~

    Lexers for semantic web and RDF query languages and markup.

    :copyright: Copyright 2006-present by the Pygments team, see AUTHORS.
    :license: BSD, see LICENSE for details.
"""

import re
from pygments.lexer import RegexLexer, bygroups, default
from pygments.token import Keyword, Punctuation, String, Number, Operator, Generic, Whitespace, Name, Literal, Comment, Text
__all__ = ['SparqlLexer', 'TurtleLexer', 'ShExCLexer']


class SparqlLexer(RegexLexer):
    """
    Lexer for SPARQL query language.
    """
    name = 'SPARQL'
    aliases = ['sparql']
    filenames = ['*.rq', '*.sparql']
    mimetypes = ['application/sparql-query']
    url = 'https://www.w3.org/TR/sparql11-query'
    version_added = '2.0'
    PN_CHARS_BASE_GRP = 'a-zA-ZÀ-ÖØ-öø-˿Ͱ-ͽͿ-\u1fff\u200c-\u200d⁰-\u218fⰀ-\u2fef、-\ud7ff豈-\ufdcfﷰ-�'
    PN_CHARS_U_GRP = PN_CHARS_BASE_GRP + '_'
    PN_CHARS_GRP = PN_CHARS_U_GRP + '\\-' + '0-9' + '·' + '̀-ͯ' + '‿-⁀'
    HEX_GRP = '0-9A-Fa-f'
    PN_LOCAL_ESC_CHARS_GRP = ' _~.\\-!$&"()*+,;=/?#@%'
    PN_CHARS_BASE = '[' + PN_CHARS_BASE_GRP + ']'
    PN_CHARS_U = '[' + PN_CHARS_U_GRP + ']'
    PN_CHARS = '[' + PN_CHARS_GRP + ']'
    HEX = '[' + HEX_GRP + ']'
    PN_LOCAL_ESC_CHARS = '[' + PN_LOCAL_ESC_CHARS_GRP + ']'
    IRIREF = '<(?:[^<>"{}|^`\\\\\\x00-\\x20])*>'
    BLANK_NODE_LABEL = '_:[0-9' + PN_CHARS_U_GRP + '](?:[' + PN_CHARS_GRP + '.]*' + PN_CHARS + ')?'
    PN_PREFIX = PN_CHARS_BASE + '(?:[' + PN_CHARS_GRP + '.]*' + PN_CHARS + ')?'
    VARNAME = '[0-9' + PN_CHARS_U_GRP + '][' + PN_CHARS_U_GRP + '0-9·̀-ͯ‿-⁀]*'
    PERCENT = '%' + HEX + HEX
    PN_LOCAL_ESC = '\\\\' + PN_LOCAL_ESC_CHARS
    PLX = '(?:' + PERCENT + ')|(?:' + PN_LOCAL_ESC + ')'
    PN_LOCAL = '(?:[' + PN_CHARS_U_GRP + ':0-9' + ']|' + PLX + ')' + '(?:(?:[' + PN_CHARS_GRP + '.:]|' + PLX + ')*(?:[' + PN_CHARS_GRP + ':]|' + PLX + '))?'
    EXPONENT = '[eE][+-]?\\d+'
    tokens = {'root': [('\\s+', Text), ('(?i)(select|construct|describe|ask|where|filter|group\\s+by|minus|distinct|reduced|from\\s+named|from|order\\s+by|desc|asc|limit|offset|values|bindings|load|into|clear|drop|create|add|move|copy|insert\\s+data|delete\\s+data|delete\\s+where|with|delete|insert|using\\s+named|using|graph|default|named|all|optional|service|silent|bind|undef|union|not\\s+in|in|as|having|to|prefix|base)\\b', Keyword), ('(a)\\b', Keyword), ('(' + IRIREF + ')', Name.Label), ('(' + BLANK_NODE_LABEL + ')', Name.Label), ('[?$]' + VARNAME, Name.Variable), ('(' + PN_PREFIX + ')?(\\:)(' + PN_LOCAL + ')?', bygroups(Name.Namespace, Punctuation, Name.Tag)), ('(?i)(str|lang|langmatches|datatype|bound|iri|uri|bnode|rand|abs|ceil|floor|round|concat|strlen|ucase|lcase|encode_for_uri|contains|strstarts|strends|strbefore|strafter|year|month|day|hours|minutes|seconds|timezone|tz|now|uuid|struuid|md5|sha1|sha256|sha384|sha512|coalesce|if|strlang|strdt|sameterm|isiri|isuri|isblank|isliteral|isnumeric|regex|substr|replace|exists|not\\s+exists|count|sum|min|max|avg|sample|group_concat|separator)\\b', Name.Function), ('(true|false)', Keyword.Constant), ('[+\\-]?(\\d+\\.\\d*' + EXPONENT + '|\\.?\\d+' + EXPONENT + ')', Number.Float), ('[+\\-]?(\\d+\\.\\d*|\\.\\d+)', Number.Float), ('[+\\-]?\\d+', Number.Integer), ('(\\|\\||&&|=|\\*|\\-|\\+|/|!=|<=|>=|!|<|>)', Operator), ('[(){}.;,:^\\[\\]]', Punctuation), ('#[^\\n]*', Comment), ('"""', String, 'triple-double-quoted-string'), ('"', String, 'single-double-quoted-string'), ("'''", String, 'triple-single-quoted-string'), ("'", String, 'single-single-quoted-string')], 'triple-double-quoted-string': [('"""', String, 'end-of-string'), ('[^\\\\]+', String), ('\\\\', String, 'string-escape')], 'single-double-quoted-string': [('"', String, 'end-of-string'), ('[^"\\\\\\n]+', String), ('\\\\', String, 'string-escape')], 'triple-single-quoted-string': [("'''", String, 'end-of-string'), ('[^\\\\]+', String), ('\\\\', String.Escape, 'string-escape')], 'single-single-quoted-string': [("'", String, 'end-of-string'), ("[^'\\\\\\n]+", String), ('\\\\', String, 'string-escape')], 'string-escape': [('u' + HEX + '{4}', String.Escape, '#pop'), ('U' + HEX + '{8}', String.Escape, '#pop'), ('.', String.Escape, '#pop')], 'end-of-string': [('(@)([a-zA-Z]+(?:-[a-zA-Z0-9]+)*)', bygroups(Operator, Name.Function), '#pop:2'), ('\\^\\^', Operator, '#pop:2'), default('#pop:2')]}



class TurtleLexer(RegexLexer):
    """
    Lexer for Turtle data language.
    """
    name = 'Turtle'
    aliases = ['turtle']
    filenames = ['*.ttl']
    mimetypes = ['text/turtle', 'application/x-turtle']
    url = 'https://www.w3.org/TR/turtle'
    version_added = '2.1'
    PN_CHARS_BASE_GRP = 'a-zA-ZÀ-ÖØ-öø-˿Ͱ-ͽͿ-\u1fff\u200c-\u200d⁰-\u218fⰀ-\u2fef、-\ud7ff豈-\ufdcfﷰ-�'
    PN_CHARS_U_GRP = PN_CHARS_BASE_GRP + '_'
    PN_CHARS_GRP = PN_CHARS_U_GRP + '\\-' + '0-9' + '·' + '̀-ͯ' + '‿-⁀'
    PN_CHARS = '[' + PN_CHARS_GRP + ']'
    PN_CHARS_BASE = '[' + PN_CHARS_BASE_GRP + ']'
    PN_PREFIX = PN_CHARS_BASE + '(?:[' + PN_CHARS_GRP + '.]*' + PN_CHARS + ')?'
    HEX_GRP = '0-9A-Fa-f'
    HEX = '[' + HEX_GRP + ']'
    PERCENT = '%' + HEX + HEX
    PN_LOCAL_ESC_CHARS_GRP = ' _~.\\-!$&"()*+,;=/?#@%'
    PN_LOCAL_ESC_CHARS = '[' + PN_LOCAL_ESC_CHARS_GRP + ']'
    PN_LOCAL_ESC = '\\\\' + PN_LOCAL_ESC_CHARS
    PLX = '(?:' + PERCENT + ')|(?:' + PN_LOCAL_ESC + ')'
    PN_LOCAL = '(?:[' + PN_CHARS_U_GRP + ':0-9' + ']|' + PLX + ')' + '(?:(?:[' + PN_CHARS_GRP + '.:]|' + PLX + ')*(?:[' + PN_CHARS_GRP + ':]|' + PLX + '))?'
    patterns = {'PNAME_NS': '((?:[a-zA-Z][\\w-]*)?\\:)', 'IRIREF': '(<[^<>"{}|^`\\\\\\x00-\\x20]*>)'}
    tokens = {'root': [('\\s+', Text), ('(@base|BASE)(\\s+){IRIREF}(\\s*)(\\.?)'.format(**patterns), bygroups(Keyword, Whitespace, Name.Variable, Whitespace, Punctuation)), ('(@prefix|PREFIX)(\\s+){PNAME_NS}(\\s+){IRIREF}(\\s*)(\\.?)'.format(**patterns), bygroups(Keyword, Whitespace, Name.Namespace, Whitespace, Name.Variable, Whitespace, Punctuation)), ('(?<=\\s)a(?=\\s)', Keyword.Type), ('{IRIREF}'.format(**patterns), Name.Variable), ('(' + PN_PREFIX + ')?(\\:)(' + PN_LOCAL + ')?', bygroups(Name.Namespace, Punctuation, Name.Tag)), ('(_)(:)([' + PN_CHARS_U_GRP + '0-9]([' + PN_CHARS_GRP + '.]*' + PN_CHARS + ')?)', bygroups(Name.Namespace, Punctuation, Name.Tag)), ('#([^\\n]+|$)', Comment), ('\\b(true|false)\\b', Literal), ('[+\\-]?\\d*\\.\\d+', Number.Float), ('[+\\-]?\\d*(:?\\.\\d+)?E[+\\-]?\\d+', Number.Float), ('[+\\-]?\\d+', Number.Integer), ('[\\[\\](){}.;,:^]', Punctuation), ('"""', String, 'triple-double-quoted-string'), ('"', String, 'single-double-quoted-string'), ("'''", String, 'triple-single-quoted-string'), ("'", String, 'single-single-quoted-string')], 'triple-double-quoted-string': [('"""', String, 'end-of-string'), ('[^\\\\]+(?=""")', String), ('\\\\', String, 'string-escape')], 'single-double-quoted-string': [('"', String, 'end-of-string'), ('[^"\\\\\\n]+', String), ('\\\\', String, 'string-escape')], 'triple-single-quoted-string': [("'''", String, 'end-of-string'), ("[^\\\\]+(?=''')", String), ('\\\\', String, 'string-escape')], 'single-single-quoted-string': [("'", String, 'end-of-string'), ("[^'\\\\\\n]+", String), ('\\\\', String, 'string-escape')], 'string-escape': [('.', String, '#pop')], 'end-of-string': [('(@)([a-zA-Z]+(?:-[a-zA-Z0-9]+)*)', bygroups(Operator, Generic.Emph), '#pop:2'), ('(\\^\\^){IRIREF}'.format(**patterns), bygroups(Operator, Generic.Emph), '#pop:2'), default('#pop:2')]}
    
    def analyse_text(text):
        for t in ('@base ', 'BASE ', '@prefix ', 'PREFIX '):
            if re.search(f'^\\s*{t}', text):
                return 0.8



class ShExCLexer(RegexLexer):
    """
    Lexer for ShExC shape expressions language syntax.
    """
    name = 'ShExC'
    aliases = ['shexc', 'shex']
    filenames = ['*.shex']
    mimetypes = ['text/shex']
    url = 'https://shex.io/shex-semantics/#shexc'
    version_added = ''
    PN_CHARS_BASE_GRP = 'a-zA-ZÀ-ÖØ-öø-˿Ͱ-ͽͿ-\u1fff\u200c-\u200d⁰-\u218fⰀ-\u2fef、-\ud7ff豈-\ufdcfﷰ-�'
    PN_CHARS_U_GRP = PN_CHARS_BASE_GRP + '_'
    PN_CHARS_GRP = PN_CHARS_U_GRP + '\\-' + '0-9' + '·' + '̀-ͯ' + '‿-⁀'
    HEX_GRP = '0-9A-Fa-f'
    PN_LOCAL_ESC_CHARS_GRP = "_~.\\-!$&'()*+,;=/?#@%"
    PN_CHARS_BASE = '[' + PN_CHARS_BASE_GRP + ']'
    PN_CHARS_U = '[' + PN_CHARS_U_GRP + ']'
    PN_CHARS = '[' + PN_CHARS_GRP + ']'
    HEX = '[' + HEX_GRP + ']'
    PN_LOCAL_ESC_CHARS = '[' + PN_LOCAL_ESC_CHARS_GRP + ']'
    UCHAR_NO_BACKSLASH = '(?:u' + HEX + '{4}|U' + HEX + '{8})'
    UCHAR = '\\\\' + UCHAR_NO_BACKSLASH
    IRIREF = '<(?:[^\\x00-\\x20<>"{}|^`\\\\]|' + UCHAR + ')*>'
    BLANK_NODE_LABEL = '_:[0-9' + PN_CHARS_U_GRP + '](?:[' + PN_CHARS_GRP + '.]*' + PN_CHARS + ')?'
    PN_PREFIX = PN_CHARS_BASE + '(?:[' + PN_CHARS_GRP + '.]*' + PN_CHARS + ')?'
    PERCENT = '%' + HEX + HEX
    PN_LOCAL_ESC = '\\\\' + PN_LOCAL_ESC_CHARS
    PLX = '(?:' + PERCENT + ')|(?:' + PN_LOCAL_ESC + ')'
    PN_LOCAL = '(?:[' + PN_CHARS_U_GRP + ':0-9' + ']|' + PLX + ')' + '(?:(?:[' + PN_CHARS_GRP + '.:]|' + PLX + ')*(?:[' + PN_CHARS_GRP + ':]|' + PLX + '))?'
    EXPONENT = '[eE][+-]?\\d+'
    tokens = {'root': [('\\s+', Text), ('(?i)(base|prefix|start|external|literal|iri|bnode|nonliteral|length|minlength|maxlength|mininclusive|minexclusive|maxinclusive|maxexclusive|totaldigits|fractiondigits|closed|extra)\\b', Keyword), ('(a)\\b', Keyword), ('(' + IRIREF + ')', Name.Label), ('(' + BLANK_NODE_LABEL + ')', Name.Label), ('(' + PN_PREFIX + ')?(\\:)(' + PN_LOCAL + ')?', bygroups(Name.Namespace, Punctuation, Name.Tag)), ('(true|false)', Keyword.Constant), ('[+\\-]?(\\d+\\.\\d*' + EXPONENT + '|\\.?\\d+' + EXPONENT + ')', Number.Float), ('[+\\-]?(\\d+\\.\\d*|\\.\\d+)', Number.Float), ('[+\\-]?\\d+', Number.Integer), ('[@|$&=*+?^\\-~]', Operator), ('(?i)(and|or|not)\\b', Operator.Word), ('[(){}.;,:^\\[\\]]', Punctuation), ('#[^\\n]*', Comment), ('"""', String, 'triple-double-quoted-string'), ('"', String, 'single-double-quoted-string'), ("'''", String, 'triple-single-quoted-string'), ("'", String, 'single-single-quoted-string')], 'triple-double-quoted-string': [('"""', String, 'end-of-string'), ('[^\\\\]+', String), ('\\\\', String, 'string-escape')], 'single-double-quoted-string': [('"', String, 'end-of-string'), ('[^"\\\\\\n]+', String), ('\\\\', String, 'string-escape')], 'triple-single-quoted-string': [("'''", String, 'end-of-string'), ('[^\\\\]+', String), ('\\\\', String.Escape, 'string-escape')], 'single-single-quoted-string': [("'", String, 'end-of-string'), ("[^'\\\\\\n]+", String), ('\\\\', String, 'string-escape')], 'string-escape': [(UCHAR_NO_BACKSLASH, String.Escape, '#pop'), ('.', String.Escape, '#pop')], 'end-of-string': [('(@)([a-zA-Z]+(?:-[a-zA-Z0-9]+)*)', bygroups(Operator, Name.Function), '#pop:2'), ('\\^\\^', Operator, '#pop:2'), default('#pop:2')]}


