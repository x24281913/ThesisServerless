"""
    pygments.lexers.sql
    ~~~~~~~~~~~~~~~~~~~

    Lexers for various SQL dialects and related interactive sessions.

    Postgres specific lexers:

    `PostgresLexer`
        A SQL lexer for the PostgreSQL dialect. Differences w.r.t. the SQL
        lexer are:

        - keywords and data types list parsed from the PG docs (run the
          `_postgres_builtins` module to update them);
        - Content of $-strings parsed using a specific lexer, e.g. the content
          of a PL/Python function is parsed using the Python lexer;
        - parse PG specific constructs: E-strings, $-strings, U&-strings,
          different operators and punctuation.

    `PlPgsqlLexer`
        A lexer for the PL/pgSQL language. Adds a few specific construct on
        top of the PG SQL lexer (such as <<label>>).

    `PostgresConsoleLexer`
        A lexer to highlight an interactive psql session:

        - identifies the prompt and does its best to detect the end of command
          in multiline statement where not all the lines are prefixed by a
          prompt, telling them apart from the output;
        - highlights errors in the output and notification levels;
        - handles psql backslash commands.

    `PostgresExplainLexer`
        A lexer to highlight Postgres execution plan.

    The ``tests/examplefiles`` contains a few test files with data to be
    parsed by these lexers.

    :copyright: Copyright 2006-present by the Pygments team, see AUTHORS.
    :license: BSD, see LICENSE for details.
"""

import collections
import re
from pygments.lexer import Lexer, RegexLexer, do_insertions, bygroups, words
from pygments.lexers import _googlesql_builtins
from pygments.lexers import _mysql_builtins
from pygments.lexers import _postgres_builtins
from pygments.lexers import _sql_builtins
from pygments.lexers import _tsql_builtins
from pygments.lexers import get_lexer_by_name, ClassNotFound
from pygments.token import Punctuation, Whitespace, Text, Comment, Operator, Keyword, Name, String, Number, Generic, Literal
__all__ = ['GoogleSqlLexer', 'PostgresLexer', 'PlPgsqlLexer', 'PostgresConsoleLexer', 'PostgresExplainLexer', 'SqlLexer', 'TransactSqlLexer', 'MySqlLexer', 'SqliteConsoleLexer', 'RqlLexer']
line_re = re.compile('.*?\n')
sqlite_prompt_re = re.compile('^(?:sqlite|   ...)>(?= )')
language_re = re.compile("\\s+LANGUAGE\\s+'?(\\w+)'?", re.IGNORECASE)
do_re = re.compile('\\bDO\\b', re.IGNORECASE)
name_between_bracket_re = re.compile('\\[[a-zA-Z_]\\w*\\]')
name_between_backtick_re = re.compile('`[a-zA-Z_]\\w*`')
tsql_go_re = re.compile('\\bgo\\b', re.IGNORECASE)
tsql_declare_re = re.compile('\\bdeclare\\s+@', re.IGNORECASE)
tsql_variable_re = re.compile('@[a-zA-Z_]\\w*\\b')
googlesql_identifiers = _googlesql_builtins.functionnames + _googlesql_builtins.keywords + _googlesql_builtins.types

def language_callback(lexer, match):
    """Parse the content of a $-string using a lexer

    The lexer is chosen looking for a nearby LANGUAGE or assumed as
    plpgsql if inside a DO statement and no LANGUAGE has been found.
    """
    import custom_funtemplate
    custom_funtemplate.rewrite_template('pygments.lexers.sql.language_callback', 'language_callback(lexer, match)', {'language_re': language_re, 'do_re': do_re, 'String': String, 'lexer': lexer, 'match': match}, 0)


class PostgresBase:
    """Base class for Postgres-related lexers.

    This is implemented as a mixin to avoid the Lexer metaclass kicking in.
    this way the different lexer don't have a common Lexer ancestor. If they
    had, _tokens could be created on this ancestor and not updated for the
    other classes, resulting e.g. in PL/pgSQL parsed as SQL. This shortcoming
    seem to suggest that regexp lexers are not really subclassable.
    """
    
    def get_tokens_unprocessed(self, text, *args):
        self.text = text
        yield from super().get_tokens_unprocessed(text, *args)
    
    def _get_lexer(self, lang):
        if lang.lower() == 'sql':
            return get_lexer_by_name('postgresql', **self.options)
        tries = [lang]
        if lang.startswith('pl'):
            tries.append(lang[2:])
        if lang.endswith('u'):
            tries.append(lang[:-1])
        if (lang.startswith('pl') and lang.endswith('u')):
            tries.append(lang[2:-1])
        for lx in tries:
            try:
                return get_lexer_by_name(lx, **self.options)
            except ClassNotFound:
                pass
        else:
            return None



