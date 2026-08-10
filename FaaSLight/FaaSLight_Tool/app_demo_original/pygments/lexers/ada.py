"""
    pygments.lexers.ada
    ~~~~~~~~~~~~~~~~~~~

    Lexers for Ada family languages.

    :copyright: Copyright 2006-present by the Pygments team, see AUTHORS.
    :license: BSD, see LICENSE for details.
"""

import re
from pygments.lexer import RegexLexer, include, bygroups, words, using, this, default
from pygments.token import Text, Comment, Operator, Keyword, Name, String, Number, Punctuation
from pygments.lexers._ada_builtins import KEYWORD_LIST, BUILTIN_LIST
__all__ = ['AdaLexer']


class AdaLexer(RegexLexer):
    """
    For Ada source code.
    """
    name = 'Ada'
    aliases = ['ada', 'ada95', 'ada2005']
    filenames = ['*.adb', '*.ads', '*.ada']
    mimetypes = ['text/x-ada']
    url = 'https://www.adaic.org'
    version_added = '1.3'
    flags = re.MULTILINE | re.IGNORECASE
    tokens = {'root': [('[^\\S\\n]+', Text), ('--.*?\\n', Comment.Single), ('[^\\S\\n]+', Text), ('function|procedure|entry', Keyword.Declaration, 'subprogram'), ('(subtype|type)(\\s+)(\\w+)', bygroups(Keyword.Declaration, Text, Keyword.Type), 'type_def'), ('task|protected', Keyword.Declaration), ('(subtype)(\\s+)', bygroups(Keyword.Declaration, Text)), ('(end)(\\s+)', bygroups(Keyword.Reserved, Text), 'end'), ('(pragma)(\\s+)(\\w+)', bygroups(Keyword.Reserved, Text, Comment.Preproc)), ('(true|false|null)\\b', Keyword.Constant), (words(BUILTIN_LIST, suffix='\\b'), Keyword.Type), ('(and(\\s+then)?|in|mod|not|or(\\s+else)|rem)\\b', Operator.Word), ('generic|private', Keyword.Declaration), ('package', Keyword.Declaration, 'package'), ('array\\b', Keyword.Reserved, 'array_def'), ('(with|use)(\\s+)', bygroups(Keyword.Namespace, Text), 'import'), ('(\\w+)(\\s*)(:)(\\s*)(constant)', bygroups(Name.Constant, Text, Punctuation, Text, Keyword.Reserved)), ('<<\\w+>>', Name.Label), ('(\\w+)(\\s*)(:)(\\s*)(declare|begin|loop|for|while)', bygroups(Name.Label, Text, Punctuation, Text, Keyword.Reserved)), (words(KEYWORD_LIST, prefix='\\b', suffix='\\b'), Keyword.Reserved), ('"[^"]*"', String), include('attribute'), include('numbers'), ("'[^']'", String.Character), ('(\\w+)(\\s*|[(,])', bygroups(Name, using(this))), ("(<>|=>|:=|@|[\\[\\]]|[()|:;,.'])", Punctuation), ('[*<>+=/&-]', Operator), ('\\n+', Text)], 'numbers': [('[0-9_]+#[0-9a-f_\\.]+#', Number.Hex), ('[0-9_]+\\.[0-9_]*', Number.Float), ('[0-9_]+', Number.Integer)], 'attribute': [("(')(\\w+)", bygroups(Punctuation, Name.Attribute))], 'subprogram': [('\\(', Punctuation, ('#pop', 'formal_part')), (';', Punctuation, '#pop'), ('is\\b', Keyword.Reserved, '#pop'), ('"[^"]+"|\\w+', Name.Function), include('root')], 'end': [('(if|case|record|loop|select)', Keyword.Reserved), ('"[^"]+"|[\\w.]+', Name.Function), ('\\s+', Text), (';', Punctuation, '#pop')], 'type_def': [(';', Punctuation, '#pop'), ('\\(', Punctuation, 'formal_part'), ('\\[', Punctuation, 'formal_part'), ('with|and|use', Keyword.Reserved), ('array\\b', Keyword.Reserved, ('#pop', 'array_def')), ('record\\b', Keyword.Reserved, 'record_def'), ('(null record)(;)', bygroups(Keyword.Reserved, Punctuation), '#pop'), include('root')], 'array_def': [(';', Punctuation, '#pop'), ('(\\w+)(\\s+)(range)', bygroups(Keyword.Type, Text, Keyword.Reserved)), include('root')], 'record_def': [('end record', Keyword.Reserved, '#pop'), include('root')], 'import': [('[\\w.]+', Name, '#pop'), default('#pop')], 'formal_part': [('\\)', Punctuation, '#pop'), ('\\]', Punctuation, '#pop'), ('\\w+', Name.Variable), (',|:[^=]', Punctuation), ('(in|not|null|out|access)\\b', Keyword.Reserved), include('root')], 'package': [('body', Keyword.Declaration), ('is\\s+new|renames', Keyword.Reserved), ('is', Keyword.Reserved, '#pop'), (';', Punctuation, '#pop'), ('\\(', Punctuation, 'package_instantiation'), ('([\\w.]+)', Name.Class), include('root')], 'package_instantiation': [('("[^"]+"|\\w+)(\\s+)(=>)', bygroups(Name.Variable, Text, Punctuation)), ('[\\w.\\\'"]', Text), ('\\)', Punctuation, '#pop'), include('root')]}


