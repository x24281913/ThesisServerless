from __future__ import annotations
import importlib
from codecs import IncrementalDecoder
from functools import lru_cache
from .constant import FREQUENCIES, KO_NAMES, LANGUAGE_SUPPORTED_COUNT, TOO_SMALL_SEQUENCE, ZH_NAMES, _FREQUENCIES_SET, _FREQUENCIES_RANK
from .md import _ASCII_CHAR_INFO, _char_info, is_suspiciously_successive_range
from .models import CoherenceMatches
from .utils import is_multi_byte_encoding, is_unicode_range_secondary

def encoding_unicode_range(iana_name: str) -> list[str]:
    """
    Return associated unicode ranges in a single byte code page.
    """
    import custom_funtemplate
    return custom_funtemplate.rewrite_template('charset_normalizer.cd.encoding_unicode_range', 'encoding_unicode_range(iana_name)', {'is_multi_byte_encoding': is_multi_byte_encoding, 'importlib': importlib, 'IncrementalDecoder': IncrementalDecoder, '_ASCII_CHAR_INFO': _ASCII_CHAR_INFO, '_char_info': _char_info, 'is_unicode_range_secondary': is_unicode_range_secondary, 'iana_name': iana_name, 'list': list, 'str': str}, 1)

def unicode_range_languages(primary_range: str) -> list[str]:
    """
    Return inferred languages used with a unicode range.
    """
    import custom_funtemplate
    return custom_funtemplate.rewrite_template('charset_normalizer.cd.unicode_range_languages', 'unicode_range_languages(primary_range)', {'FREQUENCIES': FREQUENCIES, '_ASCII_CHAR_INFO': _ASCII_CHAR_INFO, '_char_info': _char_info, 'primary_range': primary_range, 'list': list, 'str': str}, 1)

@lru_cache()
def encoding_languages(iana_name: str) -> list[str]:
    """
    Single-byte encoding language association. Some code page are heavily linked to particular language(s).
    This function does the correspondence.
    """
    import custom_funtemplate
    return custom_funtemplate.rewrite_template('charset_normalizer.cd.encoding_languages', 'encoding_languages(iana_name)', {'encoding_unicode_range': encoding_unicode_range, 'unicode_range_languages': unicode_range_languages, 'lru_cache': lru_cache, 'iana_name': iana_name, 'list': list, 'str': str}, 1)

@lru_cache()
def mb_encoding_languages(iana_name: str) -> list[str]:
    """
    Multi-byte encoding language association. Some code page are heavily linked to particular language(s).
    This function does the correspondence.
    """
    import custom_funtemplate
    return custom_funtemplate.rewrite_template('charset_normalizer.cd.mb_encoding_languages', 'mb_encoding_languages(iana_name)', {'ZH_NAMES': ZH_NAMES, 'KO_NAMES': KO_NAMES, 'lru_cache': lru_cache, 'iana_name': iana_name, 'list': list, 'str': str}, 1)

@lru_cache(maxsize=LANGUAGE_SUPPORTED_COUNT)
def get_target_features(language: str) -> tuple[(bool, bool)]:
    """
    Determine main aspects from a supported language if it contains accents and if is pure Latin.
    """
    import custom_funtemplate
    return custom_funtemplate.rewrite_template('charset_normalizer.cd.get_target_features', 'get_target_features(language)', {'FREQUENCIES': FREQUENCIES, '_ASCII_CHAR_INFO': _ASCII_CHAR_INFO, '_char_info': _char_info, 'lru_cache': lru_cache, 'LANGUAGE_SUPPORTED_COUNT': LANGUAGE_SUPPORTED_COUNT, 'language': language, 'tuple': tuple, 'bool': bool, 'bool': bool}, 2)

