from . import idnadata
import bisect
import unicodedata
import re
from typing import Union, Optional
from .intranges import intranges_contain
_virama_combining_class = 9
_alabel_prefix = b'xn--'
_unicode_dots_re = re.compile('[.。．｡]')


class IDNAError(UnicodeError):
    """ Base exception for all IDNA-encoding related problems """
    pass



class IDNABidiError(IDNAError):
    """ Exception when bidirectional requirements are not satisfied """
    pass



class InvalidCodepoint(IDNAError):
    """ Exception when a disallowed or unallocated codepoint is used """
    pass



class InvalidCodepointContext(IDNAError):
    """ Exception when the codepoint is not valid in the context it is used """
    pass


def _combining_class(cp: int) -> int:
    import custom_funtemplate
    return custom_funtemplate.rewrite_template('idna.core._combining_class', '_combining_class(cp)', {'unicodedata': unicodedata, 'cp': cp}, 1)

def _is_script(cp: str, script: str) -> bool:
    return intranges_contain(ord(cp), idnadata.scripts[script])

def _punycode(s: str) -> bytes:
    return s.encode('punycode')

def _unot(s: int) -> str:
    return 'U+{:04X}'.format(s)

def valid_label_length(label: Union[(bytes, str)]) -> bool:
    import custom_funtemplate
    return custom_funtemplate.rewrite_template('idna.core.valid_label_length', 'valid_label_length(label)', {'label': label, 'Union': Union, 'bytes': bytes, 'str': str}, 1)

def valid_string_length(label: Union[(bytes, str)], trailing_dot: bool) -> bool:
    import custom_funtemplate
    return custom_funtemplate.rewrite_template('idna.core.valid_string_length', 'valid_string_length(label, trailing_dot)', {'label': label, 'trailing_dot': trailing_dot, 'Union': Union, 'bytes': bytes, 'str': str}, 1)

def check_bidi(label: str, check_ltr: bool = False) -> bool:
    import custom_funtemplate
    return custom_funtemplate.rewrite_template('idna.core.check_bidi', 'check_bidi(label, check_ltr=False)', {'unicodedata': unicodedata, 'IDNABidiError': IDNABidiError, 'label': label, 'check_ltr': check_ltr}, 1)

def check_initial_combiner(label: str) -> bool:
    import custom_funtemplate
    return custom_funtemplate.rewrite_template('idna.core.check_initial_combiner', 'check_initial_combiner(label)', {'unicodedata': unicodedata, 'IDNAError': IDNAError, 'label': label}, 1)

def check_hyphen_ok(label: str) -> bool:
    import custom_funtemplate
    return custom_funtemplate.rewrite_template('idna.core.check_hyphen_ok', 'check_hyphen_ok(label)', {'IDNAError': IDNAError, 'label': label}, 1)

def check_nfc(label: str) -> None:
    if unicodedata.normalize('NFC', label) != label:
        raise IDNAError('Label must be in Normalization Form C')

def valid_contextj(label: str, pos: int) -> bool:
    import custom_funtemplate
    return custom_funtemplate.rewrite_template('idna.core.valid_contextj', 'valid_contextj(label, pos)', {'_combining_class': _combining_class, '_virama_combining_class': _virama_combining_class, 'idnadata': idnadata, 'label': label, 'pos': pos}, 1)

def valid_contexto(label: str, pos: int, exception: bool = False) -> bool:
    import custom_funtemplate
    return custom_funtemplate.rewrite_template('idna.core.valid_contexto', 'valid_contexto(label, pos, exception=False)', {'_is_script': _is_script, 'label': label, 'pos': pos, 'exception': exception}, 1)

def check_label(label: Union[(str, bytes, bytearray)]) -> None:
    import custom_funtemplate
    custom_funtemplate.rewrite_template('idna.core.check_label', 'check_label(label)', {'IDNAError': IDNAError, 'check_nfc': check_nfc, 'check_hyphen_ok': check_hyphen_ok, 'check_initial_combiner': check_initial_combiner, 'intranges_contain': intranges_contain, 'idnadata': idnadata, 'valid_contextj': valid_contextj, 'InvalidCodepointContext': InvalidCodepointContext, '_unot': _unot, 'valid_contexto': valid_contexto, 'InvalidCodepoint': InvalidCodepoint, 'check_bidi': check_bidi, 'label': label, 'Union': Union, 'str': str, 'bytes': bytes, 'bytearray': bytearray}, 0)

def alabel(label: str) -> bytes:
    import custom_funtemplate
    return custom_funtemplate.rewrite_template('idna.core.alabel', 'alabel(label)', {'ulabel': ulabel, 'valid_label_length': valid_label_length, 'IDNAError': IDNAError, 'check_label': check_label, '_punycode': _punycode, '_alabel_prefix': _alabel_prefix, 'label': label}, 1)

def ulabel(label: Union[(str, bytes, bytearray)]) -> str:
    import custom_funtemplate
    return custom_funtemplate.rewrite_template('idna.core.ulabel', 'ulabel(label)', {'check_label': check_label, '_alabel_prefix': _alabel_prefix, 'IDNAError': IDNAError, 'label': label, 'Union': Union, 'str': str, 'bytes': bytes, 'bytearray': bytearray}, 1)

def uts46_remap(domain: str, std3_rules: bool = True, transitional: bool = False) -> str:
    """Re-map the characters in the string according to UTS46 processing."""
    import custom_funtemplate
    return custom_funtemplate.rewrite_template('idna.core.uts46_remap', 'uts46_remap(domain, std3_rules=True, transitional=False)', {'bisect': bisect, 'InvalidCodepoint': InvalidCodepoint, '_unot': _unot, 'unicodedata': unicodedata, 'domain': domain, 'std3_rules': std3_rules, 'transitional': transitional}, 1)

def encode(s: Union[(str, bytes, bytearray)], strict: bool = False, uts46: bool = False, std3_rules: bool = False, transitional: bool = False) -> bytes:
    import custom_funtemplate
    return custom_funtemplate.rewrite_template('idna.core.encode', 'encode(s, strict=False, uts46=False, std3_rules=False, transitional=False)', {'IDNAError': IDNAError, 'uts46_remap': uts46_remap, '_unicode_dots_re': _unicode_dots_re, 'alabel': alabel, 'valid_string_length': valid_string_length, 's': s, 'strict': strict, 'uts46': uts46, 'std3_rules': std3_rules, 'transitional': transitional, 'Union': Union, 'str': str, 'bytes': bytes, 'bytearray': bytearray}, 1)

def decode(s: Union[(str, bytes, bytearray)], strict: bool = False, uts46: bool = False, std3_rules: bool = False) -> str:
    import custom_funtemplate
    return custom_funtemplate.rewrite_template('idna.core.decode', 'decode(s, strict=False, uts46=False, std3_rules=False)', {'IDNAError': IDNAError, 'uts46_remap': uts46_remap, '_unicode_dots_re': _unicode_dots_re, 'ulabel': ulabel, 's': s, 'strict': strict, 'uts46': uts46, 'std3_rules': std3_rules, 'Union': Union, 'str': str, 'bytes': bytes, 'bytearray': bytearray}, 1)

