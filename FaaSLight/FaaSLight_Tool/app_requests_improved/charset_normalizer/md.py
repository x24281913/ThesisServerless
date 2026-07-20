from __future__ import annotations
import sys
from functools import lru_cache
from logging import getLogger
if sys.version_info >= (3, 8):
    from typing import final
else:
    try:
        from typing_extensions import final
    except ImportError:
        
        def final(cls):
            return cls
from .constant import COMMON_CJK_CHARACTERS, COMMON_SAFE_ASCII_CHARACTERS, TRACE, UNICODE_SECONDARY_RANGE_KEYWORD, _ACCENTUATED, _ARABIC, _ARABIC_ISOLATED_FORM, _CJK, _HANGUL, _HIRAGANA, _KATAKANA, _LATIN, _THAI
from .utils import _character_flags, is_emoticon, is_punctuation, is_separator, is_symbol, remove_accent, unicode_range
_GLYPH_MASK: int = _CJK | _HANGUL | _KATAKANA | _HIRAGANA | _THAI


@final
class CharInfo:
    """Pre-computed character properties shared across all detectors."""
    __slots__ = ('character', 'printable', 'alpha', 'upper', 'lower', 'space', 'digit', 'is_ascii', 'case_variable', 'flags', 'accentuated', 'latin', 'is_cjk', 'is_arabic', 'is_glyph', 'punct', 'sym', 'range', 'sep', 'emoticon', 'safe', 'common_cjk')
    character: str
    printable: bool
    alpha: bool
    upper: bool
    lower: bool
    space: bool
    digit: bool
    is_ascii: bool
    case_variable: bool
    flags: int
    accentuated: bool
    latin: bool
    is_cjk: bool
    is_arabic: bool
    is_glyph: bool
    punct: bool
    sym: bool
    range: str | None
    sep: bool
    emoticon: bool
    safe: bool
    common_cjk: bool
    
    def __init__(self, character: str) -> None:
        """Compute all properties for *character* (built once per codepoint,
        every branch assigns every slot)."""
        self.character = character
        o: int = ord(character)
        if o < 128:
            self.is_ascii = True
            self.accentuated = False
            self.is_cjk = False
            self.is_arabic = False
            self.is_glyph = False
            if 65 <= o <= 90:
                self.alpha = True
                self.upper = True
                self.lower = False
                self.space = False
                self.digit = False
                self.printable = True
                self.case_variable = True
                self.flags = _LATIN
                self.latin = True
                self.punct = False
                self.sym = False
            elif 97 <= o <= 122:
                self.alpha = True
                self.upper = False
                self.lower = True
                self.space = False
                self.digit = False
                self.printable = True
                self.case_variable = True
                self.flags = _LATIN
                self.latin = True
                self.punct = False
                self.sym = False
            elif 48 <= o <= 57:
                self.alpha = False
                self.upper = False
                self.lower = False
                self.space = False
                self.digit = True
                self.printable = True
                self.case_variable = False
                self.flags = 0
                self.latin = False
                self.punct = False
                self.sym = False
            elif (o == 32 or 9 <= o <= 13):
                self.alpha = False
                self.upper = False
                self.lower = False
                self.space = True
                self.digit = False
                self.printable = o == 32
                self.case_variable = False
                self.flags = 0
                self.latin = False
                self.punct = False
                self.sym = False
            else:
                self.printable = character.isprintable()
                self.alpha = False
                self.upper = False
                self.lower = False
                self.space = False
                self.digit = False
                self.case_variable = False
                self.flags = 0
                self.latin = False
                self.punct = (is_punctuation(character) if self.printable else False)
                self.sym = (is_symbol(character) if self.printable else False)
        else:
            self.is_ascii = False
            self.printable = character.isprintable()
            self.alpha = character.isalpha()
            self.upper = character.isupper()
            self.lower = character.islower()
            self.space = character.isspace()
            self.digit = character.isdigit()
            self.case_variable = self.lower != self.upper
            flags: int
            if self.alpha:
                flags = _character_flags(character)
            else:
                flags = 0
            self.flags = flags
            self.accentuated = bool(flags & _ACCENTUATED)
            self.latin = bool(flags & _LATIN)
            self.is_cjk = bool(flags & _CJK)
            self.is_arabic = bool(flags & _ARABIC)
            self.is_glyph = bool(flags & _GLYPH_MASK)
            self.punct = (is_punctuation(character) if self.printable else False)
            self.sym = (is_symbol(character) if self.printable else False)
        self.range = unicode_range(character)
        self.sep = is_separator(character)
        self.emoticon = is_emoticon(character)
        self.safe = character in COMMON_SAFE_ASCII_CHARACTERS
        self.common_cjk = character in COMMON_CJK_CHARACTERS


