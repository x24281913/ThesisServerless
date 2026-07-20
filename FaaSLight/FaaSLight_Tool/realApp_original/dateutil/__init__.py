import sys
try:
    from ._version import version as __version__
except ImportError:
    __version__ = 'unknown'
__all__ = ['easter', 'parser', 'relativedelta', 'rrule', 'tz', 'utils', 'zoneinfo']

def __getattr__(name):
    import custom_funtemplate
    return custom_funtemplate.rewrite_template('dateutil.__init__.__getattr__', '__getattr__(name)', {'__all__': __all__, '__name__': __name__, 'name': name}, 1)

def __dir__():
    return [x for x in globals() if x not in sys.modules] + __all__

