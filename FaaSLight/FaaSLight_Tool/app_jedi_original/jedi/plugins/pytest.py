import sys
from typing import List
from pathlib import Path
from parso.tree import search_ancestor
from jedi.inference.cache import inference_state_method_cache
from jedi.inference.imports import goto_import, load_module_from_path
from jedi.inference.filters import ParserTreeFilter
from jedi.inference.base_value import NO_VALUES, ValueSet
from jedi.inference.helpers import infer_call_of_leaf
_PYTEST_FIXTURE_MODULES = [('_pytest', 'monkeypatch'), ('_pytest', 'capture'), ('_pytest', 'logging'), ('_pytest', 'tmpdir'), ('_pytest', 'pytester')]

def execute(callback):
    import custom_funtemplate
    return custom_funtemplate.rewrite_template('jedi.plugins.pytest.execute', 'execute(callback)', {'NO_VALUES': NO_VALUES, 'callback': callback}, 1)

def infer_anonymous_param(func):
    import custom_funtemplate
    return custom_funtemplate.rewrite_template('jedi.plugins.pytest.infer_anonymous_param', 'infer_anonymous_param(func)', {'ValueSet': ValueSet, '_is_a_pytest_param_and_inherited': _is_a_pytest_param_and_inherited, '_goto_pytest_fixture': _goto_pytest_fixture, 'func': func}, 1)

def goto_anonymous_param(func):
    import custom_funtemplate
    return custom_funtemplate.rewrite_template('jedi.plugins.pytest.goto_anonymous_param', 'goto_anonymous_param(func)', {'_is_a_pytest_param_and_inherited': _is_a_pytest_param_and_inherited, '_goto_pytest_fixture': _goto_pytest_fixture, 'func': func}, 1)

def complete_param_names(func):
    import custom_funtemplate
    return custom_funtemplate.rewrite_template('jedi.plugins.pytest.complete_param_names', 'complete_param_names(func)', {'_is_pytest_func': _is_pytest_func, '_iter_pytest_modules': _iter_pytest_modules, 'FixtureFilter': FixtureFilter, 'func': func}, 1)

def _goto_pytest_fixture(module_context, name, skip_own_module):
    import custom_funtemplate
    return custom_funtemplate.rewrite_template('jedi.plugins.pytest._goto_pytest_fixture', '_goto_pytest_fixture(module_context, name, skip_own_module)', {'_iter_pytest_modules': _iter_pytest_modules, 'FixtureFilter': FixtureFilter, 'module_context': module_context, 'name': name, 'skip_own_module': skip_own_module}, 1)

def _is_a_pytest_param_and_inherited(param_name):
    """
    Pytest params are either in a `test_*` function or have a pytest fixture
    with the decorator @pytest.fixture.

    This is a heuristic and will work in most cases.
    """
    import custom_funtemplate
    return custom_funtemplate.rewrite_template('jedi.plugins.pytest._is_a_pytest_param_and_inherited', '_is_a_pytest_param_and_inherited(param_name)', {'search_ancestor': search_ancestor, '_is_pytest_func': _is_pytest_func, 'param_name': param_name}, 2)

def _is_pytest_func(func_name, decorator_nodes):
    return (func_name.startswith('test') or any(('fixture' in n.get_code() for n in decorator_nodes)))

def _find_pytest_plugin_modules() -> List[List[str]]:
    """
    Finds pytest plugin modules hooked by setuptools entry points

    See https://docs.pytest.org/en/stable/how-to/writing_plugins.html#setuptools-entry-points
    """
    import custom_funtemplate
    return custom_funtemplate.rewrite_template('jedi.plugins.pytest._find_pytest_plugin_modules', '_find_pytest_plugin_modules()', {'sys': sys, 'List': List, 'List': List, 'str': str}, 1)

@inference_state_method_cache()
def _iter_pytest_modules(module_context, skip_own_module=False):
    import custom_funtemplate
    custom_funtemplate.rewrite_template('jedi.plugins.pytest._iter_pytest_modules', '_iter_pytest_modules(module_context, skip_own_module=False)', {'Path': Path, 'load_module_from_path': load_module_from_path, '_load_pytest_plugins': _load_pytest_plugins, '_PYTEST_FIXTURE_MODULES': _PYTEST_FIXTURE_MODULES, '_find_pytest_plugin_modules': _find_pytest_plugin_modules, 'inference_state_method_cache': inference_state_method_cache, 'module_context': module_context, 'skip_own_module': skip_own_module}, 0)

def _load_pytest_plugins(module_context, name):
    import custom_funtemplate
    custom_funtemplate.rewrite_template('jedi.plugins.pytest._load_pytest_plugins', '_load_pytest_plugins(module_context, name)', {'module_context': module_context, 'name': name}, 0)


class FixtureFilter(ParserTreeFilter):
    
    def _filter(self, names):
        for name in super()._filter(names):
            if name.parent.type == 'import_from':
                imported_names = goto_import(self.parent_context, name)
                if any((self._is_fixture(iname.parent_context, iname.tree_name) for iname in imported_names if iname.tree_name)):
                    yield name
            elif self._is_fixture(self.parent_context, name):
                yield name
    
    def _is_fixture(self, context, name):
        funcdef = name.parent
        if funcdef.type != 'funcdef':
            return False
        decorated = funcdef.parent
        if decorated.type != 'decorated':
            return False
        decorators = decorated.children[0]
        if decorators.type == 'decorators':
            decorators = decorators.children
        else:
            decorators = [decorators]
        for decorator in decorators:
            dotted_name = decorator.children[1]
            if 'fixture' in dotted_name.get_code():
                if dotted_name.type == 'atom_expr':
                    last_trailer = dotted_name.children[-1]
                    last_leaf = last_trailer.get_last_leaf()
                    if last_leaf == ')':
                        values = infer_call_of_leaf(context, last_leaf, cut_own_trailer=True)
                    else:
                        values = context.infer_node(dotted_name)
                else:
                    values = context.infer_node(dotted_name)
                for value in values:
                    if value.name.get_qualified_names(include_module_names=True) == ('_pytest', 'fixtures', 'fixture'):
                        return True
        return False


