import argparse
import sys
from json import dumps
from os.path import abspath
from platform import python_version
from typing import List, Optional
try:
    from unicodedata2 import unidata_version
except ImportError:
    from unicodedata import unidata_version
from charset_normalizer import from_fp
from charset_normalizer.models import CliDetectionResult
from charset_normalizer.version import __version__

def query_yes_no(question: str, default: str = 'yes') -> bool:
    """Ask a yes/no question via input() and return their answer.

    "question" is a string that is presented to the user.
    "default" is the presumed answer if the user just hits <Enter>.
        It must be "yes" (the default), "no" or None (meaning
        an answer is required of the user).

    The "answer" return value is True for "yes" or False for "no".

    Credit goes to (c) https://stackoverflow.com/questions/3041986/apt-command-line-interface-like-yes-no-input
    """
    import custom_funtemplate
    return custom_funtemplate.rewrite_template('charset_normalizer.cli.normalizer.query_yes_no', "query_yes_no(question, default='yes')", {'sys': sys, 'question': question, 'default': default}, 1)

def cli_detect(argv: Optional[List[str]] = None) -> int:
    """
    CLI assistant using ARGV and ArgumentParser
    :param argv:
    :return: 0 if everything is fine, anything else equal trouble
    """
    import custom_funtemplate
    return custom_funtemplate.rewrite_template('charset_normalizer.cli.normalizer.cli_detect', 'cli_detect(argv=None)', {'argparse': argparse, '__version__': __version__, 'python_version': python_version, 'unidata_version': unidata_version, 'sys': sys, 'from_fp': from_fp, 'CliDetectionResult': CliDetectionResult, 'abspath': abspath, 'List': List, 'query_yes_no': query_yes_no, 'IOError': IOError, 'dumps': dumps, 'argv': argv, 'Optional': Optional, 'List': List, 'str': str}, 1)
if __name__ == '__main__':
    cli_detect()