def alphabet_languages(characters: list[str], ignore_non_latin: bool = False) -> list[str]:
    """
    Return associated languages associated to given characters.
    """
    import custom_funtemplate
    return custom_funtemplate.rewrite_template('charset_normalizer.cd.alphabet_languages', 'alphabet_languages(characters, ignore_non_latin=False)', {'_ASCII_CHAR_INFO': _ASCII_CHAR_INFO, '_char_info': _char_info, 'FREQUENCIES': FREQUENCIES, 'get_target_features': get_target_features, '_FREQUENCIES_SET': _FREQUENCIES_SET, 'characters': characters, 'ignore_non_latin': ignore_non_latin, 'list': list, 'str': str, 'list': list, 'str': str}, 1)

def characters_popularity_compare(language: str, ordered_characters: list[str]) -> float:
    """
    Determine if a ordered characters list (by occurrence from most appearance to rarest) match a particular language.
    The result is a ratio between 0. (absolutely no correspondence) and 1. (near perfect fit).
    Beware that is function is not strict on the match in order to ease the detection. (Meaning close match is 1.)
    """
    import custom_funtemplate
    return custom_funtemplate.rewrite_template('charset_normalizer.cd.characters_popularity_compare', 'characters_popularity_compare(language, ordered_characters)', {'FREQUENCIES': FREQUENCIES, '_FREQUENCIES_RANK': _FREQUENCIES_RANK, 'language': language, 'ordered_characters': ordered_characters, 'list': list, 'str': str}, 1)

def alpha_unicode_split(decoded_sequence: str) -> list[str]:
    """
    Given a decoded text sequence, return a list of str. Unicode range / alphabet separation.
    Ex. a text containing English/Latin with a bit a Hebrew will return two items in the resulting list;
    One containing the latin letters and the other hebrew.
    """
    import custom_funtemplate
    return custom_funtemplate.rewrite_template('charset_normalizer.cd.alpha_unicode_split', 'alpha_unicode_split(decoded_sequence)', {'_ASCII_CHAR_INFO': _ASCII_CHAR_INFO, '_char_info': _char_info, 'is_suspiciously_successive_range': is_suspiciously_successive_range, 'decoded_sequence': decoded_sequence, 'list': list, 'str': str}, 1)

def merge_coherence_ratios(results: list[CoherenceMatches]) -> CoherenceMatches:
    """
    This function merge results previously given by the function coherence_ratio.
    The return type is the same as coherence_ratio.
    """
    import custom_funtemplate
    return custom_funtemplate.rewrite_template('charset_normalizer.cd.merge_coherence_ratios', 'merge_coherence_ratios(results)', {'results': results, 'list': list, 'CoherenceMatches': CoherenceMatches}, 1)

def filter_alt_coherence_matches(results: CoherenceMatches) -> CoherenceMatches:
    """
    We shall NOT return "English—" in CoherenceMatches because it is an alternative
    of "English". This function only keeps the best match and remove the em-dash in it.
    """
    import custom_funtemplate
    return custom_funtemplate.rewrite_template('charset_normalizer.cd.filter_alt_coherence_matches', 'filter_alt_coherence_matches(results)', {'CoherenceMatches': CoherenceMatches, 'results': results}, 1)

def coherence_ratio(decoded_sequence: str, threshold: float = 0.1, lg_inclusion: str | None = None) -> CoherenceMatches:
    """
    Detect ANY language that can be identified in given sequence. The sequence will be analysed by layers.
    A layer = Character extraction by alphabets/ranges.
    """
    import custom_funtemplate
    return custom_funtemplate.rewrite_template('charset_normalizer.cd.coherence_ratio', 'coherence_ratio(decoded_sequence, threshold=0.1, lg_inclusion=None)', {'alpha_unicode_split': alpha_unicode_split, 'TOO_SMALL_SEQUENCE': TOO_SMALL_SEQUENCE, 'alphabet_languages': alphabet_languages, 'characters_popularity_compare': characters_popularity_compare, 'filter_alt_coherence_matches': filter_alt_coherence_matches, 'decoded_sequence': decoded_sequence, 'threshold': threshold, 'lg_inclusion': lg_inclusion, 'str': str}, 1)