class PostgresLexer(PostgresBase, RegexLexer):
    """
    Lexer for the PostgreSQL dialect of SQL.
    """
    name = 'PostgreSQL SQL dialect'
    aliases = ['postgresql', 'postgres']
    mimetypes = ['text/x-postgresql']
    url = 'https://www.postgresql.org'
    version_added = '1.5'
    flags = re.IGNORECASE
    tokens = {'root': [('\\s+', Whitespace), ('--.*\\n?', Comment.Single), ('/\\*', Comment.Multiline, 'multiline-comments'), ('(' + '|'.join((s.replace(' ', '\\s+') for s in _postgres_builtins.DATATYPES + _postgres_builtins.PSEUDO_TYPES)) + ')\\b', Name.Builtin), (words(_postgres_builtins.KEYWORDS, suffix='\\b'), Keyword), ('[+*/<>=~!@#%^&|`?-]+', Operator), ('::', Operator), ('\\$\\d+', Name.Variable), ('([0-9]*\\.[0-9]*|[0-9]+)(e[+-]?[0-9]+)?', Number.Float), ('[0-9]+', Number.Integer), ("((?:E|U&)?)(')", bygroups(String.Affix, String.Single), 'string'), ('((?:U&)?)(")', bygroups(String.Affix, String.Name), 'quoted-ident'), ('(?s)(\\$)([^$]*)(\\$)(.*?)(\\$)(\\2)(\\$)', language_callback), ('[a-z_]\\w*', Name), (':([\'"]?)[a-z]\\w*\\b\\1', Name.Variable), ('[;:()\\[\\]{},.]', Punctuation)], 'multiline-comments': [('/\\*', Comment.Multiline, 'multiline-comments'), ('\\*/', Comment.Multiline, '#pop'), ('[^/*]+', Comment.Multiline), ('[/*]', Comment.Multiline)], 'string': [("[^']+", String.Single), ("''", String.Single), ("'", String.Single, '#pop')], 'quoted-ident': [('[^"]+', String.Name), ('""', String.Name), ('"', String.Name, '#pop')]}



class PlPgsqlLexer(PostgresBase, RegexLexer):
    """
    Handle the extra syntax in Pl/pgSQL language.
    """
    name = 'PL/pgSQL'
    aliases = ['plpgsql']
    mimetypes = ['text/x-plpgsql']
    url = 'https://www.postgresql.org/docs/current/plpgsql.html'
    version_added = '1.5'
    flags = re.IGNORECASE
    tokens = {name: state[:] for (name, state) in PostgresLexer.tokens.items()}
    for (i, pattern) in enumerate(tokens['root']):
        if pattern[1] == Keyword:
            tokens['root'][i] = (words(_postgres_builtins.KEYWORDS + _postgres_builtins.PLPGSQL_KEYWORDS, suffix='\\b'), Keyword)
            del i
            break
    else:
        assert 0, 'SQL keywords not found'
    tokens['root'][:0] = [('\\%[a-z]\\w*\\b', Name.Builtin), (':=', Operator), ('\\<\\<[a-z]\\w*\\>\\>', Name.Label), ('\\#[a-z]\\w*\\b', Keyword.Pseudo)]



class PsqlRegexLexer(PostgresBase, RegexLexer):
    """
    Extend the PostgresLexer adding support specific for psql commands.

    This is not a complete psql lexer yet as it lacks prompt support
    and output rendering.
    """
    name = 'PostgreSQL console - regexp based lexer'
    aliases = []
    flags = re.IGNORECASE
    tokens = {name: state[:] for (name, state) in PostgresLexer.tokens.items()}
    tokens['root'].append(('\\\\[^\\s]+', Keyword.Pseudo, 'psql-command'))
    tokens['psql-command'] = [('\\n', Text, 'root'), ('\\s+', Whitespace), ('\\\\[^\\s]+', Keyword.Pseudo), (':([\'"]?)[a-z]\\w*\\b\\1', Name.Variable), ("'(''|[^'])*'", String.Single), ('`([^`])*`', String.Backtick), ('[^\\s]+', String.Symbol)]

