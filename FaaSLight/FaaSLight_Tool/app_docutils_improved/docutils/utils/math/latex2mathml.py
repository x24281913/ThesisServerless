"""Convert LaTex maths code into presentational MathML.

This module is provisional:
the API is not settled and may change with any minor Docutils version.
"""

import re
import unicodedata
from docutils.utils.math import MathError, mathalphabet2unichar, tex2unichar, toplevel_code
from docutils.utils.math.mathml_elements import math, mtable, mrow, mtr, mtd, menclose, mphantom, msqrt, mi, mn, mo, mtext, msub, msup, msubsup, munder, mover, munderover, mroot, mfrac, mspace, MathRow
letters = {'hbar': 'ℏ'}
letters.update(tex2unichar.mathalpha)
ordinary = tex2unichar.mathord
greek_capitals = {'Phi': 'Φ', 'Xi': 'Ξ', 'Sigma': 'Σ', 'Psi': 'Ψ', 'Delta': 'Δ', 'Theta': 'Θ', 'Upsilon': 'ϒ', 'Pi': 'Π', 'Omega': 'Ω', 'Gamma': 'Γ', 'Lambda': 'Λ'}
functions = {'liminf': 'lim\u202finf', 'limsup': 'lim\u202fsup', 'injlim': 'inj\u202flim', 'projlim': 'proj\u202flim', 'varlimsup': 'lim', 'varliminf': 'lim', 'varprojlim': 'lim', 'varinjlim': 'lim', 'operatorname': None}
functions.update(((name, name) for name in ('arccos', 'arcsin', 'arctan', 'arg', 'cos', 'cosh', 'cot', 'coth', 'csc', 'deg', 'det', 'dim', 'exp', 'gcd', 'hom', 'ker', 'lg', 'ln', 'log', 'Pr', 'sec', 'sin', 'sinh', 'tan', 'tanh')))
modulo_functions = {'bmod': (True, True, False, '0.278em'), 'pmod': (False, True, True, '0.444em'), 'mod': (False, True, False, '0.667em'), 'pod': (False, False, True, '0.444em')}
math_alphabets = {'mathbb': 'double-struck', 'mathbf': 'bold', 'mathbfit': 'bold-italic', 'mathcal': 'script', 'mathfrak': 'fraktur', 'mathit': 'italic', 'mathrm': 'normal', 'mathscr': 'script', 'mathsf': 'sans-serif', 'mathbfsfit': 'sans-serif-bold-italic', 'mathsfbfit': 'sans-serif-bold-italic', 'mathsfit': 'sans-serif-italic', 'mathtt': 'monospace'}
stretchables = {'backslash': '\\', 'uparrow': '↑', 'downarrow': '↓', 'updownarrow': '↕', 'Uparrow': '⇑', 'Downarrow': '⇓', 'Updownarrow': '⇕', 'lmoustache': '⎰', 'rmoustache': '⎱', 'arrowvert': '⏐', 'bracevert': '⎪', 'lvert': '|', 'lVert': '‖', 'rvert': '|', 'rVert': '‖', 'Arrowvert': '‖'}
stretchables.update(tex2unichar.mathfence)
stretchables.update(tex2unichar.mathopen)
stretchables.update(tex2unichar.mathclose)
operators = {'nleqq': '≦̸', 'ngeqq': '≧̸', 'nleqslant': '⩽̸', 'ngeqslant': '⩾̸', 'ngtrless': '≹', 'nlessgtr': '≸', 'nsubseteqq': '⫅̸', 'nsupseteqq': '⫆̸', 'centerdot': '⬝', 'varnothing': '⌀', 'varpropto': '∝', 'triangle': '△', 'triangledown': '▽', 'dotsb': '⋯', 'dotsc': '…', 'dotsi': '⋯', 'dotsm': '⋯', 'dotso': '…', 'lim': 'lim', 'sup': 'sup', 'inf': 'inf', 'max': 'max', 'min': 'min'}
operators.update(tex2unichar.mathbin)
operators.update(tex2unichar.mathrel)
operators.update(tex2unichar.mathpunct)
operators.update(tex2unichar.mathop)
operators.update(stretchables)
thick_operators = {'thicksim': '∼', 'thickapprox': '≈'}
small_operators = {'shortmid': '∣', 'shortparallel': '∥', 'nshortmid': '∤', 'nshortparallel': '∦', 'smallfrown': '⌢', 'smallsmile': '⌣', 'smallint': '∫'}
movablelimits = ('bigcap', 'bigcup', 'bigodot', 'bigoplus', 'bigotimes', 'bigsqcup', 'biguplus', 'bigvee', 'bigwedge', 'coprod', 'intop', 'ointop', 'prod', 'sum', 'lim', 'max', 'min', 'sup', 'inf')
spaces = {'qquad': '2em', 'quad': '1em', 'thickspace': '0.2778em', ';': '0.2778em', ' ': '0.25em', '\n': '0.25em', 'medspace': '0.2222em', ':': '0.2222em', 'thinspace': '0.1667em', ',': '0.1667em', 'negthinspace': '-0.1667em', '!': '-0.1667em', 'negmedspace': '-0.2222em', 'negthickspace': '-0.2778em'}
accents = {'acute': '´', 'bar': 'ˉ', 'breve': '˘', 'check': 'ˇ', 'dot': '˙', 'ddot': '¨', 'dddot': '˙˙˙', 'ddddot': '˙˙˙˙', 'grave': '`', 'hat': 'ˆ', 'mathring': '˚', 'tilde': '~', 'vec': '→'}
over = {'overbrace': ('⏞', -0.2), 'overleftarrow': ('←', -0.2), 'overleftrightarrow': ('↔', -0.2), 'overline': ('_', -0.2), 'overrightarrow': ('→', -0.2), 'widehat': ('^', -0.5), 'widetilde': ('~', -0.3)}
under = {'underbrace': ('⏟', 0.1), 'underleftarrow': ('←', -0.2), 'underleftrightarrow': ('↔', -0.2), 'underline': ('_', -0.8), 'underrightarrow': ('→', -0.2)}
anomalous_chars = {'-': '−', ':': '∶', '~': '\xa0'}
mathbb = {'Γ': 'ℾ', 'Π': 'ℿ', 'Σ': '⅀', 'γ': 'ℽ', 'π': 'ℼ'}
matrices = {'matrix': ('', ''), 'smallmatrix': ('', ''), 'pmatrix': ('(', ')'), 'bmatrix': ('[', ']'), 'Bmatrix': ('{', '}'), 'vmatrix': ('|', '|'), 'Vmatrix': ('‖', '‖'), 'aligned': ('', ''), 'cases': ('{', '')}
layout_styles = {'displaystyle': {'displaystyle': True, 'scriptlevel': 0}, 'textstyle': {'displaystyle': False, 'scriptlevel': 0}, 'scriptstyle': {'displaystyle': False, 'scriptlevel': 1}, 'scriptscriptstyle': {'displaystyle': False, 'scriptlevel': 2}}
fractions = {'frac': {}, 'cfrac': {'displaystyle': True, 'scriptlevel': 0, 'class': 'cfrac'}, 'dfrac': layout_styles['displaystyle'], 'tfrac': layout_styles['textstyle'], 'binom': {'linethickness': 0}, 'dbinom': layout_styles['displaystyle'] | {'linethickness': 0}, 'tbinom': layout_styles['textstyle'] | {'linethickness': 0}}
delimiter_sizes = ['', '1.2em', '1.623em', '2.047em', '2.470em']
bigdelimiters = {'left': 0, 'right': 0, 'bigl': 1, 'bigr': 1, 'Bigl': 2, 'Bigr': 2, 'biggl': 3, 'biggr': 3, 'Biggl': 4, 'Biggr': 4}

