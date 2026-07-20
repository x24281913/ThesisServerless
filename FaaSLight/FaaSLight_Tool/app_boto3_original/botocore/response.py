import logging
from io import IOBase
from urllib3.exceptions import ProtocolError as URLLib3ProtocolError
from urllib3.exceptions import ReadTimeoutError as URLLib3ReadTimeoutError
from botocore import ScalarTypes, parsers
from botocore.compat import XMLParseError, set_socket_timeout
from botocore.exceptions import IncompleteReadError, ReadTimeoutError, ResponseStreamingError
from botocore.hooks import first_non_none_response
logger = logging.getLogger(__name__)


class StreamingBody(IOBase):
    """Wrapper class for an http response body.

    This provides a few additional conveniences that do not exist
    in the urllib3 model:

        * Set the timeout on the socket (i.e read() timeouts)
        * Auto validation of content length, if the amount of bytes
          we read does not match the content length, an exception
          is raised.

    """
    _DEFAULT_CHUNK_SIZE = 1024
    
    def __init__(self, raw_stream, content_length):
        self._raw_stream = raw_stream
        self._content_length = content_length
        self._amount_read = 0
    
    def __del__(self):
        pass
    
    def set_socket_timeout(self, timeout):
        """Set the timeout seconds on the socket."""
        try:
            set_socket_timeout(self._raw_stream, timeout)
        except AttributeError:
            logger.exception("Cannot access the socket object of a streaming response. It's possible the interface has changed.")
            raise
    
    def readable(self):
        try:
            return self._raw_stream.readable()
        except AttributeError:
            return False
    
    def read(self, amt=None):
        """Read at most amt bytes from the stream.

        If the amt argument is omitted, read all data.
        """
        try:
            chunk = self._raw_stream.read(amt)
        except URLLib3ReadTimeoutError as e:
            raise ReadTimeoutError(endpoint_url=e.url, error=e)
        except URLLib3ProtocolError as e:
            raise ResponseStreamingError(error=e)
        self._amount_read += len(chunk)
        if (amt is None or (not chunk and amt > 0)):
            self._verify_content_length()
        return chunk
    
    def readinto(self, b):
        """Read bytes into a pre-allocated, writable bytes-like object b, and return the number of bytes read."""
        try:
            amount_read = self._raw_stream.readinto(b)
        except URLLib3ReadTimeoutError as e:
            raise ReadTimeoutError(endpoint_url=e.url, error=e)
        except URLLib3ProtocolError as e:
            raise ResponseStreamingError(error=e)
        self._amount_read += amount_read
        if (amount_read == 0 and len(b) > 0):
            self._verify_content_length()
        return amount_read
    
    def readlines(self):
        return self._raw_stream.readlines()
    
    def __iter__(self):
        """Return an iterator to yield 1k chunks from the raw stream."""
        return self.iter_chunks(self._DEFAULT_CHUNK_SIZE)
    
    def __next__(self):
        """Return the next 1k chunk from the raw stream."""
        current_chunk = self.read(self._DEFAULT_CHUNK_SIZE)
        if current_chunk:
            return current_chunk
        raise StopIteration()
    
    def __enter__(self):
        return self._raw_stream
    
    def __exit__(self, type, value, traceback):
        self._raw_stream.close()
    next = __next__
    
    def iter_lines(self, chunk_size=_DEFAULT_CHUNK_SIZE, keepends=False):
        """Return an iterator to yield lines from the raw stream.

        This is achieved by reading chunk of bytes (of size chunk_size) at a
        time from the raw stream, and then yielding lines from there.
        """
        pending = b''
        for chunk in self.iter_chunks(chunk_size):
            lines = (pending + chunk).splitlines(True)
            for line in lines[:-1]:
                yield line.splitlines(keepends)[0]
            pending = lines[-1]
        if pending:
            yield pending.splitlines(keepends)[0]
    
    def iter_chunks(self, chunk_size=_DEFAULT_CHUNK_SIZE):
        """Return an iterator to yield chunks of chunk_size bytes from the raw
        stream.
        """
        while True:
            current_chunk = self.read(chunk_size)
            if current_chunk == b'':
                break
            yield current_chunk
    
    def _verify_content_length(self):
        if (self._content_length is not None and self._amount_read != int(self._content_length)):
            raise IncompleteReadError(actual_bytes=self._amount_read, expected_bytes=int(self._content_length))
    
    def tell(self):
        return self._raw_stream.tell()
    
    def close(self):
        """Close the underlying http response stream."""
        self._raw_stream.close()


def get_response(operation_model, http_response):
    protocol = operation_model.service_model.resolved_protocol
    response_dict = {'headers': http_response.headers, 'status_code': http_response.status_code}
    if response_dict['status_code'] >= 300:
        response_dict['body'] = http_response.content
    elif operation_model.has_streaming_output:
        response_dict['body'] = StreamingBody(http_response.raw, response_dict['headers'].get('content-length'))
    else:
        response_dict['body'] = http_response.content
    parser = parsers.create_parser(protocol)
    return (http_response, parser.parse(response_dict, operation_model.output_shape))