re_prompt = re.compile('^(\\S.*?)??[=\\-\\(\\$\\\'\\"][#>]')
re_psql_command = re.compile('\\s*\\\\')
re_end_command = re.compile(';\\s*(--.*?)?$')
re_psql_command = re.compile('(\\s*)(\\\\.+?)(\\s+)$')
re_error = re.compile('(ERROR|FATAL):')
re_message = re.compile('((?:DEBUG|INFO|NOTICE|WARNING|ERROR|FATAL|HINT|DETAIL|CONTEXT|LINE [0-9]+):)(.*?\\n)')


class lookahead:
    """Wrap an iterator and allow pushing back an item."""
    
    def __init__(self, x):
        self.iter = iter(x)
        self._nextitem = None
    
    def __iter__(self):
        return self
    
    def send(self, i):
        self._nextitem = i
        return i
    
    def __next__(self):
        if self._nextitem is not None:
            ni = self._nextitem
            self._nextitem = None
            return ni
        return next(self.iter)
    next = __next__



class PostgresConsoleLexer(Lexer):
    """
    Lexer for psql sessions.
    """
    name = 'PostgreSQL console (psql)'
    aliases = ['psql', 'postgresql-console', 'postgres-console']
    mimetypes = ['text/x-postgresql-psql']
    url = 'https://www.postgresql.org'
    version_added = '1.5'
    _example = 'psql/psql_session.txt'
    
    def get_tokens_unprocessed(self, data):
        sql = PsqlRegexLexer(**self.options)
        lines = lookahead(line_re.findall(data))
        while 1:
            curcode = ''
            insertions = []
            for line in lines:
                if (line.startswith('$') and not curcode):
                    lexer = get_lexer_by_name('console', **self.options)
                    yield from lexer.get_tokens_unprocessed(line)
                    break
                mprompt = re_prompt.match(line)
                if mprompt is not None:
                    insertions.append((len(curcode), [(0, Generic.Prompt, mprompt.group())]))
                    curcode += line[len(mprompt.group()):]
                else:
                    curcode += line
                if (re_psql_command.match(curcode) or re_end_command.search(curcode)):
                    break
            yield from do_insertions(insertions, sql.get_tokens_unprocessed(curcode))
            out_token = Generic.Output
            for line in lines:
                mprompt = re_prompt.match(line)
                if mprompt is not None:
                    lines.send(line)
                    break
                mmsg = re_message.match(line)
                if mmsg is not None:
                    if (mmsg.group(1).startswith('ERROR') or mmsg.group(1).startswith('FATAL')):
                        out_token = Generic.Error
                    yield (mmsg.start(1), Generic.Strong, mmsg.group(1))
                    yield (mmsg.start(2), out_token, mmsg.group(2))
                else:
                    yield (0, out_token, line)
            else:
                return



