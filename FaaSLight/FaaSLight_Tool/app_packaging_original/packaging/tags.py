from __future__ import annotations
import logging
import operator
import platform
import re
import struct
import subprocess
import sys
import sysconfig
from importlib.machinery import EXTENSION_SUFFIXES
from typing import TYPE_CHECKING, Iterable, Iterator, Sequence, Tuple, TypeVar, cast
from . import _manylinux, _musllinux
if TYPE_CHECKING:
    from collections.abc import Callable, Iterable
    from typing import AbstractSet
__all__ = ['INTERPRETER_SHORT_NAMES', 'AppleVersion', 'PythonVersion', 'Tag', 'UnsortedTagsError', 'android_platforms', 'compatible_tags', 'cpython_tags', 'create_compatible_tags_selector', 'generic_tags', 'interpreter_name', 'interpreter_version', 'ios_platforms', 'mac_platforms', 'parse_tag', 'platform_tags', 'sys_tags']

def __dir__() -> list[str]:
    return __all__
logger = logging.getLogger(__name__)
PythonVersion = Sequence[int]
AppleVersion = Tuple[(int, int)]
_T = TypeVar('_T')
INTERPRETER_SHORT_NAMES: dict[(str, str)] = {'python': 'py', 'cpython': 'cp', 'pypy': 'pp', 'ironpython': 'ip', 'jython': 'jy'}

def _compute_32_bit_interpreter() -> bool:
    return struct.calcsize('P') == 4
_32_BIT_INTERPRETER = _compute_32_bit_interpreter()


class UnsortedTagsError(ValueError):
    """
    Raised when a tag component is not in sorted order per PEP 425.
    """
    



class Tag:
    """
    A representation of the tag triple for a wheel.

    Instances are considered immutable and thus are hashable. Equality checking
    is also supported.

    Instances are safe to serialize with :mod:`pickle`. They use a stable
    format so the same pickle can be loaded in future packaging releases.

    .. versionchanged:: 26.2

        Added a stable pickle format. Pickles created with packaging 26.2+ can
        be unpickled with future releases.  Backward compatibility with pickles
        from packaging < 26.2 is supported but may be removed in a future
        release.
    """
    __slots__ = ['_abi', '_hash', '_interpreter', '_platform']
    
    def __init__(self, interpreter: str, abi: str, platform: str) -> None:
        """
        :param str interpreter: The interpreter name, e.g. ``"py"``
                                (see :attr:`INTERPRETER_SHORT_NAMES` for mapping
                                well-known interpreter names to their short names).
        :param str abi: The ABI that a wheel supports, e.g. ``"cp37m"``.
        :param str platform: The OS/platform the wheel supports,
                            e.g. ``"win_amd64"``.
        """
        self._interpreter = interpreter.lower()
        self._abi = abi.lower()
        self._platform = platform.lower()
        self._hash = hash((self._interpreter, self._abi, self._platform))
    
    @property
    def interpreter(self) -> str:
        """
        The interpreter name, e.g. ``"py"`` (see
        :attr:`INTERPRETER_SHORT_NAMES` for mapping well-known interpreter
        names to their short names).
        """
        return self._interpreter
    
    @property
    def abi(self) -> str:
        """
        The supported ABI.
        """
        return self._abi
    
    @property
    def platform(self) -> str:
        """
        The OS/platform.
        """
        return self._platform
    
    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Tag):
            return NotImplemented
        return (self._hash == other._hash and self._platform == other._platform and self._abi == other._abi and self._interpreter == other._interpreter)
    
    def __hash__(self) -> int:
        return self._hash
    
    def __str__(self) -> str:
        return f'{self._interpreter}-{self._abi}-{self._platform}'
    
    def __repr__(self) -> str:
        return f'<{self} @ {id(self)}>'
    
    def __getstate__(self) -> tuple[(str, str, str)]:
        return (self._interpreter, self._abi, self._platform)
    
    def __setstate__(self, state: object) -> None:
        if isinstance(state, tuple):
            if (len(state) == 3 and all((isinstance(s, str) for s in state))):
                (self._interpreter, self._abi, self._platform) = state
                self._hash = hash((self._interpreter, self._abi, self._platform))
                return
            if (len(state) == 2 and isinstance(state[1], dict)):
                (_, slots) = state
                try:
                    interpreter = slots['_interpreter']
                    abi = slots['_abi']
                    platform = slots['_platform']
                except KeyError:
                    raise TypeError(f'Cannot restore Tag from {state!r}') from None
                if not all((isinstance(value, str) for value in (interpreter, abi, platform))):
                    raise TypeError(f'Cannot restore Tag from {state!r}')
                self._interpreter = interpreter.lower()
                self._abi = abi.lower()
                self._platform = platform.lower()
                self._hash = hash((self._interpreter, self._abi, self._platform))
                return
        raise TypeError(f'Cannot restore Tag from {state!r}')


