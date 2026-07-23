"""
Implementations of standard library functions, because it's not possible to
understand them with Jedi.

To add a new implementation, create a function and add it to the
``_implemented`` dict at the bottom of this module.

Note that this module exists only to implement very specific functionality in
the standard library. The usual way to understand the standard library is the
compiled module that returns the types for C-builtins.
"""

import parso
import os
from inspect import Parameter
from jedi import debug
from jedi.inference.utils import safe_property
from jedi.inference.helpers import get_str_or_none
from jedi.inference.arguments import iterate_argument_clinic, ParamIssue, repack_with_argument_clinic, AbstractArguments, TreeArgumentsWrapper
from jedi.inference import analysis
from jedi.inference import compiled
from jedi.inference.value.instance import AnonymousMethodExecutionContext, MethodExecutionContext
from jedi.inference.base_value import ContextualizedNode, NO_VALUES, ValueSet, ValueWrapper, LazyValueWrapper
from jedi.inference.value import ClassValue, ModuleValue
from jedi.inference.value.klass import ClassMixin
from jedi.inference.value.function import FunctionMixin
from jedi.inference.value import iterable
from jedi.inference.lazy_value import LazyTreeValue, LazyKnownValue, LazyKnownValues
from jedi.inference.names import ValueName, BaseTreeParamName
from jedi.inference.filters import AttributeOverwrite, publish_method, ParserTreeFilter, DictFilter
from jedi.inference.signature import AbstractSignature, SignatureWrapper
_NAMEDTUPLE_CLASS_TEMPLATE = "_property = property\n_tuple = tuple\nfrom operator import itemgetter as _itemgetter\nfrom collections import OrderedDict\n\nclass {typename}(tuple):\n    __slots__ = ()\n\n    _fields = {field_names!r}\n\n    def __new__(_cls, {arg_list}):\n        'Create new instance of {typename}({arg_list})'\n        return _tuple.__new__(_cls, ({arg_list}))\n\n    @classmethod\n    def _make(cls, iterable, new=tuple.__new__, len=len):\n        'Make a new {typename} object from a sequence or iterable'\n        result = new(cls, iterable)\n        if len(result) != {num_fields:d}:\n            raise TypeError('Expected {num_fields:d} arguments, got %d' % len(result))\n        return result\n\n    def _replace(_self, **kwds):\n        'Return a new {typename} object replacing specified fields with new values'\n        result = _self._make(map(kwds.pop, {field_names!r}, _self))\n        if kwds:\n            raise ValueError('Got unexpected field names: %r' % list(kwds))\n        return result\n\n    def __repr__(self):\n        'Return a nicely formatted representation string'\n        return self.__class__.__name__ + '({repr_fmt})' % self\n\n    def _asdict(self):\n        'Return a new OrderedDict which maps field names to their values.'\n        return OrderedDict(zip(self._fields, self))\n\n    def __getnewargs__(self):\n        'Return self as a plain tuple.  Used by copy and pickle.'\n        return tuple(self)\n\n    # These methods were added by Jedi.\n    # __new__ doesn't really work with Jedi. So adding this to nametuples seems\n    # like the easiest way.\n    def __init__(self, {arg_list}):\n        'A helper function for namedtuple.'\n        self.__iterable = ({arg_list})\n\n    def __iter__(self):\n        for i in self.__iterable:\n            yield i\n\n    def __getitem__(self, y):\n        return self.__iterable[y]\n\n{field_defs}\n"
_NAMEDTUPLE_FIELD_TEMPLATE = "    {name} = _property(_itemgetter({index:d}), doc='Alias for field number {index:d}')\n"

def execute(callback):
    import custom_funtemplate
    return custom_funtemplate.rewrite_template('jedi.plugins.stdlib.execute', 'execute(callback)', {'_implemented': _implemented, 'callback': callback}, 1)

