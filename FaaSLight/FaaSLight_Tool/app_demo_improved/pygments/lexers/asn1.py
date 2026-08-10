"""
    pygments.lexers.asn1
    ~~~~~~~~~~~~~~~~~~~~

    Pygments lexers for ASN.1.

    :copyright: Copyright 2006-present by the Pygments team, see AUTHORS.
    :license: BSD, see LICENSE for details.
"""

import re
from pygments.token import Comment, Operator, Keyword, Name, String, Number, Punctuation, Whitespace
from pygments.lexer import RegexLexer, words, bygroups
__all__ = ['Asn1Lexer']
SINGLE_WORD_KEYWORDS = ['ENCODED', 'ABSTRACT-SYNTAX', 'END', 'APPLICATION', 'EXPLICIT', 'IMPLICIT', 'AUTOMATIC', 'TAGS', 'BEGIN', 'EXTENSIBILITY', 'BY', 'FROM', 'COMPONENT', 'UNIVERSAL', 'COMPONENTS', 'CONSTRAINED', 'IMPLIED', 'DEFINITIONS', 'INCLUDES', 'PRIVATE', 'WITH', 'OF']
OPERATOR_WORDS = ['EXCEPT', 'UNION', 'INTERSECTION']
SINGLE_WORD_NAMESPACE_KEYWORDS = ['EXPORTS', 'IMPORTS']
MULTI_WORDS_DECLARATIONS = ['SEQUENCE OF', 'SET OF', 'INSTANCE OF', 'WITH SYNTAX']
SINGLE_WORDS_DECLARATIONS = ['SIZE', 'SEQUENCE', 'SET', 'CLASS', 'UNIQUE', 'DEFAULT', 'CHOICE', 'PATTERN', 'OPTIONAL', 'PRESENT', 'ABSENT', 'CONTAINING', 'ENUMERATED', 'ALL']
TWO_WORDS_TYPES = ['OBJECT IDENTIFIER', 'BIT STRING', 'OCTET STRING', 'CHARACTER STRING', 'EMBEDDED PDV']
SINGLE_WORD_TYPES = ['RELATIVE-OID', 'TYPE-IDENTIFIER', 'ObjectDescriptor', 'IA5String', 'INTEGER', 'ISO646String', 'T61String', 'BMPString', 'NumericString', 'TeletexString', 'GeneralizedTime', 'REAL', 'BOOLEAN', 'GeneralString', 'GraphicString', 'UniversalString', 'UTCTime', 'VisibleString', 'UTF8String', 'PrintableString', 'VideotexString', 'EXTERNAL']

def word_sequences(tokens):
    return '(' + '|'.join((token.replace(' ', '\\s+') for token in tokens)) + ')\\b'


class Asn1Lexer(RegexLexer):
    """
    Lexer for ASN.1 module definition
    """
    flags = re.MULTILINE
    name = 'ASN.1'
    aliases = ['asn1']
    filenames = ['*.asn1']
    url = 'https://www.itu.int/ITU-T/studygroups/com17/languages/X.680-0207.pdf'
    version_added = '2.16'
    tokens = {'root': [('\\s+', Whitespace), ('--.*$', Comment.Single), ('/\\*', Comment.Multiline, 'comment'), ('\\d+\\.\\d+([eE][-+]?\\d+)?', Number.Float), ('\\d+', Number.Integer), ('&?[a-z][-a-zA-Z0-9]*[a-zA-Z0-9]\\b', Name.Variable), (words(('TRUE', 'FALSE', 'NULL', 'MINUS-INFINITY', 'PLUS-INFINITY', 'MIN', 'MAX'), suffix='\\b'), Keyword.Constant), (word_sequences(TWO_WORDS_TYPES), Keyword.Type), (words(SINGLE_WORD_TYPES, suffix='\\b'), Keyword.Type), ('EXPORTS\\s+ALL\\b', Keyword.Namespace), (words(SINGLE_WORD_NAMESPACE_KEYWORDS, suffix='\\b'), Operator.Namespace), (word_sequences(MULTI_WORDS_DECLARATIONS), Keyword.Declaration), (words(SINGLE_WORDS_DECLARATIONS, suffix='\\b'), Keyword.Declaration), (words(OPERATOR_WORDS, suffix='\\b'), Operator.Word), (words(SINGLE_WORD_KEYWORDS), Keyword), ('&?[A-Z][-a-zA-Z0-9]*[a-zA-Z0-9]\\b', Name.Type), ('(::=|\\.\\.\\.|\\.\\.|\\[\\[|\\]\\]|\\||\\^|-)', Operator), ('(\\.|,|\\{|\\}|\\(|\\)|\\[|\\])', Punctuation), ('"', String, 'string'), ("('[01 ]*')(B)\\b", bygroups(String, String.Affix)), ("('[0-9A-F ]*')(H)\\b", bygroups(String, String.Affix))], 'comment': [('[^*/]+', Comment.Multiline), ('/\\*', Comment.Multiline, '#push'), ('\\*/', Comment.Multiline, '#pop'), ('[*/]', Comment.Multiline)], 'string': [('""', String), ('"', String, '#pop'), ('[^"]', String)]}


