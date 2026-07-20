import errno
import select
import sys
from functools import partial
try:
    from time import monotonic
except ImportError:
    from time import time as monotonic
__all__ = ['NoWayToWaitForSocketError', 'wait_for_read', 'wait_for_write']


class NoWayToWaitForSocketError(Exception):
    pass

if sys.version_info >= (3, 5):
    
    def _retry_on_intr(fn, timeout):
        return fn(timeout)
else:
    
    def _retry_on_intr(fn, timeout):
        import custom_funtemplate
        return custom_funtemplate.rewrite_template('urllib3.util.wait._retry_on_intr', '_retry_on_intr(fn, timeout)', {'monotonic': monotonic, 'select': select, 'errno': errno, 'fn': fn, 'timeout': timeout}, 1)

def select_wait_for_socket(sock, read=False, write=False, timeout=None):
    import custom_funtemplate
    return custom_funtemplate.rewrite_template('urllib3.util.wait.select_wait_for_socket', 'select_wait_for_socket(sock, read=False, write=False, timeout=None)', {'partial': partial, 'select': select, '_retry_on_intr': _retry_on_intr, 'sock': sock, 'read': read, 'write': write, 'timeout': timeout}, 1)

def poll_wait_for_socket(sock, read=False, write=False, timeout=None):
    import custom_funtemplate
    return custom_funtemplate.rewrite_template('urllib3.util.wait.poll_wait_for_socket', 'poll_wait_for_socket(sock, read=False, write=False, timeout=None)', {'select': select, '_retry_on_intr': _retry_on_intr, 'sock': sock, 'read': read, 'write': write, 'timeout': timeout}, 1)

def null_wait_for_socket(*args, **kwargs):
    raise NoWayToWaitForSocketError('no select-equivalent available')

def _have_working_poll():
    import custom_funtemplate
    return custom_funtemplate.rewrite_template('urllib3.util.wait._have_working_poll', '_have_working_poll()', {'select': select, '_retry_on_intr': _retry_on_intr}, 1)

def wait_for_socket(*args, **kwargs):
    import custom_funtemplate
    return custom_funtemplate.rewrite_template('urllib3.util.wait.wait_for_socket', 'wait_for_socket(*args, **kwargs)', {'_have_working_poll': _have_working_poll, 'poll_wait_for_socket': poll_wait_for_socket, 'select': select, 'select_wait_for_socket': select_wait_for_socket, 'null_wait_for_socket': null_wait_for_socket, 'args': args, 'kwargs': kwargs}, 1)

def wait_for_read(sock, timeout=None):
    """Waits for reading to be available on a given socket.
    Returns True if the socket is readable, or False if the timeout expired.
    """
    return wait_for_socket(sock, read=True, timeout=timeout)

def wait_for_write(sock, timeout=None):
    """Waits for writing to be available on a given socket.
    Returns True if the socket is readable, or False if the timeout expired.
    """
    return wait_for_socket(sock, write=True, timeout=timeout)

