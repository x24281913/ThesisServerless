"""
    pygments.lexers.grammar_notation
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    Lexers for grammar notations like BNF.

    :copyright: Copyright 2006-present by the Pygments team, see AUTHORS.
    :license: BSD, see LICENSE for details.
"""

from pygments.lexer import RegexLexer, bygroups, include, this, using, words
from pygments.token import Comment, Keyword, Literal, Name, Number, Operator, Punctuation, String, Text, Whitespace
__all__ = ['BnfLexer', 'AbnfLexer', 'JsgfLexer', 'PegLexer']


class BnfLexer(RegexLexer):
    """
    This lexer is for grammar notations which are similar to
    original BNF.

    In order to maximize a number of targets of this lexer,
    let's decide some designs:

    * We don't distinguish `Terminal Symbol`.

    * We do assume that `NonTerminal Symbol` are always enclosed
      with arrow brackets.

    * We do assume that `NonTerminal Symbol` may include
      any printable characters except arrow brackets and ASCII 0x20.
      This assumption is for `RBNF <http://www.rfc-base.org/txt/rfc-5511.txt>`_.

    * We do assume that target notation doesn't support comment.

    * We don't distinguish any operators and punctuation except
      `::=`.

    Though these decision making might cause too minimal highlighting
    and you might be disappointed, but it is reasonable for us.
    """
    name = 'BNF'
    aliases = ['bnf']
    filenames = ['*.bnf']
    mimetypes = ['text/x-bnf']
    url = 'https://en.wikipedia.org/wiki/Backus%E2%80%93Naur_form'
    version_added = '2.1'
    tokens = {'root': [('(<)([ -;=?-~]+)(>)', bygroups(Punctuation, Name.Class, Punctuation)), ('::=', Operator), ('[^<>:]+', Text), ('.', Text)]}



class AbnfLexer(RegexLexer):
    """
    Lexer for IETF 7405 ABNF.

    (Updates `5234 <http://www.ietf.org/rfc/rfc5234.txt>`_) grammars.
    """
    name = 'ABNF'
    url = 'http://www.ietf.org/rfc/rfc7405.txt'
    aliases = ['abnf']
    filenames = ['*.abnf']
    mimetypes = ['text/x-abnf']
    version_added = '2.1'
    _core_rules = ('ALPHA', 'BIT', 'CHAR', 'CR', 'CRLF', 'CTL', 'DIGIT', 'DQUOTE', 'HEXDIG', 'HTAB', 'LF', 'LWSP', 'OCTET', 'SP', 'VCHAR', 'WSP')
    tokens = {'root': [(';.*$', Comment.Single), ('(%[si])?"[^"]*"', Literal), ('%b[01]+\\-[01]+\\b', Literal), ('%b[01]+(\\.[01]+)*\\b', Literal), ('%d[0-9]+\\-[0-9]+\\b', Literal), ('%d[0-9]+(\\.[0-9]+)*\\b', Literal), ('%x[0-9a-fA-F]+\\-[0-9a-fA-F]+\\b', Literal), ('%x[0-9a-fA-F]+(\\.[0-9a-fA-F]+)*\\b', Literal), ('\\b[0-9]+\\*[0-9]+', Operator), ('\\b[0-9]+\\*', Operator), ('\\b[0-9]+', Operator), ('\\*', Operator), (words(_core_rules, suffix='\\b'), Keyword), ('[a-zA-Z][a-zA-Z0-9-]*\\b', Name.Class), ('(=/|=|/)', Operator), ('[\\[\\]()]', Punctuation), ('\\s+', Whitespace), ('.', Text)]}



