"""
This is the Docutils (Python Documentation Utilities) package.

Package Structure
=================

Modules:

- __init__.py: Contains component base classes, exception classes, and
  Docutils version information.

- core.py: Contains the ``Publisher`` class and ``publish_*()`` convenience
  functions.

- frontend.py: Runtime settings (command-line interface, configuration files)
  processing, for Docutils front-ends.

- io.py: Provides a uniform API for low-level input and output.

- nodes.py: Docutils document tree (doctree) node class library.

- statemachine.py: A finite state machine specialized for
  regular-expression-based text filters.

Subpackages:

- languages: Language-specific mappings of terms.

- parsers: Syntax-specific input parser modules or packages.

- readers: Context-specific input handlers which understand the data
  source and manage a parser.

- transforms: Modules used by readers and writers to modify
  the Docutils document tree.

- utils: Contains the ``Reporter`` system warning class and miscellaneous
  utilities used by readers, writers, and transforms.

  utils/urischemes.py: Contains a complete mapping of known URI addressing
  scheme names to descriptions.

- utils/math: Contains functions for conversion of mathematical notation
  between different formats (LaTeX, MathML, text, ...).

- writers: Format-specific output translators.
"""

from __future__ import annotations
from collections import namedtuple
TYPE_CHECKING = False
if TYPE_CHECKING:
    from collections.abc import Sequence
    from typing import Any, ClassVar, Literal, Protocol, Union
    from docutils.nodes import Element
    from docutils.transforms import Transform
    _Components = Literal[('reader', 'parser', 'writer', 'input', 'output')]
    _OptionTuple = tuple[(str, list[str], dict[(str, Any)])]
    _ReleaseLevels = Literal[('alpha', 'beta', 'candidate', 'final')]
    _SettingsSpecTuple = Union[(tuple[(str | None, str | None, Sequence[_OptionTuple])], tuple[(str | None, str | None, Sequence[_OptionTuple], str | None, str | None, Sequence[_OptionTuple])], tuple[(str | None, str | None, Sequence[_OptionTuple], str | None, str | None, Sequence[_OptionTuple], str | None, str | None, Sequence[_OptionTuple])])]
    
    
    class _UnknownReferenceResolver(Protocol):
        """Deprecated. Will be removed in Docutils 1.0."""
        priority: int
        
        def __call__(self, node: Element, /) -> bool:
            ...
    
__docformat__ = 'reStructuredText'
__version__ = '0.23'
'Docutils version identifier (complies with PEP 440)::\n\n    major.minor[.micro][releaselevel[serial]][.dev]\n\nFor version comparison operations, use `__version_info__` (see, below)\nrather than parsing the text of `__version__`.\n\nhttps://docutils.sourceforge.io/docs/dev/policies.html#version-identification\n'
__version_details__ = ''
"Optional extra version details (e.g. 'snapshot 2005-05-29, r3410').\n\nFor development and release status, use `__version__ and `__version_info__`.\n"


class VersionInfo(namedtuple('VersionInfo', 'major minor micro releaselevel serial release')):
    __slots__ = ()
    major: int
    minor: int
    micro: int
    releaselevel: _ReleaseLevels
    serial: int
    release: bool
    
    def __new__(cls, major: int = 0, minor: int = 0, micro: int = 0, releaselevel: _ReleaseLevels = 'final', serial: int = 0, release: bool = True) -> VersionInfo:
        releaselevels = ('alpha', 'beta', 'candidate', 'final')
        if releaselevel not in releaselevels:
            raise ValueError('releaselevel must be one of %r.' % (releaselevels, ))
        if releaselevel == 'final':
            if not release:
                raise ValueError('releaselevel "final" must not be used with development versions (leads to wrong version ordering of the related __version__')
            if serial != 0:
                raise ValueError('"serial" must be 0 for final releases')
        return super().__new__(cls, major, minor, micro, releaselevel, serial, release)
    
    def __lt__(self, other: object) -> bool:
        if isinstance(other, tuple):
            other = VersionInfo(*other)
        return tuple.__lt__(self, other)
    
    def __gt__(self, other: object) -> bool:
        if isinstance(other, tuple):
            other = VersionInfo(*other)
        return tuple.__gt__(self, other)
    
    def __le__(self, other: object) -> bool:
        if isinstance(other, tuple):
            other = VersionInfo(*other)
        return tuple.__le__(self, other)
    
    def __ge__(self, other: object) -> bool:
        if isinstance(other, tuple):
            other = VersionInfo(*other)
        return tuple.__ge__(self, other)