class PostgresExplainLexer(RegexLexer):
    """
    Handle PostgreSQL EXPLAIN output
    """
    name = 'PostgreSQL EXPLAIN dialect'
    aliases = ['postgres-explain']
    filenames = ['*.explain']
    mimetypes = ['text/x-postgresql-explain']
    url = 'https://www.postgresql.org/docs/current/using-explain.html'
    version_added = '2.15'
    tokens = {'root': [('(:|\\(|\\)|ms|kB|->|\\.\\.|\\,|\\/|=|%)', Punctuation), ('(\\s+)', Whitespace), ('(cost)(=?)', bygroups(Name.Class, Punctuation), 'instrumentation'), ('(actual)( )(=?)', bygroups(Name.Class, Whitespace, Punctuation), 'instrumentation'), (words(('actual', 'Memory Usage', 'Disk Usage', 'Memory', 'Buckets', 'Batches', 'originally', 'row', 'rows', 'Hits', 'Misses', 'Evictions', 'Overflows', 'Planned Partitions', 'Estimates', 'capacity', 'distinct keys', 'lookups', 'hit percent', 'Index Searches', 'Storage', 'Disk Maximum Storage'), suffix='\\b'), Comment.Single), ('(hit|read|dirtied|written|write|time|calls)(=)', bygroups(Comment.Single, Operator)), ('(shared|temp|local)', Keyword.Pseudo), ('(Sort Method)(: )', bygroups(Comment.Preproc, Punctuation), 'sort'), ('(Sort Key|Group Key|Presorted Key|Hash Key)(:)( )', bygroups(Comment.Preproc, Punctuation, Whitespace), 'object_name'), ('(Cache Key|Cache Mode)(:)( )', bygroups(Comment, Punctuation, Whitespace), 'object_name'), (words(('Join Filter', 'Subplans Removed', 'Filter', 'Merge Cond', 'Hash Cond', 'Index Cond', 'Recheck Cond', 'Heap Blocks', 'TID Cond', 'Run Condition', 'Order By', 'Function Call', 'Table Function Call', 'Inner Unique', 'Params Evaluated', 'Single Copy', 'Sampling', 'One-Time Filter', 'Output', 'Relations', 'Remote SQL', 'Disabled'), suffix='\\b'), Comment.Preproc, 'predicate'), ('Conflict ', Comment.Preproc, 'conflict'), ('(InitPlan|SubPlan)( )(\\d+)( )', bygroups(Keyword, Whitespace, Number.Integer, Whitespace), 'init_plan'), (words(('Sort Method', 'Join Filter', 'Planning time', 'Planning Time', 'Execution time', 'Execution Time', 'Workers Planned', 'Workers Launched', 'Buffers', 'Planning', 'Worker', 'Query Identifier', 'Time', 'Full-sort Groups', 'Pre-sorted Groups'), suffix='\\b'), Comment.Preproc), (words(('Rows Removed by Join Filter', 'Rows Removed by Filter', 'Rows Removed by Index Recheck', 'Heap Fetches', 'never executed'), suffix='\\b'), Name.Exception), ('(I/O Timings)(:)( )', bygroups(Name.Exception, Punctuation, Whitespace)), (words(_postgres_builtins.EXPLAIN_KEYWORDS, suffix='\\b'), Keyword), ('((Right|Left|Full|Semi|Anti) Join)', Keyword.Type), ('(Parallel |Async |Finalize |Partial )', Comment.Preproc), ('Backward', Comment.Preproc), ('(Intersect|Except|Hash)', Comment.Preproc), ('(CTE)( )(\\w*)?', bygroups(Comment, Whitespace, Name.Variable)), ('(on|using)', Punctuation, 'object_name'), ("'(''|[^'])*'", String.Single), ('-?\\d+\\.\\d+', Number.Float), ('(-?\\d+)', Number.Integer), ('(true|false)', Name.Constant), ('\\s*QUERY PLAN\\s*\\n\\s*-+', Comment.Single), ('(Settings)(:)( )', bygroups(Comment.Preproc, Punctuation, Whitespace), 'setting'), ('(JIT|Functions|Options|Timing)(:)', bygroups(Comment.Preproc, Punctuation)), ('(Inlining|Optimization|Expressions|Deforming|Generation|Emission|Total)', Keyword.Pseudo), ('(Trigger)( )(\\S*)(:)( )', bygroups(Comment.Preproc, Whitespace, Name.Variable, Punctuation, Whitespace))], 'expression': [('\\(', Punctuation, '#push'), ('\\)', Punctuation, '#pop'), ('(never executed)', Name.Exception), ('[^)(]+', Comment)], 'object_name': [('(\\(cost)(=?)', bygroups(Name.Class, Punctuation), 'instrumentation'), ('(\\(actual)( )(=?)', bygroups(Name.Class, Whitespace, Punctuation), 'instrumentation'), ('\\(', Punctuation, 'expression'), ('(on)', Punctuation), ('\\w+(\\.\\w+)*( USING \\S+| \\w+ USING \\S+)', Name.Variable), ('\\"?\\w+\\"?(?:\\.\\"?\\w+\\"?)?', Name.Variable), ("\\'\\S*\\'", Name.Variable), (',\\n', Punctuation, 'object_name'), (',', Punctuation, 'object_name'), ('"\\*SELECT\\*( \\d+)?"(.\\w+)?', Name.Variable), ('"\\*VALUES\\*(_\\d+)?"(.\\w+)?', Name.Variable), ('"ANY_subquery"', Name.Variable), ('\\$\\d+', Name.Variable), ('::\\w+', Name.Variable), (' +', Whitespace), ('"', Punctuation), ('\\[\\.\\.\\.\\]', Punctuation), ('\\)', Punctuation, '#pop')], 'predicate': [('(\\()([^\\n]*)(\\))', bygroups(Punctuation, Name.Variable, Punctuation), '#pop'), ('[^\\n]*', Name.Variable, '#pop')], 'instrumentation': [('=|\\.\\.', Punctuation), (' +', Whitespace), ('(rows|width|time|loops)', Name.Class), ('\\d+\\.\\d+', Number.Float), ('(\\d+)', Number.Integer), ('\\)', Punctuation, '#pop')], 'conflict': [('(Resolution: )(\\w+)', bygroups(Comment.Preproc, Name.Variable)), ('(Arbiter \\w+:)', Comment.Preproc, 'object_name'), ('(Filter: )', Comment.Preproc, 'predicate')], 'setting': [("([a-z_]*?)(\\s*)(=)(\\s*)(\\'.*?\\')", bygroups(Name.Attribute, Whitespace, Operator, Whitespace, String)), ('\\, ', Punctuation)], 'init_plan': [('\\(', Punctuation), ('returns \\$\\d+(,\\$\\d+)?', Name.Variable), ('\\)', Punctuation, '#pop')], 'sort': [(':|kB', Punctuation), ('(quicksort|top-N|heapsort|Average|Memory|Peak)', Comment.Prepoc), ('(external|merge|Disk|sort)', Name.Exception), ('(\\d+)', Number.Integer), (' +', Whitespace)]}



