"""
    pygments.lexers.nimrod
    ~~~~~~~~~~~~~~~~~~~~~~

    Lexer for the Nim language (formerly known as Nimrod).

    :copyright: Copyright 2006-present by the Pygments team, see AUTHORS.
    :license: BSD, see LICENSE for details.
"""

import re
from pygments.lexer import RegexLexer, include, default, bygroups
from pygments.token import Text, Comment, Operator, Keyword, Name, String, Number, Punctuation, Error
__all__ = ['NimrodLexer']


class NimrodLexer(RegexLexer):
    """
    For Nim source code.
    """
    name = 'Nimrod'
    url = 'http://nim-lang.org/'
    aliases = ['nimrod', 'nim']
    filenames = ['*.nim', '*.nimrod']
    mimetypes = ['text/x-nim']
    version_added = '1.5'
    flags = re.MULTILINE | re.IGNORECASE
    
    def underscorize(words):
        newWords = []
        new = []
        for word in words:
            for ch in word:
                new.append(ch)
                new.append('_?')
            newWords.append(''.join(new))
            new = []
        return '|'.join(newWords)
    keywords = ['addr', 'and', 'as', 'asm', 'bind', 'block', 'break', 'case', 'cast', 'concept', 'const', 'continue', 'converter', 'defer', 'discard', 'distinct', 'div', 'do', 'elif', 'else', 'end', 'enum', 'except', 'export', 'finally', 'for', 'if', 'in', 'yield', 'interface', 'is', 'isnot', 'iterator', 'let', 'mixin', 'mod', 'not', 'notin', 'object', 'of', 'or', 'out', 'ptr', 'raise', 'ref', 'return', 'shl', 'shr', 'static', 'try', 'tuple', 'type', 'using', 'when', 'while', 'xor']
    keywordsPseudo = ['nil', 'true', 'false']
    opWords = ['and', 'or', 'not', 'xor', 'shl', 'shr', 'div', 'mod', 'in', 'notin', 'is', 'isnot']
    types = ['int', 'int8', 'int16', 'int32', 'int64', 'float', 'float32', 'float64', 'bool', 'char', 'range', 'array', 'seq', 'set', 'string']
    tokens = {'root': [('##\\[', String.Doc, 'doccomment'), ('##.*$', String.Doc), ('#\\[', Comment.Multiline, 'comment'), ('#.*$', Comment), ('\\{\\.', String.Other, 'pragma'), ('[*=><+\\-/@$~&%!?|\\\\\\[\\]]', Operator), ('\\.\\.|\\.|,|\\[\\.|\\.\\]|\\{\\.|\\.\\}|\\(\\.|\\.\\)|\\{|\\}|\\(|\\)|:|\\^|`|;', Punctuation), ('(\\n\\s*)(of)(\\s)', bygroups(Text.Whitespace, Keyword, Text.Whitespace), 'casebranch'), ('(?:[\\w]+)"', String, 'rdqs'), ('"""', String.Double, 'tdqs'), ('"', String, 'dqs'), ("'", String.Char, 'chars'), (f'({underscorize(opWords)})\\b', Operator.Word), ('(proc|func|method|macro|template)(\\s)(?![(\\[\\]])', bygroups(Keyword, Text.Whitespace), 'funcname'), (f'({underscorize(keywords)})\\b', Keyword), ('({})\\b'.format(underscorize(['from', 'import', 'include', 'export'])), Keyword.Namespace), ('(v_?a_?r)\\b', Keyword.Declaration), (f'({underscorize(types)})\\b', Name.Builtin), (f'({underscorize(keywordsPseudo)})\\b', Keyword.Pseudo), ('\\b((?![_\\d])\\w)(((?!_)\\w)|(_(?!_)\\w))*', Name), ("[0-9][0-9_]*(?=([e.]|\\'f(32|64)))", Number.Float, ('float-suffix', 'float-number')), ('0x[a-f0-9][a-f0-9_]*', Number.Hex, 'int-suffix'), ('0b[01][01_]*', Number.Bin, 'int-suffix'), ('0o[0-7][0-7_]*', Number.Oct, 'int-suffix'), ('[0-9][0-9_]*', Number.Integer, 'int-suffix'), ('\\s+', Text.Whitespace), ('.+$', Error)], 'chars': [('\\\\([\\\\abcefnrtvl"\\\']|x[a-f0-9]{2}|[0-9]{1,3})', String.Escape), ("'", String.Char, '#pop'), ('.', String.Char)], 'strings': [('(?<!\\$)\\$(\\d+|#|\\w+)+', String.Interpol), ('[^\\\\\\\'"$\\n]+', String), ('[\\\'"\\\\]', String), ('\\$', String)], 'doccomment': [('[^\\]#]+', String.Doc), ('##\\[', String.Doc, '#push'), ('\\]##', String.Doc, '#pop'), ('[\\]#]', String.Doc)], 'comment': [('[^\\]#]+', Comment.Multiline), ('#\\[', Comment.Multiline, '#push'), ('\\]#', Comment.Multiline, '#pop'), ('[\\]#]', Comment.Multiline)], 'dqs': [('\\\\([\\\\abcefnrtvl"\\\']|\\n|x[a-f0-9]{2}|[0-9]{1,3})', String.Escape), ('"', String, '#pop'), include('strings')], 'rdqs': [('"(?!")', String, '#pop'), ('""', String.Escape), include('strings')], 'tdqs': [('"""', String.Double, '#pop'), include('strings'), ('\\n', String.Double)], 'funcname': [('((?![\\d_])\\w)(((?!_)\\w)|(_(?!_)\\w))*', Name.Function, '#pop'), ('`.+`', Name.Function, '#pop')], 'nl': [('\\n', String)], 'float-number': [('\\.(?!\\.)[0-9_]*[f]*', Number.Float), ('e[+-]?[0-9][0-9_]*', Number.Float), default('#pop')], 'float-suffix': [("\\'f(32|64)", Number.Float), default('#pop')], 'int-suffix': [("\\'i(32|64)", Number.Integer.Long), ("\\'i(8|16)", Number.Integer), default('#pop')], 'casebranch': [(',', Punctuation), ('[\\n ]+', Text.Whitespace), (':', Operator, '#pop'), ('\\w+|[^:]', Name.Label)], 'pragma': [('[:,]', Text), ('[\\n ]+', Text.Whitespace), ('\\.\\}', String.Other, '#pop'), ('\\w+|\\W+|[^.}]', String.Other)]}