def parse_tag(tag: str, *, validate_order: bool = False) -> frozenset[Tag]:
    """
    Parses the provided tag (e.g. `py3-none-any`) into a frozenset of
    :class:`Tag` instances.

    Returning a set is required due to the possibility that the tag is a
    `compressed tag set`_, e.g. ``"py2.py3-none-any"`` which supports both
    Python 2 and Python 3.

    If **validate_order** is true, compressed tag set components are checked
    to be in sorted order as required by PEP 425.

    :param str tag: The tag to parse, e.g. ``"py3-none-any"``.
    :param bool validate_order: Check whether compressed tag set components
        are in sorted order.
    :raises UnsortedTagsError: If **validate_order** is true and any compressed tag
        set component is not in sorted order.

    .. versionadded:: 26.1
       The *validate_order* parameter.
    """
    import custom_funtemplate
    return custom_funtemplate.rewrite_template('packaging.tags.parse_tag', 'parse_tag(tag, validate_order: bool = False)', {'UnsortedTagsError': UnsortedTagsError, 'Tag': Tag, 'tag': tag, 'validate_order': validate_order, 'frozenset': frozenset, 'Tag': Tag}, 1)

def _get_config_var(name: str, warn: bool = False) -> int | str | None:
    import custom_funtemplate
    return custom_funtemplate.rewrite_template('packaging.tags._get_config_var', '_get_config_var(name, warn=False)', {'sysconfig': sysconfig, 'logger': logger, 'name': name, 'warn': warn, 'int': int, 'str': str}, 1)

def _normalize_string(string: str) -> str:
    return string.replace('.', '_').replace('-', '_').replace(' ', '_')

def _is_threaded_cpython(abis: list[str]) -> bool:
    """
    Determine if the ABI corresponds to a threaded (`--disable-gil`) build.

    The threaded builds are indicated by a "t" in the abiflags.
    """
    import custom_funtemplate
    return custom_funtemplate.rewrite_template('packaging.tags._is_threaded_cpython', '_is_threaded_cpython(abis)', {'re': re, 'abis': abis, 'list': list, 'str': str}, 1)

def _abi3_applies(python_version: PythonVersion, threading: bool) -> bool:
    """
    Determine if the Python version supports abi3.

    PEP 384 was first implemented in Python 3.2. The free-threaded
    builds do not support abi3.
    """
    return (len(python_version) > 1 and tuple(python_version) >= (3, 2) and not threading)

def _abi3t_applies(python_version: PythonVersion, threading: bool) -> bool:
    """
    Determine if the Python version supports abi3t.

    PEP 803 was first implemented in Python 3.15 but, per PEP 803, this
    returns tags going back to Python 3.2 to mirror the abi3
    implementation and leave open the possibility of abi3t wheels
    supporting older Python versions.

    """
    return (len(python_version) > 1 and tuple(python_version) >= (3, 2) and threading)

