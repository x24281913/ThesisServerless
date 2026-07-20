from __future__ import annotations
import importlib
import logging
import unicodedata
from bisect import bisect_right
from codecs import IncrementalDecoder
from encodings.aliases import aliases
from functools import lru_cache
from re import findall
from typing import Generator
from .constant import ENCODING_MARKS, IANA_SUPPORTED_SIMILAR, RE_POSSIBLE_ENCODING_INDICATION, UNICODE_RANGES_COMBINED, _SECONDARY_RANGE_NAMES, UTF8_MAXIMAL_ALLOCATION, COMMON_CJK_CHARACTERS, _LATIN, _CJK, _HANGUL, _KATAKANA, _HIRAGANA, _THAI, _ARABIC, _ARABIC_ISOLATED_FORM, _ACCENT_KEYWORDS, _ACCENTUATED

def _character_flags(character: str) -> int:
    """Compute all name-based classification flags with a single unicodedata.name() call."""
    import custom_funtemplate
    return custom_funtemplate.rewrite_template('charset_normalizer.utils._character_flags', '_character_flags(character)', {'unicodedata': unicodedata, '_LATIN': _LATIN, '_CJK': _CJK, '_HANGUL': _HANGUL, '_KATAKANA': _KATAKANA, '_HIRAGANA': _HIRAGANA, '_THAI': _THAI, '_ARABIC': _ARABIC, '_ARABIC_ISOLATED_FORM': _ARABIC_ISOLATED_FORM, '_ACCENT_KEYWORDS': _ACCENT_KEYWORDS, '_ACCENTUATED': _ACCENTUATED, 'character': character}, 1)

def is_accentuated(character: str) -> bool:
    return bool(_character_flags(character) & _ACCENTUATED)

@lru_cache(maxsize=UTF8_MAXIMAL_ALLOCATION)
def remove_accent(character: str) -> str:
    import custom_funtemplate
    return custom_funtemplate.rewrite_template('charset_normalizer.utils.remove_accent', 'remove_accent(character)', {'unicodedata': unicodedata, 'lru_cache': lru_cache, 'UTF8_MAXIMAL_ALLOCATION': UTF8_MAXIMAL_ALLOCATION, 'character': character}, 1)
_UNICODE_RANGES_SORTED: list[tuple[(int, int, str)]] = sorted(((ord_range.start, ord_range.stop, name) for (name, ord_range) in UNICODE_RANGES_COMBINED.items()))
_UNICODE_RANGE_STARTS: list[int] = [e[0] for e in _UNICODE_RANGES_SORTED]

def unicode_range(character: str) -> str | None:
    """
    Retrieve the Unicode range official name from a single character.
    """
    import custom_funtemplate
    return custom_funtemplate.rewrite_template('charset_normalizer.utils.unicode_range', 'unicode_range(character)', {'bisect_right': bisect_right, '_UNICODE_RANGE_STARTS': _UNICODE_RANGE_STARTS, '_UNICODE_RANGES_SORTED': _UNICODE_RANGES_SORTED, 'character': character, 'str': str}, 1)

def is_latin(character: str) -> bool:
    return bool(_character_flags(character) & _LATIN)

def is_punctuation(character: str) -> bool:
    import custom_funtemplate
    return custom_funtemplate.rewrite_template('charset_normalizer.utils.is_punctuation', 'is_punctuation(character)', {'unicodedata': unicodedata, 'unicode_range': unicode_range, 'character': character}, 1)

def is_symbol(character: str) -> bool:
    import custom_funtemplate
    return custom_funtemplate.rewrite_template('charset_normalizer.utils.is_symbol', 'is_symbol(character)', {'unicodedata': unicodedata, 'unicode_range': unicode_range, 'character': character}, 1)

def is_emoticon(character: str) -> bool:
    import custom_funtemplate
    return custom_funtemplate.rewrite_template('charset_normalizer.utils.is_emoticon', 'is_emoticon(character)', {'unicode_range': unicode_range, 'character': character}, 1)

def is_separator(character: str) -> bool:
    import custom_funtemplate
    return custom_funtemplate.rewrite_template('charset_normalizer.utils.is_separator', 'is_separator(character)', {'unicodedata': unicodedata, 'character': character}, 1)

@lru_cache(maxsize=UTF8_MAXIMAL_ALLOCATION)
def is_case_variable(character: str) -> bool:
    return character.islower() != character.isupper()

@lru_cache(maxsize=UTF8_MAXIMAL_ALLOCATION)
def is_cjk(character: str) -> bool:
    return bool(_character_flags(character) & _CJK)

@lru_cache(maxsize=UTF8_MAXIMAL_ALLOCATION)
def is_hiragana(character: str) -> bool:
    return bool(_character_flags(character) & _HIRAGANA)

@lru_cache(maxsize=UTF8_MAXIMAL_ALLOCATION)
def is_katakana(character: str) -> bool:
    return bool(_character_flags(character) & _KATAKANA)

@lru_cache(maxsize=UTF8_MAXIMAL_ALLOCATION)
def is_hangul(character: str) -> bool:
    return bool(_character_flags(character) & _HANGUL)

@lru_cache(maxsize=UTF8_MAXIMAL_ALLOCATION)
def is_thai(character: str) -> bool:
    return bool(_character_flags(character) & _THAI)

@lru_cache(maxsize=UTF8_MAXIMAL_ALLOCATION)
def is_arabic(character: str) -> bool:
    return bool(_character_flags(character) & _ARABIC)

@lru_cache(maxsize=UTF8_MAXIMAL_ALLOCATION)
def is_arabic_isolated_form(character: str) -> bool:
    return bool(_character_flags(character) & _ARABIC_ISOLATED_FORM)

