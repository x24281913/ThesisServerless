from __future__ import annotations
import select
import socket
from functools import partial
__all__ = ['wait_for_read', 'wait_for_write']

def select_wait_for_socket(sock: socket.socket, read: bool = False, write: bool = False, timeout: float | None = None) -> bool:
    import custom_funtemplate
    return custom_funtemplate.rewrite_template('urllib3.util.wait.select_wait_for_socket', 'select_wait_for_socket(sock, read=False, write=False, timeout=None)', {'partial': partial, 'select': select, 'sock': sock, 'read': read, 'write': write, 'timeout': timeout, 'socket': socket, 'float': float}, 1)

def poll_wait_for_socket(sock: socket.socket, read: bool = False, write: bool = False, timeout: float | None = None) -> bool:
    import custom_funtemplate
    return custom_funtemplate.rewrite_template('urllib3.util.wait.poll_wait_for_socket', 'poll_wait_for_socket(sock, read=False, write=False, timeout=None)', {'select': select, 'sock': sock, 'read': read, 'write': write, 'timeout': timeout, 'socket': socket, 'float': float}, 1)

def _have_working_poll() -> bool:
    import custom_funtemplate
    return custom_funtemplate.rewrite_template('urllib3.util.wait._have_working_poll', '_have_working_poll()', {'select': select}, 1)

def wait_for_socket(sock: socket.socket, read: bool = False, write: bool = False, timeout: float | None = None) -> bool:
    import custom_funtemplate
    return custom_funtemplate.rewrite_template('urllib3.util.wait.wait_for_socket', 'wait_for_socket(sock, read=False, write=False, timeout=None)', {'_have_working_poll': _have_working_poll, 'poll_wait_for_socket': poll_wait_for_socket, 'select': select, 'select_wait_for_socket': select_wait_for_socket, 'sock': sock, 'read': read, 'write': write, 'timeout': timeout, 'socket': socket, 'float': float}, 1)

def wait_for_read(sock: socket.socket, timeout: float | None = None) -> bool:
    """Waits for reading to be available on a given socket.
    Returns True if the socket is readable, or False if the timeout expired.
    """
    return wait_for_socket(sock, read=True, timeout=timeout)

def wait_for_write(sock: socket.socket, timeout: float | None = None) -> bool:
    """Waits for writing to be available on a given socket.
    Returns True if the socket is readable, or False if the timeout expired.
    """
    return wait_for_socket(sock, write=True, timeout=timeout)

