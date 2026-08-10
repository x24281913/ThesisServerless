"""
    Pygments
    ~~~~~~~~

    Pygments is a syntax highlighting package written in Python.

    It is a generic syntax highlighter for general use in all kinds of software
    such as forum systems, wikis or other applications that need to prettify
    source code. Highlights are:

    * a wide range of common languages and markup formats is supported
    * special attention is paid to details, increasing quality by a fair amount
    * support for new languages and formats are added easily
    * a number of output formats, presently HTML, LaTeX, RTF, SVG, all image
      formats that PIL supports, and ANSI sequences
    * it is usable as a command-line tool and as a library
    * ... and it highlights even Brainfuck!

    The `Pygments master branch`_ is installable with ``easy_install Pygments==dev``.

    .. _Pygments master branch:
       https://github.com/pygments/pygments/archive/master.zip#egg=Pygments-dev

    :copyright: Copyright 2006-present by the Pygments team, see AUTHORS.
    :license: BSD, see LICENSE for details.
"""

from io import StringIO, BytesIO
__version__ = '2.20.0'
__docformat__ = 'restructuredtext'
__all__ = ['lex', 'format', 'highlight']

def lex(code, lexer):
    """
    Lex `code` with the `lexer` (must be a `Lexer` instance)
    and return an iterable of tokens. Currently, this only calls
    `lexer.get_tokens()`.
    """
    import custom_funtemplate
    return custom_funtemplate.rewrite_template('pygments.__init__.lex', 'lex(code, lexer)', {'code': code, 'lexer': lexer}, 1)

def format(tokens, formatter, outfile=None):
    """
    Format ``tokens`` (an iterable of tokens) with the formatter ``formatter``
    (a `Formatter` instance).

    If ``outfile`` is given and a valid file object (an object with a
    ``write`` method), the result will be written to it, otherwise it
    is returned as a string.
    """
    import custom_funtemplate
    return custom_funtemplate.rewrite_template('pygments.__init__.format', 'format(tokens, formatter, outfile=None)', {'BytesIO': BytesIO, 'StringIO': StringIO, 'tokens': tokens, 'formatter': formatter, 'outfile': outfile}, 1)

def highlight(code, lexer, formatter, outfile=None):
    """
    This is the most high-level highlighting function. It combines `lex` and
    `format` in one function.
    """
    return format(lex(code, lexer), formatter, outfile)

