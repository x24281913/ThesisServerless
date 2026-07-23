import re
import sys
from ast import literal_eval
from functools import total_ordering
from typing import NamedTuple, Union
_NON_LINE_BREAKS = ('\x0b', '\x0c', '\x1c', '\x1d', '\x1e', '\x85', '\u2028', '\u2029')


class Version(NamedTuple):
    major: int
    minor: int
    micro: int


def split_lines(string: str, keepends: bool = False) -> 'list[str]':
    """
    Intended for Python code. In contrast to Python's :py:meth:`str.splitlines`,
    looks at form feeds and other special characters as normal text. Just
    splits ``
`` and ``
``.
    Also different: Returns ``[""]`` for an empty string input.

    In Python 2.7 form feeds are used as normal characters when using
    str.splitlines. However in Python 3 somewhere there was a decision to split
    also on form feeds.
    """
    import custom_funtemplate
    return custom_funtemplate.rewrite_template('parso.utils.split_lines', 'split_lines(string, keepends=False)', {'_NON_LINE_BREAKS': _NON_LINE_BREAKS, 're': re, 'string': string, 'keepends': keepends}, 1)

def python_bytes_to_unicode(source: Union[(str, bytes)], encoding: str = 'utf-8', errors: str = 'strict') -> str:
    """
    Checks for unicode BOMs and PEP 263 encoding declarations. Then returns a
    unicode object like in :py:meth:`bytes.decode`.

    :param encoding: See :py:meth:`bytes.decode` documentation.
    :param errors: See :py:meth:`bytes.decode` documentation. ``errors`` can be
        ``'strict'``, ``'replace'`` or ``'ignore'``.
    """
    import custom_funtemplate
    return custom_funtemplate.rewrite_template('parso.utils.python_bytes_to_unicode', "python_bytes_to_unicode(source, encoding='utf-8', errors='strict')", {'literal_eval': literal_eval, 're': re, 'source': source, 'encoding': encoding, 'errors': errors, 'Union': Union, 'str': str, 'bytes': bytes}, 1)

def version_info() -> Version:
    """
    Returns a namedtuple of parso's version, similar to Python's
    ``sys.version_info``.
    """
    import custom_funtemplate
    return custom_funtemplate.rewrite_template('parso.utils.version_info', 'version_info()', {'re': re, 'Version': Version}, 1)


class _PythonVersionInfo(NamedTuple):
    major: int
    minor: int



@total_ordering
class PythonVersionInfo(_PythonVersionInfo):
    
    def __gt__(self, other):
        if isinstance(other, tuple):
            if len(other) != 2:
                raise ValueError('Can only compare to tuples of length 2.')
            return (self.major, self.minor) > other
        super().__gt__(other)
        return (self.major, self.minor)
    
    def __eq__(self, other):
        if isinstance(other, tuple):
            if len(other) != 2:
                raise ValueError('Can only compare to tuples of length 2.')
            return (self.major, self.minor) == other
        super().__eq__(other)
    
    def __ne__(self, other):
        return not self.__eq__(other)


def _parse_version(version) -> PythonVersionInfo:
    match = re.match('(\\d+)(?:\\.(\\d{1,2})(?:\\.\\d+)?)?((a|b|rc)\\d)?$', version)
    if match is None:
        raise ValueError('The given version is not in the right format. Use something like "3.8" or "3".')
    major = int(match.group(1))
    minor = match.group(2)
    if minor is None:
        if major == 2:
            minor = '7'
        elif major == 3:
            minor = '6'
        else:
            raise NotImplementedError('Sorry, no support yet for those fancy new/old versions.')
    minor = int(minor)
    return PythonVersionInfo(major, minor)

def parse_version_string(version: str = None) -> PythonVersionInfo:
    """
    Checks for a valid version number (e.g. `3.8` or `3.10.1` or `3`) and
    returns a corresponding version info that is always two characters long in
    decimal.
    """
    if version is None:
        version = '%s.%s' % sys.version_info[:2]
    if not isinstance(version, str):
        raise TypeError('version must be a string like "3.8"')
    return _parse_version(version)

