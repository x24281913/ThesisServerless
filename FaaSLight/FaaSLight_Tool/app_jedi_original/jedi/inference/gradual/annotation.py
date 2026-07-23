"""
PEP 0484 ( https://www.python.org/dev/peps/pep-0484/ ) describes type hints
through function annotations. There is a strong suggestion in this document
that only the type of type hinting defined in PEP0484 should be allowed
as annotations in future python versions.
"""

import re
from inspect import Parameter
from parso import ParserSyntaxError, parse
from jedi.inference.cache import inference_state_method_cache
from jedi.inference.base_value import ValueSet, NO_VALUES
from jedi.inference.gradual.base import DefineGenericBaseClass, GenericClass
from jedi.inference.gradual.generics import TupleGenericManager
from jedi.inference.gradual.type_var import TypeVar
from jedi.inference.helpers import is_string
from jedi.inference.compiled import builtin_from_name
from jedi.inference.param import get_executed_param_names
from jedi import debug
from jedi import parser_utils

def infer_annotation(context, annotation):
    """
    Inferes an annotation node. This means that it inferes the part of
    `int` here:

        foo: int = 3

    Also checks for forward references (strings)
    """
    value_set = context.infer_node(annotation)
    if len(value_set) != 1:
        debug.warning('Inferred typing index %s should lead to 1 object,  not %s' % (annotation, value_set))
        return value_set
    inferred_value = list(value_set)[0]
    if is_string(inferred_value):
        result = _get_forward_reference_node(context, inferred_value.get_safe_value())
        if result is not None:
            return context.infer_node(result)
    return value_set

def _infer_annotation_string(context, string, index=None):
    node = _get_forward_reference_node(context, string)
    if node is None:
        return NO_VALUES
    value_set = context.infer_node(node)
    if index is not None:
        value_set = value_set.filter(lambda value: (value.array_type == 'tuple' and len(list(value.py__iter__())) >= index)).py__simple_getitem__(index)
    return value_set

def _get_forward_reference_node(context, string):
    try:
        new_node = context.inference_state.grammar.parse(string, start_symbol='eval_input', error_recovery=False)
    except ParserSyntaxError:
        debug.warning('Annotation not parsed: %s' % string)
        return None
    else:
        module = context.tree_node.get_root_node()
        parser_utils.move(new_node, module.end_pos[0])
        new_node.parent = context.tree_node
        return new_node

def _split_comment_param_declaration(decl_text):
    """
    Split decl_text on commas, but group generic expressions
    together.

    For example, given "foo, Bar[baz, biz]" we return
    ['foo', 'Bar[baz, biz]'].

    """
    import custom_funtemplate
    return custom_funtemplate.rewrite_template('jedi.inference.gradual.annotation._split_comment_param_declaration', '_split_comment_param_declaration(decl_text)', {'parse': parse, 'ParserSyntaxError': ParserSyntaxError, 'debug': debug, 'decl_text': decl_text}, 1)

@inference_state_method_cache()
def infer_param(function_value, param, ignore_stars=False):
    import custom_funtemplate
    return custom_funtemplate.rewrite_template('jedi.inference.gradual.annotation.infer_param', 'infer_param(function_value, param, ignore_stars=False)', {'_infer_param': _infer_param, 'builtin_from_name': builtin_from_name, 'ValueSet': ValueSet, 'GenericClass': GenericClass, 'TupleGenericManager': TupleGenericManager, 'inference_state_method_cache': inference_state_method_cache, 'function_value': function_value, 'param': param, 'ignore_stars': ignore_stars}, 1)

def _infer_param(function_value, param):
    """
    Infers the type of a function parameter, using type annotations.
    """
    import custom_funtemplate
    return custom_funtemplate.rewrite_template('jedi.inference.gradual.annotation._infer_param', '_infer_param(function_value, param)', {'parser_utils': parser_utils, 'NO_VALUES': NO_VALUES, 're': re, '_split_comment_param_declaration': _split_comment_param_declaration, 'debug': debug, '_infer_annotation_string': _infer_annotation_string, 'infer_annotation': infer_annotation, 'function_value': function_value, 'param': param}, 1)