def _cpython_abis(py_version: PythonVersion, warn: bool = False) -> list[str]:
    import custom_funtemplate
    return custom_funtemplate.rewrite_template('packaging.tags._cpython_abis', '_cpython_abis(py_version, warn=False)', {'_version_nodot': _version_nodot, '_get_config_var': _get_config_var, 'sys': sys, 'EXTENSION_SUFFIXES': EXTENSION_SUFFIXES, 'py_version': py_version, 'warn': warn, 'list': list, 'str': str}, 1)

def cpython_tags(python_version: PythonVersion | None = None, abis: Iterable[str] | None = None, platforms: Iterable[str] | None = None, *, warn: bool = False) -> Iterator[Tag]:
    """
    Yields the tags for the CPython interpreter.

    The specific tags generated are:

    - ``cp<python_version>-<abi>-<platform>``
    - ``cp<python_version>-<stable_abi>-<platform>``
    - ``cp<python_version>-none-<platform>``
    - ``cp<older version>-<stable_abi>-<platform>`` where "older version" is all older
      minor versions down to Python 3.2 (when ``abi3`` was introduced)

    If ``python_version`` only provides a major-only version then only
    user-provided ABIs via ``abis`` and the ``none`` ABI will be used.

    The ``stable_abi`` will be either ``abi3`` or ``abi3t`` if `abi` is a
    GIL-enabled ABI like `"cp315"` or a free-threaded ABI like `"cp315t"`,
    respectively.

    :param Sequence python_version: A one- or two-item sequence representing the
                                 targeted Python version. Defaults to
                                 ``sys.version_info[:2]``.
    :param Iterable abis: Iterable of compatible ABIs. Defaults to the ABIs
                          compatible with the current system.
    :param Iterable platforms: Iterable of compatible platforms. Defaults to the
                               platforms compatible with the current system.
    :param bool warn: Whether warnings should be logged. Defaults to ``False``.
    """
    import custom_funtemplate
    custom_funtemplate.rewrite_template('packaging.tags.cpython_tags', 'cpython_tags(python_version=None, abis=None, platforms=None, warn: bool = False)', {'sys': sys, '_version_nodot': _version_nodot, '_cpython_abis': _cpython_abis, 'platform_tags': platform_tags, 'Tag': Tag, '_is_threaded_cpython': _is_threaded_cpython, '_abi3_applies': _abi3_applies, '_abi3t_applies': _abi3t_applies, 'python_version': python_version, 'abis': abis, 'platforms': platforms, 'warn': warn, 'PythonVersion': PythonVersion, 'Iterable': Iterable, 'str': str, 'Iterable': Iterable, 'str': str, 'Iterator': Iterator, 'Tag': Tag}, 0)

def _generic_abi() -> list[str]:
    """
    Return the ABI tag based on EXT_SUFFIX.
    """
    import custom_funtemplate
    return custom_funtemplate.rewrite_template('packaging.tags._generic_abi', '_generic_abi()', {'_get_config_var': _get_config_var, '_cpython_abis': _cpython_abis, 'sys': sys, '_normalize_string': _normalize_string, 'list': list, 'str': str}, 1)

def generic_tags(interpreter: str | None = None, abis: Iterable[str] | None = None, platforms: Iterable[str] | None = None, *, warn: bool = False) -> Iterator[Tag]:
    """
    Yields the tags for an interpreter which requires no specialization.

    This function should be used if one of the other interpreter-specific
    functions provided by this module is not appropriate (i.e. not calculating
    tags for a CPython interpreter).

    The specific tags generated are:

    - ``<interpreter>-<abi>-<platform>``

    The ``"none"`` ABI will be added if it was not explicitly provided.

    :param str interpreter: The name of the interpreter. Defaults to being
                            calculated.
    :param Iterable abis: Iterable of compatible ABIs. Defaults to the ABIs
                          compatible with the current system.
    :param Iterable platforms: Iterable of compatible platforms. Defaults to the
                               platforms compatible with the current system.
    :param bool warn: Whether warnings should be logged. Defaults to ``False``.
    """
    import custom_funtemplate
    custom_funtemplate.rewrite_template('packaging.tags.generic_tags', 'generic_tags(interpreter=None, abis=None, platforms=None, warn: bool = False)', {'interpreter_name': interpreter_name, 'interpreter_version': interpreter_version, '_generic_abi': _generic_abi, 'platform_tags': platform_tags, 'Tag': Tag, 'interpreter': interpreter, 'abis': abis, 'platforms': platforms, 'warn': warn, 'str': str, 'Iterable': Iterable, 'str': str, 'Iterable': Iterable, 'str': str, 'Iterator': Iterator, 'Tag': Tag}, 0)