@lru_cache(maxsize=UTF8_MAXIMAL_ALLOCATION)
def is_cjk_uncommon(character: str) -> bool:
    return character not in COMMON_CJK_CHARACTERS

def is_unicode_range_secondary(range_name: str) -> bool:
    return range_name in _SECONDARY_RANGE_NAMES

@lru_cache(maxsize=UTF8_MAXIMAL_ALLOCATION)
def is_unprintable(character: str) -> bool:
    return (not character.isspace() and not character.isprintable() and character != '\x1a' and character != '\ufeff')

def any_specified_encoding(sequence: bytes | bytearray, search_zone: int = 8192) -> str | None:
    """
    Extract using ASCII-only decoder any specified encoding in the first n-bytes.
    """
    import custom_funtemplate
    return custom_funtemplate.rewrite_template('charset_normalizer.utils.any_specified_encoding', 'any_specified_encoding(sequence, search_zone=8192)', {'findall': findall, 'RE_POSSIBLE_ENCODING_INDICATION': RE_POSSIBLE_ENCODING_INDICATION, 'aliases': aliases, 'sequence': sequence, 'search_zone': search_zone, 'bytes': bytes, 'bytearray': bytearray, 'str': str}, 1)

@lru_cache(maxsize=128)
def is_multi_byte_encoding(name: str) -> bool:
    """
    Verify is a specific encoding is a multi byte one based on it IANA name
    """
    import custom_funtemplate
    return custom_funtemplate.rewrite_template('charset_normalizer.utils.is_multi_byte_encoding', 'is_multi_byte_encoding(name)', {'importlib': importlib, 'lru_cache': lru_cache, 'name': name}, 1)

def identify_sig_or_bom(sequence: bytes | bytearray) -> tuple[(str | None, bytes)]:
    """
    Identify and extract SIG/BOM in given sequence.
    """
    import custom_funtemplate
    return custom_funtemplate.rewrite_template('charset_normalizer.utils.identify_sig_or_bom', 'identify_sig_or_bom(sequence)', {'ENCODING_MARKS': ENCODING_MARKS, 'sequence': sequence, 'bytes': bytes, 'bytearray': bytearray, 'tuple': tuple, 'bytes': bytes}, 2)

def should_strip_sig_or_bom(iana_encoding: str) -> bool:
    return iana_encoding not in {'utf_16', 'utf_32'}

def iana_name(cp_name: str, strict: bool = True) -> str:
    """Returns the Python normalized encoding name (Not the IANA official name)."""
    cp_name = cp_name.lower().replace('-', '_')
    encoding_alias: str
    encoding_iana: str
    for (encoding_alias, encoding_iana) in aliases.items():
        if cp_name in [encoding_alias, encoding_iana]:
            return encoding_iana
    if strict:
        raise ValueError(f"Unable to retrieve IANA for '{cp_name}'")
    return cp_name

def cp_similarity(iana_name_a: str, iana_name_b: str) -> float:
    import custom_funtemplate
    return custom_funtemplate.rewrite_template('charset_normalizer.utils.cp_similarity', 'cp_similarity(iana_name_a, iana_name_b)', {'is_multi_byte_encoding': is_multi_byte_encoding, 'importlib': importlib, 'IncrementalDecoder': IncrementalDecoder, 'iana_name_a': iana_name_a, 'iana_name_b': iana_name_b}, 1)

def is_cp_similar(iana_name_a: str, iana_name_b: str) -> bool:
    """
    Determine if two code page are at least 80% similar. IANA_SUPPORTED_SIMILAR dict was generated using
    the function cp_similarity.
    """
    return (iana_name_a in IANA_SUPPORTED_SIMILAR and iana_name_b in IANA_SUPPORTED_SIMILAR[iana_name_a])

def set_logging_handler(name: str = 'charset_normalizer', level: int = logging.INFO, format_string: str = '%(asctime)s | %(levelname)s | %(message)s') -> None:
    import custom_funtemplate
    custom_funtemplate.rewrite_template('charset_normalizer.utils.set_logging_handler', "set_logging_handler(name='charset_normalizer', level=logging.INFO, format_string='%(asctime)s | %(levelname)s | %(message)s')", {'logging': logging, 'name': name, 'level': level, 'format_string': format_string}, 0)

def cut_sequence_chunks(sequences: bytes | bytearray, encoding_iana: str, offsets: range, chunk_size: int, bom_or_sig_available: bool, strip_sig_or_bom: bool, sig_payload: bytes, is_multi_byte_decoder: bool, decoded_payload: str | None = None, deferred_decoding: bool = False) -> Generator[(str, None, None)]:
    import custom_funtemplate
    custom_funtemplate.rewrite_template('charset_normalizer.utils.cut_sequence_chunks', 'cut_sequence_chunks(sequences, encoding_iana, offsets, chunk_size, bom_or_sig_available, strip_sig_or_bom, sig_payload, is_multi_byte_decoder, decoded_payload=None, deferred_decoding=False)', {'sequences': sequences, 'encoding_iana': encoding_iana, 'offsets': offsets, 'chunk_size': chunk_size, 'bom_or_sig_available': bom_or_sig_available, 'strip_sig_or_bom': strip_sig_or_bom, 'sig_payload': sig_payload, 'is_multi_byte_decoder': is_multi_byte_decoder, 'decoded_payload': decoded_payload, 'deferred_decoding': deferred_decoding, 'bytes': bytes, 'bytearray': bytearray, 'str': str, 'Generator': Generator, 'str': str}, 0)