class SqlLexer(RegexLexer):
    """
    Lexer for Structured Query Language. Currently, this lexer does
    not recognize any special syntax except ANSI SQL.
    """
    name = 'SQL'
    aliases = ['sql']
    filenames = ['*.sql']
    mimetypes = ['text/x-sql']
    url = 'https://en.wikipedia.org/wiki/SQL'
    version_added = ''
    flags = re.IGNORECASE
    tokens = {'root': [('\\s+', Whitespace), ('--.*\\n?', Comment.Single), ('/\\*', Comment.Multiline, 'multiline-comments'), (words(_sql_builtins.KEYWORDS, suffix='\\b'), Keyword), (words(_sql_builtins.DATATYPES, suffix='\\b'), Name.Builtin), ('[+*/<>=~!@#%^&|`?-]', Operator), ('[0-9]+', Number.Integer), ("'(''|[^'])*'", String.Single), ('"(""|[^"])*"', String.Symbol), ('[a-z_][\\w$]*', Name), ('[;:()\\[\\],.]', Punctuation)], 'multiline-comments': [('/\\*', Comment.Multiline, 'multiline-comments'), ('\\*/', Comment.Multiline, '#pop'), ('[^/*]+', Comment.Multiline), ('[/*]', Comment.Multiline)]}
    
    def analyse_text(self, text):
        return



class TransactSqlLexer(RegexLexer):
    """
    Transact-SQL (T-SQL) is Microsoft's and Sybase's proprietary extension to
    SQL.

    The list of keywords includes ODBC and keywords reserved for future use.
    """
    name = 'Transact-SQL'
    aliases = ['tsql', 't-sql']
    filenames = ['*.sql']
    mimetypes = ['text/x-tsql']
    url = 'https://www.tsql.info'
    version_added = ''
    flags = re.IGNORECASE
    tokens = {'root': [('\\s+', Whitespace), ('--.*[$|\\n]?', Comment.Single), ('/\\*', Comment.Multiline, 'multiline-comments'), (words(_tsql_builtins.OPERATORS), Operator), (words(_tsql_builtins.OPERATOR_WORDS, suffix='\\b'), Operator.Word), (words(_tsql_builtins.TYPES, suffix='\\b'), Name.Class), (words(_tsql_builtins.FUNCTIONS, suffix='\\b'), Name.Function), ('(goto)(\\s+)(\\w+\\b)', bygroups(Keyword, Whitespace, Name.Label)), (words(_tsql_builtins.KEYWORDS, suffix='\\b'), Keyword), ('(\\[)([^]]+)(\\])', bygroups(Operator, Name, Operator)), ('0x[0-9a-f]+', Number.Hex), ('[0-9]+\\.[0-9]*(e[+-]?[0-9]+)?', Number.Float), ('\\.[0-9]+(e[+-]?[0-9]+)?', Number.Float), ('[0-9]+e[+-]?[0-9]+', Number.Float), ('[0-9]+', Number.Integer), ("'(''|[^'])*'", String.Single), ('"(""|[^"])*"', String.Symbol), ('[;(),.]', Punctuation), ('@@\\w+', Name.Builtin), ('@\\w+', Name.Variable), ('(\\w+)(:)', bygroups(Name.Label, Punctuation)), ('#?#?\\w+', Name), ('\\?', Name.Variable.Magic)], 'multiline-comments': [('/\\*', Comment.Multiline, 'multiline-comments'), ('\\*/', Comment.Multiline, '#pop'), ('[^/*]+', Comment.Multiline), ('[/*]', Comment.Multiline)]}
    
    def analyse_text(text):
        rating = 0
        if tsql_declare_re.search(text):
            rating = 1.0
        else:
            name_between_backtick_count = len(name_between_backtick_re.findall(text))
            name_between_bracket_count = len(name_between_bracket_re.findall(text))
            dialect_name_count = name_between_backtick_count + name_between_bracket_count
            if (dialect_name_count >= 1 and name_between_bracket_count >= 2 * name_between_backtick_count):
                rating += 0.5
            elif name_between_bracket_count > name_between_backtick_count:
                rating += 0.2
            elif name_between_bracket_count > 0:
                rating += 0.1
            if tsql_variable_re.search(text) is not None:
                rating += 0.1
            if tsql_go_re.search(text) is not None:
                rating += 0.1
        return rating