def tex_cmdname(string):
    """Return leading TeX command name and remainder of `string`.

    >>> tex_cmdname('mymacro2') # up to first non-letter
    ('mymacro', '2')
    >>> tex_cmdname('name 2') # strip trailing whitespace
    ('name', '2')
    >>> tex_cmdname('_2') # single non-letter character
    ('_', '2')

    """
    import custom_funtemplate
    return custom_funtemplate.rewrite_template('docutils.utils.math.latex2mathml.tex_cmdname', 'tex_cmdname(string)', {'re': re, 'string': string}, 2)

def tex_number(string):
    """Return leading number literal and remainder of `string`.

    >>> tex_number('123.4')
    ('123.4', '')

    """
    import custom_funtemplate
    return custom_funtemplate.rewrite_template('docutils.utils.math.latex2mathml.tex_number', 'tex_number(string)', {'re': re, 'string': string}, 2)

def tex_token(string):
    """Return first simple TeX token and remainder of `string`.

    >>> tex_token('\command{without argument}')
    ('\command', '{without argument}')
    >>> tex_token('or first character')
    ('o', 'r first character')

    """
    import custom_funtemplate
    return custom_funtemplate.rewrite_template('docutils.utils.math.latex2mathml.tex_token', 'tex_token(string)', {'re': re, 'string': string}, 2)

