"""
An interface to html5lib that mimics the lxml.html interface.
"""

import sys
import string
from html5lib import HTMLParser as _HTMLParser
from html5lib.treebuilders.etree_lxml import TreeBuilder
from lxml import etree
from lxml.html import Element, XHTML_NAMESPACE, _contains_block_level_tag
try:
    _strings = basestring
except NameError:
    _strings = (bytes, str)
try:
    from urllib2 import urlopen
except ImportError:
    from urllib.request import urlopen
try:
    from urlparse import urlparse
except ImportError:
    from urllib.parse import urlparse


class HTMLParser(_HTMLParser):
    """An html5lib HTML parser with lxml as tree."""
    
    def __init__(self, strict=False, **kwargs):
        _HTMLParser.__init__(self, strict=strict, tree=TreeBuilder, **kwargs)

try:
    from html5lib import XHTMLParser as _XHTMLParser
except ImportError:
    pass
else:
    
    
    class XHTMLParser(_XHTMLParser):
        """An html5lib XHTML Parser with lxml as tree."""
        
        def __init__(self, strict=False, **kwargs):
            _XHTMLParser.__init__(self, strict=strict, tree=TreeBuilder, **kwargs)
    
    xhtml_parser = XHTMLParser()

def _find_tag(tree, tag):
    import custom_funtemplate
    return custom_funtemplate.rewrite_template('lxml.html.html5parser._find_tag', '_find_tag(tree, tag)', {'XHTML_NAMESPACE': XHTML_NAMESPACE, 'tree': tree, 'tag': tag}, 1)

def document_fromstring(html, guess_charset=None, parser=None):
    """
    Parse a whole document into a string.

    If `guess_charset` is true, or if the input is not Unicode but a
    byte string, the `chardet` library will perform charset guessing
    on the string.
    """
    import custom_funtemplate
    return custom_funtemplate.rewrite_template('lxml.html.html5parser.document_fromstring', 'document_fromstring(html, guess_charset=None, parser=None)', {'_strings': _strings, 'html_parser': html_parser, 'html': html, 'guess_charset': guess_charset, 'parser': parser}, 1)

def fragments_fromstring(html, no_leading_text=False, guess_charset=None, parser=None):
    """Parses several HTML elements, returning a list of elements.

    The first item in the list may be a string.  If no_leading_text is true,
    then it will be an error if there is leading text, and it will always be
    a list of only elements.

    If `guess_charset` is true, the `chardet` library will perform charset
    guessing on the string.
    """
    import custom_funtemplate
    return custom_funtemplate.rewrite_template('lxml.html.html5parser.fragments_fromstring', 'fragments_fromstring(html, no_leading_text=False, guess_charset=None, parser=None)', {'_strings': _strings, 'html_parser': html_parser, 'etree': etree, 'html': html, 'no_leading_text': no_leading_text, 'guess_charset': guess_charset, 'parser': parser}, 1)

def fragment_fromstring(html, create_parent=False, guess_charset=None, parser=None):
    """Parses a single HTML element; it is an error if there is more than
    one element, or if anything but whitespace precedes or follows the
    element.

    If 'create_parent' is true (or is a tag name) then a parent node
    will be created to encapsulate the HTML in a single element.  In
    this case, leading or trailing text is allowed.

    If `guess_charset` is true, the `chardet` library will perform charset
    guessing on the string.
    """
    import custom_funtemplate
    return custom_funtemplate.rewrite_template('lxml.html.html5parser.fragment_fromstring', 'fragment_fromstring(html, create_parent=False, guess_charset=None, parser=None)', {'_strings': _strings, 'fragments_fromstring': fragments_fromstring, 'Element': Element, 'etree': etree, 'html': html, 'create_parent': create_parent, 'guess_charset': guess_charset, 'parser': parser}, 1)

def fromstring(html, guess_charset=None, parser=None):
    """Parse the html, returning a single element/document.

    This tries to minimally parse the chunk of text, without knowing if it
    is a fragment or a document.

    'base_url' will set the document's base_url attribute (and the tree's
    docinfo.URL)

    If `guess_charset` is true, or if the input is not Unicode but a
    byte string, the `chardet` library will perform charset guessing
    on the string.
    """
    import custom_funtemplate
    return custom_funtemplate.rewrite_template('lxml.html.html5parser.fromstring', 'fromstring(html, guess_charset=None, parser=None)', {'_strings': _strings, 'document_fromstring': document_fromstring, '_find_tag': _find_tag, '_contains_block_level_tag': _contains_block_level_tag, 'html': html, 'guess_charset': guess_charset, 'parser': parser}, 1)

def parse(filename_url_or_file, guess_charset=None, parser=None):
    """Parse a filename, URL, or file-like object into an HTML document
    tree.  Note: this returns a tree, not an element.  Use
    ``parse(...).getroot()`` to get the document root.

    If ``guess_charset`` is true, the ``useChardet`` option is passed into
    html5lib to enable character detection.  This option is on by default
    when parsing from URLs, off by default when parsing from file(-like)
    objects (which tend to return Unicode more often than not), and on by
    default when parsing from a file path (which is read in binary mode).
    """
    import custom_funtemplate
    return custom_funtemplate.rewrite_template('lxml.html.html5parser.parse', 'parse(filename_url_or_file, guess_charset=None, parser=None)', {'html_parser': html_parser, '_strings': _strings, '_looks_like_url': _looks_like_url, 'urlopen': urlopen, 'filename_url_or_file': filename_url_or_file, 'guess_charset': guess_charset, 'parser': parser}, 1)

def _looks_like_url(str):
    import custom_funtemplate
    return custom_funtemplate.rewrite_template('lxml.html.html5parser._looks_like_url', '_looks_like_url(str)', {'urlparse': urlparse, 'sys': sys, 'string': string, 'str': str}, 1)
html_parser = HTMLParser()