def py__annotations__(funcdef):
    dct = {}
    for function_param in funcdef.get_params():
        param_annotation = function_param.annotation
        if param_annotation is not None:
            dct[function_param.name.value] = param_annotation
    return_annotation = funcdef.annotation
    if return_annotation:
        dct['return'] = return_annotation
    return dct

def resolve_forward_references(context, all_annotations):
    
    def resolve(node):
        if (node is None or node.type != 'string'):
            return node
        node = _get_forward_reference_node(context, context.inference_state.compiled_subprocess.safe_literal_eval(node.value))
        if node is None:
            return None
        node = node.children[0]
        return node
    return {name: resolve(node) for (name, node) in all_annotations.items()}

@inference_state_method_cache()
def infer_return_types(function, arguments):
    """
    Infers the type of a function's return value,
    according to type annotations.
    """
    context = function.get_default_param_context()
    all_annotations = resolve_forward_references(context, py__annotations__(function.tree_node))
    annotation = all_annotations.get('return', None)
    if annotation is None:
        node = function.tree_node
        comment = parser_utils.get_following_comment_same_line(node)
        if comment is None:
            return NO_VALUES
        match = re.match('^#\\s*type:\\s*\\([^#]*\\)\\s*->\\s*([^#]*)', comment)
        if not match:
            return NO_VALUES
        return _infer_annotation_string(context, match.group(1).strip()).execute_annotation()
    unknown_type_vars = find_unknown_type_vars(context, annotation)
    annotation_values = infer_annotation(context, annotation)
    if not unknown_type_vars:
        return annotation_values.execute_annotation()
    type_var_dict = infer_type_vars_for_execution(function, arguments, all_annotations)
    return ValueSet.from_sets(((ann.define_generics(type_var_dict) if isinstance(ann, (DefineGenericBaseClass, TypeVar)) else ValueSet({ann})) for ann in annotation_values)).execute_annotation()

def infer_type_vars_for_execution(function, arguments, annotation_dict):
    """
    Some functions use type vars that are not defined by the class, but rather
    only defined in the function. See for example `iter`. In those cases we
    want to:

    1. Search for undefined type vars.
    2. Infer type vars with the execution state we have.
    3. Return the union of all type vars that have been found.
    """
    context = function.get_default_param_context()
    annotation_variable_results = {}
    executed_param_names = get_executed_param_names(function, arguments)
    for executed_param_name in executed_param_names:
        try:
            annotation_node = annotation_dict[executed_param_name.string_name]
        except KeyError:
            continue
        annotation_variables = find_unknown_type_vars(context, annotation_node)
        if annotation_variables:
            annotation_value_set = context.infer_node(annotation_node)
            kind = executed_param_name.get_kind()
            actual_value_set = executed_param_name.infer()
            if kind is Parameter.VAR_POSITIONAL:
                actual_value_set = actual_value_set.merge_types_of_iterate()
            elif kind is Parameter.VAR_KEYWORD:
                actual_value_set = actual_value_set.try_merge('_dict_values')
            merge_type_var_dicts(annotation_variable_results, annotation_value_set.infer_type_vars(actual_value_set))
    return annotation_variable_results

def infer_return_for_callable(arguments, param_values, result_values):
    import custom_funtemplate
    return custom_funtemplate.rewrite_template('jedi.inference.gradual.annotation.infer_return_for_callable', 'infer_return_for_callable(arguments, param_values, result_values)', {'_infer_type_vars_for_callable': _infer_type_vars_for_callable, 'ValueSet': ValueSet, 'DefineGenericBaseClass': DefineGenericBaseClass, 'TypeVar': TypeVar, 'arguments': arguments, 'param_values': param_values, 'result_values': result_values}, 1)

def _infer_type_vars_for_callable(arguments, lazy_params):
    """
    Infers type vars for the Calllable class:

        def x() -> Callable[[Callable[..., _T]], _T]: ...
    """
    import custom_funtemplate
    return custom_funtemplate.rewrite_template('jedi.inference.gradual.annotation._infer_type_vars_for_callable', '_infer_type_vars_for_callable(arguments, lazy_params)', {'merge_type_var_dicts': merge_type_var_dicts, 'arguments': arguments, 'lazy_params': lazy_params}, 1)

