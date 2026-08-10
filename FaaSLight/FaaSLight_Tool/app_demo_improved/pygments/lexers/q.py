"""
    pygments.lexers.q
    ~~~~~~~~~~~~~~~~~

    Lexer for the Q programming language.

    :copyright: Copyright 2006-present by the Pygments team, see AUTHORS.
    :license: BSD, see LICENSE for details.
"""

from pygments.lexer import RegexLexer, words, include, bygroups, inherit
from pygments.token import Comment, Name, Number, Operator, Punctuation, String, Whitespace, Literal, Generic
__all__ = ['KLexer', 'QLexer']


class KLexer(RegexLexer):
    """
    For K source code.
    """
    name = 'K'
    aliases = ['k']
    filenames = ['*.k']
    url = 'https://code.kx.com'
    version_added = '2.12'
    tokens = {'whitespace': [('^#!.*', Comment.Hashbang), ('^/\\s*\\n', Comment.Multiline, 'comments'), ('(?<!\\S)/.*', Comment.Single), ('\\s+', Whitespace), ('\\"', String.Double, 'strings')], 'root': [include('whitespace'), include('keywords'), include('declarations')], 'keywords': [(words(('abs', 'acos', 'asin', 'atan', 'avg', 'bin', 'binr', 'by', 'cor', 'cos', 'cov', 'dev', 'delete', 'div', 'do', 'enlist', 'exec', 'exit', 'exp', 'from', 'getenv', 'hopen', 'if', 'in', 'insert', 'last', 'like', 'log', 'max', 'min', 'prd', 'select', 'setenv', 'sin', 'sqrt', 'ss', 'sum', 'tan', 'update', 'var', 'wavg', 'while', 'within', 'wsum', 'xexp'), suffix='\\b'), Operator.Word)], 'declarations': [('^\\\\ts?', Comment.Preproc), ('^(\\\\\\w\\s+[^/\\n]*?)(/.*)', bygroups(Comment.Preproc, Comment.Single)), ('^\\\\\\w.*', Comment.Preproc), ('^[a-zA-Z]\\)', Generic.Prompt), ("([.]?[a-zA-Z][\\w.]*)(\\s*)([-.~=!@#$%^&*_+|,<>?/\\\\:']?:)(\\s*)(\\{)", bygroups(Name.Function, Whitespace, Operator, Whitespace, Punctuation), 'functions'), ("([.]?[a-zA-Z][\\w.]*)(\\s*)([-.~=!@#$%^&*_+|,<>?/\\\\:']?:)", bygroups(Name.Variable, Whitespace, Operator)), ('\\{', Punctuation, 'functions'), ('\\(', Punctuation, 'parentheses'), ('\\[', Punctuation, 'brackets'), ("'`([a-zA-Z][\\w.]*)?", Name.Exception), ('`:([a-zA-Z/][\\w./]*)?', String.Symbol), ('`([a-zA-Z][\\w.]*)?', String.Symbol), include('numbers'), ('[a-zA-Z][\\w.]*', Name), ("[-=+*#$%@!~^&:.,<>'\\\\|/?_]", Operator), (';', Punctuation)], 'functions': [include('root'), ('\\}', Punctuation, '#pop')], 'parentheses': [include('root'), ('\\)', Punctuation, '#pop')], 'brackets': [include('root'), ('\\]', Punctuation, '#pop')], 'numbers': [('[01]+b', Number.Bin), ('0[nNwW][cefghijmndzuvtp]?', Number), ('(?:[0-9]{4}[.][0-9]{2}[.][0-9]{2}|[0-9]+)D(?:[0-9](?:[0-9](?::[0-9]{2}(?::[0-9]{2}(?:[.][0-9]*)?)?)?)?)?', Literal.Date), ('[0-9]{4}[.][0-9]{2}(?:m|[.][0-9]{2}(?:T(?:[0-9]{2}:[0-9]{2}(?::[0-9]{2}(?:[.][0-9]*)?)?)?)?)', Literal.Date), ('[0-9]{2}:[0-9]{2}(?::[0-9]{2}(?:[.][0-9]{1,3})?)?', Literal.Date), ('[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}', Number.Hex), ('0x[0-9a-fA-F]+', Number.Hex), ('([0-9]*[.]?[0-9]+|[0-9]+[.]?[0-9]*)[eE][+-]?[0-9]+[ef]?', Number.Float), ('([0-9]*[.][0-9]+|[0-9]+[.][0-9]*)[ef]?', Number.Float), ('[0-9]+[ef]', Number.Float), ('[0-9]+c', Number), ('[0-9]+[ihtuv]', Number.Integer), ('[0-9]+[jnp]?', Number.Integer.Long)], 'comments': [('[^\\\\]+', Comment.Multiline), ('^\\\\', Comment.Multiline, '#pop'), ('\\\\', Comment.Multiline)], 'strings': [('[^"\\\\]+', String.Double), ('\\\\.', String.Escape), ('"', String.Double, '#pop')]}



class QLexer(KLexer):
    """
    For `Q <https://code.kx.com/>`_ source code.
    """
    name = 'Q'
    aliases = ['q']
    filenames = ['*.q']
    version_added = '2.12'
    tokens = {'root': [(words(('aj', 'aj0', 'ajf', 'ajf0', 'all', 'and', 'any', 'asc', 'asof', 'attr', 'avgs', 'ceiling', 'cols', 'count', 'cross', 'csv', 'cut', 'deltas', 'desc', 'differ', 'distinct', 'dsave', 'each', 'ej', 'ema', 'eval', 'except', 'fby', 'fills', 'first', 'fkeys', 'flip', 'floor', 'get', 'group', 'gtime', 'hclose', 'hcount', 'hdel', 'hsym', 'iasc', 'idesc', 'ij', 'ijf', 'inter', 'inv', 'key', 'keys', 'lj', 'ljf', 'load', 'lower', 'lsq', 'ltime', 'ltrim', 'mavg', 'maxs', 'mcount', 'md5', 'mdev', 'med', 'meta', 'mins', 'mmax', 'mmin', 'mmu', 'mod', 'msum', 'neg', 'next', 'not', 'null', 'or', 'over', 'parse', 'peach', 'pj', 'prds', 'prior', 'prev', 'rand', 'rank', 'ratios', 'raze', 'read0', 'read1', 'reciprocal', 'reval', 'reverse', 'rload', 'rotate', 'rsave', 'rtrim', 'save', 'scan', 'scov', 'sdev', 'set', 'show', 'signum', 'ssr', 'string', 'sublist', 'sums', 'sv', 'svar', 'system', 'tables', 'til', 'trim', 'txf', 'type', 'uj', 'ujf', 'ungroup', 'union', 'upper', 'upsert', 'value', 'view', 'views', 'vs', 'where', 'wj', 'wj1', 'ww', 'xasc', 'xbar', 'xcol', 'xcols', 'xdesc', 'xgroup', 'xkey', 'xlog', 'xprev', 'xrank'), suffix='\\b'), Name.Builtin), inherit]}