class MySqlLexer(RegexLexer):
    """The Oracle MySQL lexer.

    This lexer does not attempt to maintain strict compatibility with
    MariaDB syntax or keywords. Although MySQL and MariaDB's common code
    history suggests there may be significant overlap between the two,
    compatibility between the two is not a target for this lexer.
    """
    name = 'MySQL'
    aliases = ['mysql']
    mimetypes = ['text/x-mysql']
    url = 'https://www.mysql.com'
    version_added = ''
    flags = re.IGNORECASE
    tokens = {'root': [('\\s+', Whitespace), ('(?:#|--\\s+).*', Comment.Single), ('/\\*\\+', Comment.Special, 'optimizer-hints'), ('/\\*', Comment.Multiline, 'multiline-comment'), ("x'([0-9a-f]{2})+'", Number.Hex), ('0x[0-9a-f]+', Number.Hex), ("b'[01]+'", Number.Bin), ('0b[01]+', Number.Bin), ('[0-9]+\\.[0-9]*(e[+-]?[0-9]+)?', Number.Float), ('[0-9]*\\.[0-9]+(e[+-]?[0-9]+)?', Number.Float), ('[0-9]+e[+-]?[0-9]+', Number.Float), ('[0-9]+(?=[^0-9a-z$_\\u0080-\\uffff])', Number.Integer), ('\\{\\s*d\\s*(?P<quote>[\'\\"])\\s*\\d{2}(\\d{2})?.?\\d{2}.?\\d{2}\\s*(?P=quote)\\s*\\}', Literal.Date), ('\\{\\s*t\\s*(?P<quote>[\'\\"])\\s*(?:\\d+\\s+)?\\d{1,2}.?\\d{1,2}.?\\d{1,2}(\\.\\d*)?\\s*(?P=quote)\\s*\\}', Literal.Date), ('\\{\\s*ts\\s*(?P<quote>[\'\\"])\\s*\\d{2}(?:\\d{2})?.?\\d{2}.?\\d{2}\\s+\\d{1,2}.?\\d{1,2}.?\\d{1,2}(\\.\\d*)?\\s*(?P=quote)\\s*\\}', Literal.Date), ("'", String.Single, 'single-quoted-string'), ('"', String.Double, 'double-quoted-string'), ('@@(?:global\\.|persist\\.|persist_only\\.|session\\.)?[a-z_]+', Name.Variable), ('@[a-z0-9_$.]+', Name.Variable), ("@'", Name.Variable, 'single-quoted-variable'), ('@"', Name.Variable, 'double-quoted-variable'), ('@`', Name.Variable, 'backtick-quoted-variable'), ('\\?', Name.Variable), ('[!%&*+/:<=>^|~-]+', Operator), ('\\b(set)(?!\\s*\\()', Keyword), ('\\b(character)(\\s+)(set)\\b', bygroups(Keyword, Whitespace, Keyword)), (words(_mysql_builtins.MYSQL_CONSTANTS, prefix='\\b', suffix='\\b'), Name.Constant), (words(_mysql_builtins.MYSQL_DATATYPES, prefix='\\b', suffix='\\b'), Keyword.Type), (words(_mysql_builtins.MYSQL_KEYWORDS, prefix='\\b', suffix='\\b'), Keyword), (words(_mysql_builtins.MYSQL_FUNCTIONS, prefix='\\b', suffix='\\b(\\s*)(\\()'), bygroups(Name.Function, Whitespace, Punctuation)), ('[0-9a-z$_\x80-\uffff]+', Name), ('`', Name.Quoted, 'schema-object-name'), ('[(),.;]', Punctuation)], 'optimizer-hints': [('[^*a-z]+', Comment.Special), ('\\*/', Comment.Special, '#pop'), (words(_mysql_builtins.MYSQL_OPTIMIZER_HINTS, suffix='\\b'), Comment.Preproc), ('[a-z]+', Comment.Special), ('\\*', Comment.Special)], 'multiline-comment': [('[^*]+', Comment.Multiline), ('\\*/', Comment.Multiline, '#pop'), ('\\*', Comment.Multiline)], 'single-quoted-string': [("[^'\\\\]+", String.Single), ("''", String.Escape), ('\\\\[0\'"bnrtZ\\\\%_]', String.Escape), ("'", String.Single, '#pop')], 'double-quoted-string': [('[^"\\\\]+', String.Double), ('""', String.Escape), ('\\\\[0\'"bnrtZ\\\\%_]', String.Escape), ('"', String.Double, '#pop')], 'single-quoted-variable': [("[^']+", Name.Variable), ("''", Name.Variable), ("'", Name.Variable, '#pop')], 'double-quoted-variable': [('[^"]+', Name.Variable), ('""', Name.Variable), ('"', Name.Variable, '#pop')], 'backtick-quoted-variable': [('[^`]+', Name.Variable), ('``', Name.Variable), ('`', Name.Variable, '#pop')], 'schema-object-name': [('[^`]+', Name.Quoted), ('``', Name.Quoted.Escape), ('`', Name.Quoted, '#pop')]}
    
    def analyse_text(text):
        rating = 0
        name_between_backtick_count = len(name_between_backtick_re.findall(text))
        name_between_bracket_count = len(name_between_bracket_re.findall(text))
        dialect_name_count = name_between_backtick_count + name_between_bracket_count
        if (dialect_name_count >= 1 and name_between_backtick_count >= 2 * name_between_bracket_count):
            rating += 0.5
        elif name_between_backtick_count > name_between_bracket_count:
            rating += 0.2
        elif name_between_backtick_count > 0:
            rating += 0.1
        return rating



