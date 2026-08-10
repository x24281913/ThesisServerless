"""
    pygments.lexers.modeling
    ~~~~~~~~~~~~~~~~~~~~~~~~

    Lexers for modeling languages.

    :copyright: Copyright 2006-present by the Pygments team, see AUTHORS.
    :license: BSD, see LICENSE for details.
"""

import re
from pygments.lexer import RegexLexer, include, bygroups, using, default
from pygments.token import Text, Comment, Operator, Keyword, Name, String, Number, Punctuation, Whitespace
from pygments.lexers.html import HtmlLexer
from pygments.lexers import _stan_builtins
__all__ = ['ModelicaLexer', 'BugsLexer', 'JagsLexer', 'StanLexer']


class ModelicaLexer(RegexLexer):
    """
    For Modelica source code.
    """
    name = 'Modelica'
    url = 'http://www.modelica.org/'
    aliases = ['modelica']
    filenames = ['*.mo']
    mimetypes = ['text/x-modelica']
    version_added = '1.1'
    flags = re.DOTALL | re.MULTILINE
    _name = "(?:'(?:[^\\\\']|\\\\.)+'|[a-zA-Z_]\\w*)"
    tokens = {'whitespace': [('[\\s\\ufeff]+', Text), ('//[^\\n]*\\n?', Comment.Single), ('/\\*.*?\\*/', Comment.Multiline)], 'root': [include('whitespace'), ('"', String.Double, 'string'), ('[()\\[\\]{},;]+', Punctuation), ('\\.?[*^/+-]|\\.|<>|[<>:=]=?', Operator), ('\\d+(\\.?\\d*[eE][-+]?\\d+|\\.\\d*)', Number.Float), ('\\d+', Number.Integer), ('(abs|acos|actualStream|array|asin|assert|AssertionLevel|atan|atan2|backSample|Boolean|cardinality|cat|ceil|change|Clock|Connections|cos|cosh|cross|delay|diagonal|div|edge|exp|ExternalObject|fill|floor|getInstanceName|hold|homotopy|identity|inStream|integer|Integer|interval|inverse|isPresent|linspace|log|log10|matrix|max|min|mod|ndims|noClock|noEvent|ones|outerProduct|pre|previous|product|Real|reinit|rem|rooted|sample|scalar|semiLinear|shiftSample|sign|sin|sinh|size|skew|smooth|spatialDistribution|sqrt|StateSelect|String|subSample|sum|superSample|symmetric|tan|tanh|terminal|terminate|time|transpose|vector|zeros)\\b', Name.Builtin), ('(algorithm|annotation|break|connect|constant|constrainedby|der|discrete|each|else|elseif|elsewhen|encapsulated|enumeration|equation|exit|expandable|extends|external|firstTick|final|flow|for|if|import|impure|in|initial|inner|input|interval|loop|nondiscrete|outer|output|parameter|partial|protected|public|pure|redeclare|replaceable|return|stream|then|when|while)\\b', Keyword.Reserved), ('(and|not|or)\\b', Operator.Word), ('(block|class|connector|end|function|model|operator|package|record|type)\\b', Keyword.Reserved, 'class'), ('(false|true)\\b', Keyword.Constant), ('within\\b', Keyword.Reserved, 'package-prefix'), (_name, Name)], 'class': [include('whitespace'), ('(function|record)\\b', Keyword.Reserved), ('(if|for|when|while)\\b', Keyword.Reserved, '#pop'), (_name, Name.Class, '#pop'), default('#pop')], 'package-prefix': [include('whitespace'), (_name, Name.Namespace, '#pop'), default('#pop')], 'string': [('"', String.Double, '#pop'), ('\\\\[\\\'"?\\\\abfnrtv]', String.Escape), ('(?i)<\\s*html\\s*>([^\\\\"]|\\\\.)+?(<\\s*/\\s*html\\s*>|(?="))', using(HtmlLexer)), ('<|\\\\?[^"\\\\<]+', String.Double)]}



