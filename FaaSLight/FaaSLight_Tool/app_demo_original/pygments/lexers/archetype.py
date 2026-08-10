"""
    pygments.lexers.archetype
    ~~~~~~~~~~~~~~~~~~~~~~~~~

    Lexer for Archetype-related syntaxes, including ODIN, ADL and cADL.

    For uses of this syntax, see the openEHR archetypes <http://www.openEHR.org/ckm>

    Contributed by Thomas Beale <https://github.com/wolandscat>,
    <https://bitbucket.org/thomas_beale>.

    :copyright: Copyright 2006-present by the Pygments team, see AUTHORS.
    :license: BSD, see LICENSE for details.
"""

from pygments.lexer import RegexLexer, include, bygroups, using, default
from pygments.token import Text, Comment, Name, Literal, Number, String, Punctuation, Keyword, Operator, Generic, Whitespace
__all__ = ['OdinLexer', 'CadlLexer', 'AdlLexer']


class AtomsLexer(RegexLexer):
    """
    Lexer for Values used in ADL and ODIN.

    .. versionadded:: 2.1
    """
    tokens = {'whitespace': [('\\n', Whitespace), ('\\s+', Whitespace), ('([ \\t]*)(--.*)$', bygroups(Whitespace, Comment))], 'archetype_id': [('([ \\t]*)(([a-zA-Z]\\w{1,100}(\\.[a-zA-Z]\\w{1,100})*::)?[a-zA-Z]\\w{1,100}(-[a-zA-Z]\\w{1,100}){2}\\.\\w{1,100}[\\w-]*\\.v\\d+(\\.\\d+){,2}((-[a-z]+)(\\.\\d+)?)?)', bygroups(Whitespace, Name.Decorator))], 'date_constraints': [('[Xx?YyMmDdHhSs\\d]{2,4}([:-][Xx?YyMmDdHhSs\\d]{2}){2}', Literal.Date), ('(P[YyMmWwDd]+(T[HhMmSs]+)?|PT[HhMmSs]+)/?', Literal.Date)], 'ordered_values': [('\\d{4}-\\d{2}-\\d{2}T?', Literal.Date), ('\\d{2}:\\d{2}:\\d{2}(\\.\\d+)?([+-]\\d{4}|Z)?', Literal.Date), ('P((\\d*(\\.\\d+)?[YyMmWwDd]){1,3}(T(\\d*(\\.\\d+)?[HhMmSs]){,3})?|T(\\d*(\\.\\d+)?[HhMmSs]){,3})', Literal.Date), ('[+-]?(\\d+\\.\\d*|\\.\\d+|\\d+)[eE][+-]?\\d+', Number.Float), ('[+-]?\\d*\\.\\d+%?', Number.Float), ('0x[0-9a-fA-F]+', Number.Hex), ('[+-]?\\d+%?', Number.Integer)], 'values': [include('ordered_values'), ('([Tt]rue|[Ff]alse)', Literal), ('"', String, 'string'), ("'(\\\\.|\\\\[0-7]{1,3}|\\\\x[a-fA-F0-9]{1,2}|[^\\\\\\'\\n])'", String.Char), ('[a-z][a-z0-9+.-]*:', Literal, 'uri'), ('(\\[)(\\w[\\w-]*(?:\\([^)\\n]+\\))?)(::)(\\w[\\w-]*)(\\])', bygroups(Punctuation, Name.Decorator, Punctuation, Name.Decorator, Punctuation)), ('\\|', Punctuation, 'interval'), ('\\.\\.\\.', Punctuation)], 'constraint_values': [('(\\[)(\\w[\\w-]*(?:\\([^)\\n]+\\))?)(::)', bygroups(Punctuation, Name.Decorator, Punctuation), 'adl14_code_constraint'), ('(\\d*)(\\|)(\\[\\w[\\w-]*::\\w[\\w-]*\\])((?:[,;])?)', bygroups(Number, Punctuation, Name.Decorator, Punctuation)), include('date_constraints'), include('values')], 'string': [('"', String, '#pop'), ('\\\\([\\\\abfnrtv"\\\']|x[a-fA-F0-9]{2,4}|u[a-fA-F0-9]{4}|U[a-fA-F0-9]{8}|[0-7]{1,3})', String.Escape), ('[^\\\\"]+', String), ('\\\\', String)], 'uri': [('[,>\\s]', Punctuation, '#pop'), ('[^>\\s,]+', Literal)], 'interval': [('\\|', Punctuation, '#pop'), include('ordered_values'), ('\\.\\.', Punctuation), ('[<>=] *', Punctuation), ('\\+/-', Punctuation), ('\\s+', Whitespace)], 'any_code': [include('archetype_id'), ('[a-z_]\\w*[0-9.]+(@[^\\]]+)?', Name.Decorator), ('[a-z_]\\w*', Name.Class), ('[0-9]+', Text), ('\\|', Punctuation, 'code_rubric'), ('\\]', Punctuation, '#pop'), ('(\\s*)(,)(\\s*)', bygroups(Whitespace, Punctuation, Whitespace))], 'code_rubric': [('\\|', Punctuation, '#pop'), ('[^|]+', String)], 'adl14_code_constraint': [('\\]', Punctuation, '#pop'), ('\\|', Punctuation, 'code_rubric'), ('(\\w[\\w-]*)([;,]?)', bygroups(Name.Decorator, Punctuation)), include('whitespace')]}