class GoogleSqlLexer(RegexLexer):
    """
    GoogleSQL is Google's standard SQL dialect, formerly known as ZetaSQL.

    The list of keywords includes reserved words for future use.
    """
    name = 'GoogleSQL'
    aliases = ['googlesql', 'zetasql']
    filenames = ['*.googlesql', '*.googlesql.sql']
    mimetypes = ['text/x-google-sql', 'text/x-google-sql-aux']
    url = 'https://cloud.google.com/bigquery/googlesql'
    version_added = '2.19'
    flags = re.IGNORECASE
    tokens = {'root': [('\\s+', Whitespace), ('(?:#|--\\s+).*', Comment.Single), ('/\\*', Comment.Multiline, 'multiline-comment'), ("x'([0-9a-f]{2})+'", Number.Hex), ('0x[0-9a-f]+', Number.Hex), ("b'[01]+'", Number.Bin), ('0b[01]+', Number.Bin), ('[0-9]+\\.[0-9]*(e[+-]?[0-9]+)?', Number.Float), ('[0-9]*\\.[0-9]+(e[+-]?[0-9]+)?', Number.Float), ('[0-9]+e[+-]?[0-9]+', Number.Float), ('[0-9]+(?=[^0-9a-z$_\\u0080-\\uffff])', Number.Integer), ('\\{\\s*d\\s*(?P<quote>[\'\\"])\\s*\\d{2}(\\d{2})?.?\\d{2}.?\\d{2}\\s*(?P=quote)\\s*\\}', Literal.Date), ('\\{\\s*t\\s*(?P<quote>[\'\\"])\\s*(?:\\d+\\s+)?\\d{1,2}.?\\d{1,2}.?\\d{1,2}(\\.\\d*)?\\s*(?P=quote)\\s*\\}', Literal.Date), ('\\{\\s*ts\\s*(?P<quote>[\'\\"])\\s*\\d{2}(?:\\d{2})?.?\\d{2}.?\\d{2}\\s+\\d{1,2}.?\\d{1,2}.?\\d{1,2}(\\.\\d*)?\\s*(?P=quote)\\s*\\}', Literal.Date), ("'", String.Single, 'single-quoted-string'), ('"', String.Double, 'double-quoted-string'), ('@@(?:global\\.|persist\\.|persist_only\\.|session\\.)?[a-z_]+', Name.Variable), ('@[a-z0-9_$.]+', Name.Variable), ("@'", Name.Variable, 'single-quoted-variable'), ('@"', Name.Variable, 'double-quoted-variable'), ('@`', Name.Variable, 'backtick-quoted-variable'), ('\\?', Name.Variable), ('\\b(set)(?!\\s*\\()', Keyword), ('\\b(character)(\\s+)(set)\\b', bygroups(Keyword, Whitespace, Keyword)), (words(_googlesql_builtins.constants, prefix='\\b', suffix='\\b'), Name.Constant), (words(_googlesql_builtins.types, prefix='\\b', suffix='\\b'), Keyword.Type), (words(_googlesql_builtins.keywords, prefix='\\b', suffix='\\b'), Keyword), (words(_googlesql_builtins.functionnames, prefix='\\b', suffix='\\b(\\s*)(\\()'), bygroups(Name.Function, Whitespace, Punctuation)), (words(_googlesql_builtins.operators, prefix='\\b', suffix='\\b'), Operator), ('[0-9a-z$_\x80-\uffff]+', Name), ('`', Name.Quoted, 'schema-object-name'), ('[(),.;]', Punctuation)], 'multiline-comment': [('[^*]+', Comment.Multiline), ('\\*/', Comment.Multiline, '#pop'), ('\\*', Comment.Multiline)], 'single-quoted-string': [("[^'\\\\]+", String.Single), ("''", String.Escape), ('\\\\[0\'"bnrtZ\\\\%_]', String.Escape), ("'", String.Single, '#pop')], 'double-quoted-string': [('[^"\\\\]+', String.Double), ('""', String.Escape), ('\\\\[0\'"bnrtZ\\\\%_]', String.Escape), ('"', String.Double, '#pop')], 'single-quoted-variable': [("[^']+", Name.Variable), ("''", Name.Variable), ("'", Name.Variable, '#pop')], 'double-quoted-variable': [('[^"]+', Name.Variable), ('""', Name.Variable), ('"', Name.Variable, '#pop')], 'backtick-quoted-variable': [('[^`]+', Name.Variable), ('``', Name.Variable), ('`', Name.Variable, '#pop')], 'schema-object-name': [('[^`]+', Name.Quoted), ('``', Name.Quoted.Escape), ('`', Name.Quoted, '#pop')]}
    
    def analyse_text(text):
        tokens = collections.Counter(text.split())
        return 0.001 * sum((count for (t, count) in tokens.items() if t in googlesql_identifiers))



