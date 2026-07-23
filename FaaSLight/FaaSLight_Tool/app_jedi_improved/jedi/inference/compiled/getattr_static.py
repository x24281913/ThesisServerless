"""
A static version of getattr.
This is a backport of the Python 3 code with a little bit of additional
information returned to enable Jedi to make decisions.
"""

import types
from jedi import debug
_sentinel = object()

def _check_instance(obj, attr):
    import custom_funtemplate
    return custom_funtemplate.rewrite_template('jedi.inference.compiled.getattr_static._check_instance', '_check_instance(obj, attr)', {'_sentinel': _sentinel, 'obj': obj, 'attr': attr}, 1)

def _check_class(klass, attr):
    import custom_funtemplate
    return custom_funtemplate.rewrite_template('jedi.inference.compiled.getattr_static._check_class', '_check_class(klass, attr)', {'_static_getmro': _static_getmro, '_shadowed_dict': _shadowed_dict, '_sentinel': _sentinel, 'klass': klass, 'attr': attr}, 1)

def _is_type(obj):
    import custom_funtemplate
    return custom_funtemplate.rewrite_template('jedi.inference.compiled.getattr_static._is_type', '_is_type(obj)', {'_static_getmro': _static_getmro, 'obj': obj}, 1)

def _shadowed_dict(klass):
    import custom_funtemplate
    return custom_funtemplate.rewrite_template('jedi.inference.compiled.getattr_static._shadowed_dict', '_shadowed_dict(klass)', {'_static_getmro': _static_getmro, 'types': types, '_sentinel': _sentinel, 'klass': klass}, 1)

def _static_getmro(klass):
    import custom_funtemplate
    custom_funtemplate.rewrite_template('jedi.inference.compiled.getattr_static._static_getmro', '_static_getmro(klass)', {'debug': debug, 'klass': klass}, 0)

def _safe_hasattr(obj, name):
    return _check_class(type(obj), name) is not _sentinel

def _safe_is_data_descriptor(obj):
    return (_safe_hasattr(obj, '__set__') or _safe_hasattr(obj, '__delete__'))

def getattr_static(obj, attr, default=_sentinel):
    """Retrieve attributes without triggering dynamic lookup via the
       descriptor protocol,  __getattr__ or __getattribute__.

       Note: this function may not be able to retrieve all attributes
       that getattr can fetch (like dynamically created attributes)
       and may find attributes that getattr can't (like descriptors
       that raise AttributeError). It can also return descriptor objects
       instead of instance members in some cases. See the
       documentation for details.

       Returns a tuple `(attr, is_get_descriptor)`. is_get_descripter means that
       the attribute is a descriptor that has a `__get__` attribute.
    """
    import custom_funtemplate
    return custom_funtemplate.rewrite_template('jedi.inference.compiled.getattr_static.getattr_static', 'getattr_static(obj, attr, default=_sentinel)', {'_is_type': _is_type, '_shadowed_dict': _shadowed_dict, 'types': types, '_check_instance': _check_instance, '_check_class': _check_class, '_safe_hasattr': _safe_hasattr, '_safe_is_data_descriptor': _safe_is_data_descriptor, '_static_getmro': _static_getmro, 'obj': obj, 'attr': attr, 'default': default, '_sentinel': _sentinel}, 2)