class BugsLexer(RegexLexer):
    """
    Pygments Lexer for OpenBugs and WinBugs
    models.
    """
    name = 'BUGS'
    aliases = ['bugs', 'winbugs', 'openbugs']
    filenames = ['*.bug']
    url = 'https://www.mrc-bsu.cam.ac.uk/software/bugs/openbugs'
    version_added = '1.6'
    _FUNCTIONS = ('abs', 'arccos', 'arccosh', 'arcsin', 'arcsinh', 'arctan', 'arctanh', 'cloglog', 'cos', 'cosh', 'cumulative', 'cut', 'density', 'deviance', 'equals', 'expr', 'gammap', 'ilogit', 'icloglog', 'integral', 'log', 'logfact', 'loggam', 'logit', 'max', 'min', 'phi', 'post.p.value', 'pow', 'prior.p.value', 'probit', 'replicate.post', 'replicate.prior', 'round', 'sin', 'sinh', 'solution', 'sqrt', 'step', 'tan', 'tanh', 'trunc', 'inprod', 'interp.lin', 'inverse', 'logdet', 'mean', 'eigen.vals', 'ode', 'prod', 'p.valueM', 'rank', 'ranked', 'replicate.postM', 'sd', 'sort', 'sum', 'D', 'I', 'F', 'T', 'C')
    ' OpenBUGS built-in functions\n\n    From http://www.openbugs.info/Manuals/ModelSpecification.html#ContentsAII\n\n    This also includes\n\n    - T, C, I : Truncation and censoring.\n      ``T`` and ``C`` are in OpenBUGS. ``I`` in WinBUGS.\n    - D : ODE\n    - F : Functional http://www.openbugs.info/Examples/Functionals.html\n\n    '
    _DISTRIBUTIONS = ('dbern', 'dbin', 'dcat', 'dnegbin', 'dpois', 'dhyper', 'dbeta', 'dchisqr', 'ddexp', 'dexp', 'dflat', 'dgamma', 'dgev', 'df', 'dggamma', 'dgpar', 'dloglik', 'dlnorm', 'dlogis', 'dnorm', 'dpar', 'dt', 'dunif', 'dweib', 'dmulti', 'ddirch', 'dmnorm', 'dmt', 'dwish')
    ' OpenBUGS built-in distributions\n\n    Functions from\n    http://www.openbugs.info/Manuals/ModelSpecification.html#ContentsAI\n    '
    tokens = {'whitespace': [('\\s+', Text)], 'comments': [('#.*$', Comment.Single)], 'root': [include('comments'), include('whitespace'), ('(model)(\\s+)(\\{)', bygroups(Keyword.Namespace, Text, Punctuation)), ('(for|in)(?![\\w.])', Keyword.Reserved), ('({})(?=\\s*\\()'.format('|'.join(_FUNCTIONS + _DISTRIBUTIONS)), Name.Builtin), ('[A-Za-z][\\w.]*', Name), ('[-+]?[0-9]*\\.?[0-9]+([eE][-+]?[0-9]+)?', Number), ('\\[|\\]|\\(|\\)|:|,|;', Punctuation), ('<-|~', Operator), ('\\+|-|\\*|/', Operator), ('[{}]', Punctuation)]}
    
    def analyse_text(text):
        if re.search('^\\s*model\\s*{', text, re.M):
            return 0.7
        else:
            return 0.0



class JagsLexer(RegexLexer):
    """
    Pygments Lexer for JAGS.
    """
    name = 'JAGS'
    aliases = ['jags']
    filenames = ['*.jag', '*.bug']
    url = 'https://mcmc-jags.sourceforge.io'
    version_added = '1.6'
    _FUNCTIONS = ('abs', 'arccos', 'arccosh', 'arcsin', 'arcsinh', 'arctan', 'arctanh', 'cos', 'cosh', 'cloglog', 'equals', 'exp', 'icloglog', 'ifelse', 'ilogit', 'log', 'logfact', 'loggam', 'logit', 'phi', 'pow', 'probit', 'round', 'sin', 'sinh', 'sqrt', 'step', 'tan', 'tanh', 'trunc', 'inprod', 'interp.lin', 'logdet', 'max', 'mean', 'min', 'prod', 'sum', 'sd', 'inverse', 'rank', 'sort', 't', 'acos', 'acosh', 'asin', 'asinh', 'atan', 'T', 'I')
    _DISTRIBUTIONS = tuple((f'[dpq]{x}' for x in ('bern', 'beta', 'dchiqsqr', 'ddexp', 'dexp', 'df', 'gamma', 'gen.gamma', 'logis', 'lnorm', 'negbin', 'nchisqr', 'norm', 'par', 'pois', 'weib')))
    _OTHER_DISTRIBUTIONS = ('dt', 'dunif', 'dbetabin', 'dbern', 'dbin', 'dcat', 'dhyper', 'ddirch', 'dmnorm', 'dwish', 'dmt', 'dmulti', 'dbinom', 'dchisq', 'dnbinom', 'dweibull', 'ddirich')
    tokens = {'whitespace': [('\\s+', Text)], 'names': [('[a-zA-Z][\\w.]*\\b', Name)], 'comments': [('(?s)/\\*.*?\\*/', Comment.Multiline), ('#.*$', Comment.Single)], 'root': [include('comments'), include('whitespace'), ('(model|data)(\\s+)(\\{)', bygroups(Keyword.Namespace, Text, Punctuation)), ('var(?![\\w.])', Keyword.Declaration), ('(for|in)(?![\\w.])', Keyword.Reserved), ('({})(?=\\s*\\()'.format('|'.join(_FUNCTIONS + _DISTRIBUTIONS + _OTHER_DISTRIBUTIONS)), Name.Builtin), include('names'), ('[-+]?[0-9]*\\.?[0-9]+([eE][-+]?[0-9]+)?', Number), ('\\[|\\]|\\(|\\)|:|,|;', Punctuation), ('<-|~', Operator), ('\\+|-|\\*|\\/|\\|\\|[&]{2}|[<>=]=?|\\^|%.*?%', Operator), ('[{}]', Punctuation)]}
    
    def analyse_text(text):
        if re.search('^\\s*model\\s*\\{', text, re.M):
            if re.search('^\\s*data\\s*\\{', text, re.M):
                return 0.9
            elif re.search('^\\s*var', text, re.M):
                return 0.9
            else:
                return 0.3
        else:
            return 0