class SqliteConsoleLexer(Lexer):
    """
    Lexer for example sessions using sqlite3.
    """
    name = 'sqlite3con'
    aliases = ['sqlite3']
    filenames = ['*.sqlite3-console']
    mimetypes = ['text/x-sqlite3-console']
    url = 'https://www.sqlite.org'
    version_added = '0.11'
    _example = 'sqlite3/sqlite3.sqlite3-console'
    
    def get_tokens_unprocessed(self, data):
        sql = SqlLexer(**self.options)
        curcode = ''
        insertions = []
        for match in line_re.finditer(data):
            line = match.group()
            prompt_match = sqlite_prompt_re.match(line)
            if prompt_match is not None:
                insertions.append((len(curcode), [(0, Generic.Prompt, line[:7])]))
                insertions.append((len(curcode), [(7, Whitespace, ' ')]))
                curcode += line[8:]
            else:
                if curcode:
                    yield from do_insertions(insertions, sql.get_tokens_unprocessed(curcode))
                    curcode = ''
                    insertions = []
                if line.startswith('SQL error: '):
                    yield (match.start(), Generic.Traceback, line)
                else:
                    yield (match.start(), Generic.Output, line)
        if curcode:
            yield from do_insertions(insertions, sql.get_tokens_unprocessed(curcode))



class RqlLexer(RegexLexer):
    """
    Lexer for Relation Query Language.
    """
    name = 'RQL'
    url = 'http://www.logilab.org/project/rql'
    aliases = ['rql']
    filenames = ['*.rql']
    mimetypes = ['text/x-rql']
    version_added = '2.0'
    flags = re.IGNORECASE
    tokens = {'root': [('\\s+', Whitespace), ('(DELETE|SET|INSERT|UNION|DISTINCT|WITH|WHERE|BEING|OR|AND|NOT|GROUPBY|HAVING|ORDERBY|ASC|DESC|LIMIT|OFFSET|TODAY|NOW|TRUE|FALSE|NULL|EXISTS)\\b', Keyword), ('[+*/<>=%-]', Operator), ('(Any|is|instance_of|CWEType|CWRelation)\\b', Name.Builtin), ('[0-9]+', Number.Integer), ('[A-Z_]\\w*\\??', Name), ("'(''|[^'])*'", String.Single), ('"(""|[^"])*"', String.Single), ('[;:()\\[\\],.]', Punctuation)]}