def _follow_param(inference_state, arguments, index):
    import custom_funtemplate
    return custom_funtemplate.rewrite_template('jedi.plugins.stdlib._follow_param', '_follow_param(inference_state, arguments, index)', {'NO_VALUES': NO_VALUES, 'inference_state': inference_state, 'arguments': arguments, 'index': index}, 1)

def argument_clinic(clinic_string, want_value=False, want_context=False, want_arguments=False, want_inference_state=False, want_callback=False):
    """
    Works like Argument Clinic (PEP 436), to validate function params.
    """
    
    def f(func):
        
        def wrapper(value, arguments, callback):
            import custom_funtemplate
            return custom_funtemplate.rewrite_template('jedi.plugins.stdlib.argument_clinic.f.wrapper', 'wrapper(value, arguments, callback)', {'iterate_argument_clinic': iterate_argument_clinic, 'clinic_string': clinic_string, 'ParamIssue': ParamIssue, 'NO_VALUES': NO_VALUES, 'debug': debug, 'want_context': want_context, 'want_value': want_value, 'want_inference_state': want_inference_state, 'want_arguments': want_arguments, 'want_callback': want_callback, 'func': func, 'value': value, 'arguments': arguments, 'callback': callback}, 1)
        return wrapper
    return f

@argument_clinic('iterator[, default], /', want_inference_state=True)
def builtins_next(iterators, defaults, inference_state):
    return defaults | iterators.py__getattribute__('__next__').execute_with_values()

@argument_clinic('iterator[, default], /')
def builtins_iter(iterators_or_callables, defaults):
    return iterators_or_callables.py__getattribute__('__iter__').execute_with_values()

@argument_clinic('object, name[, default], /')
def builtins_getattr(objects, names, defaults=None):
    import custom_funtemplate
    return custom_funtemplate.rewrite_template('jedi.plugins.stdlib.builtins_getattr', 'builtins_getattr(objects, names, defaults=None)', {'get_str_or_none': get_str_or_none, 'debug': debug, 'NO_VALUES': NO_VALUES, 'argument_clinic': argument_clinic, 'objects': objects, 'names': names, 'defaults': defaults}, 1)

@argument_clinic('object[, bases, dict], /')
def builtins_type(objects, bases, dicts):
    import custom_funtemplate
    return custom_funtemplate.rewrite_template('jedi.plugins.stdlib.builtins_type', 'builtins_type(objects, bases, dicts)', {'NO_VALUES': NO_VALUES, 'argument_clinic': argument_clinic, 'objects': objects, 'bases': bases, 'dicts': dicts}, 1)


class SuperInstance(LazyValueWrapper):
    """To be used like the object ``super`` returns."""
    
    def __init__(self, inference_state, instance):
        self.inference_state = inference_state
        self._instance = instance
    
    def _get_bases(self):
        return self._instance.py__class__().py__bases__()
    
    def _get_wrapped_value(self):
        objs = self._get_bases()[0].infer().execute_with_values()
        if not objs:
            return self._instance
        return next(iter(objs))
    
    def get_filters(self, origin_scope=None):
        for b in self._get_bases():
            for value in b.infer().execute_with_values():
                for f in value.get_filters():
                    yield f


@argument_clinic('[type[, value]], /', want_context=True)
def builtins_super(types, objects, context):
    import custom_funtemplate
    return custom_funtemplate.rewrite_template('jedi.plugins.stdlib.builtins_super', 'builtins_super(types, objects, context)', {'AnonymousMethodExecutionContext': AnonymousMethodExecutionContext, 'MethodExecutionContext': MethodExecutionContext, 'NO_VALUES': NO_VALUES, 'ValueSet': ValueSet, 'SuperInstance': SuperInstance, 'argument_clinic': argument_clinic, 'types': types, 'objects': objects, 'context': context}, 1)


class ReversedObject(AttributeOverwrite):
    
    def __init__(self, reversed_obj, iter_list):
        super().__init__(reversed_obj)
        self._iter_list = iter_list
    
    def py__iter__(self, contextualized_node=None):
        return self._iter_list
    
    @publish_method('__next__')
    def _next(self, arguments):
        return ValueSet.from_sets((lazy_value.infer() for lazy_value in self._iter_list))


