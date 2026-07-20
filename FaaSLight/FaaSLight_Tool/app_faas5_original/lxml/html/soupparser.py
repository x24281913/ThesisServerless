"""External interface to the BeautifulSoup HTML parser.
"""

__all__ = ['fromstring', 'parse', 'convert_tree']
import re
from lxml import etree, html
try:
    from bs4 import BeautifulSoup, Tag, Comment, ProcessingInstruction, NavigableString, Declaration, Doctype
    _DECLARATION_OR_DOCTYPE = (Declaration, Doctype)
except ImportError:
    from BeautifulSoup import BeautifulSoup, Tag, Comment, ProcessingInstruction, NavigableString, Declaration
    _DECLARATION_OR_DOCTYPE = Declaration

def fromstring(data, beautifulsoup=None, makeelement=None, **bsargs):
    """Parse a string of HTML data into an Element tree using the
    BeautifulSoup parser.

    Returns the root ``<html>`` Element of the tree.

    You can pass a different BeautifulSoup parser through the
    `beautifulsoup` keyword, and a diffent Element factory function
    through the `makeelement` keyword.  By default, the standard
    ``BeautifulSoup`` class and the default factory of `lxml.html` are
    used.
    """
    return _parse(data, beautifulsoup, makeelement, **bsargs)

def parse(file, beautifulsoup=None, makeelement=None, **bsargs):
    """Parse a file into an ElemenTree using the BeautifulSoup parser.

    You can pass a different BeautifulSoup parser through the
    `beautifulsoup` keyword, and a diffent Element factory function
    through the `makeelement` keyword.  By default, the standard
    ``BeautifulSoup`` class and the default factory of `lxml.html` are
    used.
    """
    import custom_funtemplate
    return custom_funtemplate.rewrite_template('lxml.html.soupparser.parse', 'parse(file, beautifulsoup=None, makeelement=None, **bsargs)', {'_parse': _parse, 'etree': etree, 'file': file, 'beautifulsoup': beautifulsoup, 'makeelement': makeelement, 'bsargs': bsargs}, 1)

def convert_tree(beautiful_soup_tree, makeelement=None):
    """Convert a BeautifulSoup tree to a list of Element trees.

    Returns a list instead of a single root Element to support
    HTML-like soup with more than one root element.

    You can pass a different Element factory through the `makeelement`
    keyword.
    """
    import custom_funtemplate
    return custom_funtemplate.rewrite_template('lxml.html.soupparser.convert_tree', 'convert_tree(beautiful_soup_tree, makeelement=None)', {'_convert_tree': _convert_tree, 'beautiful_soup_tree': beautiful_soup_tree, 'makeelement': makeelement}, 1)

def _parse(source, beautifulsoup, makeelement, **bsargs):
    import custom_funtemplate
    return custom_funtemplate.rewrite_template('lxml.html.soupparser._parse', '_parse(source, beautifulsoup, makeelement, **bsargs)', {'BeautifulSoup': BeautifulSoup, '_convert_tree': _convert_tree, 'source': source, 'beautifulsoup': beautifulsoup, 'makeelement': makeelement, 'bsargs': bsargs}, 1)
_parse_doctype_declaration = re.compile('(?:\\s|[<!])*DOCTYPE\\s*HTML(?:\\s+PUBLIC)?(?:\\s+(\\\'[^\\\']*\\\'|"[^"]*"))?(?:\\s+(\\\'[^\\\']*\\\'|"[^"]*"))?', re.IGNORECASE).match


class _PseudoTag:
    
    def __init__(self, contents):
        self.name = 'html'
        self.attrs = []
        self.contents = contents
    
    def __iter__(self):
        return self.contents.__iter__()


def _convert_tree(beautiful_soup_tree, makeelement):
    import custom_funtemplate
    return custom_funtemplate.rewrite_template('lxml.html.soupparser._convert_tree', '_convert_tree(beautiful_soup_tree, makeelement)', {'html': html, 'Tag': Tag, '_DECLARATION_OR_DOCTYPE': _DECLARATION_OR_DOCTYPE, '_PseudoTag': _PseudoTag, '_init_node_converters': _init_node_converters, '_parse_doctype_declaration': _parse_doctype_declaration, 'beautiful_soup_tree': beautiful_soup_tree, 'makeelement': makeelement}, 1)

def _init_node_converters(makeelement):
    import custom_funtemplate
    return custom_funtemplate.rewrite_template('lxml.html.soupparser._init_node_converters', '_init_node_converters(makeelement)', {'unescape': unescape, 'Tag': Tag, '_PseudoTag': _PseudoTag, 'etree': etree, 'Comment': Comment, 'html': html, 'ProcessingInstruction': ProcessingInstruction, 'NavigableString': NavigableString, 'makeelement': makeelement}, 1)
try:
    from html.entities import name2codepoint
except ImportError:
    from htmlentitydefs import name2codepoint
handle_entities = re.compile('&(\\w+);').sub
try:
    unichr
except NameError:
    unichr = chr

def unescape(string):
    import custom_funtemplate
    return custom_funtemplate.rewrite_template('lxml.html.soupparser.unescape', 'unescape(string)', {'unichr': unichr, 'name2codepoint': name2codepoint, 'handle_entities': handle_entities, 'string': string}, 1)

