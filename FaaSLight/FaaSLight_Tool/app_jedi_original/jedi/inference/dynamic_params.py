"""
One of the really important features of |jedi| is to have an option to
understand code like this::

    def foo(bar):
        bar. # completion here
    foo(1)

There's no doubt wheter bar is an ``int`` or not, but if there's also a call
like ``foo('str')``, what would happen? Well, we'll just show both. Because
that's what a human would expect.

It works as follows:

- |Jedi| sees a param
- search for function calls named ``foo``
- execute these calls and check the input.
"""

from jedi import settings
from jedi import debug
from jedi.parser_utils import get_parent_scope
from jedi.inference.cache import inference_state_method_cache
from jedi.inference.arguments import TreeArguments
from jedi.inference.param import get_executed_param_names
from jedi.inference.helpers import is_stdlib_path
from jedi.inference.utils import to_list
from jedi.inference.value import instance
from jedi.inference.base_value import ValueSet, NO_VALUES
from jedi.inference.references import get_module_contexts_containing_name
from jedi.inference import recursion
MAX_PARAM_SEARCHES = 20

def _avoid_recursions(func):
    import custom_funtemplate
    return custom_funtemplate.rewrite_template('jedi.inference.dynamic_params._avoid_recursions', '_avoid_recursions(func)', {'recursion': recursion, 'NO_VALUES': NO_VALUES, 'func': func}, 1)

@debug.increase_indent
@_avoid_recursions
def dynamic_param_lookup(function_value, param_index):
    """
    A dynamic search for param values. If you try to complete a type:

    >>> def func(foo):
    ...     foo
    >>> func(1)
    >>> func("")

    It is not known what the type ``foo`` without analysing the whole code. You
    have to look for all calls to ``func`` to find out what ``foo`` possibly
    is.
    """
    import custom_funtemplate
    return custom_funtemplate.rewrite_template('jedi.inference.dynamic_params.dynamic_param_lookup', 'dynamic_param_lookup(function_value, param_index)', {'NO_VALUES': NO_VALUES, 'is_stdlib_path': is_stdlib_path, '_get_lambda_name': _get_lambda_name, '_search_function_arguments': _search_function_arguments, 'ValueSet': ValueSet, 'get_executed_param_names': get_executed_param_names, 'debug': debug, '_avoid_recursions': _avoid_recursions, 'function_value': function_value, 'param_index': param_index}, 1)

@inference_state_method_cache(default=None)
@to_list
def _search_function_arguments(module_context, funcdef, string_name):
    """
    Returns a list of param names.
    """
    import custom_funtemplate
    return custom_funtemplate.rewrite_template('jedi.inference.dynamic_params._search_function_arguments', '_search_function_arguments(module_context, funcdef, string_name)', {'get_parent_scope': get_parent_scope, 'settings': settings, 'get_module_contexts_containing_name': get_module_contexts_containing_name, '_get_potential_nodes': _get_potential_nodes, 'MAX_PARAM_SEARCHES': MAX_PARAM_SEARCHES, '_check_name_for_execution': _check_name_for_execution, 'inference_state_method_cache': inference_state_method_cache, 'to_list': to_list, 'module_context': module_context, 'funcdef': funcdef, 'string_name': string_name}, 1)

def _get_lambda_name(node):
    import custom_funtemplate
    return custom_funtemplate.rewrite_template('jedi.inference.dynamic_params._get_lambda_name', '_get_lambda_name(node)', {'node': node}, 1)

def _get_potential_nodes(module_value, func_string_name):
    import custom_funtemplate
    return custom_funtemplate.rewrite_template('jedi.inference.dynamic_params._get_potential_nodes', '_get_potential_nodes(module_value, func_string_name)', {'module_value': module_value, 'func_string_name': func_string_name}, 1)

def _check_name_for_execution(inference_state, context, compare_node, name, trailer):
    import custom_funtemplate
    return custom_funtemplate.rewrite_template('jedi.inference.dynamic_params._check_name_for_execution', '_check_name_for_execution(inference_state, context, compare_node, name, trailer)', {'TreeArguments': TreeArguments, 'instance': instance, '_get_potential_nodes': _get_potential_nodes, '_check_name_for_execution': _check_name_for_execution, 'inference_state': inference_state, 'context': context, 'compare_node': compare_node, 'name': name, 'trailer': trailer}, 1)