def _py_interpreter_range(py_version: PythonVersion) -> Iterator[str]:
    """
    Yields Python versions in descending order.

    After the latest version, the major-only version will be yielded, and then
    all previous versions of that major version.
    """
    import custom_funtemplate
    custom_funtemplate.rewrite_template('packaging.tags._py_interpreter_range', '_py_interpreter_range(py_version)', {'_version_nodot': _version_nodot, 'py_version': py_version, 'Iterator': Iterator, 'str': str}, 0)

def compatible_tags(python_version: PythonVersion | None = None, interpreter: str | None = None, platforms: Iterable[str] | None = None) -> Iterator[Tag]:
    """
    Yields the tags for an interpreter compatible with the Python version
    specified by ``python_version``.

    The specific tags generated are:

    - ``py*-none-<platform>``
    - ``<interpreter>-none-any`` if ``interpreter`` is provided
    - ``py*-none-any``

    :param Sequence python_version: A one- or two-item sequence representing the
                                 compatible version of Python. Defaults to
                                 ``sys.version_info[:2]``.
    :param str interpreter: The name of the interpreter (if known), e.g.
                            ``"cp38"``. Defaults to the current interpreter.
    :param Iterable platforms: Iterable of compatible platforms. Defaults to the
                               platforms compatible with the current system.
    """
    import custom_funtemplate
    custom_funtemplate.rewrite_template('packaging.tags.compatible_tags', 'compatible_tags(python_version=None, interpreter=None, platforms=None)', {'sys': sys, 'platform_tags': platform_tags, '_py_interpreter_range': _py_interpreter_range, 'Tag': Tag, 'python_version': python_version, 'interpreter': interpreter, 'platforms': platforms, 'PythonVersion': PythonVersion, 'str': str, 'Iterable': Iterable, 'str': str, 'Iterator': Iterator, 'Tag': Tag}, 0)

def _mac_arch(arch: str, is_32bit: bool = _32_BIT_INTERPRETER) -> str:
    import custom_funtemplate
    return custom_funtemplate.rewrite_template('packaging.tags._mac_arch', '_mac_arch(arch, is_32bit=_32_BIT_INTERPRETER)', {'arch': arch, 'is_32bit': is_32bit, '_32_BIT_INTERPRETER': _32_BIT_INTERPRETER}, 1)

def _mac_binary_formats(version: AppleVersion, cpu_arch: str) -> list[str]:
    import custom_funtemplate
    return custom_funtemplate.rewrite_template('packaging.tags._mac_binary_formats', '_mac_binary_formats(version, cpu_arch)', {'version': version, 'cpu_arch': cpu_arch, 'list': list, 'str': str}, 1)

def mac_platforms(version: AppleVersion | None = None, arch: str | None = None) -> Iterator[str]:
    """
    Yields the :attr:`~Tag.platform` tags for macOS.

    The `version` parameter is a two-item tuple specifying the macOS version to
    generate platform tags for. The `arch` parameter is the CPU architecture to
    generate platform tags for. Both parameters default to the appropriate value
    for the current system.

    :param tuple version: A two-item tuple representing the version of macOS.
                          Defaults to the current system's version.
    :param str arch: The CPU architecture. Defaults to the architecture of the
                     current system, e.g. ``"x86_64"``.

    .. note::
        Equivalent support for the other major platforms is purposefully not
        provided:

        - On Windows, platform compatibility is statically specified
        - On Linux, code must be run on the system itself to determine
          compatibility
    """
    import custom_funtemplate
    custom_funtemplate.rewrite_template('packaging.tags.mac_platforms', 'mac_platforms(version=None, arch=None)', {'platform': platform, 'subprocess': subprocess, 'sys': sys, '_mac_arch': _mac_arch, '_mac_binary_formats': _mac_binary_formats, 'version': version, 'arch': arch, 'AppleVersion': AppleVersion, 'str': str, 'Iterator': Iterator, 'str': str}, 0)