class StanLexer(RegexLexer):
    """Pygments Lexer for Stan models.

    The Stan modeling language is specified in the *Stan Modeling Language
    User's Guide and Reference Manual, v2.17.0*,
    `pdf <https://github.com/stan-dev/stan/releases/download/v2.17.0/stan-reference-2.17.0.pdf>`__.
    """
    name = 'Stan'
    aliases = ['stan']
    filenames = ['*.stan']
    url = 'https://mc-stan.org'
    version_added = '1.6'
    tokens = {'whitespace': [('\\s+', Text)], 'comments': [('(?s)/\\*.*?\\*/', Comment.Multiline), ('(//|#).*$', Comment.Single)], 'root': [('"[^"]*"', String), include('comments'), include('whitespace'), ('({})(\\s*)(\\{{)'.format('|'.join(('functions', 'data', 'transformed\\s+?data', 'parameters', 'transformed\\s+parameters', 'model', 'generated\\s+quantities'))), bygroups(Keyword.Namespace, Text, Punctuation)), ('target\\s*\\+=', Keyword), ('jacobian\\s*\\+=', Keyword), ('({})\\b'.format('|'.join(_stan_builtins.KEYWORDS)), Keyword), ('T(?=\\s*\\[)', Keyword), ('({})\\b'.format('|'.join(_stan_builtins.TYPES)), Keyword.Type), ('(<)(\\s*)(upper|lower|offset|multiplier)(\\s*)(=)', bygroups(Operator, Whitespace, Keyword, Whitespace, Punctuation)), ('(,)(\\s*)(upper)(\\s*)(=)', bygroups(Punctuation, Whitespace, Keyword, Whitespace, Punctuation)), ('[;,\\[\\]()]', Punctuation), ('({})(?=\\s*\\()'.format('|'.join(_stan_builtins.FUNCTIONS)), Name.Builtin), ('(~)(\\s*)({})(?=\\s*\\()'.format('|'.join(_stan_builtins.DISTRIBUTIONS)), bygroups(Operator, Whitespace, Name.Builtin)), ('[A-Za-z]\\w*__\\b', Name.Builtin.Pseudo), ('({})\\b'.format('|'.join(_stan_builtins.RESERVED)), Keyword.Reserved), ('[A-Za-z]\\w*(?=\\s*\\()]', Name.Function), ('[0-9]+(\\.[0-9]*)?([eE][+-]?[0-9]+)?i', Number.Float), ('\\.[0-9]+([eE][+-]?[0-9]+)?i', Number.Float), ('[0-9]+i', Number.Float), ('[0-9]+(\\.[0-9]*)?([eE][+-]?[0-9]+)?', Number.Float), ('\\.[0-9]+([eE][+-]?[0-9]+)?', Number.Float), ('[0-9]+', Number.Integer), ('[A-Za-z]\\w*\\b', Name), ('<-|(?:\\+|-|\\.?/|\\.?\\*|=)?=|~', Operator), ("\\+|-|\\.?\\*|\\.?/|\\\\|'|\\.?\\^|!=?|<=?|>=?|\\|\\||&&|%|\\?|:|%/%|!", Operator), ('[{}]', Punctuation), ('\\|', Punctuation)]}
    
    def analyse_text(text):
        if re.search('^\\s*parameters\\s*\\{', text, re.M):
            return 1.0
        else:
            return 0.0


