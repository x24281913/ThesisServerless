"""
    pygments.lexers.smv
    ~~~~~~~~~~~~~~~~~~~

    Lexers for the SMV languages.

    :copyright: Copyright 2006-present by the Pygments team, see AUTHORS.
    :license: BSD, see LICENSE for details.
"""

from pygments.lexer import RegexLexer, words
from pygments.token import Comment, Keyword, Name, Number, Operator, Punctuation, Text
__all__ = ['NuSMVLexer']


class NuSMVLexer(RegexLexer):
    """
    Lexer for the NuSMV language.
    """
    name = 'NuSMV'
    aliases = ['nusmv']
    filenames = ['*.smv']
    mimetypes = []
    url = 'https://nusmv.fbk.eu'
    version_added = '2.2'
    tokens = {'root': [('(?s)\\/\\-\\-.*?\\-\\-/', Comment), ('--.*\\n', Comment), (words(('MODULE', 'DEFINE', 'MDEFINE', 'CONSTANTS', 'VAR', 'IVAR', 'FROZENVAR', 'INIT', 'TRANS', 'INVAR', 'SPEC', 'CTLSPEC', 'LTLSPEC', 'PSLSPEC', 'COMPUTE', 'NAME', 'INVARSPEC', 'FAIRNESS', 'JUSTICE', 'COMPASSION', 'ISA', 'ASSIGN', 'CONSTRAINT', 'SIMPWFF', 'CTLWFF', 'LTLWFF', 'PSLWFF', 'COMPWFF', 'IN', 'MIN', 'MAX', 'MIRROR', 'PRED', 'PREDICATES'), suffix='(?![\\w$#-])'), Keyword.Declaration), ('process(?![\\w$#-])', Keyword), (words(('array', 'of', 'boolean', 'integer', 'real', 'word'), suffix='(?![\\w$#-])'), Keyword.Type), (words(('case', 'esac'), suffix='(?![\\w$#-])'), Keyword), (words(('word1', 'bool', 'signed', 'unsigned', 'extend', 'resize', 'sizeof', 'uwconst', 'swconst', 'init', 'self', 'count', 'abs', 'max', 'min'), suffix='(?![\\w$#-])'), Name.Builtin), (words(('EX', 'AX', 'EF', 'AF', 'EG', 'AG', 'E', 'F', 'O', 'G', 'H', 'X', 'Y', 'Z', 'A', 'U', 'S', 'V', 'T', 'BU', 'EBF', 'ABF', 'EBG', 'ABG', 'next', 'mod', 'union', 'in', 'xor', 'xnor'), suffix='(?![\\w$#-])'), Operator.Word), (words(('TRUE', 'FALSE'), suffix='(?![\\w$#-])'), Keyword.Constant), ('[a-zA-Z_][\\w$#-]*', Name.Variable), (':=', Operator), ('[-&|+*/<>!=]', Operator), ('\\-?\\d+\\b', Number.Integer), ('0[su][bB]\\d*_[01_]+', Number.Bin), ('0[su][oO]\\d*_[0-7_]+', Number.Oct), ('0[su][dD]\\d*_[\\d_]+', Number.Decimal), ('0[su][hH]\\d*_[\\da-fA-F_]+', Number.Hex), ('\\s+', Text.Whitespace), ('[()\\[\\]{};?:.,]', Punctuation)]}


