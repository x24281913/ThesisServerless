"""
    pygments.lexers.smalltalk
    ~~~~~~~~~~~~~~~~~~~~~~~~~

    Lexers for Smalltalk and related languages.

    :copyright: Copyright 2006-present by the Pygments team, see AUTHORS.
    :license: BSD, see LICENSE for details.
"""

from pygments.lexer import RegexLexer, include, bygroups, default
from pygments.token import Text, Comment, Operator, Keyword, Name, String, Number, Punctuation
__all__ = ['SmalltalkLexer', 'NewspeakLexer']


class SmalltalkLexer(RegexLexer):
    """
    For Smalltalk syntax.
    Contributed by Stefan Matthias Aust.
    Rewritten by Nils Winter.
    """
    name = 'Smalltalk'
    url = 'http://www.smalltalk.org/'
    filenames = ['*.st']
    aliases = ['smalltalk', 'squeak', 'st']
    mimetypes = ['text/x-smalltalk']
    version_added = '0.10'
    tokens = {'root': [('(<)(\\w+:)(.*?)(>)', bygroups(Text, Keyword, Text, Text)), include('squeak fileout'), include('whitespaces'), include('method definition'), ('(\\|)([\\w\\s]*)(\\|)', bygroups(Operator, Name.Variable, Operator)), include('objects'), ('\\^|\\:=|\\_', Operator), ('[\\]({}.;!]', Text)], 'method definition': [('([a-zA-Z]+\\w*:)(\\s*)(\\w+)', bygroups(Name.Function, Text, Name.Variable)), ('^(\\b[a-zA-Z]+\\w*\\b)(\\s*)$', bygroups(Name.Function, Text)), ('^([-+*/\\\\~<>=|&!?,@%]+)(\\s*)(\\w+)(\\s*)$', bygroups(Name.Function, Text, Name.Variable, Text))], 'blockvariables': [include('whitespaces'), ('(:)(\\s*)(\\w+)', bygroups(Operator, Text, Name.Variable)), ('\\|', Operator, '#pop'), default('#pop')], 'literals': [("'(''|[^'])*'", String, 'afterobject'), ('\\$.', String.Char, 'afterobject'), ('#\\(', String.Symbol, 'parenth'), ('\\)', Text, 'afterobject'), ('(\\d+r)?-?\\d+(\\.\\d+)?(e-?\\d+)?', Number, 'afterobject')], '_parenth_helper': [include('whitespaces'), ('(\\d+r)?-?\\d+(\\.\\d+)?(e-?\\d+)?', Number), ('[-+*/\\\\~<>=|&#!?,@%\\w:]+', String.Symbol), ("'(''|[^'])*'", String), ('\\$.', String.Char), ('#*\\(', String.Symbol, 'inner_parenth')], 'parenth': [('\\)', String.Symbol, ('root', 'afterobject')), include('_parenth_helper')], 'inner_parenth': [('\\)', String.Symbol, '#pop'), include('_parenth_helper')], 'whitespaces': [('\\s+', Text), ('"(""|[^"])*"', Comment)], 'objects': [('\\[', Text, 'blockvariables'), ('\\]', Text, 'afterobject'), ('\\b(self|super|true|false|nil|thisContext)\\b', Name.Builtin.Pseudo, 'afterobject'), ('\\b[A-Z]\\w*(?!:)\\b', Name.Class, 'afterobject'), ('\\b[a-z]\\w*(?!:)\\b', Name.Variable, 'afterobject'), ('#("(""|[^"])*"|[-+*/\\\\~<>=|&!?,@%]+|[\\w:]+)', String.Symbol, 'afterobject'), include('literals')], 'afterobject': [('! !$', Keyword, '#pop'), include('whitespaces'), ('\\b(ifTrue:|ifFalse:|whileTrue:|whileFalse:|timesRepeat:)', Name.Builtin, '#pop'), ('\\b(new\\b(?!:))', Name.Builtin), ('\\:=|\\_', Operator, '#pop'), ('\\b[a-zA-Z]+\\w*:', Name.Function, '#pop'), ('\\b[a-zA-Z]+\\w*', Name.Function), ('\\w+:?|[-+*/\\\\~<>=|&!?,@%]+', Name.Function, '#pop'), ('\\.', Punctuation, '#pop'), (';', Punctuation), ('[\\])}]', Text), ('[\\[({]', Text, '#pop')], 'squeak fileout': [('^"(""|[^"])*"!', Keyword), ("^'(''|[^'])*'!", Keyword), ('^(!)(\\w+)( commentStamp: )(.*?)( prior: .*?!\\n)(.*?)(!)', bygroups(Keyword, Name.Class, Keyword, String, Keyword, Text, Keyword)), ("^(!)(\\w+(?: class)?)( methodsFor: )('(?:''|[^'])*')(.*?!)", bygroups(Keyword, Name.Class, Keyword, String, Keyword)), ('^(\\w+)( subclass: )(#\\w+)(\\s+instanceVariableNames: )(.*?)(\\s+classVariableNames: )(.*?)(\\s+poolDictionaries: )(.*?)(\\s+category: )(.*?)(!)', bygroups(Name.Class, Keyword, String.Symbol, Keyword, String, Keyword, String, Keyword, String, Keyword, String, Keyword)), ('^(\\w+(?: class)?)(\\s+instanceVariableNames: )(.*?)(!)', bygroups(Name.Class, Keyword, String, Keyword)), ('(!\\n)(\\].*)(! !)$', bygroups(Keyword, Text, Keyword)), ('! !$', Keyword)]}



class NewspeakLexer(RegexLexer):
    """
    For Newspeak syntax.
    """
    name = 'Newspeak'
    url = 'http://newspeaklanguage.org/'
    filenames = ['*.ns2']
    aliases = ['newspeak']
    mimetypes = ['text/x-newspeak']
    version_added = '1.1'
    tokens = {'root': [('\\b(Newsqueak2)\\b', Keyword.Declaration), ("'[^']*'", String), ('\\b(class)(\\s+)(\\w+)(\\s*)', bygroups(Keyword.Declaration, Text, Name.Class, Text)), ('\\b(mixin|self|super|private|public|protected|nil|true|false)\\b', Keyword), ('(\\w+\\:)(\\s*)([a-zA-Z_]\\w+)', bygroups(Name.Function, Text, Name.Variable)), ('(\\w+)(\\s*)(=)', bygroups(Name.Attribute, Text, Operator)), ('<\\w+>', Comment.Special), include('expressionstat'), include('whitespace')], 'expressionstat': [('(\\d+\\.\\d*|\\.\\d+|\\d+[fF])[fF]?', Number.Float), ('\\d+', Number.Integer), (':\\w+', Name.Variable), ('(\\w+)(::)', bygroups(Name.Variable, Operator)), ('\\w+:', Name.Function), ('\\w+', Name.Variable), ('\\(|\\)', Punctuation), ('\\[|\\]', Punctuation), ('\\{|\\}', Punctuation), ('(\\^|\\+|\\/|~|\\*|<|>|=|@|%|\\||&|\\?|!|,|-|:)', Operator), ('\\.|;', Punctuation), include('whitespace'), include('literals')], 'literals': [('\\$.', String), ("'[^']*'", String), ("#'[^']*'", String.Symbol), ('#\\w+:?', String.Symbol), ('#(\\+|\\/|~|\\*|<|>|=|@|%|\\||&|\\?|!|,|-)+', String.Symbol)], 'whitespace': [('\\s+', Text), ('"[^"]*"', Comment)]}


