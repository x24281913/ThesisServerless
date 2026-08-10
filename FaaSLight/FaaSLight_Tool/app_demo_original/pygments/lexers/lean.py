"""
    pygments.lexers.lean
    ~~~~~~~~~~~~~~~~~~~~

    Lexers for the Lean theorem prover.

    :copyright: Copyright 2006-present by the Pygments team, see AUTHORS.
    :license: BSD, see LICENSE for details.
"""

import re
from pygments.lexer import RegexLexer, words, include
from pygments.token import Comment, Operator, Keyword, Name, String, Number, Generic, Whitespace
__all__ = ['Lean3Lexer', 'Lean4Lexer']


class Lean3Lexer(RegexLexer):
    """
    For the Lean 3 theorem prover.
    """
    name = 'Lean'
    url = 'https://leanprover-community.github.io/lean3'
    aliases = ['lean', 'lean3']
    filenames = ['*.lean']
    mimetypes = ['text/x-lean', 'text/x-lean3']
    version_added = '2.0'
    _name_segment = "(?![λΠΣ])[_a-zA-Zα-ωΑ-Ωϊ-ϻἀ-῾℀-⅏𝒜-𝖟](?:(?![λΠΣ])[_a-zA-Zα-ωΑ-Ωϊ-ϻἀ-῾℀-⅏𝒜-𝖟0-9'ⁿ-₉ₐ-ₜᵢ-ᵪ])*"
    _name = _name_segment + '(\\.' + _name_segment + ')*'
    tokens = {'expression': [('\\s+', Whitespace), ('/--', String.Doc, 'docstring'), ('/-', Comment, 'comment'), ('--.*?$', Comment.Single), (words(('forall', 'fun', 'Pi', 'from', 'have', 'show', 'assume', 'suffices', 'let', 'if', 'else', 'then', 'in', 'with', 'calc', 'match', 'do'), prefix='\\b', suffix='\\b'), Keyword), (words(('sorry', 'admit'), prefix='\\b', suffix='\\b'), Generic.Error), (words(('Sort', 'Prop', 'Type'), prefix='\\b', suffix='\\b'), Keyword.Type), (words(('(', ')', ':', '{', '}', '[', ']', '⟨', '⟩', '‹', '›', '⦃', '⦄', ':=', ',')), Operator), (_name, Name), ('``?' + _name, String.Symbol), ('0x[A-Za-z0-9]+', Number.Integer), ('0b[01]+', Number.Integer), ('\\d+', Number.Integer), ('"', String.Double, 'string'), ('\'(?:(\\\\[\\\\\\"\'nt])|(\\\\x[0-9a-fA-F]{2})|(\\\\u[0-9a-fA-F]{4})|.)\'', String.Char), ("[~?][a-z][\\w\\']*:", Name.Variable), ('\\S', Name.Builtin.Pseudo)], 'root': [(words(('import', 'renaming', 'hiding', 'namespace', 'local', 'private', 'protected', 'section', 'include', 'omit', 'section', 'protected', 'export', 'open', 'attribute'), prefix='\\b', suffix='\\b'), Keyword.Namespace), (words(('lemma', 'theorem', 'def', 'definition', 'example', 'axiom', 'axioms', 'constant', 'constants', 'universe', 'universes', 'inductive', 'coinductive', 'structure', 'extends', 'class', 'instance', 'abbreviation', 'noncomputable theory', 'noncomputable', 'mutual', 'meta', 'attribute', 'parameter', 'parameters', 'variable', 'variables', 'reserve', 'precedence', 'postfix', 'prefix', 'notation', 'infix', 'infixl', 'infixr', 'begin', 'by', 'end', 'set_option', 'run_cmd'), prefix='\\b', suffix='\\b'), Keyword.Declaration), ('@\\[', Keyword.Declaration, 'attribute'), (words(('#eval', '#check', '#reduce', '#exit', '#print', '#help'), suffix='\\b'), Keyword), include('expression')], 'attribute': [('\\]', Keyword.Declaration, '#pop'), include('expression')], 'comment': [('[^/-]+', Comment.Multiline), ('/-', Comment.Multiline, '#push'), ('-/', Comment.Multiline, '#pop'), ('[/-]', Comment.Multiline)], 'docstring': [('[^/-]+', String.Doc), ('-/', String.Doc, '#pop'), ('[/-]', String.Doc)], 'string': [('[^\\\\"]+', String.Double), ('(?:(\\\\[\\\\\\"\'nt])|(\\\\x[0-9a-fA-F]{2})|(\\\\u[0-9a-fA-F]{4}))', String.Escape), ('"', String.Double, '#pop')]}
    
    def analyse_text(text):
        if re.search('^import [a-z]', text, re.MULTILINE):
            return 0.1