def tex_group(string):
    """Return first TeX group or token and remainder of `string`.

    >>> tex_group('{first group} returned without brackets')
    ('first group', ' returned without brackets')

    """
    import custom_funtemplate
    return custom_funtemplate.rewrite_template('docutils.utils.math.latex2mathml.tex_group', 'tex_group(string)', {'MathError': MathError, 'string': string}, 2)

def tex_token_or_group(string):
    """Return first TeX group or token and remainder of `string`.

    >>> tex_token_or_group('\command{without argument}')
    ('\command', '{without argument}')
    >>> tex_token_or_group('first character')
    ('f', 'irst character')
    >>> tex_token_or_group(' also whitespace')
    (' ', 'also whitespace')
    >>> tex_token_or_group('{first group} keep rest')
    ('first group', ' keep rest')

    """
    import custom_funtemplate
    return custom_funtemplate.rewrite_template('docutils.utils.math.latex2mathml.tex_token_or_group', 'tex_token_or_group(string)', {'tex_token': tex_token, 'tex_group': tex_group, 'string': string}, 2)

def tex_optarg(string):
    """Return optional argument and remainder.

    >>> tex_optarg('[optional argument] returned without brackets')
    ('optional argument', ' returned without brackets')
    >>> tex_optarg('{empty string, if there is no optional arg}')
    ('', '{empty string, if there is no optional arg}')

    """
    import custom_funtemplate
    return custom_funtemplate.rewrite_template('docutils.utils.math.latex2mathml.tex_optarg', 'tex_optarg(string)', {'re': re, 'MathError': MathError, 'string': string}, 2)

def parse_latex_math(root, source):
    """Append MathML conversion of `string` to `node` and return it.

    >>> parse_latex_math(math(), r'lpha')
    math(mi('α'))
    >>> parse_latex_math(mrow(), r'x_{n}')
    mrow(msub(mi('x'), mi('n')))

    """
    import custom_funtemplate
    return custom_funtemplate.rewrite_template('docutils.utils.math.latex2mathml.parse_latex_math', 'parse_latex_math(root, source)', {'tex_cmdname': tex_cmdname, 'handle_cmd': handle_cmd, 'handle_script_or_limit': handle_script_or_limit, 'MathRow': MathRow, 'mrow': mrow, 'mtd': mtd, 'mi': mi, 'tex_number': tex_number, 'mn': mn, 'anomalous_chars': anomalous_chars, 'mo': mo, 'MathError': MathError, 'root': root, 'source': source}, 1)