class JsgfLexer(RegexLexer):
    """
    For JSpeech Grammar Format grammars.
    """
    name = 'JSGF'
    url = 'https://www.w3.org/TR/jsgf/'
    aliases = ['jsgf']
    filenames = ['*.jsgf']
    mimetypes = ['application/jsgf', 'application/x-jsgf', 'text/jsgf']
    version_added = '2.2'
    tokens = {'root': [include('comments'), include('non-comments')], 'comments': [('/\\*\\*(?!/)', Comment.Multiline, 'documentation comment'), ('/\\*[\\w\\W]*?\\*/', Comment.Multiline), ('//.*$', Comment.Single)], 'non-comments': [('\\A#JSGF[^;]*', Comment.Preproc), ('\\s+', Whitespace), (';', Punctuation), ('[=|()\\[\\]*+]', Operator), ('/[^/]+/', Number.Float), ('"', String.Double, 'string'), ('\\{', String.Other, 'tag'), (words(('import', 'public'), suffix='\\b'), Keyword.Reserved), ('grammar\\b', Keyword.Reserved, 'grammar name'), ('(<)(NULL|VOID)(>)', bygroups(Punctuation, Name.Builtin, Punctuation)), ('<', Punctuation, 'rulename'), ('\\w+|[^\\s;=|()\\[\\]*+/"{<\\w]+', Text)], 'string': [('"', String.Double, '#pop'), ('\\\\.', String.Escape), ('[^\\\\"]+', String.Double)], 'tag': [('\\}', String.Other, '#pop'), ('\\\\.', String.Escape), ('[^\\\\}]+', String.Other)], 'grammar name': [(';', Punctuation, '#pop'), ('\\s+', Whitespace), ('\\.', Punctuation), ('[^;\\s.]+', Name.Namespace)], 'rulename': [('>', Punctuation, '#pop'), ('\\*', Punctuation), ('\\s+', Whitespace), ('([^.>]+)(\\s*)(\\.)', bygroups(Name.Namespace, Text, Punctuation)), ('[^.>]+', Name.Constant)], 'documentation comment': [('\\*/', Comment.Multiline, '#pop'), ('^(\\s*)(\\*?)(\\s*)(@(?:example|see))(\\s+)([\\w\\W]*?(?=(?:^\\s*\\*?\\s*@|\\*/)))', bygroups(Whitespace, Comment.Multiline, Whitespace, Comment.Special, Whitespace, using(this, state='example'))), ('(^\\s*\\*?\\s*)(@\\S*)', bygroups(Comment.Multiline, Comment.Special)), ('[^*\\n@]+|\\w|\\W', Comment.Multiline)], 'example': [('(\\n\\s*)(\\*)', bygroups(Whitespace, Comment.Multiline)), include('non-comments'), ('.', Comment.Multiline)]}



class PegLexer(RegexLexer):
    """
    This lexer is for Parsing Expression Grammars (PEG).

    Various implementations of PEG have made different decisions
    regarding the syntax, so let's try to be accommodating:

    * `<-`, `←`, `:`, and `=` are all accepted as rule operators.

    * Both `|` and `/` are choice operators.

    * `^`, `↑`, and `~` are cut operators.

    * A single `a-z` character immediately before a string, or
      multiple `a-z` characters following a string, are part of the
      string (e.g., `r"..."` or `"..."ilmsuxa`).
    """
    name = 'PEG'
    url = 'https://bford.info/pub/lang/peg.pdf'
    aliases = ['peg']
    filenames = ['*.peg']
    mimetypes = ['text/x-peg']
    version_added = '2.6'
    tokens = {'root': [('#.*$', Comment.Single), ('<-|[←:=/|&!?*+^↑~]', Operator), ('[()]', Punctuation), ('\\.', Keyword), ('(\\[)([^\\]]*(?:\\\\.[^\\]\\\\]*)*)(\\])', bygroups(Punctuation, String, Punctuation)), ('[a-z]?"[^"\\\\]*(?:\\\\.[^"\\\\]*)*"[a-z]*', String.Double), ("[a-z]?'[^'\\\\]*(?:\\\\.[^'\\\\]*)*'[a-z]*", String.Single), ('[^\\s<←:=/|&!?*+\\^↑~()\\[\\]"\\\'#]+', Name.Class), ('.', Text)]}


