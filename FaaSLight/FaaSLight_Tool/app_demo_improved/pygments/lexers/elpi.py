"""
    pygments.lexers.elpi
    ~~~~~~~~~~~~~~~~~~~~

    Lexer for the `Elpi <http://github.com/LPCIC/elpi>`_ programming language.

    :copyright: Copyright 2006-present by the Pygments team, see AUTHORS.
    :license: BSD, see LICENSE for details.
"""

from pygments.lexer import RegexLexer, bygroups, include, using
from pygments.token import Text, Comment, Operator, Keyword, Name, String, Number, Punctuation
__all__ = ['ElpiLexer']
from pygments.lexers.theorem import RocqLexer


class ElpiLexer(RegexLexer):
    """
    Lexer for the Elpi programming language.
    """
    name = 'Elpi'
    url = 'http://github.com/LPCIC/elpi'
    aliases = ['elpi']
    filenames = ['*.elpi']
    mimetypes = ['text/x-elpi']
    version_added = '2.11'
    lcase_re = '[a-z]'
    ucase_re = '[A-Z]'
    digit_re = '[0-9]'
    schar2_re = "([+*^?/<>`'@#~=&!])"
    schar_re = f'({schar2_re}|-|\\$|_)'
    idchar_re = f'({lcase_re}|{ucase_re}|{digit_re}|{schar_re})'
    idcharstarns_re = f'({idchar_re}*(\\.({lcase_re}|{ucase_re}){idchar_re}*)*)'
    symbchar_re = f'({lcase_re}|{ucase_re}|{digit_re}|{schar_re}|:)'
    constant_re = f'({ucase_re}{idchar_re}*|{lcase_re}{idcharstarns_re}|{schar2_re}{symbchar_re}*|_{idchar_re}+)'
    symbol_re = '(,|<=>|->|:-|;|\\?-|->|&|=>|\\bas\\b|\\buvar\\b|<|=<|=|==|>=|>|\\bi<|\\bi=<|\\bi>=|\\bi>|\\bis\\b|\\br<|\\br=<|\\br>=|\\br>|\\bs<|\\bs=<|\\bs>=|\\bs>|@|::|\\[\\]|`->|`:|`:=|\\^|-|\\+|\\bi-|\\bi\\+|r-|r\\+|/|\\*|\\bdiv\\b|\\bi\\*|\\bmod\\b|\\br\\*|~|\\bi~|\\br~)'
    escape_re = f'\\(({constant_re}|{symbol_re})\\)'
    const_sym_re = f'({constant_re}|{symbol_re}|{escape_re})'
    tokens = {'root': [include('elpi')], 'elpi': [include('_elpi-comment'), ('(:before|:after|:if|:name)(\\s*)(\\")', bygroups(Keyword.Mode, Text.Whitespace, String.Double), 'elpi-string'), ('(:index)(\\s*)(\\()', bygroups(Keyword.Mode, Text.Whitespace, Punctuation), 'elpi-indexing-expr'), (f'\\b(external pred|pred)(\\s+)({const_sym_re})', bygroups(Keyword.Declaration, Text.Whitespace, Name.Function), 'elpi-pred-item'), (f'\\b(func)(\\s+)({const_sym_re})', bygroups(Keyword.Declaration, Text.Whitespace, Name.Function), 'elpi-func-item'), (f'\\b(external type|type)(\\s+)(({const_sym_re}(,\\s*)?)+)', bygroups(Keyword.Declaration, Text.Whitespace, Name.Function), 'elpi-type'), (f'\\b(kind)(\\s+)(({const_sym_re}|,)+)', bygroups(Keyword.Declaration, Text.Whitespace, Name.Function), 'elpi-type'), (f'\\b(typeabbrev)(\\s+)({const_sym_re})', bygroups(Keyword.Declaration, Text.Whitespace, Name.Function), 'elpi-type'), ('\\b(typeabbrev)(\\s+)(\\([^)]+\\))', bygroups(Keyword.Declaration, Text.Whitespace, Name.Function), 'elpi-type'), ('\\b(accumulate)(\\s+)(\\")', bygroups(Keyword.Declaration, Text.Whitespace, String.Double), 'elpi-string'), (f'\\b(accumulate|namespace|local)(\\s+)({constant_re})', bygroups(Keyword.Declaration, Text.Whitespace, Text)), (f'\\b(shorten)(\\s+)({constant_re}\\.)', bygroups(Keyword.Declaration, Text.Whitespace, Text)), ('\\b(pi|sigma)(\\s+)([a-zA-Z][A-Za-z0-9_ ]*)(\\\\)', bygroups(Keyword.Declaration, Text.Whitespace, Name.Variable, Text)), (f'\\b(constraint)(\\s+)(({const_sym_re}(\\s+)?)+)', bygroups(Keyword.Declaration, Text.Whitespace, Name.Function), 'elpi-chr-rule-start'), (f'(?=[A-Z_]){constant_re}', Name.Variable), (f'(?=[a-z_])({constant_re}|_)\\\\', Name.Variable), ('_', Name.Variable), (f'({symbol_re}|!|=>|;)', Keyword.Declaration), (constant_re, Text), ('\\[|\\]|\\||=>', Keyword.Declaration), ('"', String.Double, 'elpi-string'), ('`', String.Double, 'elpi-btick'), ("\\'", String.Double, 'elpi-tick'), ('\\{\\{', Punctuation, 'elpi-quote'), ('\\{[^\\{]', Text, 'elpi-spill'), ('\\(', Punctuation, 'elpi-in-parens'), ('\\d[\\d_]*', Number.Integer), ('-?\\d[\\d_]*(.[\\d_]*)?([eE][+\\-]?\\d[\\d_]*)', Number.Float), ('[\\+\\*\\-/\\^\\.]', Operator)], '_elpi-comment': [('%[^\\n]*\\n', Comment), ('/(?:\\\\\\n)?[*](?:[^*]|[*](?!(?:\\\\\\n)?/))*[*](?:\\\\\\n)?/', Comment), ('\\s+', Text.Whitespace)], 'elpi-indexing-expr': [('[0-9 _]+', Number.Integer), ('\\)', Punctuation, '#pop')], 'elpi-type': [('(ctype\\s+)(\\")', bygroups(Keyword.Type, String.Double), 'elpi-string'), ('->', Keyword.Type), ('prop', Keyword.Mode), (constant_re, Keyword.Type), ('\\(|\\)', Keyword.Type), ('\\.', Text, '#pop'), include('_elpi-comment')], 'elpi-chr-rule-start': [('\\{', Punctuation, 'elpi-chr-rule'), include('_elpi-comment')], 'elpi-chr-rule': [('\\brule\\b', Keyword.Declaration), ('\\\\', Keyword.Declaration), ('\\}', Punctuation, '#pop:2'), include('elpi')], 'elpi-pred-item': [('[io]:', Keyword.Mode), ('\\.', Text, '#pop'), (',', Keyword.Mode), include('_elpi-inner-pred-fun'), ('\\)', Keyword.Mode, '#pop'), ('\\(', Keyword.Type, '_elpi-type-item'), include('_elpi-comment'), include('_elpi-type-item')], 'elpi-func-item': [(constant_re, Keyword.Type), ('\\.', Text, '#pop'), (',', Keyword.Mode), ('->', Keyword.Mode), include('_elpi-inner-pred-fun'), ('\\)', Keyword.Mode, '#pop'), ('\\(', Keyword.Type, '_elpi-type-item'), include('_elpi-comment'), include('_elpi-type-item')], '_elpi-inner-pred-fun': [('(\\()(\\s*)(pred)', bygroups(Keyword.Mode, Text.Whitespace, Keyword.Declaration), 'elpi-pred-item'), ('(\\()(\\s*)(func)', bygroups(Keyword.Mode, Text.Whitespace, Keyword.Declaration), 'elpi-func-item')], '_elpi-type-item': [('->', Keyword.Type), (constant_re, Keyword.Type), include('_elpi-inner-pred-fun'), ('\\(', Keyword.Type, '#push'), ('\\)', Keyword.Type, '#pop'), include('_elpi-comment')], 'elpi-btick': [('[^` ]+', String.Double), ('`', String.Double, '#pop')], 'elpi-tick': [("[^\\' ]+", String.Double), ("\\'", String.Double, '#pop')], 'elpi-string': [('[^\\"]+', String.Double), ('"', String.Double, '#pop')], 'elpi-quote': [('\\}\\}', Punctuation, '#pop'), ('\\s+', Text.Whitespace), ('(lp:)(\\{\\{)', bygroups(Number, Punctuation), 'elpi-quote-exit'), (f'(lp:)((?=[A-Z_]){constant_re})', bygroups(Number, Name.Variable)), ('((?!lp:|\\}\\}).)+', using(RocqLexer))], 'elpi-quote-exit': [include('elpi'), ('\\}\\}', Punctuation, '#pop')], 'elpi-spill': [('\\{[^\\{]', Text, '#push'), ('\\}[^\\}]', Text, '#pop'), include('elpi')], 'elpi-in-parens': [('\\(', Punctuation, '#push'), include('elpi'), ('\\)', Punctuation, '#pop')]}


