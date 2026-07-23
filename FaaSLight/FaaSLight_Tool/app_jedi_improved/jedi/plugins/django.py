"""
Module is used to infer Django model fields.
"""

from inspect import Parameter
from jedi import debug
from jedi.inference.cache import inference_state_function_cache
from jedi.inference.base_value import ValueSet, iterator_to_value_set, ValueWrapper
from jedi.inference.filters import DictFilter, AttributeOverwrite
from jedi.inference.names import NameWrapper, BaseTreeParamName
from jedi.inference.compiled.value import EmptyCompiledName
from jedi.inference.value.instance import TreeInstance
from jedi.inference.value.klass import ClassMixin
from jedi.inference.gradual.base import GenericClass
from jedi.inference.gradual.generics import TupleGenericManager
from jedi.inference.signature import AbstractSignature
mapping = {'IntegerField': (None, 'int'), 'BigIntegerField': (None, 'int'), 'PositiveIntegerField': (None, 'int'), 'SmallIntegerField': (None, 'int'), 'CharField': (None, 'str'), 'TextField': (None, 'str'), 'EmailField': (None, 'str'), 'GenericIPAddressField': (None, 'str'), 'URLField': (None, 'str'), 'FloatField': (None, 'float'), 'BinaryField': (None, 'bytes'), 'BooleanField': (None, 'bool'), 'DecimalField': ('decimal', 'Decimal'), 'TimeField': ('datetime', 'time'), 'DurationField': ('datetime', 'timedelta'), 'DateField': ('datetime', 'date'), 'DateTimeField': ('datetime', 'datetime'), 'UUIDField': ('uuid', 'UUID')}
_FILTER_LIKE_METHODS = ('create', 'filter', 'exclude', 'update', 'get', 'get_or_create', 'update_or_create')

@inference_state_function_cache()
def _get_deferred_attributes(inference_state):
    return inference_state.import_module(('django', 'db', 'models', 'query_utils')).py__getattribute__('DeferredAttribute').execute_annotation()

def _infer_scalar_field(inference_state, field_name, field_tree_instance, is_instance):
    import custom_funtemplate
    return custom_funtemplate.rewrite_template('jedi.plugins.django._infer_scalar_field', '_infer_scalar_field(inference_state, field_name, field_tree_instance, is_instance)', {'mapping': mapping, '_get_deferred_attributes': _get_deferred_attributes, 'inference_state': inference_state, 'field_name': field_name, 'field_tree_instance': field_tree_instance, 'is_instance': is_instance}, 1)

@iterator_to_value_set
def _get_foreign_key_values(cls, field_tree_instance):
    import custom_funtemplate
    custom_funtemplate.rewrite_template('jedi.plugins.django._get_foreign_key_values', '_get_foreign_key_values(cls, field_tree_instance)', {'TreeInstance': TreeInstance, 'iterator_to_value_set': iterator_to_value_set, 'cls': cls, 'field_tree_instance': field_tree_instance}, 0)

def _infer_field(cls, field_name, is_instance):
    import custom_funtemplate
    return custom_funtemplate.rewrite_template('jedi.plugins.django._infer_field', '_infer_field(cls, field_name, is_instance)', {'_infer_scalar_field': _infer_scalar_field, '_get_deferred_attributes': _get_deferred_attributes, '_get_foreign_key_values': _get_foreign_key_values, 'ValueSet': ValueSet, '_create_manager_for': _create_manager_for, 'debug': debug, 'cls': cls, 'field_name': field_name, 'is_instance': is_instance}, 1)


class DjangoModelName(NameWrapper):
    
    def __init__(self, cls, name, is_instance):
        super().__init__(name)
        self._cls = cls
        self._is_instance = is_instance
    
    def infer(self):
        return _infer_field(self._cls, self._wrapped_name, self._is_instance)


def _create_manager_for(cls, manager_cls='BaseManager'):
    import custom_funtemplate
    return custom_funtemplate.rewrite_template('jedi.plugins.django._create_manager_for', "_create_manager_for(cls, manager_cls='BaseManager')", {'TupleGenericManager': TupleGenericManager, 'ValueSet': ValueSet, 'GenericClass': GenericClass, 'cls': cls, 'manager_cls': manager_cls}, 1)