@argument_clinic('sequence, /', want_value=True, want_arguments=True)
def builtins_reversed(sequences, value, arguments):
    import custom_funtemplate
    return custom_funtemplate.rewrite_template('jedi.plugins.stdlib.builtins_reversed', 'builtins_reversed(sequences, value, arguments)', {'LazyTreeValue': LazyTreeValue, 'ContextualizedNode': ContextualizedNode, 'ValueSet': ValueSet, 'ReversedObject': ReversedObject, 'argument_clinic': argument_clinic, 'sequences': sequences, 'value': value, 'arguments': arguments}, 1)

@argument_clinic('value, type, /', want_arguments=True, want_inference_state=True)
def builtins_isinstance(objects, types, arguments, inference_state):
    import custom_funtemplate
    return custom_funtemplate.rewrite_template('jedi.plugins.stdlib.builtins_isinstance', 'builtins_isinstance(objects, types, arguments, inference_state)', {'ValueSet': ValueSet, 'LazyTreeValue': LazyTreeValue, 'analysis': analysis, 'compiled': compiled, 'argument_clinic': argument_clinic, 'objects': objects, 'types': types, 'arguments': arguments, 'inference_state': inference_state}, 1)


class StaticMethodObject(ValueWrapper):
    
    def py__get__(self, instance, class_value):
        return ValueSet([self._wrapped_value])


@argument_clinic('sequence, /')
def builtins_staticmethod(functions):
    return ValueSet((StaticMethodObject(f) for f in functions))


class ClassMethodObject(ValueWrapper):
    
    def __init__(self, class_method_obj, function):
        super().__init__(class_method_obj)
        self._function = function
    
    def py__get__(self, instance, class_value):
        return ValueSet([ClassMethodGet(__get__, class_value, self._function) for __get__ in self._wrapped_value.py__getattribute__('__get__')])



class ClassMethodGet(ValueWrapper):
    
    def __init__(self, get_method, klass, function):
        super().__init__(get_method)
        self._class = klass
        self._function = function
    
    def get_signatures(self):
        return [sig.bind(self._function) for sig in self._function.get_signatures()]
    
    def py__call__(self, arguments):
        return self._function.execute(ClassMethodArguments(self._class, arguments))



class ClassMethodArguments(TreeArgumentsWrapper):
    
    def __init__(self, klass, arguments):
        super().__init__(arguments)
        self._class = klass
    
    def unpack(self, func=None):
        yield (None, LazyKnownValue(self._class))
        for values in self._wrapped_arguments.unpack(func):
            yield values


@argument_clinic('sequence, /', want_value=True, want_arguments=True)
def builtins_classmethod(functions, value, arguments):
    return ValueSet((ClassMethodObject(class_method_object, function) for class_method_object in value.py__call__(arguments=arguments) for function in functions))


class PropertyObject(AttributeOverwrite, ValueWrapper):
    api_type = 'property'
    
    def __init__(self, property_obj, function):
        super().__init__(property_obj)
        self._function = function
    
    def py__get__(self, instance, class_value):
        if instance is None:
            return ValueSet([self])
        return self._function.execute_with_values(instance)
    
    @publish_method('deleter')
    @publish_method('getter')
    @publish_method('setter')
    def _return_self(self, arguments):
        return ValueSet({self})


@argument_clinic('func, /', want_callback=True)
def builtins_property(functions, callback):
    return ValueSet((PropertyObject(property_value, function) for property_value in callback() for function in functions))

