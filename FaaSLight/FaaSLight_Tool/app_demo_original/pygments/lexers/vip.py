"""
    pygments.lexers.vip
    ~~~~~~~~~~~~~~~~~~~

    Lexers for Visual Prolog & Grammar files.

    :copyright: Copyright 2006-present by the Pygments team, see AUTHORS.
    :license: BSD, see LICENSE for details.
"""

import re
from pygments.lexer import RegexLexer, inherit, words, include
from pygments.token import Text, Comment, Operator, Keyword, Name, String, Number, Punctuation, Whitespace
__all__ = ['VisualPrologLexer', 'VisualPrologGrammarLexer']


class VisualPrologBaseLexer(RegexLexer):
    minorendkw = ('try', 'foreach', 'if')
    minorkwexp = ('and', 'catch', 'do', 'else', 'elseif', 'erroneous', 'externally', 'failure', 'finally', 'foreach', 'if', 'or', 'orelse', 'otherwise', 'then', 'try', 'div', 'mod', 'rem', 'quot')
    dockw = ('short', 'detail', 'end', 'withdomain')
    tokens = {'root': [('\\s+', Whitespace), (words(minorendkw, prefix='\\bend\\s+', suffix='\\b'), Keyword.Minor), ('end', Keyword), (words(minorkwexp, suffix='\\b'), Keyword.Minor), ('0[xo][\\da-fA-F_]+', Number), ('((\\d[\\d_]*)?\\.)?\\d[\\d_]*([eE][\\-+]?\\d+)?', Number), ('_\\w*', Name.Variable.Anonymous), ('[A-Z]\\w*', Name.Variable), ('@\\w+', Name.Variable), ('[a-z]\\w*', Name), ('/\\*', Comment, 'comment'), ('\\%', Comment, 'commentline'), ('"', String.Symbol, 'string'), ("\\'", String.Symbol, 'stringsingle'), ('@"', String.Symbol, 'atstring'), ('[\\-+*^/!?<>=~:]+', Operator), ('[$,.[\\]|(){}\\\\]+', Punctuation), ('.', Text)], 'commentdoc': [(words(dockw, prefix='@', suffix='\\b'), Comment.Preproc), ('@', Comment)], 'commentline': [include('commentdoc'), ('[^@\\n]+', Comment), ('$', Comment, '#pop')], 'comment': [include('commentdoc'), ('[^@*/]+', Comment), ('/\\*', Comment, '#push'), ('\\*/', Comment, '#pop'), ('[*/]', Comment)], 'stringescape': [('\\\\u[0-9a-fA-F]{4}', String.Escape), ('\\\\[\\\'"ntr\\\\]', String.Escape)], 'stringsingle': [include('stringescape'), ("\\'", String.Symbol, '#pop'), ("[^\\'\\\\\\n]+", String), ('\\n', String.Escape.Error, '#pop')], 'string': [include('stringescape'), ('"', String.Symbol, '#pop'), ('[^"\\\\\\n]+', String), ('\\n', String.Escape.Error, '#pop')], 'atstring': [('""', String.Escape), ('"', String.Symbol, '#pop'), ('[^"]+', String)]}



class VisualPrologLexer(VisualPrologBaseLexer):
    """Lexer for VisualProlog
    """
    name = 'Visual Prolog'
    url = 'https://www.visual-prolog.com/'
    aliases = ['visualprolog']
    filenames = ['*.pro', '*.cl', '*.i', '*.pack', '*.ph']
    version_added = '2.17'
    majorkw = ('goal', 'namespace', 'interface', 'class', 'implement', 'where', 'open', 'inherits', 'supports', 'resolve', 'delegate', 'monitor', 'constants', 'domains', 'predicates', 'constructors', 'properties', 'clauses', 'facts')
    minorkw = ('align', 'anyflow', 'as', 'bitsize', 'determ', 'digits', 'erroneous', 'externally', 'failure', 'from', 'guard', 'multi', 'nondeterm', 'or', 'orelse', 'otherwise', 'procedure', 'resolve', 'single', 'suspending')
    directivekw = ('bininclude', 'else', 'elseif', 'endif', 'error', 'export', 'externally', 'from', 'grammargenerate', 'grammarinclude', 'if', 'include', 'message', 'options', 'orrequires', 'requires', 'stringinclude', 'then')
    tokens = {'root': [(words(minorkw, suffix='\\b'), Keyword.Minor), (words(majorkw, suffix='\\b'), Keyword), (words(directivekw, prefix='#', suffix='\\b'), Keyword.Directive), inherit]}
    
    def analyse_text(text):
        """Competes with IDL and Prolog on *.pro; div. lisps on*.cl and SwigLexer on *.i"""
        if re.search('^\\s*(end\\s+(interface|class|implement)|(clauses|predicates|domains|facts|constants|properties)\\s*$)', text):
            return 0.98
        else:
            return 0



class VisualPrologGrammarLexer(VisualPrologBaseLexer):
    """Lexer for VisualProlog grammar
    """
    name = 'Visual Prolog Grammar'
    url = 'https://www.visual-prolog.com/'
    aliases = ['visualprologgrammar']
    filenames = ['*.vipgrm']
    version_added = '2.17'
    majorkw = ('open', 'namespace', 'grammar', 'nonterminals', 'startsymbols', 'terminals', 'rules', 'precedence')
    directivekw = ('bininclude', 'stringinclude')
    tokens = {'root': [(words(majorkw, suffix='\\b'), Keyword), (words(directivekw, prefix='#', suffix='\\b'), Keyword.Directive), inherit]}
    
    def analyse_text(text):
        """No competditors (currently)"""
        if re.search('^\\s*(end\\s+grammar|(nonterminals|startsymbols|terminals|rules|precedence)\\s*$)', text):
            return 0.98
        else:
            return 0


