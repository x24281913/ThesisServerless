import bisect
import re
import unicodedata
import warnings
from typing import Optional, Union
from . import idnadata
from .intranges import intranges_contain
_virama_combining_class = 9
_alabel_prefix = b'xn--'
_max_input_length = 1024
_unicode_dots_re = re.compile('[.。．｡]')
_bidi_rtl_first = frozenset({'R', 'AL'})
_bidi_rtl_categories = frozenset({'R', 'AL', 'AN'})
_bidi_rtl_allowed = frozenset({'R', 'AL', 'AN', 'EN', 'ES', 'CS', 'ET', 'ON', 'BN', 'NSM'})
_bidi_rtl_valid_ending = frozenset({'R', 'AL', 'EN', 'AN'})
_bidi_rtl_numeric = frozenset({'AN', 'EN'})
_bidi_ltr_allowed = frozenset({'L', 'EN', 'ES', 'CS', 'ET', 'ON', 'BN', 'NSM'})
_bidi_ltr_valid_ending = frozenset({'L', 'EN'})
_bidi_joiner_l_or_d = frozenset({'L', 'D'})
_bidi_joiner_r_or_d = frozenset({'R', 'D'})

def _joining_type(cp: int) -> Optional[str]:
    import custom_funtemplate
    return custom_funtemplate.rewrite_template('idna.core._joining_type', '_joining_type(cp)', {'idnadata': idnadata, 'intranges_contain': intranges_contain, 'cp': cp, 'Optional': Optional, 'str': str}, 1)


class IDNAError(UnicodeError):
    """Base exception for all IDNA-encoding related problems"""
    



class IDNABidiError(IDNAError):
    """Exception when bidirectional requirements are not satisfied"""
    



class InvalidCodepoint(IDNAError):
    """Exception when a disallowed or unallocated codepoint is used"""
    



class InvalidCodepointContext(IDNAError):
    """Exception when the codepoint is not valid in the context it is used"""
    


def _combining_class(cp: int) -> int:
    import custom_funtemplate
    return custom_funtemplate.rewrite_template('idna.core._combining_class', '_combining_class(cp)', {'unicodedata': unicodedata, 'cp': cp}, 1)

def _is_script(cp: str, script: str) -> bool:
    return intranges_contain(ord(cp), idnadata.scripts[script])

def _punycode(s: str) -> bytes:
    return s.encode('punycode')

def _unot(s: int) -> str:
    return f'U+{s:04X}'

def valid_label_length(label: Union[(bytes, str)]) -> bool:
    """Check that a label does not exceed the maximum permitted length.

    Per :rfc:`1035` (and :rfc:`5891` §4.2.4) a DNS label must not exceed
    63 octets. The argument may be either a :class:`str` (a U-label, where
    length is measured in characters) or :class:`bytes` (an A-label, where
    length is measured in octets).

    :param label: The label to check.
    :returns: ``True`` if the label is within the length limit, otherwise
        ``False``.
    """
    return len(label) <= 63

def valid_string_length(domain: Union[(bytes, str)], trailing_dot: bool) -> bool:
    """Check that a full domain name does not exceed the maximum length.

    Per :rfc:`1035`, a domain name is limited to 253 octets when no trailing
    dot is present, or 254 octets when one is included.

    :param domain: The full (possibly multi-label) domain name.
    :param trailing_dot: ``True`` if ``domain`` includes a trailing ``.``.
    :returns: ``True`` if the domain is within the length limit, otherwise
        ``False``.
    """
    return len(domain) <= ((254 if trailing_dot else 253))

def check_bidi(label: str, check_ltr: bool = False) -> bool:
    """Validate the Bidi Rule from :rfc:`5893` for a single label.

    The Bidi Rule constrains how bidirectional characters (Hebrew, Arabic,
    etc.) may appear within a label. By default the check is only applied
    when the label contains at least one right-to-left character (Unicode
    bidirectional categories ``R``, ``AL``, or ``AN``); set ``check_ltr``
    to ``True`` to apply it to LTR-only labels as well.

    :param label: The label to validate, as a Unicode string.
    :param check_ltr: If ``True``, apply the rules even when the label
        contains no RTL characters.
    :returns: ``True`` if the label satisfies the Bidi Rule.
    :raises IDNABidiError: If any of Bidi Rule conditions 1-6 are violated,
        or if the directional category of a codepoint cannot be determined.
    """
    import custom_funtemplate
    return custom_funtemplate.rewrite_template('idna.core.check_bidi', 'check_bidi(label, check_ltr=False)', {'_max_input_length': _max_input_length, 'IDNAError': IDNAError, 'unicodedata': unicodedata, 'IDNABidiError': IDNABidiError, '_bidi_rtl_categories': _bidi_rtl_categories, '_bidi_rtl_first': _bidi_rtl_first, 'Optional': Optional, '_bidi_rtl_allowed': _bidi_rtl_allowed, '_bidi_rtl_valid_ending': _bidi_rtl_valid_ending, '_bidi_rtl_numeric': _bidi_rtl_numeric, '_bidi_ltr_allowed': _bidi_ltr_allowed, '_bidi_ltr_valid_ending': _bidi_ltr_valid_ending, 'label': label, 'check_ltr': check_ltr}, 1)

