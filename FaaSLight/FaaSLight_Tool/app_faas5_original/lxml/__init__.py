__version__ = '4.9.1'

def get_include():
    """
    Returns a list of header include paths (for lxml itself, libxml2
    and libxslt) needed to compile C code against lxml if it was built
    with statically linked libraries.
    """
    import custom_funtemplate
    return custom_funtemplate.rewrite_template('lxml.__init__.get_include', 'get_include()', {'__path__': __path__}, 1)

