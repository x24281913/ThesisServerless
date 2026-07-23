"""
Used only for REPL Completion.
"""

import inspect
from pathlib import Path
from jedi.parser_utils import get_cached_code_lines
from jedi import settings
from jedi.cache import memoize_method
from jedi.inference import compiled
from jedi.file_io import FileIO
from jedi.inference.names import NameWrapper
from jedi.inference.base_value import ValueSet, ValueWrapper, NO_VALUES
from jedi.inference.value import ModuleValue
from jedi.inference.cache import inference_state_function_cache, inference_state_method_cache
from jedi.inference.compiled.access import ALLOWED_GETITEM_TYPES, get_api_type
from jedi.inference.gradual.conversion import to_stub
from jedi.inference.context import CompiledContext, CompiledModuleContext, TreeContextMixin
_sentinel = object()


class MixedObject(ValueWrapper):
    """
    A ``MixedObject`` is used in two ways:

    1. It uses the default logic of ``parser.python.tree`` objects,
    2. except for getattr calls and signatures. The names dicts are generated
       in a fashion like ``CompiledValue``.

    This combined logic makes it possible to provide more powerful REPL
    completion. It allows side effects that are not noticable with the default
    parser structure to still be completable.

    The biggest difference from CompiledValue to MixedObject is that we are
    generally dealing with Python code and not with C code. This will generate
    fewer special cases, because we in Python you don't have the same freedoms
    to modify the runtime.
    """
    
    def __init__(self, compiled_value, tree_value):
        super().__init__(tree_value)
        self.compiled_value = compiled_value
        self.access_handle = compiled_value.access_handle
    
    def get_filters(self, *args, **kwargs):
        yield MixedObjectFilter(self.inference_state, self.compiled_value, self._wrapped_value)
    
    def get_signatures(self):
        return self.compiled_value.get_signatures()
    
    @inference_state_method_cache(default=NO_VALUES)
    def py__call__(self, arguments):
        values = to_stub(self._wrapped_value)
        if not values:
            values = self._wrapped_value
        return values.py__call__(arguments)
    
    def get_safe_value(self, default=_sentinel):
        if default is _sentinel:
            return self.compiled_value.get_safe_value()
        else:
            return self.compiled_value.get_safe_value(default)
    
    @property
    def array_type(self):
        return self.compiled_value.array_type
    
    def get_key_values(self):
        return self.compiled_value.get_key_values()
    
    def py__simple_getitem__(self, index):
        python_object = self.compiled_value.access_handle.access._obj
        if type(python_object) in ALLOWED_GETITEM_TYPES:
            return self.compiled_value.py__simple_getitem__(index)
        return self._wrapped_value.py__simple_getitem__(index)
    
    def negate(self):
        return self.compiled_value.negate()
    
    def _as_context(self):
        if self.parent_context is None:
            return MixedModuleContext(self)
        return MixedContext(self)
    
    def __repr__(self):
        return '<%s: %s; %s>' % (type(self).__name__, self.access_handle.get_repr(), self._wrapped_value)



class MixedContext(CompiledContext, TreeContextMixin):
    
    @property
    def compiled_value(self):
        return self._value.compiled_value



class MixedModuleContext(CompiledModuleContext, MixedContext):
    pass



class MixedName(NameWrapper):
    """
    The ``CompiledName._compiled_value`` is our MixedObject.
    """
    
    def __init__(self, wrapped_name, parent_tree_value):
        super().__init__(wrapped_name)
        self._parent_tree_value = parent_tree_value
    
    @property
    def start_pos(self):
        values = list(self.infer())
        if not values:
            return (0, 0)
        return values[0].name.start_pos
    
    @memoize_method
    def infer(self):
        compiled_value = self._wrapped_name.infer_compiled_value()
        tree_value = self._parent_tree_value
        if (tree_value.is_instance() or tree_value.is_class()):
            tree_values = tree_value.py__getattribute__(self.string_name)
            if compiled_value.is_function():
                return ValueSet({MixedObject(compiled_value, v) for v in tree_values})
        module_context = tree_value.get_root_context()
        return _create(self._inference_state, compiled_value, module_context)



class MixedObjectFilter(compiled.CompiledValueFilter):
    
    def __init__(self, inference_state, compiled_value, tree_value):
        super().__init__(inference_state, compiled_value)
        self._tree_value = tree_value
    
    def _create_name(self, *args, **kwargs):
        return MixedName(super()._create_name(*args, **kwargs), self._tree_value)


@inference_state_function_cache()
def _load_module(inference_state, path):
    return inference_state.parse(path=path, cache=True, diff_cache=settings.fast_parser, cache_path=settings.cache_directory).get_root_node()

def _get_object_to_check(python_object):
    """Check if inspect.getfile has a chance to find the source."""
    import custom_funtemplate
    return custom_funtemplate.rewrite_template('jedi.inference.compiled.mixed._get_object_to_check', '_get_object_to_check(python_object)', {'inspect': inspect, 'python_object': python_object}, 1)

def _find_syntax_node_name(inference_state, python_object):
    import custom_funtemplate
    return custom_funtemplate.rewrite_template('jedi.inference.compiled.mixed._find_syntax_node_name', '_find_syntax_node_name(inference_state, python_object)', {'_get_object_to_check': _get_object_to_check, 'inspect': inspect, 'Path': Path, 'FileIO': FileIO, '_load_module': _load_module, 'get_cached_code_lines': get_cached_code_lines, 'get_api_type': get_api_type, 'inference_state': inference_state, 'python_object': python_object}, 1)

@inference_state_function_cache()
def _create(inference_state, compiled_value, module_context):
    import custom_funtemplate
    return custom_funtemplate.rewrite_template('jedi.inference.compiled.mixed._create', '_create(inference_state, compiled_value, module_context)', {'_find_syntax_node_name': _find_syntax_node_name, 'ValueSet': ValueSet, 'to_stub': to_stub, 'ModuleValue': ModuleValue, 'MixedObject': MixedObject, 'inference_state_function_cache': inference_state_function_cache, 'inference_state': inference_state, 'compiled_value': compiled_value, 'module_context': module_context}, 1)