@lru_cache(maxsize=None)
def _char_info(character: str) -> CharInfo:
    """Build (once per codepoint) and cache the CharInfo for *character*."""
    return CharInfo(character)
_ASCII_CHAR_INFO: list[CharInfo] = [CharInfo(chr(_codepoint)) for _codepoint in range(128)]


class MessDetectorPlugin:
    """
    Base abstract class used for mess detection plugins.
    All detectors MUST extend and implement given methods.
    """
    __slots__ = ()
    
    def feed_info(self, character: str, info: CharInfo) -> None:
        """
        The main routine to be executed upon character.
        Insert the logic in witch the text would be considered chaotic.
        """
        raise NotImplementedError
    
    def reset(self) -> None:
        """
        Permit to reset the plugin to the initial state.
        """
        raise NotImplementedError
    
    @property
    def ratio(self) -> float:
        """
        Compute the chaos ratio based on what your feed() has seen.
        Must NOT be lower than 0.; No restriction gt 0.
        """
        raise NotImplementedError



@final
class TooManySymbolOrPunctuationPlugin(MessDetectorPlugin):
    __slots__ = ('_punctuation_count', '_symbol_count', '_character_count', '_last_printable_char', '_frenzy_symbol_in_word')
    
    def __init__(self) -> None:
        self._punctuation_count: int = 0
        self._symbol_count: int = 0
        self._character_count: int = 0
        self._last_printable_char: str | None = None
        self._frenzy_symbol_in_word: bool = False
    
    def feed_info(self, character: str, info: CharInfo) -> None:
        """Optimized feed using pre-computed character info."""
        self._character_count += 1
        if (character != self._last_printable_char and not info.safe):
            if info.punct:
                self._punctuation_count += 1
            elif (not info.digit and info.sym and not info.emoticon):
                self._symbol_count += 2
        self._last_printable_char = character
    
    def reset(self) -> None:
        self._punctuation_count = 0
        self._character_count = 0
        self._symbol_count = 0
    
    @property
    def ratio(self) -> float:
        if self._character_count == 0:
            return 0.0
        ratio_of_punctuation: float = (self._punctuation_count + self._symbol_count) / self._character_count
        return (ratio_of_punctuation if ratio_of_punctuation >= 0.3 else 0.0)



@final
class TooManyAccentuatedPlugin(MessDetectorPlugin):
    __slots__ = ('_character_count', '_accentuated_count')
    
    def __init__(self) -> None:
        self._character_count: int = 0
        self._accentuated_count: int = 0
    
    def feed_info(self, character: str, info: CharInfo) -> None:
        """Optimized feed using pre-computed character info."""
        self._character_count += 1
        if info.accentuated:
            self._accentuated_count += 1
    
    def reset(self) -> None:
        self._character_count = 0
        self._accentuated_count = 0
    
    @property
    def ratio(self) -> float:
        if self._character_count < 8:
            return 0.0
        ratio_of_accentuation: float = self._accentuated_count / self._character_count
        return (ratio_of_accentuation if ratio_of_accentuation >= 0.35 else 0.0)



@final
class UnprintablePlugin(MessDetectorPlugin):
    __slots__ = ('_unprintable_count', '_character_count')
    
    def __init__(self) -> None:
        self._unprintable_count: int = 0
        self._character_count: int = 0
    
    def feed_info(self, character: str, info: CharInfo) -> None:
        """Optimized feed using pre-computed character info."""
        if (not info.space and not info.printable and character != '\x1a' and character != '\ufeff'):
            self._unprintable_count += 1
        self._character_count += 1
    
    def reset(self) -> None:
        self._unprintable_count = 0
    
    @property
    def ratio(self) -> float:
        if self._character_count == 0:
            return 0.0
        return self._unprintable_count * 8 / self._character_count