def merge_type_var_dicts(base_dict, new_dict):
    for (type_var_name, values) in new_dict.items():
        if values:
            try:
                base_dict[type_var_name] |= values
            except KeyError:
                base_dict[type_var_name] = values

def merge_pairwise_generics(annotation_value, annotated_argument_class):
    """
    Match up the generic parameters from the given argument class to the
    target annotation.

    This walks the generic parameters immediately within the annotation and
    argument's type, in order to determine the concrete values of the
    annotation's parameters for the current case.

    For example, given the following code:

        def values(mapping: Mapping[K, V]) -> List[V]: ...

        for val in values({1: 'a'}):
            val

    Then this function should be given representations of `Mapping[K, V]`
    and `Mapping[int, str]`, so that it can determine that `K` is `int and
    `V` is `str`.

    Note that it is responsibility of the caller to traverse the MRO of the
    argument type as needed in order to find the type matching the
    annotation (in this case finding `Mapping[int, str]` as a parent of
    `Dict[int, str]`).

    Parameters
    ----------

    `annotation_value`: represents the annotation to infer the concrete
        parameter types of.

    `annotated_argument_class`: represents the annotated class of the
        argument being passed to the object annotated by `annotation_value`.
    """
    type_var_dict = {}
    if not isinstance(annotated_argument_class, DefineGenericBaseClass):
        return type_var_dict
    annotation_generics = annotation_value.get_generics()
    actual_generics = annotated_argument_class.get_generics()
    for (annotation_generics_set, actual_generic_set) in zip(annotation_generics, actual_generics):
        merge_type_var_dicts(type_var_dict, annotation_generics_set.infer_type_vars(actual_generic_set.execute_annotation()))
    return type_var_dict

def find_type_from_comment_hint_for(context, node, name):
    return _find_type_from_comment_hint(context, node, node.children[1], name)

def find_type_from_comment_hint_with(context, node, name):
    if len(node.children) > 4:
        return []
    assert len(node.children[1].children) == 3, "Can only be here when children[1] is 'foo() as f'"
    varlist = node.children[1].children[2]
    return _find_type_from_comment_hint(context, node, varlist, name)

def find_type_from_comment_hint_assign(context, node, name):
    return _find_type_from_comment_hint(context, node, node.children[0], name)

def _find_type_from_comment_hint(context, node, varlist, name):
    index = None
    if varlist.type in ('testlist_star_expr', 'exprlist', 'testlist'):
        index = 0
        for child in varlist.children:
            if child == name:
                break
            if child.type == 'operator':
                continue
            index += 1
        else:
            return []
    comment = parser_utils.get_following_comment_same_line(node)
    if comment is None:
        return []
    match = re.match('^#\\s*type:\\s*([^#]*)', comment)
    if match is None:
        return []
    return _infer_annotation_string(context, match.group(1).strip(), index).execute_annotation()

def find_unknown_type_vars(context, node):
    
    def check_node(node):
        if node.type in ('atom_expr', 'power'):
            trailer = node.children[-1]
            if (trailer.type == 'trailer' and trailer.children[0] == '['):
                for subscript_node in _unpack_subscriptlist(trailer.children[1]):
                    check_node(subscript_node)
        else:
            found[:] = _filter_type_vars(context.infer_node(node), found)
    found = []
    check_node(node)
    return found

def _filter_type_vars(value_set, found=()):
    new_found = list(found)
    for type_var in value_set:
        if (isinstance(type_var, TypeVar) and type_var not in found):
            new_found.append(type_var)
    return new_found

def _unpack_subscriptlist(subscriptlist):
    if subscriptlist.type == 'subscriptlist':
        for subscript in subscriptlist.children[::2]:
            if subscript.type != 'subscript':
                yield subscript
    elif subscriptlist.type != 'subscript':
        yield subscriptlist

