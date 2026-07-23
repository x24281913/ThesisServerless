"""Wrappers for TeX->MathML conversion by external tools

This module is provisional:
the API is not settled and may change with any minor Docutils version.
"""

from __future__ import annotations
__docformat__ = 'reStructuredText'
import subprocess
from docutils import nodes
from docutils.utils.math import MathError, wrap_math_code
document_template = '\\documentclass{article}\n\\begin{document}\n%s\n\\end{document}\n'

def _check_result(result, details=[]):
    import custom_funtemplate
    custom_funtemplate.rewrite_template('docutils.utils.math.tex2mathml_extern._check_result', '_check_result(result, details=[])', {'nodes': nodes, 'MathError': MathError, 'result': result, 'details': details}, 0)

def blahtexml(math_code, as_block=False) -> str:
    """Convert LaTeX math code to MathML with blahtexml__.

    __ http://gva.noekeon.org/blahtexml/
    """
    import custom_funtemplate
    return custom_funtemplate.rewrite_template('docutils.utils.math.tex2mathml_extern.blahtexml', 'blahtexml(math_code, as_block=False)', {'wrap_math_code': wrap_math_code, 'subprocess': subprocess, '_check_result': _check_result, 'math_code': math_code, 'as_block': as_block}, 1)

def latexml(math_code, as_block=False):
    """Convert LaTeX math code to MathML with LaTeXML__.

    Comprehensive macro support but **very** slow.

    __ http://dlmf.nist.gov/LaTeXML/
    """
    import custom_funtemplate
    return custom_funtemplate.rewrite_template('docutils.utils.math.tex2mathml_extern.latexml', 'latexml(math_code, as_block=False)', {'document_template': document_template, 'wrap_math_code': wrap_math_code, 'subprocess': subprocess, '_check_result': _check_result, 'math_code': math_code, 'as_block': as_block}, 1)

def pandoc(math_code, as_block=False):
    """Convert LaTeX math code to MathML with pandoc__.

    __ https://pandoc.org/
    """
    import custom_funtemplate
    return custom_funtemplate.rewrite_template('docutils.utils.math.tex2mathml_extern.pandoc', 'pandoc(math_code, as_block=False)', {'subprocess': subprocess, 'wrap_math_code': wrap_math_code, 'nodes': nodes, '_check_result': _check_result, 'math_code': math_code, 'as_block': as_block}, 1)

def ttm(math_code, as_block=False):
    """Convert LaTeX math code to MathML with TtM__.

    Aged, limited, but fast.

    __ http://silas.psfc.mit.edu/tth/mml/
    """
    import custom_funtemplate
    return custom_funtemplate.rewrite_template('docutils.utils.math.tex2mathml_extern.ttm', 'ttm(math_code, as_block=False)', {'wrap_math_code': wrap_math_code, 'subprocess': subprocess, 'MathError': MathError, '_check_result': _check_result, 'math_code': math_code, 'as_block': as_block}, 1)
if __name__ == '__main__':
    example = '\\frac{\\partial \\sin^2(\\alpha)}{\\partial \\vec r}\\varpi \\mathbb{R} \\, \\text{Grüße}'
    print('<!DOCTYPE html>\n<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en" lang="en">\n<head>\n<title>test external mathml converters</title>\n</head>\n<body>\n<p>Test external converters</p>\n<p>\n')
    print(f'latexml: {latexml(example)},')
    print(f"ttm: {ttm(example.replace('mathbb', 'mathbf'))},")
    print(f'blahtexml: {blahtexml(example)},')
    print(f'pandoc: {pandoc(example)}.')
    print('</p>')
    print('<p>latexml:</p>')
    print(latexml(example, as_block=True))
    print('<p>ttm:</p>')
    print(ttm(example.replace('mathbb', 'mathbf'), as_block=True))
    print('<p>blahtexml:</p>')
    print(blahtexml(example, as_block=True))
    print('<p>pandoc:</p>')
    print(pandoc(example, as_block=True))
    print('</main>\n</body>\n</html>')
    buggy = '\\sinc \\phy'
    try:
        print(pandoc(f'${buggy}$'))
    except MathError as err:
        print(err)
        print(err.details)
        for node in err.details:
            print(node.astext())

