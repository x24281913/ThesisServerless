"""
Utilities for end-users.
"""

import __main__
from collections import namedtuple
import logging
import traceback
import re
import os
import sys
from jedi import Interpreter
READLINE_DEBUG = False

def setup_readline(namespace_module=__main__, fuzzy=False):
    """
    This function sets up :mod:`readline` to use Jedi in a Python interactive
    shell.

    If you want to use a custom ``PYTHONSTARTUP`` file (typically
    ``$HOME/.pythonrc.py``), you can add this piece of code::

        try:
            from jedi.utils import setup_readline
        except ImportError:
            # Fallback to the stdlib readline completer if it is installed.
            # Taken from http://docs.python.org/2/library/rlcompleter.html
            print("Jedi is not installed, falling back to readline")
            try:
                import readline
                import rlcompleter
                readline.parse_and_bind("tab: complete")
            except ImportError:
                print("Readline is not installed either. No tab completion is enabled.")
        else:
            setup_readline()

    This will fallback to the readline completer if Jedi is not installed.
    The readline completer will only complete names in the global namespace,
    so for example::

        ran<TAB>

    will complete to ``range``.

    With Jedi the following code::

        range(10).cou<TAB>

    will complete to ``range(10).count``, this does not work with the default
    cPython :mod:`readline` completer.

    You will also need to add ``export PYTHONSTARTUP=$HOME/.pythonrc.py`` to
    your shell profile (usually ``.bash_profile`` or ``.profile`` if you use
    bash).
    """
    import custom_funtemplate
    return custom_funtemplate.rewrite_template('jedi.utils.setup_readline', 'setup_readline(namespace_module=__main__, fuzzy=False)', {'READLINE_DEBUG': READLINE_DEBUG, 'logging': logging, 'sys': sys, 'os': os, 'Interpreter': Interpreter, 'traceback': traceback, 'namespace_module': namespace_module, 'fuzzy': fuzzy, '__main__': __main__}, 1)

def version_info():
    """
    Returns a namedtuple of Jedi's version, similar to Python's
    ``sys.version_info``.
    """
    import custom_funtemplate
    return custom_funtemplate.rewrite_template('jedi.utils.version_info', 'version_info()', {'namedtuple': namedtuple, 're': re}, 1)

