from jedi import debug
from jedi.inference.base_value import ValueSet, NO_VALUES
from jedi.inference.utils import to_list
from jedi.inference.gradual.stub_value import StubModuleValue
from jedi.inference.gradual.typeshed import try_to_load_stub_cached
from jedi.inference.value.decorator import Decoratee

def _stub_to_python_value_set(stub_value, ignore_compiled=False):
    stub_module_context = stub_value.get_root_context()
    if not stub_module_context.is_stub():
        return ValueSet([stub_value])
    decorates = None
    if isinstance(stub_value, Decoratee):
        decorates = stub_value._original_value
    was_instance = stub_value.is_instance()
    if was_instance:
        arguments = getattr(stub_value, '_arguments', None)
        stub_value = stub_value.py__class__()
    qualified_names = stub_value.get_qualified_names()
    if qualified_names is None:
        return NO_VALUES
    was_bound_method = stub_value.is_bound_method()
    if was_bound_method:
        method_name = qualified_names[-1]
        qualified_names = qualified_names[:-1]
        was_instance = True
        arguments = None
    values = _infer_from_stub(stub_module_context, qualified_names, ignore_compiled)
    if was_instance:
        values = ValueSet.from_sets(((c.execute_with_values() if arguments is None else c.execute(arguments)) for c in values if c.is_class()))
    if was_bound_method:
        values = values.py__getattribute__(method_name)
    if decorates is not None:
        values = ValueSet((Decoratee(v, decorates) for v in values))
    return values

def _infer_from_stub(stub_module_context, qualified_names, ignore_compiled):
    from jedi.inference.compiled.mixed import MixedObject
    stub_module = stub_module_context.get_value()
    assert isinstance(stub_module, (StubModuleValue, MixedObject)), stub_module_context
    non_stubs = stub_module.non_stub_value_set
    if ignore_compiled:
        non_stubs = non_stubs.filter(lambda c: not c.is_compiled())
    for name in qualified_names:
        non_stubs = non_stubs.py__getattribute__(name)
    return non_stubs

@to_list
def _try_stub_to_python_names(names, prefer_stub_to_compiled=False):
    import custom_funtemplate
    custom_funtemplate.rewrite_template('jedi.inference.gradual.conversion._try_stub_to_python_names', '_try_stub_to_python_names(names, prefer_stub_to_compiled=False)', {'convert_values': convert_values, '_stub_to_python_value_set': _stub_to_python_value_set, 'to_list': to_list, 'names': names, 'prefer_stub_to_compiled': prefer_stub_to_compiled}, 0)

def _load_stub_module(module):
    if module.is_stub():
        return module
    return try_to_load_stub_cached(module.inference_state, import_names=module.string_names, python_value_set=ValueSet([module]), parent_module_value=None, sys_path=module.inference_state.get_sys_path())

@to_list
def _python_to_stub_names(names, fallback_to_python=False):
    import custom_funtemplate
    custom_funtemplate.rewrite_template('jedi.inference.gradual.conversion._python_to_stub_names', '_python_to_stub_names(names, fallback_to_python=False)', {'convert_values': convert_values, '_python_to_stub_names': _python_to_stub_names, 'to_stub': to_stub, 'to_list': to_list, 'names': names, 'fallback_to_python': fallback_to_python}, 0)

def convert_names(names, only_stubs=False, prefer_stubs=False, prefer_stub_to_compiled=True):
    import custom_funtemplate
    return custom_funtemplate.rewrite_template('jedi.inference.gradual.conversion.convert_names', 'convert_names(names, only_stubs=False, prefer_stubs=False, prefer_stub_to_compiled=True)', {'debug': debug, '_python_to_stub_names': _python_to_stub_names, '_try_stub_to_python_names': _try_stub_to_python_names, 'names': names, 'only_stubs': only_stubs, 'prefer_stubs': prefer_stubs, 'prefer_stub_to_compiled': prefer_stub_to_compiled}, 1)

def convert_values(values, only_stubs=False, prefer_stubs=False, ignore_compiled=True):
    assert not ((only_stubs and prefer_stubs))
    with debug.increase_indent_cm('convert values'):
        if (only_stubs or prefer_stubs):
            return ValueSet.from_sets(((to_stub(value) or ((ValueSet({value}) if prefer_stubs else NO_VALUES))) for value in values))
        else:
            return ValueSet.from_sets(((_stub_to_python_value_set(stub_value, ignore_compiled=ignore_compiled) or ValueSet({stub_value})) for stub_value in values))

def to_stub(value):
    if value.is_stub():
        return ValueSet([value])
    was_instance = value.is_instance()
    if was_instance:
        value = value.py__class__()
    qualified_names = value.get_qualified_names()
    stub_module = _load_stub_module(value.get_root_context().get_value())
    if (stub_module is None or qualified_names is None):
        return NO_VALUES
    was_bound_method = value.is_bound_method()
    if was_bound_method:
        method_name = qualified_names[-1]
        qualified_names = qualified_names[:-1]
        was_instance = True
    stub_values = ValueSet([stub_module])
    for name in qualified_names:
        stub_values = stub_values.py__getattribute__(name)
    if was_instance:
        stub_values = ValueSet.from_sets((c.execute_with_values() for c in stub_values if c.is_class()))
    if was_bound_method:
        stub_values = stub_values.py__getattribute__(method_name)
    return stub_values