@final
class SuspiciousDuplicateAccentPlugin(MessDetectorPlugin):
    __slots__ = ('_successive_count', '_character_count', '_last_latin_character', '_last_was_accentuated')
    
    def __init__(self) -> None:
        self._successive_count: int = 0
        self._character_count: int = 0
        self._last_latin_character: str | None = None
        self._last_was_accentuated: bool = False
    
    def feed_info(self, character: str, info: CharInfo) -> None:
        """Optimized feed using pre-computed character info."""
        self._character_count += 1
        if (self._last_latin_character is not None and info.accentuated and self._last_was_accentuated):
            if (info.upper and self._last_latin_character.isupper()):
                self._successive_count += 1
            if remove_accent(character) == remove_accent(self._last_latin_character):
                self._successive_count += 1
        self._last_latin_character = character
        self._last_was_accentuated = info.accentuated
    
    def reset(self) -> None:
        self._successive_count = 0
        self._character_count = 0
        self._last_latin_character = None
        self._last_was_accentuated = False
    
    @property
    def ratio(self) -> float:
        if self._character_count == 0:
            return 0.0
        return self._successive_count * 2 / self._character_count



@final
class SuspiciousRange(MessDetectorPlugin):
    __slots__ = ('_suspicious_successive_range_count', '_character_count', '_last_printable_seen', '_last_printable_range')
    
    def __init__(self) -> None:
        self._suspicious_successive_range_count: int = 0
        self._character_count: int = 0
        self._last_printable_seen: str | None = None
        self._last_printable_range: str | None = None
    
    def feed_info(self, character: str, info: CharInfo) -> None:
        """Optimized feed using pre-computed character info."""
        self._character_count += 1
        if (info.space or info.punct or info.safe):
            self._last_printable_seen = None
            self._last_printable_range = None
            return
        if self._last_printable_seen is None:
            self._last_printable_seen = character
            self._last_printable_range = info.range
            return
        unicode_range_a: str | None = self._last_printable_range
        unicode_range_b: str | None = info.range
        if (unicode_range_a != unicode_range_b or unicode_range_a is None):
            if is_suspiciously_successive_range(unicode_range_a, unicode_range_b):
                self._suspicious_successive_range_count += 1
        self._last_printable_seen = character
        self._last_printable_range = unicode_range_b
    
    def reset(self) -> None:
        self._character_count = 0
        self._suspicious_successive_range_count = 0
        self._last_printable_seen = None
        self._last_printable_range = None
    
    @property
    def ratio(self) -> float:
        if self._character_count <= 13:
            return 0.0
        ratio_of_suspicious_range_usage: float = self._suspicious_successive_range_count * 2 / self._character_count
        return ratio_of_suspicious_range_usage