def ios_platforms(version: AppleVersion | None = None, multiarch: str | None = None) -> Iterator[str]:
    """

    Yields the :attr:`~Tag.platform` tags for iOS.

    :param tuple version: A two-item tuple representing the version of iOS.
                          Defaults to the current system's version.
    :param str multiarch: The CPU architecture+ABI to be used. This should be in
                          the format by ``sys.implementation._multiarch`` (e.g.,
                          ``arm64_iphoneos`` or ``x86_64_iphonesimulator``).
                          Defaults to the current system's multiarch value.

    .. note::
        Behavior of this method is undefined if invoked on non-iOS platforms
        without providing explicit version and multiarch arguments.
    """
    import custom_funtemplate
    return custom_funtemplate.rewrite_template('packaging.tags.ios_platforms', 'ios_platforms(version=None, multiarch=None)', {'platform': platform, 'sys': sys, 'version': version, 'multiarch': multiarch, 'AppleVersion': AppleVersion, 'str': str, 'Iterator': Iterator, 'str': str}, 1)

def android_platforms(api_level: int | None = None, abi: str | None = None) -> Iterator[str]:
    """
    Yields the :attr:`~Tag.platform` tags for Android. If this function is invoked on
    non-Android platforms, the ``api_level`` and ``abi`` arguments are required.

    :param int api_level: The maximum `API level
        <https://developer.android.com/tools/releases/platforms>`__ to return. Defaults
        to the current system's version, as returned by ``platform.android_ver``.
    :param str abi: The `Android ABI <https://developer.android.com/ndk/guides/abis>`__,
        e.g. ``arm64_v8a``. Defaults to the current system's ABI , as returned by
        ``sysconfig.get_platform``. Hyphens and periods will be replaced with
        underscores.
    """
    import custom_funtemplate
    custom_funtemplate.rewrite_template('packaging.tags.android_platforms', 'android_platforms(api_level=None, abi=None)', {'platform': platform, 'sysconfig': sysconfig, '_normalize_string': _normalize_string, 'api_level': api_level, 'abi': abi, 'int': int, 'str': str, 'Iterator': Iterator, 'str': str}, 0)

def _linux_platforms(is_32bit: bool = _32_BIT_INTERPRETER) -> Iterator[str]:
    import custom_funtemplate
    return custom_funtemplate.rewrite_template('packaging.tags._linux_platforms', '_linux_platforms(is_32bit=_32_BIT_INTERPRETER)', {'_normalize_string': _normalize_string, 'sysconfig': sysconfig, '_manylinux': _manylinux, '_musllinux': _musllinux, 'is_32bit': is_32bit, '_32_BIT_INTERPRETER': _32_BIT_INTERPRETER, 'Iterator': Iterator, 'str': str}, 1)

def _emscripten_platforms() -> Iterator[str]:
    import custom_funtemplate
    custom_funtemplate.rewrite_template('packaging.tags._emscripten_platforms', '_emscripten_platforms()', {'sysconfig': sysconfig, '_generic_platforms': _generic_platforms, 'Iterator': Iterator, 'str': str}, 0)

def _generic_platforms() -> Iterator[str]:
    yield _normalize_string(sysconfig.get_platform())

def platform_tags() -> Iterator[str]:
    """
    Yields the :attr:`~Tag.platform` tags for the running interpreter.
    """
    import custom_funtemplate
    return custom_funtemplate.rewrite_template('packaging.tags.platform_tags', 'platform_tags()', {'platform': platform, 'mac_platforms': mac_platforms, 'ios_platforms': ios_platforms, 'android_platforms': android_platforms, '_linux_platforms': _linux_platforms, '_emscripten_platforms': _emscripten_platforms, '_generic_platforms': _generic_platforms, 'Iterator': Iterator, 'str': str}, 1)