def collections_namedtuple(value, arguments, callback):
    """
    Implementation of the namedtuple function.

    This has to be done by processing the namedtuple class template and
    inferring the result.

    """
    import custom_funtemplate
    return custom_funtemplate.rewrite_template('jedi.plugins.stdlib.collections_namedtuple', 'collections_namedtuple(value, arguments, callback)', {'_follow_param': _follow_param, 'get_str_or_none': get_str_or_none, 'NO_VALUES': NO_VALUES, 'iterable': iterable, '_NAMEDTUPLE_CLASS_TEMPLATE': _NAMEDTUPLE_CLASS_TEMPLATE, '_NAMEDTUPLE_FIELD_TEMPLATE': _NAMEDTUPLE_FIELD_TEMPLATE, 'ModuleValue': ModuleValue, 'parso': parso, 'ValueSet': ValueSet, 'ClassValue': ClassValue, 'value': value, 'arguments': arguments, 'callback': callback}, 1)


class PartialObject(ValueWrapper):
    
    def __init__(self, actual_value, arguments, instance=None):
        super().__init__(actual_value)
        self._arguments = arguments
        self._instance = instance
    
    def _get_functions(self, unpacked_arguments):
        (key, lazy_value) = next(unpacked_arguments, (None, None))
        if (key is not None or lazy_value is None):
            debug.warning('Partial should have a proper function %s', self._arguments)
            return None
        return lazy_value.infer()
    
    def get_signatures(self):
        unpacked_arguments = self._arguments.unpack()
        funcs = self._get_functions(unpacked_arguments)
        if funcs is None:
            return []
        arg_count = 0
        if self._instance is not None:
            arg_count = 1
        keys = set()
        for (key, _) in unpacked_arguments:
            if key is None:
                arg_count += 1
            else:
                keys.add(key)
        return [PartialSignature(s, arg_count, keys) for s in funcs.get_signatures()]
    
    def py__call__(self, arguments):
        funcs = self._get_functions(self._arguments.unpack())
        if funcs is None:
            return NO_VALUES
        return funcs.execute(MergedPartialArguments(self._arguments, arguments, self._instance))
    
    def py__doc__(self):
        """
        In CPython partial does not replace the docstring. However we are still
        imitating it here, because we want this docstring to be worth something
        for the user.
        """
        callables = self._get_functions(self._arguments.unpack())
        if callables is None:
            return ''
        for callable_ in callables:
            return callable_.py__doc__()
        return ''
    
    def py__get__(self, instance, class_value):
        return ValueSet([self])



class PartialMethodObject(PartialObject):
    
    def py__get__(self, instance, class_value):
        if instance is None:
            return ValueSet([self])
        return ValueSet([PartialObject(self._wrapped_value, self._arguments, instance)])



class PartialSignature(SignatureWrapper):
    
    def __init__(self, wrapped_signature, skipped_arg_count, skipped_arg_set):
        super().__init__(wrapped_signature)
        self._skipped_arg_count = skipped_arg_count
        self._skipped_arg_set = skipped_arg_set
    
    def get_param_names(self, resolve_stars=False):
        names = self._wrapped_signature.get_param_names()[self._skipped_arg_count:]
        return [n for n in names if n.string_name not in self._skipped_arg_set]



class MergedPartialArguments(AbstractArguments):
    
    def __init__(self, partial_arguments, call_arguments, instance=None):
        self._partial_arguments = partial_arguments
        self._call_arguments = call_arguments
        self._instance = instance
    
    def unpack(self, funcdef=None):
        unpacked = self._partial_arguments.unpack(funcdef)
        next(unpacked, None)
        if self._instance is not None:
            yield (None, LazyKnownValue(self._instance))
        for key_lazy_value in unpacked:
            yield key_lazy_value
        for key_lazy_value in self._call_arguments.unpack(funcdef):
            yield key_lazy_value


def functools_partial(value, arguments, callback):
    return ValueSet((PartialObject(instance, arguments) for instance in value.py__call__(arguments)))

def functools_partialmethod(value, arguments, callback):
    return ValueSet((PartialMethodObject(instance, arguments) for instance in value.py__call__(arguments)))

@argument_clinic('first, /')
def _return_first_param(firsts):
    return firsts

