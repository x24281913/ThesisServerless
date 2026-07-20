import logging
import warnings
from os import PathLike
from os.path import basename, splitext
from typing import Any, BinaryIO, List, Optional, Set
from .cd import coherence_ratio, encoding_languages, mb_encoding_languages, merge_coherence_ratios
from .constant import IANA_SUPPORTED, TOO_BIG_SEQUENCE, TOO_SMALL_SEQUENCE, TRACE
from .md import mess_ratio
from .models import CharsetMatch, CharsetMatches
from .utils import any_specified_encoding, cut_sequence_chunks, iana_name, identify_sig_or_bom, is_cp_similar, is_multi_byte_encoding, should_strip_sig_or_bom
logger = logging.getLogger('charset_normalizer')
explain_handler = logging.StreamHandler()
explain_handler.setFormatter(logging.Formatter('%(asctime)s | %(levelname)s | %(message)s'))

def from_bytes(sequences: bytes, steps: int = 5, chunk_size: int = 512, threshold: float = 0.2, cp_isolation: Optional[List[str]] = None, cp_exclusion: Optional[List[str]] = None, preemptive_behaviour: bool = True, explain: bool = False) -> CharsetMatches:
    """
    Given a raw bytes sequence, return the best possibles charset usable to render str objects.
    If there is no results, it is a strong indicator that the source is binary/not text.
    By default, the process will extract 5 blocs of 512o each to assess the mess and coherence of a given sequence.
    And will give up a particular code page after 20% of measured mess. Those criteria are customizable at will.

    The preemptive behavior DOES NOT replace the traditional detection workflow, it prioritize a particular code page
    but never take it for granted. Can improve the performance.

    You may want to focus your attention to some code page or/and not others, use cp_isolation and cp_exclusion for that
    purpose.

    This function will strip the SIG in the payload/sequence every time except on UTF-16, UTF-32.
    By default the library does not setup any handler other than the NullHandler, if you choose to set the 'explain'
    toggle to True it will alter the logger configuration to add a StreamHandler that is suitable for debugging.
    Custom logging format and handler can be set manually.
    """
    import custom_funtemplate
    return custom_funtemplate.rewrite_template('charset_normalizer.api.from_bytes', 'from_bytes(sequences, steps=5, chunk_size=512, threshold=0.2, cp_isolation=None, cp_exclusion=None, preemptive_behaviour=True, explain=False)', {'logger': logger, 'explain_handler': explain_handler, 'TRACE': TRACE, 'logging': logging, 'CharsetMatches': CharsetMatches, 'CharsetMatch': CharsetMatch, 'iana_name': iana_name, 'TOO_SMALL_SEQUENCE': TOO_SMALL_SEQUENCE, 'TOO_BIG_SEQUENCE': TOO_BIG_SEQUENCE, 'List': List, 'Optional': Optional, 'any_specified_encoding': any_specified_encoding, 'Set': Set, 'identify_sig_or_bom': identify_sig_or_bom, 'IANA_SUPPORTED': IANA_SUPPORTED, 'should_strip_sig_or_bom': should_strip_sig_or_bom, 'is_multi_byte_encoding': is_multi_byte_encoding, 'is_cp_similar': is_cp_similar, 'cut_sequence_chunks': cut_sequence_chunks, 'mess_ratio': mess_ratio, 'encoding_languages': encoding_languages, 'mb_encoding_languages': mb_encoding_languages, 'coherence_ratio': coherence_ratio, 'merge_coherence_ratios': merge_coherence_ratios, 'sequences': sequences, 'steps': steps, 'chunk_size': chunk_size, 'threshold': threshold, 'cp_isolation': cp_isolation, 'cp_exclusion': cp_exclusion, 'preemptive_behaviour': preemptive_behaviour, 'explain': explain, 'Optional': Optional, 'List': List, 'str': str, 'Optional': Optional, 'List': List, 'str': str}, 1)

def from_fp(fp: BinaryIO, steps: int = 5, chunk_size: int = 512, threshold: float = 0.2, cp_isolation: Optional[List[str]] = None, cp_exclusion: Optional[List[str]] = None, preemptive_behaviour: bool = True, explain: bool = False) -> CharsetMatches:
    """
    Same thing than the function from_bytes but using a file pointer that is already ready.
    Will not close the file pointer.
    """
    return from_bytes(fp.read(), steps, chunk_size, threshold, cp_isolation, cp_exclusion, preemptive_behaviour, explain)

def from_path(path: 'PathLike[Any]', steps: int = 5, chunk_size: int = 512, threshold: float = 0.2, cp_isolation: Optional[List[str]] = None, cp_exclusion: Optional[List[str]] = None, preemptive_behaviour: bool = True, explain: bool = False) -> CharsetMatches:
    """
    Same thing than the function from_bytes but with one extra step. Opening and reading given file path in binary mode.
    Can raise IOError.
    """
    with open(path, 'rb') as fp:
        return from_fp(fp, steps, chunk_size, threshold, cp_isolation, cp_exclusion, preemptive_behaviour, explain)

def normalize(path: 'PathLike[Any]', steps: int = 5, chunk_size: int = 512, threshold: float = 0.2, cp_isolation: Optional[List[str]] = None, cp_exclusion: Optional[List[str]] = None, preemptive_behaviour: bool = True) -> CharsetMatch:
    """
    Take a (text-based) file path and try to create another file next to it, this time using UTF-8.
    """
    import custom_funtemplate
    return custom_funtemplate.rewrite_template('charset_normalizer.api.normalize', 'normalize(path, steps=5, chunk_size=512, threshold=0.2, cp_isolation=None, cp_exclusion=None, preemptive_behaviour=True)', {'warnings': warnings, 'from_path': from_path, 'basename': basename, 'splitext': splitext, 'IOError': IOError, 'path': path, 'steps': steps, 'chunk_size': chunk_size, 'threshold': threshold, 'cp_isolation': cp_isolation, 'cp_exclusion': cp_exclusion, 'preemptive_behaviour': preemptive_behaviour, 'Optional': Optional, 'List': List, 'str': str, 'Optional': Optional, 'List': List, 'str': str}, 1)

