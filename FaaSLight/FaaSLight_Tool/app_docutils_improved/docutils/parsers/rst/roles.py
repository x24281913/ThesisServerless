"""
This module defines standard interpreted text role functions, a registry for
interpreted text roles, and an API for adding to and retrieving from the
registry. See also `Creating reStructuredText Interpreted Text Roles`__.

__ https://docutils.sourceforge.io/docs/ref/rst/roles.html


The interface for interpreted role functions is as follows::

    def role_fn(name, rawtext, text, lineno, inliner,
                options=None, content=None):
        code...

    # Set function attributes for customization:
    role_fn.options = ...
    role_fn.content = ...

Parameters:

- ``name`` is the local name of the interpreted text role, the role name
  actually used in the document.

- ``rawtext`` is a string containing the entire interpreted text construct.
  Return it as a ``problematic`` node linked to a system message if there is a
  problem.

- ``text`` is the interpreted text content, with backslash escapes converted
  to nulls (``
``).

- ``lineno`` is the line number where the text block containing the
  interpreted text begins.

- ``inliner`` is the Inliner object that called the role function.
  It defines the following useful attributes: ``reporter``,
  ``problematic``, ``memo``, ``parent``, ``document``.

- ``options``: A dictionary of directive options for customization, to be
  interpreted by the role function.  Used for additional attributes for the
  generated elements and other functionality.

- ``content``: A list of strings, the directive content for customization
  ("role" directive).  To be interpreted by the role function.

Function attributes for customization, interpreted by the "role" directive:

- ``options``: A dictionary, mapping known option names to conversion
  functions such as `int` or `float`.  ``None`` or an empty dict implies no
  options to parse.  Several directive option conversion functions are defined
  in the `directives` module.

  All role functions implicitly support the "class" option, unless disabled
  with an explicit ``{'class': None}``.

- ``content``: A boolean; true if content is allowed.  Client code must handle
  the case where content is required but not supplied (an empty content list
  will be supplied).

Note that unlike directives, the "arguments" function attribute is not
supported for role customization.  Directive arguments are handled by the
"role" directive itself.

Interpreted role functions return a tuple of two values:

- A list of nodes which will be inserted into the document tree at the
  point where the interpreted role was encountered (can be an empty
  list).

- A list of system messages, which will be inserted into the document tree
  immediately after the end of the current inline block (can also be empty).
"""

from __future__ import annotations
__docformat__ = 'reStructuredText'
import warnings
from docutils import nodes
from docutils.parsers.rst import directives
from docutils.parsers.rst.languages import en as _fallback_language_module
from docutils.utils.code_analyzer import Lexer, LexerError
DEFAULT_INTERPRETED_ROLE = 'title-reference'
'The canonical name of the default interpreted role.\n\nThis role is used when no role is specified for a piece of interpreted text.\n'
_role_registry = {}
'Mapping of canonical role names to role functions.\n\nLanguage-dependent role names are defined in the ``language`` subpackage.\n'
_roles = {}
'Mapping of local or language-dependent interpreted text role names to role\nfunctions.'

def role(role_name, language_module, lineno, reporter):
    """
    Locate and return a role function from its language-dependent name, along
    with a list of system messages.

    If the role is not found in the current language, check English. Return a
    2-tuple: role function (``None`` if the named role cannot be found) and a
    list of system messages.
    """
    import custom_funtemplate
    return custom_funtemplate.rewrite_template('docutils.parsers.rst.roles.role', 'role(role_name, language_module, lineno, reporter)', {'_roles': _roles, 'DEFAULT_INTERPRETED_ROLE': DEFAULT_INTERPRETED_ROLE, '_fallback_language_module': _fallback_language_module, '_role_registry': _role_registry, 'register_local_role': register_local_role, 'role_name': role_name, 'language_module': language_module, 'lineno': lineno, 'reporter': reporter}, 2)

