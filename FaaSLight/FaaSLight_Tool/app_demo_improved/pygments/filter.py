"""
    pygments.filter
    ~~~~~~~~~~~~~~~

    Module that implements the default filter.

    :copyright: Copyright 2006-present by the Pygments team, see AUTHORS.
    :license: BSD, see LICENSE for details.
"""


def apply_filters(stream, filters, lexer=None):
    """
    Use this method to apply an iterable of filters to
    a stream. If lexer is given it's forwarded to the
    filter, otherwise the filter receives `None`.
    """
    import custom_funtemplate
    return custom_funtemplate.rewrite_template('pygments.filter.apply_filters', 'apply_filters(stream, filters, lexer=None)', {'stream': stream, 'filters': filters, 'lexer': lexer}, 1)

def simplefilter(f):
    """
    Decorator that converts a function into a filter::

        @simplefilter
        def lowercase(self, lexer, stream, options):
            for ttype, value in stream:
                yield ttype, value.lower()
    """
    return type(f.__name__, (FunctionFilter, ), {'__module__': getattr(f, '__module__'), '__doc__': f.__doc__, 'function': f})


class Filter:
    """
    Default filter. Subclass this class or use the `simplefilter`
    decorator to create own filters.
    """
    
    def __init__(self, **options):
        self.options = options
    
    def filter(self, lexer, stream):
        raise NotImplementedError()



class FunctionFilter(Filter):
    """
    Abstract class used by `simplefilter` to create simple
    function filters on the fly. The `simplefilter` decorator
    automatically creates subclasses of this class for
    functions passed to it.
    """
    function = None
    
    def __init__(self, **options):
        if not hasattr(self, 'function'):
            raise TypeError(f'{self.__class__.__name__!r} used without bound function')
        Filter.__init__(self, **options)
    
    def filter(self, lexer, stream):
        yield from self.function(lexer, stream, self.options)