@argument_clinic('seq')
def _random_choice(sequences):
    return ValueSet.from_sets((lazy_value.infer() for sequence in sequences for lazy_value in sequence.py__iter__()))

def _dataclass(value, arguments, callback):
    import custom_funtemplate
    return custom_funtemplate.rewrite_template('jedi.plugins.stdlib._dataclass', '_dataclass(value, arguments, callback)', {'_follow_param': _follow_param, 'ValueSet': ValueSet, 'DataclassWrapper': DataclassWrapper, 'NO_VALUES': NO_VALUES, 'value': value, 'arguments': arguments, 'callback': callback}, 1)


class DataclassWrapper(ValueWrapper, ClassMixin):
    
    def get_signatures(self):
        param_names = []
        for cls in reversed(list(self.py__mro__())):
            if isinstance(cls, DataclassWrapper):
                filter_ = cls.as_context().get_global_filter()
                for name in sorted(filter_.values(), key=lambda name: name.start_pos):
                    d = name.tree_name.get_definition()
                    annassign = d.children[1]
                    if (d.type == 'expr_stmt' and annassign.type == 'annassign'):
                        if len(annassign.children) < 4:
                            default = None
                        else:
                            default = annassign.children[3]
                        param_names.append(DataclassParamName(parent_context=cls.parent_context, tree_name=name.tree_name, annotation_node=annassign.children[1], default_node=default))
        return [DataclassSignature(cls, param_names)]



class DataclassSignature(AbstractSignature):
    
    def __init__(self, value, param_names):
        super().__init__(value)
        self._param_names = param_names
    
    def get_param_names(self, resolve_stars=False):
        return self._param_names



class DataclassParamName(BaseTreeParamName):
    
    def __init__(self, parent_context, tree_name, annotation_node, default_node):
        super().__init__(parent_context, tree_name)
        self.annotation_node = annotation_node
        self.default_node = default_node
    
    def get_kind(self):
        return Parameter.POSITIONAL_OR_KEYWORD
    
    def infer(self):
        if self.annotation_node is None:
            return NO_VALUES
        else:
            return self.parent_context.infer_node(self.annotation_node)



class ItemGetterCallable(ValueWrapper):
    
    def __init__(self, instance, args_value_set):
        super().__init__(instance)
        self._args_value_set = args_value_set
    
    @repack_with_argument_clinic('item, /')
    def py__call__(self, item_value_set):
        value_set = NO_VALUES
        for args_value in self._args_value_set:
            lazy_values = list(args_value.py__iter__())
            if len(lazy_values) == 1:
                value_set |= item_value_set.get_item(lazy_values[0].infer(), None)
            else:
                value_set |= ValueSet([iterable.FakeList(self._wrapped_value.inference_state, [LazyKnownValues(item_value_set.get_item(lazy_value.infer(), None)) for lazy_value in lazy_values])])
        return value_set


@argument_clinic('func, /')
def _functools_wraps(funcs):
    return ValueSet((WrapsCallable(func) for func in funcs))


class WrapsCallable(ValueWrapper):
    
    @repack_with_argument_clinic('func, /')
    def py__call__(self, funcs):
        return ValueSet({Wrapped(func, self._wrapped_value) for func in funcs})



class Wrapped(ValueWrapper, FunctionMixin):
    
    def __init__(self, func, original_function):
        super().__init__(func)
        self._original_function = original_function
    
    @property
    def name(self):
        return self._original_function.name
    
    def get_signature_functions(self):
        return [self]


@argument_clinic('*args, /', want_value=True, want_arguments=True)
def _operator_itemgetter(args_value_set, value, arguments):
    return ValueSet([ItemGetterCallable(instance, args_value_set) for instance in value.py__call__(arguments)])

