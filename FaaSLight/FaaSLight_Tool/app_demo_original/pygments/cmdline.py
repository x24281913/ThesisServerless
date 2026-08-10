"""
    pygments.cmdline
    ~~~~~~~~~~~~~~~~

    Command line interface.

    :copyright: Copyright 2006-present by the Pygments team, see AUTHORS.
    :license: BSD, see LICENSE for details.
"""

import os
import sys
import shutil
import argparse
from textwrap import dedent
from pygments import __version__, highlight
from pygments.util import ClassNotFound, OptionError, docstring_headline, guess_decode, guess_decode_from_terminal, terminal_encoding, UnclosingTextIOWrapper
from pygments.lexers import get_all_lexers, get_lexer_by_name, guess_lexer, load_lexer_from_file, get_lexer_for_filename, find_lexer_class_for_filename
from pygments.lexers.special import TextLexer
from pygments.formatters.latex import LatexEmbeddedLexer, LatexFormatter
from pygments.formatters import get_all_formatters, get_formatter_by_name, load_formatter_from_file, get_formatter_for_filename, find_formatter_class
from pygments.formatters.terminal import TerminalFormatter
from pygments.formatters.terminal256 import Terminal256Formatter, TerminalTrueColorFormatter
from pygments.filters import get_all_filters, find_filter_class
from pygments.styles import get_all_styles, get_style_by_name

def _parse_options(o_strs):
    import custom_funtemplate
    return custom_funtemplate.rewrite_template('pygments.cmdline._parse_options', '_parse_options(o_strs)', {'o_strs': o_strs}, 1)

def _parse_filters(f_strs):
    import custom_funtemplate
    return custom_funtemplate.rewrite_template('pygments.cmdline._parse_filters', '_parse_filters(f_strs)', {'_parse_options': _parse_options, 'f_strs': f_strs}, 1)

def _print_help(what, name):
    import custom_funtemplate
    return custom_funtemplate.rewrite_template('pygments.cmdline._print_help', '_print_help(what, name)', {'get_lexer_by_name': get_lexer_by_name, 'dedent': dedent, 'find_formatter_class': find_formatter_class, 'find_filter_class': find_filter_class, 'sys': sys, 'what': what, 'name': name}, 1)

def _print_list(what):
    import custom_funtemplate
    custom_funtemplate.rewrite_template('pygments.cmdline._print_list', '_print_list(what)', {'get_all_lexers': get_all_lexers, 'get_all_formatters': get_all_formatters, 'docstring_headline': docstring_headline, 'get_all_filters': get_all_filters, 'find_filter_class': find_filter_class, 'get_all_styles': get_all_styles, 'get_style_by_name': get_style_by_name, 'what': what}, 0)

def _print_list_as_json(requested_items):
    import custom_funtemplate
    custom_funtemplate.rewrite_template('pygments.cmdline._print_list_as_json', '_print_list_as_json(requested_items)', {'get_all_lexers': get_all_lexers, 'get_all_formatters': get_all_formatters, 'docstring_headline': docstring_headline, 'get_all_filters': get_all_filters, 'find_filter_class': find_filter_class, 'get_all_styles': get_all_styles, 'get_style_by_name': get_style_by_name, 'sys': sys, 'requested_items': requested_items}, 0)

def main_inner(parser, argns):
    import custom_funtemplate
    return custom_funtemplate.rewrite_template('pygments.cmdline.main_inner', 'main_inner(parser, argns)', {'__version__': __version__, 'sys': sys, 'main': main, '_print_list': _print_list, '_print_list_as_json': _print_list_as_json, '_print_help': _print_help, '_parse_options': _parse_options, 'find_lexer_class_for_filename': find_lexer_class_for_filename, 'TextLexer': TextLexer, 'guess_lexer': guess_lexer, 'ClassNotFound': ClassNotFound, 'get_formatter_by_name': get_formatter_by_name, '_parse_filters': _parse_filters, 'load_lexer_from_file': load_lexer_from_file, 'get_lexer_by_name': get_lexer_by_name, 'OptionError': OptionError, 'guess_decode': guess_decode, 'get_lexer_for_filename': get_lexer_for_filename, 'guess_decode_from_terminal': guess_decode_from_terminal, 'load_formatter_from_file': load_formatter_from_file, 'get_formatter_for_filename': get_formatter_for_filename, 'os': os, 'TerminalTrueColorFormatter': TerminalTrueColorFormatter, 'Terminal256Formatter': Terminal256Formatter, 'TerminalFormatter': TerminalFormatter, 'terminal_encoding': terminal_encoding, 'UnclosingTextIOWrapper': UnclosingTextIOWrapper, 'colorama': colorama, 'LatexFormatter': LatexFormatter, 'LatexEmbeddedLexer': LatexEmbeddedLexer, 'highlight': highlight, 'parser': parser, 'argns': argns}, 1)


class HelpFormatter(argparse.HelpFormatter):
    
    def __init__(self, prog, indent_increment=2, max_help_position=16, width=None):
        if width is None:
            try:
                width = shutil.get_terminal_size().columns - 2
            except Exception:
                pass
        argparse.HelpFormatter.__init__(self, prog, indent_increment, max_help_position, width)


def main(args=sys.argv):
    """
    Main command line entry point.
    """
    import custom_funtemplate
    return custom_funtemplate.rewrite_template('pygments.cmdline.main', 'main(args=sys.argv)', {'argparse': argparse, 'HelpFormatter': HelpFormatter, 'main_inner': main_inner, 'sys': sys, 'args': args}, 1)