class OdinLexer(AtomsLexer):
    """
    Lexer for ODIN syntax.
    """
    name = 'ODIN'
    aliases = ['odin']
    filenames = ['*.odin']
    mimetypes = ['text/odin']
    url = 'https://github.com/openEHR/odin'
    version_added = '2.1'
    tokens = {'path': [('>', Punctuation, '#pop'), ('[a-z_]\\w*', Name.Class), ('/', Punctuation), ('\\[', Punctuation, 'key'), ('(\\s*)(,)(\\s*)', bygroups(Whitespace, Punctuation, Whitespace), '#pop'), ('\\s+', Whitespace, '#pop')], 'key': [include('values'), ('\\]', Punctuation, '#pop')], 'type_cast': [('\\)', Punctuation, '#pop'), ('[^)]+', Name.Class)], 'root': [include('whitespace'), ('([Tt]rue|[Ff]alse)', Literal), include('values'), ('/', Punctuation, 'path'), ('\\[', Punctuation, 'key'), ('[a-z_]\\w*', Name.Class), ('=', Operator), ('\\(', Punctuation, 'type_cast'), (',', Punctuation), ('<', Punctuation), ('>', Punctuation), (';', Punctuation)]}



class CadlLexer(AtomsLexer):
    """
    Lexer for cADL syntax.
    """
    name = 'cADL'
    aliases = ['cadl']
    filenames = ['*.cadl']
    url = 'https://specifications.openehr.org/releases/AM/latest/ADL2.html#_cadl_constraint_adl'
    version_added = '2.1'
    tokens = {'path': [('[a-z_]\\w*', Name.Class), ('/', Punctuation), ('\\[', Punctuation, 'any_code'), ('\\s+', Punctuation, '#pop')], 'root': [include('whitespace'), ('(cardinality|existence|occurrences|group|include|exclude|allow_archetype|use_archetype|use_node)\\W', Keyword.Type), ('(and|or|not|there_exists|xor|implies|for_all)\\W', Keyword.Type), ('(after|before|closed)\\W', Keyword.Type), ('(not)\\W', Operator), ('(matches|is_in)\\W', Operator), ('(∈|∉)', Operator), ('(∃|∄|∀|∧|∨|⊻|\x93C)', Operator), ('(\\{)(\\s*)(/[^}]+/)(\\s*)(\\})', bygroups(Punctuation, Whitespace, String.Regex, Whitespace, Punctuation)), ('(\\{)(\\s*)(\\^[^}]+\\^)(\\s*)(\\})', bygroups(Punctuation, Whitespace, String.Regex, Whitespace, Punctuation)), ('/', Punctuation, 'path'), ('(\\{)((?:\\d+\\.\\.)?(?:\\d+|\\*))((?:\\s*;\\s*(?:ordered|unordered|unique)){,2})(\\})', bygroups(Punctuation, Number, Number, Punctuation)), ('\\[\\{', Punctuation), ('\\}\\]', Punctuation), ('\\{', Punctuation), ('\\}', Punctuation), include('constraint_values'), ('[A-Z]\\w+(<[A-Z]\\w+([A-Za-z_<>]*)>)?', Name.Class), ('[a-z_]\\w*', Name.Class), ('\\[', Punctuation, 'any_code'), ('(~|//|\\\\\\\\|\\+|-|/|\\*|\\^|!=|=|<=|>=|<|>]?)', Operator), ('\\(', Punctuation), ('\\)', Punctuation), (',', Punctuation), ('"', String, 'string'), (';', Punctuation)]}



class AdlLexer(AtomsLexer):
    """
    Lexer for ADL syntax.
    """
    name = 'ADL'
    aliases = ['adl']
    filenames = ['*.adl', '*.adls', '*.adlf', '*.adlx']
    url = 'https://specifications.openehr.org/releases/AM/latest/ADL2.html'
    version_added = '2.1'
    tokens = {'whitespace': [('\\s*\\n', Whitespace), ('^([ \\t]*)(--.*)$', bygroups(Whitespace, Comment))], 'odin_section': [('^(language|description|ontology|terminology|annotations|component_terminologies|revision_history)([ \\t]*\\n)', bygroups(Generic.Heading, Whitespace)), ('^(definition)([ \\t]*\\n)', bygroups(Generic.Heading, Whitespace), 'cadl_section'), ('^([ \\t]*|[ \\t]+.*)\\n', using(OdinLexer)), ('^([^"]*")(>[ \\t]*\\n)', bygroups(String, Punctuation)), ('^----------*\\n', Text, '#pop'), ('^.*\\n', String), default('#pop')], 'cadl_section': [('^([ \\t]*|[ \\t]+.*)\\n', using(CadlLexer)), default('#pop')], 'rules_section': [('^[ \\t]+.*\\n', using(CadlLexer)), default('#pop')], 'metadata': [('\\)', Punctuation, '#pop'), (';', Punctuation), ('([Tt]rue|[Ff]alse)', Literal), ('\\d+(\\.\\d+)*', Literal), ('[0-9a-fA-F]{1,36}(-[0-9a-fA-F]{1,36}){3,}', Literal), ('\\w+', Name.Class), ('"', String, 'string'), ('=', Operator), ('[ \\t]+', Whitespace), default('#pop')], 'root': [('^(archetype|template_overlay|operational_template|template|speciali[sz]e)', Generic.Heading), ('^(language|description|ontology|terminology|annotations|component_terminologies|revision_history)[ \\t]*\\n', Generic.Heading, 'odin_section'), ('^(definition)[ \\t]*\\n', Generic.Heading, 'cadl_section'), ('^(rules)[ \\t]*\\n', Generic.Heading, 'rules_section'), include('archetype_id'), ('([ \\t]*)(\\()', bygroups(Whitespace, Punctuation), 'metadata'), include('whitespace')]}