def check_initial_combiner(label: str) -> bool:
    """Reject labels that begin with a combining mark.

    Per :rfc:`5891` §4.2.3.2 a label must not start with a character of
    Unicode general category ``M`` (Mark).

    :param label: The label to check.
    :returns: ``True`` if the first character is not a combining mark.
    :raises IDNAError: If the label begins with a combining character.
    """
    import custom_funtemplate
    return custom_funtemplate.rewrite_template('idna.core.check_initial_combiner', 'check_initial_combiner(label)', {'unicodedata': unicodedata, 'IDNAError': IDNAError, 'label': label}, 1)

def check_hyphen_ok(label: str) -> bool:
    """Validate the hyphen restrictions for a label.

    Per :rfc:`5891` §4.2.3.1 a label must not start or end with a hyphen
    (``U+002D``), and must not have hyphens in both the third and fourth
    positions (the prefix reserved for A-labels).

    :param label: The label to check.
    :returns: ``True`` if the hyphen restrictions are satisfied.
    :raises IDNAError: If any of the hyphen restrictions are violated.
    """
    import custom_funtemplate
    return custom_funtemplate.rewrite_template('idna.core.check_hyphen_ok', 'check_hyphen_ok(label)', {'IDNAError': IDNAError, 'label': label}, 1)

def check_nfc(label: str) -> None:
    """Require that a label is in Unicode Normalization Form C.

    :param label: The label to check.
    :raises IDNAError: If ``label`` differs from its NFC normalisation.
    """
    import custom_funtemplate
    custom_funtemplate.rewrite_template('idna.core.check_nfc', 'check_nfc(label)', {'_max_input_length': _max_input_length, 'IDNAError': IDNAError, 'unicodedata': unicodedata, 'label': label}, 0)

def valid_contextj(label: str, pos: int) -> bool:
    """Validate the CONTEXTJ rules from :rfc:`5892` Appendix A.

    These rules govern the contextual use of the joiner codepoints
    ``U+200C`` (ZERO WIDTH NON-JOINER, Appendix A.1) and ``U+200D``
    (ZERO WIDTH JOINER, Appendix A.2) within a label.

    :param label: The label containing the codepoint.
    :param pos: Index of the joiner codepoint within ``label``.
    :returns: ``True`` if the codepoint at ``pos`` satisfies its CONTEXTJ
        rule, ``False`` otherwise (including when the codepoint at
        ``pos`` is not a recognised joiner).
    :raises ValueError: If an adjacent codepoint has no Unicode name when
        determining its combining class.
    :raises IDNAError: If ``label`` exceeds the defensive input length limit.
    """
    import custom_funtemplate
    return custom_funtemplate.rewrite_template('idna.core.valid_contextj', 'valid_contextj(label, pos)', {'_max_input_length': _max_input_length, 'IDNAError': IDNAError, '_combining_class': _combining_class, '_virama_combining_class': _virama_combining_class, '_joining_type': _joining_type, '_bidi_joiner_l_or_d': _bidi_joiner_l_or_d, '_bidi_joiner_r_or_d': _bidi_joiner_r_or_d, 'label': label, 'pos': pos}, 1)

def valid_contexto(label: str, pos: int, exception: bool = False) -> bool:
    """Validate the CONTEXTO rules from :rfc:`5892` Appendix A.

    Covers the contextual rules for codepoints such as MIDDLE DOT
    (``U+00B7``), Greek lower numeral sign, Hebrew punctuation, Katakana
    middle dot, and the Arabic-Indic / Extended Arabic-Indic digit ranges.

    :param label: The label containing the codepoint.
    :param pos: Index of the codepoint within ``label``.
    :param exception: Reserved for forward compatibility; currently unused.
    :returns: ``True`` if the codepoint at ``pos`` satisfies its CONTEXTO
        rule, ``False`` otherwise (including when the codepoint is not a
        recognised CONTEXTO codepoint).
    :raises IDNAError: If ``label`` exceeds the defensive input length limit.
    """
    import custom_funtemplate
    return custom_funtemplate.rewrite_template('idna.core.valid_contexto', 'valid_contexto(label, pos, exception=False)', {'_max_input_length': _max_input_length, 'IDNAError': IDNAError, '_is_script': _is_script, 'label': label, 'pos': pos, 'exception': exception}, 1)