@final
class SuperWeirdWordPlugin(MessDetectorPlugin):
    __slots__ = ('_word_count', '_bad_word_count', '_foreign_long_count', '_is_current_word_bad', '_foreign_long_watch', '_character_count', '_bad_character_count', '_buffer_length', '_buffer_last_char', '_buffer_last_char_accentuated', '_buffer_accent_count', '_buffer_glyph_count', '_buffer_upper_count', '_buffer_first_lower', '_buffer_has_non_ascii')
    
    def __init__(self) -> None:
        self._word_count: int = 0
        self._bad_word_count: int = 0
        self._foreign_long_count: int = 0
        self._is_current_word_bad: bool = False
        self._foreign_long_watch: bool = False
        self._character_count: int = 0
        self._bad_character_count: int = 0
        self._buffer_length: int = 0
        self._buffer_last_char: str | None = None
        self._buffer_last_char_accentuated: bool = False
        self._buffer_accent_count: int = 0
        self._buffer_glyph_count: int = 0
        self._buffer_upper_count: int = 0
        self._buffer_first_lower: bool = False
        self._buffer_has_non_ascii: bool = False
    
    def feed_info(self, character: str, info: CharInfo) -> None:
        """Optimized feed using pre-computed character info."""
        if info.alpha:
            if self._buffer_length == 0:
                self._buffer_first_lower = info.lower
            self._buffer_length += 1
            self._buffer_last_char = character
            if info.upper:
                self._buffer_upper_count += 1
            if not info.is_ascii:
                self._buffer_has_non_ascii = True
            self._buffer_last_char_accentuated = info.accentuated
            if info.accentuated:
                self._buffer_accent_count += 1
            if (not self._foreign_long_watch and ((not info.latin or info.accentuated)) and not info.is_glyph):
                self._foreign_long_watch = True
            if info.is_glyph:
                self._buffer_glyph_count += 1
            return
        if not self._buffer_length:
            return
        if (info.space or info.punct or info.sep):
            self._word_count += 1
            buffer_length: int = self._buffer_length
            self._character_count += buffer_length
            if buffer_length >= 4:
                if self._buffer_accent_count / buffer_length >= 0.5:
                    self._is_current_word_bad = True
                elif (self._buffer_last_char_accentuated and self._buffer_last_char.isupper() and self._buffer_upper_count != buffer_length):
                    self._foreign_long_count += 1
                    self._is_current_word_bad = True
                elif self._buffer_glyph_count == 1:
                    self._is_current_word_bad = True
                    self._foreign_long_count += 1
                elif (self._buffer_has_non_ascii and self._buffer_first_lower and self._buffer_upper_count == buffer_length - 1):
                    self._foreign_long_count += 1
                    self._is_current_word_bad = True
            if (buffer_length >= 24 and self._foreign_long_watch):
                probable_camel_cased: bool = (self._buffer_upper_count > 0 and self._buffer_upper_count / buffer_length <= 0.3)
                if not probable_camel_cased:
                    self._foreign_long_count += 1
                    self._is_current_word_bad = True
            if self._is_current_word_bad:
                self._bad_word_count += 1
                self._bad_character_count += buffer_length
                self._is_current_word_bad = False
            self._foreign_long_watch = False
            self._buffer_length = 0
            self._buffer_last_char = None
            self._buffer_last_char_accentuated = False
            self._buffer_accent_count = 0
            self._buffer_glyph_count = 0
            self._buffer_upper_count = 0
            self._buffer_first_lower = False
            self._buffer_has_non_ascii = False
        elif (character not in {'<', '>', '-', '=', '~', '|', '_'} and not info.digit and info.sym):
            self._is_current_word_bad = True
            self._buffer_length += 1
            self._buffer_last_char = character
            self._buffer_last_char_accentuated = False
    
    def reset(self) -> None:
        self._buffer_length = 0
        self._buffer_last_char = None
        self._buffer_last_char_accentuated = False
        self._is_current_word_bad = False
        self._foreign_long_watch = False
        self._bad_word_count = 0
        self._word_count = 0
        self._character_count = 0
        self._bad_character_count = 0
        self._foreign_long_count = 0
        self._buffer_accent_count = 0
        self._buffer_glyph_count = 0
        self._buffer_upper_count = 0
        self._buffer_first_lower = False
        self._buffer_has_non_ascii = False
    
    @property
    def ratio(self) -> float:
        if (self._word_count <= 10 and self._foreign_long_count == 0):
            return 0.0
        return self._bad_character_count / self._character_count



@final
class CjkUncommonPlugin(MessDetectorPlugin):
    """
    Detect messy CJK text that probably means nothing.
    """
    __slots__ = ('_character_count', '_uncommon_count')
    
    def __init__(self) -> None:
        self._character_count: int = 0
        self._uncommon_count: int = 0
    
    def feed_info(self, character: str, info: CharInfo) -> None:
        """Optimized feed using pre-computed character info."""
        self._character_count += 1
        if not info.common_cjk:
            self._uncommon_count += 1
    
    def reset(self) -> None:
        self._character_count = 0
        self._uncommon_count = 0
    
    @property
    def ratio(self) -> float:
        if self._character_count < 8:
            return 0.0
        uncommon_form_usage: float = self._uncommon_count / self._character_count
        return (uncommon_form_usage / 10 if uncommon_form_usage > 0.5 else 0.0)



