"""
This is the Docutils (Python Documentation Utilities) "math" sub-package.

It contains various modules for conversion between different math formats
(LaTeX, MathML, HTML).

:math2html:    LaTeX math -> HTML conversion from eLyXer
:latex2mathml: LaTeX math -> presentational MathML
:unichar2tex:  Unicode character to LaTeX math translation table
:tex2unichar:  LaTeX math to Unicode character translation dictionaries
:mathalphabet2unichar:  LaTeX math alphabets to Unicode character translation
:tex2mathml_extern: Wrapper for 3rd party TeX -> MathML converters
"""

from __future__ import annotations
__docformat__ = 'reStructuredText'


class MathError(ValueError):
    """Exception for math syntax and math conversion errors.

    The additional attribute `details` may hold a list of Docutils
    nodes suitable as children for a ``<system_message>``.
    """
    
    def __init__(self, msg, details=[]) -> None:
        super().__init__(msg)
        self.details = details


def toplevel_code(code):
    """Return string (LaTeX math) `code` with environments stripped out."""
    chunks = code.split('\\begin{')
    return '\\begin{'.join((chunk.split('\\end{')[-1] for chunk in chunks))

def pick_math_environment(code, numbered=False):
    """Return the right math environment to display `code`.

    The test simply looks for line-breaks (``\``) outside environments.
    Multi-line formulae are set with ``align``, one-liners with
    ``equation``.

    If `numbered` evaluates to ``False``, the "starred" versions are used
    to suppress numbering.
    """
    import custom_funtemplate
    return custom_funtemplate.rewrite_template('docutils.utils.math.__init__.pick_math_environment', 'pick_math_environment(code, numbered=False)', {'toplevel_code': toplevel_code, 'code': code, 'numbered': numbered}, 1)

def wrap_math_code(code, as_block) -> str:
    import custom_funtemplate
    return custom_funtemplate.rewrite_template('docutils.utils.math.__init__.wrap_math_code', 'wrap_math_code(code, as_block)', {'pick_math_environment': pick_math_environment, 'code': code, 'as_block': as_block}, 1)

