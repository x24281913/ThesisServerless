from __future__ import annotations
import argparse
import sys
import typing
from os.path import abspath, basename, dirname, join, realpath
from platform import python_version
from unicodedata import unidata_version
import charset_normalizer.md as md_module
from charset_normalizer import from_fp
from charset_normalizer.models import CliDetectionResult
from charset_normalizer.version import __version__

def query_yes_no(question: str, default: str = 'yes') -> bool:
    """Ask a yes/no question via input() and return the answer as a bool."""
    import custom_funtemplate
    return custom_funtemplate.rewrite_template('charset_normalizer.cli.__main__.query_yes_no', "query_yes_no(question, default='yes')", {'question': question, 'default': default}, 1)


class FileType:
    """Factory for creating file object types

    Instances of FileType are typically passed as type= arguments to the
    ArgumentParser add_argument() method.

    Keyword Arguments:
        - mode -- A string indicating how the file is to be opened. Accepts the
            same values as the builtin open() function.
        - bufsize -- The file's desired buffer size. Accepts the same values as
            the builtin open() function.
        - encoding -- The file's encoding. Accepts the same values as the
            builtin open() function.
        - errors -- A string indicating how encoding and decoding errors are to
            be handled. Accepts the same value as the builtin open() function.

    Backported from CPython 3.12
    """
    
    def __init__(self, mode: str = 'r', bufsize: int = -1, encoding: str | None = None, errors: str | None = None):
        self._mode = mode
        self._bufsize = bufsize
        self._encoding = encoding
        self._errors = errors
    
    def __call__(self, string: str) -> typing.IO:
        if string == '-':
            if 'r' in self._mode:
                return (sys.stdin.buffer if 'b' in self._mode else sys.stdin)
            elif any((c in self._mode for c in 'wax')):
                return (sys.stdout.buffer if 'b' in self._mode else sys.stdout)
            else:
                msg = f'argument "-" with mode {self._mode}'
                raise ValueError(msg)
        try:
            return open(string, self._mode, self._bufsize, self._encoding, self._errors)
        except OSError as e:
            message = f"can't open '{string}': {e}"
            raise argparse.ArgumentTypeError(message)
    
    def __repr__(self) -> str:
        args = (self._mode, self._bufsize)
        kwargs = [('encoding', self._encoding), ('errors', self._errors)]
        args_str = ', '.join([repr(arg) for arg in args if arg != -1] + [f'{kw}={arg!r}' for (kw, arg) in kwargs if arg is not None])
        return f'{type(self).__name__}({args_str})'


def cli_detect(argv: list[str] | None = None) -> int:
    """
    CLI assistant using ARGV and ArgumentParser
    :param argv:
    :return: 0 if everything is fine, anything else equal trouble
    """
    import custom_funtemplate
    return custom_funtemplate.rewrite_template('charset_normalizer.cli.__main__.cli_detect', 'cli_detect(argv=None)', {'argparse': argparse, 'FileType': FileType, '__version__': __version__, 'python_version': python_version, 'unidata_version': unidata_version, 'md_module': md_module, 'sys': sys, 'from_fp': from_fp, 'CliDetectionResult': CliDetectionResult, 'abspath': abspath, 'dirname': dirname, 'realpath': realpath, 'basename': basename, 'query_yes_no': query_yes_no, 'argv': argv, 'list': list, 'str': str}, 1)
if __name__ == '__main__':
    cli_detect()

