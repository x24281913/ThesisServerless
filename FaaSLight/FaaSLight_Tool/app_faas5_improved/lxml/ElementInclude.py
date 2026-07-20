"""
Limited XInclude support for the ElementTree package.

While lxml.etree has full support for XInclude (see
`etree.ElementTree.xinclude()`), this module provides a simpler, pure
Python, ElementTree compatible implementation that supports a simple
form of custom URL resolvers.
"""

from lxml import etree
try:
    from urlparse import urljoin
    from urllib2 import urlopen
except ImportError:
    from urllib.parse import urljoin
    from urllib.request import urlopen
XINCLUDE = '{http://www.w3.org/2001/XInclude}'
XINCLUDE_INCLUDE = XINCLUDE + 'include'
XINCLUDE_FALLBACK = XINCLUDE + 'fallback'
XINCLUDE_ITER_TAG = XINCLUDE + '*'
DEFAULT_MAX_INCLUSION_DEPTH = 6


class FatalIncludeError(etree.LxmlSyntaxError):
    pass



class LimitedRecursiveIncludeError(FatalIncludeError):
    pass


def default_loader(href, parse, encoding=None):
    import custom_funtemplate
    return custom_funtemplate.rewrite_template('lxml.ElementInclude.default_loader', 'default_loader(href, parse, encoding=None)', {'etree': etree, 'href': href, 'parse': parse, 'encoding': encoding}, 1)

def _lxml_default_loader(href, parse, encoding=None, parser=None):
    import custom_funtemplate
    return custom_funtemplate.rewrite_template('lxml.ElementInclude._lxml_default_loader', '_lxml_default_loader(href, parse, encoding=None, parser=None)', {'etree': etree, 'urlopen': urlopen, 'href': href, 'parse': parse, 'encoding': encoding, 'parser': parser}, 1)

def _wrap_et_loader(loader):
    import custom_funtemplate
    return custom_funtemplate.rewrite_template('lxml.ElementInclude._wrap_et_loader', '_wrap_et_loader(loader)', {'loader': loader}, 1)

def include(elem, loader=None, base_url=None, max_depth=DEFAULT_MAX_INCLUSION_DEPTH):
    import custom_funtemplate
    custom_funtemplate.rewrite_template('lxml.ElementInclude.include', 'include(elem, loader=None, base_url=None, max_depth=DEFAULT_MAX_INCLUSION_DEPTH)', {'_include': _include, 'elem': elem, 'loader': loader, 'base_url': base_url, 'max_depth': max_depth, 'DEFAULT_MAX_INCLUSION_DEPTH': DEFAULT_MAX_INCLUSION_DEPTH}, 0)

def _include(elem, loader=None, base_url=None, max_depth=DEFAULT_MAX_INCLUSION_DEPTH, _parent_hrefs=None):
    import custom_funtemplate
    return custom_funtemplate.rewrite_template('lxml.ElementInclude._include', '_include(elem, loader=None, base_url=None, max_depth=DEFAULT_MAX_INCLUSION_DEPTH, _parent_hrefs=None)', {'_wrap_et_loader': _wrap_et_loader, '_lxml_default_loader': _lxml_default_loader, 'XINCLUDE_ITER_TAG': XINCLUDE_ITER_TAG, 'XINCLUDE_INCLUDE': XINCLUDE_INCLUDE, 'urljoin': urljoin, 'FatalIncludeError': FatalIncludeError, 'LimitedRecursiveIncludeError': LimitedRecursiveIncludeError, '_include': _include, 'XINCLUDE_FALLBACK': XINCLUDE_FALLBACK, 'elem': elem, 'loader': loader, 'base_url': base_url, 'max_depth': max_depth, '_parent_hrefs': _parent_hrefs, 'DEFAULT_MAX_INCLUSION_DEPTH': DEFAULT_MAX_INCLUSION_DEPTH}, 1)

