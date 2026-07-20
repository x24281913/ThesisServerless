"""Command-line interface for the :mod:`idna` package.

Invoked via ``python -m idna``. See :func:`main` for the entry point.
"""

import argparse
import sys
from collections.abc import Iterable
from itertools import chain
from typing import IO, Optional
from . import IDNAError, decode, encode
from .core import _alabel_prefix, _unicode_dots_re
from .package_data import __version__

def _looks_like_alabel(s: str) -> bool:
    """Return True if any label in ``s`` carries the ``xn--`` ACE prefix."""
    prefix = _alabel_prefix.decode('ascii')
    return any((label.lower().startswith(prefix) for label in _unicode_dots_re.split(s)))

def _build_parser() -> argparse.ArgumentParser:
    import custom_funtemplate
    return custom_funtemplate.rewrite_template('idna.cli._build_parser', '_build_parser()', {'argparse': argparse, '__version__': __version__, 'argparse': argparse}, 1)

def _iter_stdin(stream: IO[str]) -> Iterable[str]:
    """Yield non-empty stripped lines from ``stream``, ignoring blanks."""
    import custom_funtemplate
    custom_funtemplate.rewrite_template('idna.cli._iter_stdin', '_iter_stdin(stream)', {'stream': stream, 'IO': IO, 'str': str, 'Iterable': Iterable, 'str': str}, 0)

def _convert_one(domain: str, mode: str, uts46: bool) -> bool:
    """Convert ``domain`` and write the result; return ``False`` on failure."""
    import custom_funtemplate
    return custom_funtemplate.rewrite_template('idna.cli._convert_one', '_convert_one(domain, mode, uts46)', {'IDNAError': IDNAError, 'sys': sys, 'domain': domain, 'mode': mode, 'uts46': uts46}, 1)

def main(argv: Optional[list[str]] = None) -> int:
    """Entry point for ``python -m idna``.

    When more than one domain is supplied (via positional arguments or
    piped stdin) and no mode flag is given, the first input determines
    the direction and that mode is applied uniformly to the rest.

    :param argv: Argument list excluding the program name. Defaults to
        :data:`sys.argv` when ``None``.
    :returns: ``0`` on success, ``1`` if any conversion fails.
    """
    import custom_funtemplate
    return custom_funtemplate.rewrite_template('idna.cli.main', 'main(argv=None)', {'_build_parser': _build_parser, 'Iterable': Iterable, 'sys': sys, '_iter_stdin': _iter_stdin, '_looks_like_alabel': _looks_like_alabel, '_convert_one': _convert_one, 'chain': chain, 'argv': argv, 'Optional': Optional, 'list': list, 'str': str}, 1)
if __name__ == '__main__':
    sys.exit(main())