LeanLexer = Lean3Lexer


class Lean4Lexer(RegexLexer):
    """
    For the Lean 4 theorem prover.
    """
    name = 'Lean4'
    url = 'https://github.com/leanprover/lean4'
    aliases = ['lean4']
    filenames = ['*.lean']
    mimetypes = ['text/x-lean4']
    version_added = '2.18'
    _name_segment = "(?![λΠΣ])[_a-zA-Zα-ωΑ-Ωϊ-ϻἀ-῾℀-⅏𝒜-𝖟](?:(?![λΠΣ])[_a-zA-Zα-ωΑ-Ωϊ-ϻἀ-῾℀-⅏𝒜-𝖟0-9'ⁿ-₉ₐ-ₜᵢ-ᵪ!?])*"
    _name = _name_segment + '(\\.' + _name_segment + ')*'
    keywords1 = ('import', 'unif_hint', 'renaming', 'inline', 'hiding', 'lemma', 'variable', 'theorem', 'axiom', 'inductive', 'structure', 'universe', 'alias', '#help', 'precedence', 'postfix', 'prefix', 'infix', 'infixl', 'infixr', 'notation', '#eval', '#check', '#reduce', '#exit', 'end', 'private', 'using', 'namespace', 'instance', 'section', 'protected', 'export', 'set_option', 'extends', 'open', 'example', '#print', 'opaque', 'def', 'macro', 'elab', 'syntax', 'macro_rules', '#reduce', 'where', 'abbrev', 'noncomputable', 'class', 'attribute', '#synth', 'mutual', 'scoped', 'local')
    keywords2 = ('forall', 'fun', 'obtain', 'from', 'have', 'show', 'assume', 'let', 'if', 'else', 'then', 'by', 'in', 'with', 'calc', 'match', 'nomatch', 'do', 'at')
    keywords3 = ('Type', 'Prop', 'Sort')
    operators = ('!=', '#', '&', '&&', '*', '+', '-', '/', '@', '!', '-.', '->', '.', '..', '...', '::', ':>', ';', ';;', '<', '<-', '=', '==', '>', '_', '|', '||', '~', '=>', '<=', '>=', '/\\', '\\/', '∀', 'Π', 'λ', '↔', '∧', '∨', '≠', '≤', '≥', '¬', '⁻¹', '⬝', '▸', '→', '∃', '≈', '×', '⌞', '⌟', '≡', '⟨', '⟩', '↦')
    punctuation = ('(', ')', ':', '{', '}', '[', ']', '⦃', '⦄', ':=', ',', "]'", ']?', ']!')
    tokens = {'expression': [('\\s+', Whitespace), ('/--', String.Doc, 'docstring'), ('/-', Comment, 'comment'), ('--.*$', Comment.Single), (words(keywords3, prefix='\\b', suffix='\\b'), Keyword.Type), (words(('sorry', 'admit'), prefix='\\b', suffix='\\b'), Generic.Error), (words(operators), Name.Builtin.Pseudo), (words(punctuation), Operator), (_name_segment, Name), ('``?' + _name, String.Symbol), ('(?<=\\.)\\d+', Number), ('(\\d+\\.\\d*)([eE][+-]?[0-9]+)?', Number.Float), ('\\d+', Number.Integer), ('"', String.Double, 'string'), ("[~?][a-z][\\w\\']*:", Name.Variable), ('\\S', Name.Builtin.Pseudo)], 'root': [(words(keywords1, prefix='\\b', suffix='\\b'), Keyword.Namespace), (words(keywords2, prefix='\\b', suffix='\\b'), Keyword), ('@\\[', Keyword.Declaration, 'attribute'), include('expression')], 'attribute': [('\\]', Keyword.Declaration, '#pop'), include('expression')], 'comment': [('[^/-]+', Comment.Multiline), ('/-', Comment.Multiline, '#push'), ('-/', Comment.Multiline, '#pop'), ('[/-]', Comment.Multiline)], 'docstring': [('[^/-]+', String.Doc), ('-/', String.Doc, '#pop'), ('[/-]', String.Doc)], 'string': [('[^\\\\"]+', String.Double), ('\\\\[n"\\\\\\n]', String.Escape), ('"', String.Double, '#pop')]}
    
    def analyse_text(text):
        if re.search('^import [A-Z]', text, re.MULTILINE):
            return 0.1


