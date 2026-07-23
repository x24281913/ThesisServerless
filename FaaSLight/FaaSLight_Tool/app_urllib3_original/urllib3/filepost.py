from __future__ import annotations
import binascii
import codecs
import os
import typing
from io import BytesIO
from .fields import _TYPE_FIELD_VALUE_TUPLE, RequestField
writer = codecs.lookup('utf-8')[3]
_TYPE_FIELDS_SEQUENCE = typing.Sequence[typing.Union[(tuple[(str, _TYPE_FIELD_VALUE_TUPLE)], RequestField)]]
_TYPE_FIELDS = typing.Union[(_TYPE_FIELDS_SEQUENCE, typing.Mapping[(str, _TYPE_FIELD_VALUE_TUPLE)])]

def choose_boundary() -> str:
    """
    Our embarrassingly-simple replacement for mimetools.choose_boundary.
    """
    return binascii.hexlify(os.urandom(16)).decode()

def iter_field_objects(fields: _TYPE_FIELDS) -> typing.Iterable[RequestField]:
    """
    Iterate over fields.

    Supports list of (k, v) tuples and dicts, and lists of
    :class:`~urllib3.fields.RequestField`.

    """
    import custom_funtemplate
    custom_funtemplate.rewrite_template('urllib3.filepost.iter_field_objects', 'iter_field_objects(fields)', {'typing': typing, 'RequestField': RequestField, '_TYPE_FIELD_VALUE_TUPLE': _TYPE_FIELD_VALUE_TUPLE, 'fields': fields, 'typing': typing, 'RequestField': RequestField}, 0)

def encode_multipart_formdata(fields: _TYPE_FIELDS, boundary: str | None = None) -> tuple[(bytes, str)]:
    """
    Encode a dictionary of ``fields`` using the multipart/form-data MIME format.

    :param fields:
        Dictionary of fields or list of (key, :class:`~urllib3.fields.RequestField`).
        Values are processed by :func:`urllib3.fields.RequestField.from_tuples`.

    :param boundary:
        If not specified, then a random boundary will be generated using
        :func:`urllib3.filepost.choose_boundary`.
    """
    import custom_funtemplate
    return custom_funtemplate.rewrite_template('urllib3.filepost.encode_multipart_formdata', 'encode_multipart_formdata(fields, boundary=None)', {'BytesIO': BytesIO, 'choose_boundary': choose_boundary, 'iter_field_objects': iter_field_objects, 'writer': writer, 'fields': fields, 'boundary': boundary, 'str': str, 'tuple': tuple, 'bytes': bytes, 'str': str}, 2)

