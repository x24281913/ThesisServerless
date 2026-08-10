"""
    pygments.lexers.verification
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    Lexer for Intermediate Verification Languages (IVLs).

    :copyright: Copyright 2006-present by the Pygments team, see AUTHORS.
    :license: BSD, see LICENSE for details.
"""

from pygments.lexer import RegexLexer, include, words
from pygments.token import Comment, Operator, Keyword, Name, Number, Punctuation, Text, Generic
__all__ = ['BoogieLexer', 'SilverLexer']


class BoogieLexer(RegexLexer):
    """
    For Boogie source code.
    """
    name = 'Boogie'
    url = 'https://boogie-docs.readthedocs.io/en/latest/'
    aliases = ['boogie']
    filenames = ['*.bpl']
    version_added = '2.1'
    tokens = {'root': [('\\n', Text), ('\\s+', Text), ('\\\\\\n', Text), ('//[/!](.*?)\\n', Comment.Doc), ('//(.*?)\\n', Comment.Single), ('/\\*', Comment.Multiline, 'comment'), (words(('axiom', 'break', 'call', 'ensures', 'else', 'exists', 'function', 'forall', 'if', 'invariant', 'modifies', 'procedure', 'requires', 'then', 'var', 'while'), suffix='\\b'), Keyword), (words(('const', ), suffix='\\b'), Keyword.Reserved), (words(('bool', 'int', 'ref'), suffix='\\b'), Keyword.Type), include('numbers'), ('(>=|<=|:=|!=|==>|&&|\\|\\||[+/\\-=>*<\\[\\]])', Operator), ('\\{.*?\\}', Generic.Emph), ('([{}():;,.])', Punctuation), ('[a-zA-Z_]\\w*', Name)], 'comment': [('[^*/]+', Comment.Multiline), ('/\\*', Comment.Multiline, '#push'), ('\\*/', Comment.Multiline, '#pop'), ('[*/]', Comment.Multiline)], 'numbers': [('[0-9]+', Number.Integer)]}



class SilverLexer(RegexLexer):
    """
    For Silver source code.
    """
    name = 'Silver'
    aliases = ['silver']
    filenames = ['*.sil', '*.vpr']
    url = 'https://github.com/viperproject/silver'
    version_added = '2.2'
    tokens = {'root': [('\\n', Text), ('\\s+', Text), ('\\\\\\n', Text), ('//[/!](.*?)\\n', Comment.Doc), ('//(.*?)\\n', Comment.Single), ('/\\*', Comment.Multiline, 'comment'), (words(('result', 'true', 'false', 'null', 'method', 'function', 'predicate', 'program', 'domain', 'axiom', 'var', 'returns', 'field', 'define', 'fold', 'unfold', 'inhale', 'exhale', 'new', 'assert', 'assume', 'goto', 'while', 'if', 'elseif', 'else', 'fresh', 'constraining', 'Seq', 'Set', 'Multiset', 'union', 'intersection', 'setminus', 'subset', 'unfolding', 'in', 'old', 'forall', 'exists', 'acc', 'wildcard', 'write', 'none', 'epsilon', 'perm', 'unique', 'apply', 'package', 'folding', 'label', 'forperm'), suffix='\\b'), Keyword), (words(('requires', 'ensures', 'invariant'), suffix='\\b'), Name.Decorator), (words(('Int', 'Perm', 'Bool', 'Ref', 'Rational'), suffix='\\b'), Keyword.Type), include('numbers'), ('[!%&*+=|?:<>/\\-\\[\\]]', Operator), ('\\{.*?\\}', Generic.Emph), ('([{}():;,.])', Punctuation), ('[\\w$]\\w*', Name)], 'comment': [('[^*/]+', Comment.Multiline), ('/\\*', Comment.Multiline, '#push'), ('\\*/', Comment.Multiline, '#pop'), ('[*/]', Comment.Multiline)], 'numbers': [('[0-9]+', Number.Integer)]}


