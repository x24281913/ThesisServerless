from __future__ import annotations
import http.client as httplib
from email.errors import MultipartInvariantViolationDefect, StartBoundaryNotFoundDefect
from ..exceptions import HeaderParsingError

def is_fp_closed(obj: object) -> bool:
    """
    Checks whether a given file-like object is closed.

    :param obj:
        The file-like object to check.
    """
    try:
        return obj.isclosed()
    except AttributeError:
        pass
    try:
        return obj.closed
    except AttributeError:
        pass
    try:
        return obj.fp is None
    except AttributeError:
        pass
    raise ValueError('Unable to determine whether fp is closed.')

def assert_header_parsing(headers: httplib.HTTPMessage) -> None:
    """
    Asserts whether all headers have been successfully parsed.
    Extracts encountered errors from the result of parsing headers.

    Only works on Python 3.

    :param http.client.HTTPMessage headers: Headers to verify.

    :raises urllib3.exceptions.HeaderParsingError:
        If parsing errors are found.
    """
    import custom_funtemplate
    custom_funtemplate.rewrite_template('urllib3.util.response.assert_header_parsing', 'assert_header_parsing(headers)', {'httplib': httplib, 'StartBoundaryNotFoundDefect': StartBoundaryNotFoundDefect, 'MultipartInvariantViolationDefect': MultipartInvariantViolationDefect, 'HeaderParsingError': HeaderParsingError, 'headers': headers, 'httplib': httplib}, 0)

def is_response_to_head(response: httplib.HTTPResponse) -> bool:
    """
    Checks whether the request of a response has been a HEAD-request.

    :param http.client.HTTPResponse response:
        Response to check if the originating request
        used 'HEAD' as a method.
    """
    method_str = response._method
    return method_str.upper() == 'HEAD'