def _create_string_input_function(func):
    
    @argument_clinic('string, /', want_value=True, want_arguments=True)
    def wrapper(strings, value, arguments):
        import custom_funtemplate
        return custom_funtemplate.rewrite_template('jedi.plugins.stdlib._create_string_input_function.wrapper', 'wrapper(strings, value, arguments)', {'get_str_or_none': get_str_or_none, 'func': func, 'compiled': compiled, 'ValueSet': ValueSet, 'argument_clinic': argument_clinic, 'strings': strings, 'value': value, 'arguments': arguments}, 1)
    return wrapper

@argument_clinic('*args, /', want_callback=True)
def _os_path_join(args_set, callback):
    import custom_funtemplate
    return custom_funtemplate.rewrite_template('jedi.plugins.stdlib._os_path_join', '_os_path_join(args_set, callback)', {'get_str_or_none': get_str_or_none, 'os': os, 'ValueSet': ValueSet, 'compiled': compiled, 'argument_clinic': argument_clinic, 'args_set': args_set, 'callback': callback}, 1)
_implemented = {'builtins': {'getattr': builtins_getattr, 'type': builtins_type, 'super': builtins_super, 'reversed': builtins_reversed, 'isinstance': builtins_isinstance, 'next': builtins_next, 'iter': builtins_iter, 'staticmethod': builtins_staticmethod, 'classmethod': builtins_classmethod, 'property': builtins_property}, 'copy': {'copy': _return_first_param, 'deepcopy': _return_first_param}, 'json': {'load': lambda value, arguments, callback: NO_VALUES, 'loads': lambda value, arguments, callback: NO_VALUES}, 'collections': {'namedtuple': collections_namedtuple}, 'functools': {'partial': functools_partial, 'partialmethod': functools_partialmethod, 'wraps': _functools_wraps}, '_weakref': {'proxy': _return_first_param}, 'random': {'choice': _random_choice}, 'operator': {'itemgetter': _operator_itemgetter}, 'abc': {'abstractmethod': _return_first_param}, 'typing': {'_alias': lambda value, arguments, callback: NO_VALUES, 'runtime_checkable': lambda value, arguments, callback: NO_VALUES}, 'dataclasses': {'dataclass': _dataclass}, 'attr': {'define': _dataclass, 'frozen': _dataclass}, 'attrs': {'define': _dataclass, 'frozen': _dataclass}, 'os.path': {'dirname': _create_string_input_function(os.path.dirname), 'abspath': _create_string_input_function(os.path.abspath), 'relpath': _create_string_input_function(os.path.relpath), 'join': _os_path_join}}

def get_metaclass_filters(func):
    import custom_funtemplate
    return custom_funtemplate.rewrite_template('jedi.plugins.stdlib.get_metaclass_filters', 'get_metaclass_filters(func)', {'ParserTreeFilter': ParserTreeFilter, 'DictFilter': DictFilter, 'EnumInstance': EnumInstance, 'func': func}, 1)


class EnumInstance(LazyValueWrapper):
    
    def __init__(self, cls, name):
        self.inference_state = cls.inference_state
        self._cls = cls
        self._name = name
        self.tree_node = self._name.tree_name
    
    @safe_property
    def name(self):
        return ValueName(self, self._name.tree_name)
    
    def _get_wrapped_value(self):
        n = self._name.string_name
        if ((n.startswith('__') and n.endswith('__')) or self._name.api_type == 'function'):
            inferred = self._name.infer()
            if inferred:
                return next(iter(inferred))
            (o, ) = self.inference_state.builtins_module.py__getattribute__('object')
            return o
        (value, ) = self._cls.execute_with_values()
        return value
    
    def get_filters(self, origin_scope=None):
        yield DictFilter(dict(name=compiled.create_simple_object(self.inference_state, self._name.string_name).name, value=self._name))
        for f in self._get_wrapped_value().get_filters():
            yield f


def tree_name_to_values(func):
    import custom_funtemplate
    return custom_funtemplate.rewrite_template('jedi.plugins.stdlib.tree_name_to_values', 'tree_name_to_values(func)', {'ValueSet': ValueSet, 'compiled': compiled, 'os': os, 'func': func}, 1)

