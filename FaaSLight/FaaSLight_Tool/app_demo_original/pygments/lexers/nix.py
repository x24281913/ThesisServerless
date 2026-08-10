"""
    pygments.lexers.nix
    ~~~~~~~~~~~~~~~~~~~

    Lexers for the NixOS Nix language.

    :copyright: Copyright 2006-present by the Pygments team, see AUTHORS.
    :license: BSD, see LICENSE for details.
"""

import re
from pygments.lexer import RegexLexer, include
from pygments.token import Text, Comment, Operator, Keyword, Name, String, Number, Punctuation, Literal
__all__ = ['NixLexer']


class NixLexer(RegexLexer):
    """
    For the Nix language.
    """
    name = 'Nix'
    url = 'http://nixos.org/nix/'
    aliases = ['nixos', 'nix']
    filenames = ['*.nix']
    mimetypes = ['text/x-nix']
    version_added = '2.0'
    keywords = ['rec', 'with', 'let', 'in', 'inherit', 'assert', 'if', 'else', 'then', '...']
    builtins = ['import', 'abort', 'baseNameOf', 'dirOf', 'isNull', 'builtins', 'map', 'removeAttrs', 'throw', 'toString', 'derivation']
    operators = ['++', '+', '?', '.', '!', '//', '==', '/', '!=', '&&', '||', '->', '=', '<', '>', '*', '-']
    punctuations = ['(', ')', '[', ']', ';', '{', '}', ':', ',', '@']
    tokens = {'root': [('#.*$', Comment.Single), ('/\\*', Comment.Multiline, 'comment'), ('\\s+', Text), ('({})'.format('|'.join((re.escape(entry) + '\\b' for entry in keywords))), Keyword), ('({})'.format('|'.join((re.escape(entry) + '\\b' for entry in builtins))), Name.Builtin), ('\\b(true|false|null)\\b', Name.Constant), ('-?(\\d+\\.\\d*|\\.\\d+)([eE][-+]?\\d+)?', Number.Float), ('-?[0-9]+', Number.Integer), ('[\\w.+-]*(\\/[\\w.+-]+)+', Literal), ('~(\\/[\\w.+-]+)+', Literal), ('\\<[\\w.+-]+(\\/[\\w.+-]+)*\\>', Literal), ('({})'.format('|'.join((re.escape(entry) for entry in operators))), Operator), ('\\b(or|and)\\b', Operator.Word), ('\\{', Punctuation, 'block'), ('({})'.format('|'.join((re.escape(entry) for entry in punctuations))), Punctuation), ('"', String.Double, 'doublequote'), ("''", String.Multiline, 'multiline'), ("[a-zA-Z][a-zA-Z0-9\\+\\-\\.]*\\:[\\w%/?:@&=+$,\\\\.!~*\\'-]+", Literal), ('[\\w-]+(?=\\s*=)', String.Symbol), ("[a-zA-Z_][\\w\\'-]*", Text), ('\\$\\{', String.Interpol, 'antiquote')], 'comment': [('[^/*]+', Comment.Multiline), ('/\\*', Comment.Multiline, '#push'), ('\\*/', Comment.Multiline, '#pop'), ('[*/]', Comment.Multiline)], 'multiline': [("''(\\$|'|\\\\n|\\\\r|\\\\t|\\\\)", String.Escape), ("''", String.Multiline, '#pop'), ('\\$\\{', String.Interpol, 'antiquote'), ("[^'\\$]+", String.Multiline), ("\\$[^\\{']", String.Multiline), ("'[^']", String.Multiline), ("\\$(?=')", String.Multiline)], 'doublequote': [('\\\\(\\\\|"|\\$|n)', String.Escape), ('"', String.Double, '#pop'), ('\\$\\{', String.Interpol, 'antiquote'), ('[^"\\\\\\$]+', String.Double), ('\\$[^\\{"]', String.Double), ('\\$(?=")', String.Double), ('\\\\', String.Double)], 'antiquote': [('\\}', String.Interpol, '#pop'), ('\\$\\{', String.Interpol, '#push'), include('root')], 'block': [('\\}', Punctuation, '#pop'), include('root')]}
    
    def analyse_text(text):
        rv = 0.0
        if re.search('import.+?<[^>]+>', text):
            rv += 0.4
        if re.search('mkDerivation\\s+(\\(|\\{|rec)', text):
            rv += 0.4
        if re.search('=\\s+mkIf\\s+', text):
            rv += 0.4
        if re.search('\\{[a-zA-Z,\\s]+\\}:', text):
            rv += 0.1
        return rv


