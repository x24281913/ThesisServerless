"""Generic command line interface for the `docutils` package.

See also
https://docs.python.org/3/library/__main__.html#main-py-in-python-packages
"""

from __future__ import annotations
__docformat__ = 'reStructuredText'
import argparse
import locale
import sys
import docutils
from docutils.core import Publisher, publish_cmdline, default_description


class CliSettingsSpec(docutils.SettingsSpec):
    """Runtime settings & command-line options for the generic CLI.

    Configurable reader, parser, and writer components.

    The "--writer" default will change to 'html' in Docutils 2.0
    when 'html' becomes an alias for the current value 'html5'.
    """
    settings_spec = ('Docutils Application Options', 'Reader, writer, and parser settings influence the available options.   Example: use `--help --writer=latex` to see LaTeX writer options. ', (('Reader name (currently: "%default").', ['--reader'], {'default': 'standalone', 'metavar': '<reader>'}), ('Parser name (currently: "%default").', ['--parser'], {'default': 'rst', 'metavar': '<parser>'}), ('Writer name (currently: "%default").', ['--writer'], {'default': 'html5', 'metavar': '<writer>'})))
    config_section = 'docutils application'
    config_section_dependencies = ('docutils-cli application', 'applications')


def main() -> None:
    """Generic command line interface for the Docutils Publisher.
    """
    import custom_funtemplate
    custom_funtemplate.rewrite_template('docutils.__main__.main', 'main()', {'locale': locale, 'sys': sys, 'default_description': default_description, 'Publisher': Publisher, 'CliSettingsSpec': CliSettingsSpec, 'argparse': argparse, 'publish_cmdline': publish_cmdline}, 0)
if __name__ == '__main__':
    if sys.argv[0].endswith('__main__.py'):
        sys.argv[0] = '%s -m docutils' % sys.executable
    main()