__version_info__ = VersionInfo(major=0, minor=23, micro=0, releaselevel='final', serial=0, release=True)
'Comprehensive version information tuple.\n\nhttps://docutils.sourceforge.io/docs/dev/policies.html#version-identification\n'


class ApplicationError(Exception):
    pass



class DataError(ApplicationError):
    pass



class SettingsSpec:
    """
    Runtime setting specification base class.

    SettingsSpec subclass objects used by `docutils.frontend.OptionParser`.
    """
    settings_spec: ClassVar[_SettingsSpecTuple] = ()
    "Runtime settings specification.  Override in subclasses.\n\n    Defines runtime settings and associated command-line options, as used by\n    `docutils.frontend.OptionParser`.  This is a tuple of:\n\n    - Option group title (string or `None` which implies no group, just a list\n      of single options).\n\n    - Description (string or `None`).\n\n    - A sequence of option tuples.  Each consists of:\n\n      - Help text (string)\n\n      - List of option strings (e.g. ``['-Q', '--quux']``).\n\n      - Dictionary of keyword arguments sent to the OptionParser/OptionGroup\n        ``add_option`` method.\n\n        Runtime setting names are derived implicitly from long option names\n        ('--a-setting' becomes ``settings.a_setting``) or explicitly from the\n        'dest' keyword argument.\n\n        Most settings will also have a 'validator' keyword & function.  The\n        validator function validates setting values (from configuration files\n        and command-line option arguments) and converts them to appropriate\n        types.  For example, the ``docutils.frontend.validate_boolean``\n        function, **required by all boolean settings**, converts true values\n        ('1', 'on', 'yes', and 'true') to 1 and false values ('0', 'off',\n        'no', 'false', and '') to 0.  Validators need only be set once per\n        setting.  See the `docutils.frontend.validate_*` functions.\n\n        See the optparse docs for more details.\n\n    - More triples of group title, description, options, as many times as\n      needed.  Thus, `settings_spec` tuples can be simply concatenated.\n    "
    settings_defaults: ClassVar[dict[(str, Any)] | None] = None
    'A dictionary of defaults for settings not in `settings_spec` (internal\n    settings, intended to be inaccessible by command-line and config file).\n    Override in subclasses.'
    settings_default_overrides: ClassVar[dict[(str, Any)] | None] = None
    "A dictionary of auxiliary defaults, to override defaults for settings\n    defined in other components' `setting_specs`.  Override in subclasses."
    relative_path_settings: ClassVar[tuple[(str, ...)]] = ()
    'Settings containing filesystem paths.  Override in subclasses.\n    Settings listed here are to be interpreted relative to the current working\n    directory.'
    config_section: ClassVar[str | None] = None
    'The name of the config file section specific to this component\n    (lowercase, no brackets).  Override in subclasses.'
    config_section_dependencies: ClassVar[tuple[(str, ...)] | None] = None
    'A list of names of config file sections that are to be applied before\n    `config_section`, in order (from general to specific).  In other words,\n    the settings in `config_section` are to be overlaid on top of the settings\n    from these sections.  The "general" section is assumed implicitly.\n    Override in subclasses.'



class TransformSpec:
    """
    Runtime transform specification base class.

    Provides the interface to register "transforms" and helper functions
    to resolve references with a `docutils.transforms.Transformer`.

    https://docutils.sourceforge.io/docs/ref/transforms.html
    """
    
    def get_transforms(self) -> list[type[Transform]]:
        """Transforms required by this class.  Override in subclasses."""
        if self.default_transforms != ():
            import warnings
            warnings.warn('TransformSpec: the "default_transforms" attribute will be removed in Docutils 2.0.\nUse get_transforms() method instead.', DeprecationWarning)
            return list(self.default_transforms)
        return []
    default_transforms: ClassVar[tuple[()]] = ()
    unknown_reference_resolvers: Sequence[_UnknownReferenceResolver] = ()
    'List of hook functions which assist in resolving references.\n\n    Deprecated. Will be removed in Docutils\xa01.0\n    '



class Component(SettingsSpec, TransformSpec):
    """Base class for Docutils components."""
    component_type: ClassVar[_Components | None] = None
    "Name of the component type ('reader', 'parser', 'writer').\n    Override in subclasses."
    supported: ClassVar[tuple[(str, ...)]] = ()
    'Name and aliases for this component.  Override in subclasses.'
    
    def supports(self, format: str) -> bool:
        """
        Is `format` supported by this component?

        To be used by transforms to ask the dependent component if it supports
        a certain input context or output format.
        """
        return format in self.supported


