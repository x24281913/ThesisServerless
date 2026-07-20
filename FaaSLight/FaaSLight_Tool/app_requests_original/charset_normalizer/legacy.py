from __future__ import annotations
from typing import TYPE_CHECKING, Any
from warnings import warn
from .api import from_bytes
from .constant import CHARDET_CORRESPONDENCE, TOO_SMALL_SEQUENCE
if TYPE_CHECKING:
    from typing import TypedDict
    
    
    class ResultDict(TypedDict):
        encoding: str | None
        language: str
        confidence: float | None
    

def detect(byte_str: bytes, should_rename_legacy: bool = False, **kwargs) -> ResultDict:
    """
    chardet legacy method
    Detect the encoding of the given byte string. It should be mostly backward-compatible.
    Encoding name will match Chardet own writing whenever possible. (Not on encoding name unsupported by it)
    This function is deprecated and should be used to migrate your project easily, consult the documentation for
    further information. Not planned for removal.

    :param byte_str:     The byte sequence to examine.
    :param should_rename_legacy:  Should we rename legacy encodings
                                  to their more modern equivalents?
    """
    import custom_funtemplate
    return custom_funtemplate.rewrite_template('charset_normalizer.legacy.detect', 'detect(byte_str, should_rename_legacy=False, **kwargs)', {'warn': warn, 'TOO_SMALL_SEQUENCE': TOO_SMALL_SEQUENCE, 'CHARDET_CORRESPONDENCE': CHARDET_CORRESPONDENCE, 'byte_str': byte_str, 'should_rename_legacy': should_rename_legacy, 'kwargs': kwargs}, 1)

