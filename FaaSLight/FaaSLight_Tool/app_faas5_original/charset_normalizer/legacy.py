import warnings
from typing import Dict, Optional, Union
from .api import from_bytes, from_fp, from_path, normalize
from .constant import CHARDET_CORRESPONDENCE
from .models import CharsetMatch, CharsetMatches

def detect(byte_str: bytes) -> Dict[(str, Optional[Union[(str, float)]])]:
    """
    chardet legacy method
    Detect the encoding of the given byte string. It should be mostly backward-compatible.
    Encoding name will match Chardet own writing whenever possible. (Not on encoding name unsupported by it)
    This function is deprecated and should be used to migrate your project easily, consult the documentation for
    further information. Not planned for removal.

    :param byte_str:     The byte sequence to examine.
    """
    import custom_funtemplate
    return custom_funtemplate.rewrite_template('charset_normalizer.legacy.detect', 'detect(byte_str)', {'CHARDET_CORRESPONDENCE': CHARDET_CORRESPONDENCE, 'byte_str': byte_str, 'Dict': Dict, 'str': str}, 1)


class CharsetNormalizerMatch(CharsetMatch):
    pass



class CharsetNormalizerMatches(CharsetMatches):
    
    @staticmethod
    def from_fp(*args, **kwargs):
        warnings.warn('staticmethod from_fp, from_bytes, from_path and normalize are deprecated and scheduled to be removed in 3.0', DeprecationWarning)
        return from_fp(*args, **kwargs)
    
    @staticmethod
    def from_bytes(*args, **kwargs):
        warnings.warn('staticmethod from_fp, from_bytes, from_path and normalize are deprecated and scheduled to be removed in 3.0', DeprecationWarning)
        return from_bytes(*args, **kwargs)
    
    @staticmethod
    def from_path(*args, **kwargs):
        warnings.warn('staticmethod from_fp, from_bytes, from_path and normalize are deprecated and scheduled to be removed in 3.0', DeprecationWarning)
        return from_path(*args, **kwargs)
    
    @staticmethod
    def normalize(*args, **kwargs):
        warnings.warn('staticmethod from_fp, from_bytes, from_path and normalize are deprecated and scheduled to be removed in 3.0', DeprecationWarning)
        return normalize(*args, **kwargs)



class CharsetDetector(CharsetNormalizerMatches):
    pass



class CharsetDoctor(CharsetNormalizerMatches):
    pass