@final
class ArchaicUpperLowerPlugin(MessDetectorPlugin):
    __slots__ = ('_buf', '_character_count_since_last_sep', '_successive_upper_lower_count', '_successive_upper_lower_count_final', '_character_count', '_last_alpha_seen', '_last_alpha_seen_upper', '_last_alpha_seen_lower', '_current_ascii_only')
    
    def __init__(self) -> None:
        self._buf: bool = False
        self._character_count_since_last_sep: int = 0
        self._successive_upper_lower_count: int = 0
        self._successive_upper_lower_count_final: int = 0
        self._character_count: int = 0
        self._last_alpha_seen: str | None = None
        self._last_alpha_seen_upper: bool = False
        self._last_alpha_seen_lower: bool = False
        self._current_ascii_only: bool = True
    
    def feed_info(self, character: str, info: CharInfo) -> None:
        """Optimized feed using pre-computed character info."""
        is_concerned: bool = (info.alpha and info.case_variable)
        chunk_sep: bool = not is_concerned
        if (chunk_sep and self._character_count_since_last_sep > 0):
            if (self._character_count_since_last_sep <= 64 and not info.digit and not self._current_ascii_only):
                self._successive_upper_lower_count_final += self._successive_upper_lower_count
            self._successive_upper_lower_count = 0
            self._character_count_since_last_sep = 0
            self._last_alpha_seen = None
            self._buf = False
            self._character_count += 1
            self._current_ascii_only = True
            return
        if (self._current_ascii_only and not info.is_ascii):
            self._current_ascii_only = False
        if self._last_alpha_seen is not None:
            if ((info.upper and self._last_alpha_seen_lower) or (info.lower and self._last_alpha_seen_upper)):
                if self._buf:
                    self._successive_upper_lower_count += 2
                    self._buf = False
                else:
                    self._buf = True
            else:
                self._buf = False
        self._character_count += 1
        self._character_count_since_last_sep += 1
        self._last_alpha_seen = character
        self._last_alpha_seen_upper = info.upper
        self._last_alpha_seen_lower = info.lower
    
    def reset(self) -> None:
        self._character_count = 0
        self._character_count_since_last_sep = 0
        self._successive_upper_lower_count = 0
        self._successive_upper_lower_count_final = 0
        self._last_alpha_seen = None
        self._last_alpha_seen_upper = False
        self._last_alpha_seen_lower = False
        self._buf = False
        self._current_ascii_only = True
    
    @property
    def ratio(self) -> float:
        if self._character_count == 0:
            return 0.0
        return self._successive_upper_lower_count_final / self._character_count



@final
class ArabicIsolatedFormPlugin(MessDetectorPlugin):
    __slots__ = ('_character_count', '_isolated_form_count')
    
    def __init__(self) -> None:
        self._character_count: int = 0
        self._isolated_form_count: int = 0
    
    def reset(self) -> None:
        self._character_count = 0
        self._isolated_form_count = 0
    
    def feed_info(self, character: str, info: CharInfo) -> None:
        """Optimized feed using pre-computed character info."""
        self._character_count += 1
        if info.flags & _ARABIC_ISOLATED_FORM:
            self._isolated_form_count += 1
    
    @property
    def ratio(self) -> float:
        if self._character_count < 8:
            return 0.0
        isolated_form_usage: float = self._isolated_form_count / self._character_count
        return isolated_form_usage


@lru_cache(maxsize=1024)
def is_suspiciously_successive_range(unicode_range_a: str | None, unicode_range_b: str | None) -> bool:
    """
    Determine if two Unicode range seen next to each other can be considered as suspicious.
    """
    import custom_funtemplate
    return custom_funtemplate.rewrite_template('charset_normalizer.md.is_suspiciously_successive_range', 'is_suspiciously_successive_range(unicode_range_a, unicode_range_b)', {'UNICODE_SECONDARY_RANGE_KEYWORD': UNICODE_SECONDARY_RANGE_KEYWORD, 'lru_cache': lru_cache, 'unicode_range_a': unicode_range_a, 'unicode_range_b': unicode_range_b, 'str': str, 'str': str}, 1)

def mess_ratio(decoded_sequence: str, maximum_threshold: float = 0.2, debug: bool = False) -> float:
    """
    Compute a mess ratio given a decoded bytes sequence. The maximum threshold does stop the computation earlier.
    """
    import custom_funtemplate
    return custom_funtemplate.rewrite_template('charset_normalizer.md.mess_ratio', 'mess_ratio(decoded_sequence, maximum_threshold=0.2, debug=False)', {'_ASCII_CHAR_INFO': _ASCII_CHAR_INFO, '_char_info': _char_info, 'CharInfo': CharInfo, 'TooManySymbolOrPunctuationPlugin': TooManySymbolOrPunctuationPlugin, 'TooManyAccentuatedPlugin': TooManyAccentuatedPlugin, 'UnprintablePlugin': UnprintablePlugin, 'SuspiciousDuplicateAccentPlugin': SuspiciousDuplicateAccentPlugin, 'SuspiciousRange': SuspiciousRange, 'SuperWeirdWordPlugin': SuperWeirdWordPlugin, 'CjkUncommonPlugin': CjkUncommonPlugin, 'ArchaicUpperLowerPlugin': ArchaicUpperLowerPlugin, 'ArabicIsolatedFormPlugin': ArabicIsolatedFormPlugin, 'getLogger': getLogger, 'TRACE': TRACE, 'decoded_sequence': decoded_sequence, 'maximum_threshold': maximum_threshold, 'debug': debug}, 1)

