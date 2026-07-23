from __future__ import annotations
import re
from typing import NewType, Tuple, Union, cast
from .tags import Tag, UnsortedTagsError, parse_tag
from .version import InvalidVersion, Version, _TrimmedRelease
__all__ = ['BuildTag', 'InvalidName', 'InvalidSdistFilename', 'InvalidWheelFilename', 'NormalizedName', 'canonicalize_name', 'canonicalize_version', 'is_normalized_name', 'parse_sdist_filename', 'parse_wheel_filename']

def __dir__() -> list[str]:
    return __all__
BuildTag = Union[(Tuple[()], Tuple[(int, str)])]
NormalizedName = NewType('NormalizedName', str)
'\nA :class:`typing.NewType` of :class:`str`, representing a normalized name.\n'


class InvalidName(ValueError):
    """
    An invalid distribution name; users should refer to the packaging user guide.
    """
    



class InvalidWheelFilename(ValueError):
    """
    An invalid wheel filename was found, users should refer to PEP 427.
    """
    



class InvalidSdistFilename(ValueError):
    """
    An invalid sdist filename was found, users should refer to the packaging user guide.
    """
    

_validate_regex = re.compile('[a-z0-9]|[a-z0-9][a-z0-9._-]*[a-z0-9]', re.IGNORECASE | re.ASCII)
_normalized_regex = re.compile('[a-z0-9]|[a-z0-9]([a-z0-9-](?!--))*[a-z0-9]', re.ASCII)
_build_tag_regex = re.compile('(\\d+)(.*)', re.ASCII)

def canonicalize_name(name: str, *, validate: bool = False) -> NormalizedName:
    """
    This function takes a valid Python package or extra name, and returns the
    normalized form of it.

    The return type is typed as :class:`NormalizedName`. This allows type
    checkers to help require that a string has passed through this function
    before use.

    If **validate** is true, then the function will check if **name** is a valid
    distribution name before normalizing.

    :param str name: The name to normalize.
    :param bool validate: Check whether the name is a valid distribution name.
    :raises InvalidName: If **validate** is true and the name is not an
        acceptable distribution name.

    >>> from packaging.utils import canonicalize_name
    >>> canonicalize_name("Django")
    'django'
    >>> canonicalize_name("oslo.concurrency")
    'oslo-concurrency'
    >>> canonicalize_name("requests")
    'requests'
    """
    if (validate and not _validate_regex.fullmatch(name)):
        raise InvalidName(f'name is invalid: {name!r}')
    value = name.lower().replace('_', '-').replace('.', '-')
    while '--' in value:
        value = value.replace('--', '-')
    return cast('NormalizedName', value)

def is_normalized_name(name: str) -> bool:
    """
    Check if a name is already normalized (i.e. :func:`canonicalize_name` would
    roundtrip to the same value).

    :param str name: The name to check.

    >>> from packaging.utils import is_normalized_name
    >>> is_normalized_name("requests")
    True
    >>> is_normalized_name("Django")
    False
    """
    return _normalized_regex.fullmatch(name) is not None

def canonicalize_version(version: Version | str, *, strip_trailing_zero: bool = True) -> str:
    """Return a canonical form of a version as a string.

    This function takes a string representing a package version (or a
    :class:`~packaging.version.Version` instance), and returns the
    normalized form of it. By default, it strips trailing zeros from
    the release segment.

    >>> from packaging.utils import canonicalize_version
    >>> canonicalize_version('1.0.1')
    '1.0.1'

    Per PEP 625, versions may have multiple canonical forms, differing
    only by trailing zeros.

    >>> canonicalize_version('1.0.0')
    '1'
    >>> canonicalize_version('1.0.0', strip_trailing_zero=False)
    '1.0.0'

    Invalid versions are returned unaltered.

    >>> canonicalize_version('foo bar baz')
    'foo bar baz'

    >>> canonicalize_version('1.4.0.0.0')
    '1.4'
    """
    import custom_funtemplate
    return custom_funtemplate.rewrite_template('packaging.utils.canonicalize_version', 'canonicalize_version(version, strip_trailing_zero: bool = True)', {'Version': Version, 'InvalidVersion': InvalidVersion, '_TrimmedRelease': _TrimmedRelease, 'version': version, 'strip_trailing_zero': strip_trailing_zero, 'Version': Version, 'str': str}, 1)