def register_canonical_role(name, role_fn) -> None:
    """
    Register an interpreted text role by its canonical name.

    :Parameters:
      - `name`: The canonical name of the interpreted role.
      - `role_fn`: The role function.  See the module docstring.
    """
    set_implicit_options(role_fn)
    _role_registry[name.lower()] = role_fn

def register_local_role(name, role_fn) -> None:
    """
    Register an interpreted text role by its local or language-dependent name.

    :Parameters:
      - `name`: The local or language-dependent name of the interpreted role.
      - `role_fn`: The role function.  See the module docstring.
    """
    set_implicit_options(role_fn)
    _roles[name.lower()] = role_fn

def set_implicit_options(role_fn) -> None:
    """
    Add customization options to role functions, unless explicitly set or
    disabled.
    """
    if (not hasattr(role_fn, 'options') or role_fn.options is None):
        role_fn.options = {'class': directives.class_option}
    elif 'class' not in role_fn.options:
        role_fn.options['class'] = directives.class_option

def register_generic_role(canonical_name, node_class) -> None:
    """For roles which simply wrap a given `node_class` around the text."""
    role = GenericRole(canonical_name, node_class)
    register_canonical_role(canonical_name, role)


class GenericRole:
    """
    Generic interpreted text role.

    The interpreted text is simply wrapped with the provided node class.
    """
    
    def __init__(self, role_name, node_class) -> None:
        self.name = role_name
        self.node_class = node_class
    
    def __call__(self, role, rawtext, text, lineno, inliner, options=None, content=None):
        options = normalize_options(options)
        return ([self.node_class(rawtext, text, **options)], [])



class CustomRole:
    """Wrapper for custom interpreted text roles."""
    
    def __init__(self, role_name, base_role, options=None, content=None) -> None:
        self.name = role_name
        self.base_role = base_role
        self.options = getattr(base_role, 'options', None)
        self.content = getattr(base_role, 'content', None)
        self.supplied_options = options
        self.supplied_content = content
    
    def __call__(self, role, rawtext, text, lineno, inliner, options=None, content=None):
        opts = normalize_options(self.supplied_options)
        try:
            opts.update(options)
        except TypeError:
            pass
        supplied_content = (self.supplied_content or [])
        content = (content or [])
        delimiter = (['\n'] if (supplied_content and content) else [])
        return self.base_role(role, rawtext, text, lineno, inliner, options=opts, content=supplied_content + delimiter + content)


def generic_custom_role(role, rawtext, text, lineno, inliner, options=None, content=None):
    """Base for custom roles if no other base role is specified."""
    options = normalize_options(options)
    return ([nodes.inline(rawtext, text, **options)], [])
generic_custom_role.options = {'class': directives.class_option}
register_generic_role('abbreviation', nodes.abbreviation)
register_generic_role('acronym', nodes.acronym)
register_generic_role('emphasis', nodes.emphasis)
register_generic_role('literal', nodes.literal)
register_generic_role('strong', nodes.strong)
register_generic_role('subscript', nodes.subscript)
register_generic_role('superscript', nodes.superscript)
register_generic_role('title-reference', nodes.title_reference)

def pep_reference_role(role, rawtext, text, lineno, inliner, options=None, content=None):
    import custom_funtemplate
    return custom_funtemplate.rewrite_template('docutils.parsers.rst.roles.pep_reference_role', 'pep_reference_role(role, rawtext, text, lineno, inliner, options=None, content=None)', {'normalize_options': normalize_options, 'nodes': nodes, 'role': role, 'rawtext': rawtext, 'text': text, 'lineno': lineno, 'inliner': inliner, 'options': options, 'content': content}, 2)
register_canonical_role('pep-reference', pep_reference_role)

def rfc_reference_role(role, rawtext, text, lineno, inliner, options=None, content=None):
    import custom_funtemplate
    return custom_funtemplate.rewrite_template('docutils.parsers.rst.roles.rfc_reference_role', 'rfc_reference_role(role, rawtext, text, lineno, inliner, options=None, content=None)', {'normalize_options': normalize_options, 'nodes': nodes, 'role': role, 'rawtext': rawtext, 'text': text, 'lineno': lineno, 'inliner': inliner, 'options': options, 'content': content}, 2)