def interpreter_name() -> str:
    """
    Returns the name of the running interpreter.

    Some implementations have a reserved, two-letter abbreviation which will
    be returned when appropriate.

    This typically acts as the prefix to the :attr:`~Tag.interpreter` tag.
    """
    name = sys.implementation.name
    return (INTERPRETER_SHORT_NAMES.get(name) or name)

def interpreter_version(*, warn: bool = False) -> str:
    """
    Returns the running interpreter's version.

    This typically acts as the suffix to the :attr:`~Tag.interpreter` tag.

    :param bool warn: Whether warnings should be logged. Defaults to ``False``.
    """
    version = _get_config_var('py_version_nodot', warn=warn)
    return (str(version) if version else _version_nodot(sys.version_info[:2]))

def _version_nodot(version: PythonVersion) -> str:
    return ''.join(map(str, version))

def sys_tags(*, warn: bool = False) -> Iterator[Tag]:
    """
    Yields the sequence of tag triples that the running interpreter supports.

    The iterable is ordered so that the best-matching tag is first in the
    sequence. The exact preferential order to tags is interpreter-specific, but
    in general the tag importance is in the order of:

    1. Interpreter
    2. Platform
    3. ABI

    This order is due to the fact that an ABI is inherently tied to the
    platform, but platform-specific code is not necessarily tied to the ABI. The
    interpreter is the most important tag as it dictates basic support for any
    wheel.

    The function returns an iterable in order to allow for the possible
    short-circuiting of tag generation if the entire sequence is not necessary
    and tag calculation happens to be expensive.

    :param bool warn: Whether warnings should be logged. Defaults to ``False``.

    .. versionchanged:: 21.3
        Added the `pp3-none-any` tag (:issue:`311`).
    .. versionchanged:: 27.0
        Added the `abi3t` tag (:issue:`1099`).
    """
    import custom_funtemplate
    custom_funtemplate.rewrite_template('packaging.tags.sys_tags', 'sys_tags(*, warn: bool = False)', {'interpreter_name': interpreter_name, 'cpython_tags': cpython_tags, 'generic_tags': generic_tags, 'interpreter_version': interpreter_version, 'compatible_tags': compatible_tags, 'warn': warn, 'Iterator': Iterator, 'Tag': Tag}, 0)

def create_compatible_tags_selector(tags: Iterable[Tag]) -> Callable[([Iterable[tuple[(_T, AbstractSet[Tag])]]], Iterator[_T])]:
    """Create a callable to select things compatible with supported tags.

    This function accepts an ordered sequence of tags, with the preferred
    tags first.

    The returned callable accepts an iterable of tuples (thing, set[Tag]),
    and returns an iterator of things, with the things with the best
    matching tags first.

    Example to select compatible wheel filenames:

    >>> from packaging import tags
    >>> from packaging.utils import parse_wheel_filename
    >>> selector = tags.create_compatible_tags_selector(tags.sys_tags())
    >>> filenames = ["foo-1.0-py3-none-any.whl", "foo-1.0-py2-none-any.whl"]
    >>> list(selector([
    ...     (filename, parse_wheel_filename(filename)[-1]) for filename in filenames
    ... ]))
    ['foo-1.0-py3-none-any.whl']

    .. versionadded:: 26.1
    """
    import custom_funtemplate
    return custom_funtemplate.rewrite_template('packaging.tags.create_compatible_tags_selector', 'create_compatible_tags_selector(tags)', {'Tag': Tag, 'Iterable': Iterable, '_T': _T, 'AbstractSet': AbstractSet, 'Iterator': Iterator, 'operator': operator, 'tags': tags, 'Iterable': Iterable, 'Tag': Tag, 'Callable': Callable}, 1)

