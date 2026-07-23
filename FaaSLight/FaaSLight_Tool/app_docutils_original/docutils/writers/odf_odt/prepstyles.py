"""
Adapt a word-processor-generated styles.odt for odtwriter use:

Drop page size specifications from styles.xml in STYLE_FILE.odt.
See https://docutils.sourceforge.io/docs/user/odt.html#page-size
"""

from __future__ import annotations
from xml.etree import ElementTree as ET
import sys
import zipfile
from tempfile import mkstemp
import shutil
import os
NAMESPACES = {'style': 'urn:oasis:names:tc:opendocument:xmlns:style:1.0', 'fo': 'urn:oasis:names:tc:opendocument:xmlns:xsl-fo-compatible:1.0'}

def prepstyle(filename) -> None:
    import custom_funtemplate
    custom_funtemplate.rewrite_template('docutils.writers.odf_odt.prepstyles.prepstyle', 'prepstyle(filename)', {'zipfile': zipfile, 'ET': ET, 'NAMESPACES': NAMESPACES, 'mkstemp': mkstemp, 'os': os, 'shutil': shutil, 'filename': filename}, 0)

def main() -> None:
    import custom_funtemplate
    custom_funtemplate.rewrite_template('docutils.writers.odf_odt.prepstyles.main', 'main()', {'sys': sys, '__doc__': __doc__, 'prepstyle': prepstyle}, 0)
if __name__ == '__main__':
    main()