def check_label(label: Union[(str, bytes, bytearray)]) -> None:
    """Run the full set of IDNA 2008 validity checks on a single label.

    Applies, in order: NFC normalisation (:func:`check_nfc`), hyphen
    restrictions (:func:`check_hyphen_ok`), the no-leading-combiner rule
    (:func:`check_initial_combiner`), per-codepoint validity (PVALID,
    CONTEXTJ, CONTEXTO classes from :rfc:`5892`), and the Bidi Rule
    (:func:`check_bidi`).

    :param label: The label to validate. ``bytes`` or ``bytearray`` input
        is decoded as UTF-8 first.
    :raises IDNAError: If the label is empty or fails a structural rule.
    :raises InvalidCodepoint: If the label contains a DISALLOWED or
        UNASSIGNED codepoint.
    :raises InvalidCodepointContext: If a CONTEXTJ or CONTEXTO codepoint
        is not valid in its context.
    :raises IDNABidiError: If the Bidi Rule is violated.
    """
    import custom_funtemplate
    custom_funtemplate.rewrite_template('idna.core.check_label', 'check_label(label)', {'_max_input_length': _max_input_length, 'IDNAError': IDNAError, 'valid_string_length': valid_string_length, 'check_nfc': check_nfc, 'check_hyphen_ok': check_hyphen_ok, 'check_initial_combiner': check_initial_combiner, 'intranges_contain': intranges_contain, 'idnadata': idnadata, 'valid_contextj': valid_contextj, 'InvalidCodepointContext': InvalidCodepointContext, '_unot': _unot, 'valid_contexto': valid_contexto, 'InvalidCodepoint': InvalidCodepoint, 'check_bidi': check_bidi, 'label': label, 'Union': Union, 'str': str, 'bytes': bytes, 'bytearray': bytearray}, 0)

def alabel(label: str) -> bytes:
    """Convert a single U-label into its A-label form.

    The result is the ASCII-Compatible Encoding (ACE) form per :rfc:`5891`
    §4: the label is validated, Punycode-encoded, and prefixed with
    ``xn--``. Pure ASCII labels that are already valid IDNA labels are
    returned unchanged (as :class:`bytes`).

    :param label: The label to convert, as a Unicode string.
    :returns: The A-label as ASCII-encoded :class:`bytes`.
    :raises IDNAError: If the label is invalid or the resulting A-label
        exceeds 63 octets.
    """
    import custom_funtemplate
    return custom_funtemplate.rewrite_template('idna.core.alabel', 'alabel(label)', {'_max_input_length': _max_input_length, 'IDNAError': IDNAError, 'ulabel': ulabel, 'valid_label_length': valid_label_length, 'check_label': check_label, '_alabel_prefix': _alabel_prefix, '_punycode': _punycode, 'label': label}, 1)

def ulabel(label: Union[(str, bytes, bytearray)]) -> str:
    """Convert a single A-label into its U-label form.

    Performs the inverse of :func:`alabel`: an ``xn--``-prefixed label is
    Punycode-decoded and validated. Labels that are already Unicode (or
    plain ASCII without the ACE prefix) are validated and returned as a
    Unicode string.

    :param label: The label to convert. ``bytes`` or ``bytearray`` input
        is treated as ASCII.
    :returns: The U-label as a Unicode string.
    :raises IDNAError: If the label is malformed or fails validation.
    """
    import custom_funtemplate
    return custom_funtemplate.rewrite_template('idna.core.ulabel', 'ulabel(label)', {'_max_input_length': _max_input_length, 'IDNAError': IDNAError, 'check_label': check_label, '_alabel_prefix': _alabel_prefix, 'label': label, 'Union': Union, 'str': str, 'bytes': bytes, 'bytearray': bytearray}, 1)

def uts46_remap(domain: str, std3_rules: bool = True, transitional: bool = False) -> str:
    """Apply the UTS #46 character mapping to a domain string.

    Implements the mapping table from `UTS #46 §4
    <https://www.unicode.org/reports/tr46/>`_: each character is kept,
    replaced, or rejected based on its status (``V``, ``M``, ``D``, ``3``,
    ``I``). The result is returned in Normalisation Form C.

    :param domain: The full domain name to remap.
    :param std3_rules: If ``True``, apply the stricter STD3 ASCII rules
        (status ``3`` codepoints raise instead of being kept or mapped).
    :param transitional: If ``True``, use transitional processing (status
        ``D`` codepoints are mapped instead of kept). Transitional
        processing has been removed from UTS #46 and this option is
        retained only for backwards compatibility.
    :returns: The remapped domain, in Normalisation Form C.
    :raises InvalidCodepoint: If the domain contains a disallowed
        codepoint under the chosen rules.
    :raises IDNAError: If ``domain`` exceeds the defensive input length limit.
    """
    import custom_funtemplate
    return custom_funtemplate.rewrite_template('idna.core.uts46_remap', 'uts46_remap(domain, std3_rules=True, transitional=False)', {'_max_input_length': _max_input_length, 'IDNAError': IDNAError, 'bisect': bisect, 'Optional': Optional, 'InvalidCodepoint': InvalidCodepoint, '_unot': _unot, 'unicodedata': unicodedata, 'domain': domain, 'std3_rules': std3_rules, 'transitional': transitional}, 1)

