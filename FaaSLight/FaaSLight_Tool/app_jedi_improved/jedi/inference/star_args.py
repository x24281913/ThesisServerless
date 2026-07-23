"""
This module is responsible for inferring *args and **kwargs for signatures.

This means for example in this case::

    def foo(a, b, c): ...

    def bar(*args):
        return foo(1, *args)

The signature here for bar should be `bar(b, c)` instead of bar(*args).
"""

from inspect import Parameter
from parso import tree
from jedi.inference.utils import to_list
from jedi.inference.names import ParamNameWrapper
from jedi.inference.helpers import is_big_annoying_library

def _iter_nodes_for_param(param_name):
    import custom_funtemplate
    custom_funtemplate.rewrite_template('jedi.inference.star_args._iter_nodes_for_param', '_iter_nodes_for_param(param_name)', {'tree': tree, '_goes_to_param_name': _goes_to_param_name, '_to_callables': _to_callables, 'param_name': param_name}, 0)

def _goes_to_param_name(param_name, context, potential_name):
    import custom_funtemplate
    return custom_funtemplate.rewrite_template('jedi.inference.star_args._goes_to_param_name', '_goes_to_param_name(param_name, context, potential_name)', {'param_name': param_name, 'context': context, 'potential_name': potential_name}, 1)

def _to_callables(context, trailer):
    import custom_funtemplate
    return custom_funtemplate.rewrite_template('jedi.inference.star_args._to_callables', '_to_callables(context, trailer)', {'context': context, 'trailer': trailer}, 1)

def _remove_given_params(arguments, param_names):
    import custom_funtemplate
    custom_funtemplate.rewrite_template('jedi.inference.star_args._remove_given_params', '_remove_given_params(arguments, param_names)', {'arguments': arguments, 'param_names': param_names}, 0)

@to_list
def process_params(param_names, star_count=3):
    import custom_funtemplate
    return custom_funtemplate.rewrite_template('jedi.inference.star_args.process_params', 'process_params(param_names, star_count=3)', {'is_big_annoying_library': is_big_annoying_library, 'Parameter': Parameter, '_iter_nodes_for_param': _iter_nodes_for_param, 'ParamNameFixedKind': ParamNameFixedKind, 'process_params': process_params, '_remove_given_params': _remove_given_params, 'to_list': to_list, 'param_names': param_names, 'star_count': star_count}, 1)


class ParamNameFixedKind(ParamNameWrapper):
    
    def __init__(self, param_name, new_kind):
        super().__init__(param_name)
        self._new_kind = new_kind
    
    def get_kind(self):
        return self._new_kind