def _new_dict_filter(cls, is_instance):
    filters = list(cls.get_filters(is_instance=is_instance, include_metaclasses=False, include_type_when_class=False))
    dct = {name.string_name: DjangoModelName(cls, name, is_instance) for filter_ in reversed(filters) for name in filter_.values()}
    if is_instance:
        dct['objects'] = EmptyCompiledName(cls.inference_state, 'objects')
    return DictFilter(dct)

def is_django_model_base(value):
    return (value.py__name__() == 'ModelBase' and value.get_root_context().py__name__() == 'django.db.models.base')

def get_metaclass_filters(func):
    import custom_funtemplate
    return custom_funtemplate.rewrite_template('jedi.plugins.django.get_metaclass_filters', 'get_metaclass_filters(func)', {'is_django_model_base': is_django_model_base, '_new_dict_filter': _new_dict_filter, 'func': func}, 1)

def tree_name_to_values(func):
    import custom_funtemplate
    return custom_funtemplate.rewrite_template('jedi.plugins.django.tree_name_to_values', 'tree_name_to_values(func)', {'_FILTER_LIKE_METHODS': _FILTER_LIKE_METHODS, 'ValueSet': ValueSet, 'QuerySetMethodWrapper': QuerySetMethodWrapper, 'ManagerWrapper': ManagerWrapper, 'FieldWrapper': FieldWrapper, 'func': func}, 1)

def _find_fields(cls):
    for name in _new_dict_filter(cls, is_instance=False).values():
        for value in name.infer():
            if value.name.get_qualified_names(include_module_names=True) == ('django', 'db', 'models', 'query_utils', 'DeferredAttribute'):
                yield name

def _get_signatures(cls):
    return [DjangoModelSignature(cls, field_names=list(_find_fields(cls)))]

def get_metaclass_signatures(func):
    import custom_funtemplate
    return custom_funtemplate.rewrite_template('jedi.plugins.django.get_metaclass_signatures', 'get_metaclass_signatures(func)', {'is_django_model_base': is_django_model_base, '_get_signatures': _get_signatures, 'func': func}, 1)


class ManagerWrapper(ValueWrapper):
    
    def py__getitem__(self, index_value_set, contextualized_node):
        return ValueSet((GenericManagerWrapper(generic) for generic in self._wrapped_value.py__getitem__(index_value_set, contextualized_node)))



class GenericManagerWrapper(AttributeOverwrite, ClassMixin):
    
    def py__get__on_class(self, calling_instance, instance, class_value):
        return calling_instance.class_value.with_generics((ValueSet({class_value}), )).py__call__(calling_instance._arguments)
    
    def with_generics(self, generics_tuple):
        return self._wrapped_value.with_generics(generics_tuple)



class FieldWrapper(ValueWrapper):
    
    def py__getitem__(self, index_value_set, contextualized_node):
        return ValueSet((GenericFieldWrapper(generic) for generic in self._wrapped_value.py__getitem__(index_value_set, contextualized_node)))



class GenericFieldWrapper(AttributeOverwrite, ClassMixin):
    
    def py__get__on_class(self, calling_instance, instance, class_value):
        return ValueSet({calling_instance})



class DjangoModelSignature(AbstractSignature):
    
    def __init__(self, value, field_names):
        super().__init__(value)
        self._field_names = field_names
    
    def get_param_names(self, resolve_stars=False):
        return [DjangoParamName(name) for name in self._field_names]



class DjangoParamName(BaseTreeParamName):
    
    def __init__(self, field_name):
        super().__init__(field_name.parent_context, field_name.tree_name)
        self._field_name = field_name
    
    def get_kind(self):
        return Parameter.KEYWORD_ONLY
    
    def infer(self):
        return self._field_name.infer()



class QuerySetMethodWrapper(ValueWrapper):
    
    def __init__(self, method, model_cls):
        super().__init__(method)
        self._model_cls = model_cls
    
    def py__get__(self, instance, class_value):
        return ValueSet({QuerySetBoundMethodWrapper(v, self._model_cls) for v in self._wrapped_value.py__get__(instance, class_value)})



class QuerySetBoundMethodWrapper(ValueWrapper):
    
    def __init__(self, method, model_cls):
        super().__init__(method)
        self._model_cls = model_cls
    
    def get_signatures(self):
        return _get_signatures(self._model_cls)


