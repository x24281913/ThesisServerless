from ._parser import parse, parser, parserinfo, ParserError
from ._parser import DEFAULTPARSER, DEFAULTTZPARSER
from ._parser import UnknownTimezoneWarning
from ._parser import __doc__
from .isoparser import isoparser, isoparse
__all__ = ['parse', 'parser', 'parserinfo', 'isoparse', 'isoparser', 'ParserError', 'UnknownTimezoneWarning']

def __deprecated_private_func(f):
    import custom_funtemplate
    return custom_funtemplate.rewrite_template('dateutil.parser.__init__.__deprecated_private_func', '__deprecated_private_func(f)', {'f': f}, 1)

def __deprecate_private_class(c):
    import custom_funtemplate
    return custom_funtemplate.rewrite_template('dateutil.parser.__init__.__deprecate_private_class', '__deprecate_private_class(c)', {'c': c}, 1)
from ._parser import _timelex, _resultbase
from ._parser import _tzparser, _parsetz
_timelex = __deprecate_private_class(_timelex)
_tzparser = __deprecate_private_class(_tzparser)
_resultbase = __deprecate_private_class(_resultbase)
_parsetz = __deprecated_private_func(_parsetz)