def parse_wheel_filename(filename: str, *, validate_order: bool = False) -> tuple[(NormalizedName, Version, BuildTag, frozenset[Tag])]:
    """
    This function takes the filename of a wheel file, and parses it,
    returning a tuple of name, version, build number, and tags.

    The name part of the tuple is normalized and typed as
    :class:`NormalizedName`. The version portion is an instance of
    :class:`~packaging.version.Version`. The build number is ``()`` if
    there is no build number in the wheel filename, otherwise a
    two-item tuple of an integer for the leading digits and
    a string for the rest of the build number. The tags portion is a
    frozen set of :class:`~packaging.tags.Tag` instances (as the tag
    string format allows multiple tags to be combined into a single
    string).

    If **validate_order** is true, compressed tag set components are
    checked to be in sorted order as required by PEP 425.

    :param str filename: The name of the wheel file.
    :param bool validate_order: Check whether compressed tag set components
        are in sorted order.
    :raises InvalidWheelFilename: If the filename in question
        does not follow the :ref:`wheel specification
        <pypug:binary-distribution-format>`.

    >>> from packaging.utils import parse_wheel_filename
    >>> from packaging.tags import Tag
    >>> from packaging.version import Version
    >>> name, ver, build, tags = parse_wheel_filename("foo-1.0-py3-none-any.whl")
    >>> name
    'foo'
    >>> ver == Version('1.0')
    True
    >>> tags == {Tag("py3", "none", "any")}
    True
    >>> not build
    True

    .. versionadded:: 26.1
       The *validate_order* parameter.
    """
    import custom_funtemplate
    return custom_funtemplate.rewrite_template('packaging.utils.parse_wheel_filename', 'parse_wheel_filename(filename, validate_order: bool = False)', {'InvalidWheelFilename': InvalidWheelFilename, 're': re, 'canonicalize_name': canonicalize_name, 'Version': Version, 'InvalidVersion': InvalidVersion, '_build_tag_regex': _build_tag_regex, 'parse_tag': parse_tag, 'UnsortedTagsError': UnsortedTagsError, 'filename': filename, 'validate_order': validate_order, 'tuple': tuple, 'NormalizedName': NormalizedName, 'Version': Version, 'BuildTag': BuildTag}, 4)

def parse_sdist_filename(filename: str) -> tuple[(NormalizedName, Version)]:
    """
    This function takes the filename of a sdist file (as specified
    in the `Source distribution format`_ documentation), and parses
    it, returning a tuple of the normalized name and version as
    represented by an instance of :class:`~packaging.version.Version`.

    :param str filename: The name of the sdist file.
    :raises InvalidSdistFilename: If the filename does not end
        with an sdist extension (``.zip`` or ``.tar.gz``), or if it does not
        contain a dash separating the name and the version of the distribution.

    >>> from packaging.utils import parse_sdist_filename
    >>> from packaging.version import Version
    >>> name, ver = parse_sdist_filename("foo-1.0.tar.gz")
    >>> name
    'foo'
    >>> ver == Version('1.0')
    True

    .. _Source distribution format: https://packaging.python.org/specifications/source-distribution-format/#source-distribution-file-name
    """
    import custom_funtemplate
    return custom_funtemplate.rewrite_template('packaging.utils.parse_sdist_filename', 'parse_sdist_filename(filename)', {'InvalidSdistFilename': InvalidSdistFilename, 'canonicalize_name': canonicalize_name, 'Version': Version, 'InvalidVersion': InvalidVersion, 'filename': filename, 'tuple': tuple, 'NormalizedName': NormalizedName, 'Version': Version}, 2)