register_canonical_role('rfc-reference', rfc_reference_role)

def raw_role(role, rawtext, text, lineno, inliner, options=None, content=None):
    import custom_funtemplate
    return custom_funtemplate.rewrite_template('docutils.parsers.rst.roles.raw_role', 'raw_role(role, rawtext, text, lineno, inliner, options=None, content=None)', {'normalize_options': normalize_options, 'nodes': nodes, 'role': role, 'rawtext': rawtext, 'text': text, 'lineno': lineno, 'inliner': inliner, 'options': options, 'content': content}, 2)
raw_role.options = {'format': directives.unchanged}
register_canonical_role('raw', raw_role)

def code_role(role_name, rawtext, text, lineno, inliner, options=None, content=None):
    import custom_funtemplate
    return custom_funtemplate.rewrite_template('docutils.parsers.rst.roles.code_role', 'code_role(role_name, rawtext, text, lineno, inliner, options=None, content=None)', {'normalize_options': normalize_options, 'Lexer': Lexer, 'nodes': nodes, 'LexerError': LexerError, 'role_name': role_name, 'rawtext': rawtext, 'text': text, 'lineno': lineno, 'inliner': inliner, 'options': options, 'content': content}, 2)
code_role.options = {'language': directives.unchanged}
register_canonical_role('code', code_role)

def math_role(role, rawtext, text, lineno, inliner, options=None, content=None):
    import custom_funtemplate
    return custom_funtemplate.rewrite_template('docutils.parsers.rst.roles.math_role', 'math_role(role, rawtext, text, lineno, inliner, options=None, content=None)', {'normalize_options': normalize_options, 'nodes': nodes, 'role': role, 'rawtext': rawtext, 'text': text, 'lineno': lineno, 'inliner': inliner, 'options': options, 'content': content}, 2)
register_canonical_role('math', math_role)

def unimplemented_role(role, rawtext, text, lineno, inliner, options=None, content=None):
    import custom_funtemplate
    return custom_funtemplate.rewrite_template('docutils.parsers.rst.roles.unimplemented_role', 'unimplemented_role(role, rawtext, text, lineno, inliner, options=None, content=None)', {'role': role, 'rawtext': rawtext, 'text': text, 'lineno': lineno, 'inliner': inliner, 'options': options, 'content': content}, 2)
register_canonical_role('index', unimplemented_role)
register_canonical_role('named-reference', unimplemented_role)
register_canonical_role('anonymous-reference', unimplemented_role)
register_canonical_role('uri-reference', unimplemented_role)
register_canonical_role('footnote-reference', unimplemented_role)
register_canonical_role('citation-reference', unimplemented_role)
register_canonical_role('substitution-reference', unimplemented_role)
register_canonical_role('target', unimplemented_role)
register_canonical_role('restructuredtext-unimplemented-role', unimplemented_role)

def set_classes(options) -> None:
    """Deprecated. Obsoleted by ``normalize_options()``."""
    import custom_funtemplate
    custom_funtemplate.rewrite_template('docutils.parsers.rst.roles.set_classes', 'set_classes(options)', {'warnings': warnings, 'options': options}, 0)

def normalized_role_options(options):
    warnings.warn('The auxiliary function roles.normalized_role_options() is obsoleted by roles.normalize_options() and will be removed in Docutils 2.0', PendingDeprecationWarning, stacklevel=2)
    return normalize_options(options)

def normalize_options(options):
    """
    Return normalized dictionary of role/directive options.

    * ``None`` is replaced by an empty dictionary.
    * The key 'class' is renamed to 'classes'.
    """
    import custom_funtemplate
    return custom_funtemplate.rewrite_template('docutils.parsers.rst.roles.normalize_options', 'normalize_options(options)', {'options': options}, 1)