def handle_cmd(name, node, string):
    """Process LaTeX command `name` followed by `string`.

    Append result to `node`.
    If needed, parse `string` for command argument.
    Return new current node and remainder of `string`:

    >>> handle_cmd('hbar', math(), r' rac')
    (math(mi('ℏ')), ' rac')
    >>> handle_cmd('hspace', math(), r'{1ex} (x)')
    (math(mspace(width='1ex')), ' (x)')

    """
    import custom_funtemplate
    return custom_funtemplate.rewrite_template('docutils.utils.math.latex2mathml.handle_cmd', 'handle_cmd(name, node, string)', {'letters': letters, 'mi': mi, 'greek_capitals': greek_capitals, 'ordinary': ordinary, 'functions': functions, 'tex_token_or_group': tex_token_or_group, 'munder': munder, 'mo': mo, 'mover': mover, 'modulo_functions': modulo_functions, 'mspace': mspace, 'parse_latex_math': parse_latex_math, 'mrow': mrow, 'math_alphabets': math_alphabets, 'handle_math_alphabet': handle_math_alphabet, 'thick_operators': thick_operators, 'small_operators': small_operators, 'operators': operators, 'movablelimits': movablelimits, 'bigdelimiters': bigdelimiters, 'delimiter_sizes': delimiter_sizes, 'stretchables': stretchables, 'MathError': MathError, 'tex_token': tex_token, 'unicodedata': unicodedata, 're': re, 'mtext': mtext, 'spaces': spaces, 'tex_group': tex_group, 'mphantom': mphantom, 'menclose': menclose, 'tex_optarg': tex_optarg, 'mroot': mroot, 'msqrt': msqrt, 'fractions': fractions, 'mfrac': mfrac, 'mtd': mtd, 'mtr': mtr, 'accents': accents, 'over': over, 'under': under, 'munderover': munderover, 'layout_styles': layout_styles, 'handle_script_or_limit': handle_script_or_limit, 'begin_environment': begin_environment, 'end_environment': end_environment, 'name': name, 'node': node, 'string': string}, 2)

def handle_math_alphabet(name, node, string):
    import custom_funtemplate
    return custom_funtemplate.rewrite_template('docutils.utils.math.latex2mathml.handle_math_alphabet', 'handle_math_alphabet(name, node, string)', {'tex_token_or_group': tex_token_or_group, 'mi': mi, 'mrow': mrow, 'parse_latex_math': parse_latex_math, 'mathalphabet2unichar': mathalphabet2unichar, 'mn': mn, 'name': name, 'node': node, 'string': string}, 2)

def handle_script_or_limit(node, c, limits=''):
    """Append script or limit element to `node`."""
    import custom_funtemplate
    return custom_funtemplate.rewrite_template('docutils.utils.math.latex2mathml.handle_script_or_limit', "handle_script_or_limit(node, c, limits='')", {'movablelimits': movablelimits, 'mover': mover, 'munderover': munderover, 'msup': msup, 'msubsup': msubsup, 'munder': munder, 'msub': msub, 'node': node, 'c': c, 'limits': limits}, 1)

def begin_environment(node, string):
    import custom_funtemplate
    return custom_funtemplate.rewrite_template('docutils.utils.math.latex2mathml.begin_environment', 'begin_environment(node, string)', {'tex_group': tex_group, 'matrices': matrices, 'mrow': mrow, 'mo': mo, 'mtd': mtd, 'mtable': mtable, 'mtr': mtr, 'MathError': MathError, 'node': node, 'string': string}, 2)

def end_environment(node, string):
    import custom_funtemplate
    return custom_funtemplate.rewrite_template('docutils.utils.math.latex2mathml.end_environment', 'end_environment(node, string)', {'tex_group': tex_group, 'matrices': matrices, 'mo': mo, 'MathError': MathError, 'node': node, 'string': string}, 2)

def tex_equation_columns(rows):
    import custom_funtemplate
    return custom_funtemplate.rewrite_template('docutils.utils.math.latex2mathml.tex_equation_columns', 'tex_equation_columns(rows)', {'rows': rows}, 1)

def align_attributes(rows):
    import custom_funtemplate
    return custom_funtemplate.rewrite_template('docutils.utils.math.latex2mathml.align_attributes', 'align_attributes(rows)', {'rows': rows}, 1)

def tex2mathml(tex_math, as_block=False):
    """Return string with MathML code corresponding to `tex_math`.

    Set `as_block` to ``True`` for displayed formulas.
    """
    import custom_funtemplate
    return custom_funtemplate.rewrite_template('docutils.utils.math.latex2mathml.tex2mathml', 'tex2mathml(tex_math, as_block=False)', {'math': math, 'toplevel_code': toplevel_code, 'mtd': mtd, 'mtable': mtable, 'mtr': mtr, 'parse_latex_math': parse_latex_math, 'tex_math': tex_math, 'as_block': as_block}, 1)