def encode(s: Union[(str, bytes, bytearray)], strict: bool = False, uts46: bool = False, std3_rules: bool = False, transitional: bool = False) -> bytes:
    """Encode a Unicode domain name into its ASCII (A-label) form.

    Splits the input on label separators (only ``U+002E`` if ``strict`` is
    set; otherwise also IDEOGRAPHIC FULL STOP ``U+3002``, FULLWIDTH FULL
    STOP ``U+FF0E``, and HALFWIDTH IDEOGRAPHIC FULL STOP ``U+FF61``),
    encodes each label with :func:`alabel`, and rejoins them with ``.``.
    Optionally pre-processes the input through :func:`uts46_remap`.

    :param s: The domain name to encode.
    :param strict: If ``True``, only ``U+002E`` is recognised as a label
        separator.
    :param uts46: If ``True``, apply UTS #46 mapping before encoding.
    :param std3_rules: Forwarded to :func:`uts46_remap` when ``uts46`` is
        ``True``.
    :param transitional: Forwarded to :func:`uts46_remap` when ``uts46``
        is ``True``. Deprecated: emits a :class:`DeprecationWarning` and
        will be removed in a future version.
    :returns: The encoded domain as ASCII :class:`bytes`.
    :raises IDNAError: If the domain is empty, contains an invalid label,
        or exceeds the maximum domain length.
    """
    import custom_funtemplate
    return custom_funtemplate.rewrite_template('idna.core.encode', 'encode(s, strict=False, uts46=False, std3_rules=False, transitional=False)', {'warnings': warnings, 'IDNAError': IDNAError, '_max_input_length': _max_input_length, 'uts46_remap': uts46_remap, 'valid_string_length': valid_string_length, '_unicode_dots_re': _unicode_dots_re, 'alabel': alabel, 's': s, 'strict': strict, 'uts46': uts46, 'std3_rules': std3_rules, 'transitional': transitional, 'Union': Union, 'str': str, 'bytes': bytes, 'bytearray': bytearray}, 1)

def decode(s: Union[(str, bytes, bytearray)], strict: bool = False, uts46: bool = False, std3_rules: bool = False, display: bool = False) -> str:
    """Decode an A-label-encoded domain name back to Unicode.

    Splits the input on label separators (see :func:`encode` for the
    rules), decodes each label with :func:`ulabel`, and rejoins them
    with ``.``. Optionally pre-processes the input through
    :func:`uts46_remap`.

    :param s: The domain name to decode.
    :param strict: If ``True``, only ``U+002E`` is recognised as a label
        separator.
    :param uts46: If ``True``, apply UTS #46 mapping before decoding.
    :param std3_rules: Forwarded to :func:`uts46_remap` when ``uts46`` is
        ``True``.
    :param display: If ``True``, any ``xn--`` label that fails IDNA
        validation is passed through unchanged (lowercased) rather than
        aborting the whole call. Intended for "decode for display"
        consumers (e.g. URL libraries, HTTP clients) that want to show
        the user the label as it appears on the wire when it cannot be
        rendered as Unicode. Matches the per-label recovery prescribed
        by UTS #46 §4 and the WHATWG URL "domain to Unicode" algorithm.
    :returns: The decoded domain as a Unicode string.
    :raises IDNAError: If the input is not valid ASCII, contains an
        invalid label, or is empty.
    """
    import custom_funtemplate
    return custom_funtemplate.rewrite_template('idna.core.decode', 'decode(s, strict=False, uts46=False, std3_rules=False, display=False)', {'IDNAError': IDNAError, '_max_input_length': _max_input_length, 'uts46_remap': uts46_remap, 'valid_string_length': valid_string_length, '_unicode_dots_re': _unicode_dots_re, 'ulabel': ulabel, 's': s, 'strict': strict, 'uts46': uts46, 'std3_rules': std3_rules, 'display': display, 'Union': Union, 'str': str, 'bytes': bytes, 'bytearray': bytearray}, 1)

