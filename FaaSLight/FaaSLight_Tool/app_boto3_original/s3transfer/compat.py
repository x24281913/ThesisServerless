import errno
import inspect
import os
import socket
import sys
from botocore.compat import six
if sys.platform.startswith('win'):
    
    def rename_file(current_filename, new_filename):
        import custom_funtemplate
        custom_funtemplate.rewrite_template('s3transfer.compat.rename_file', 'rename_file(current_filename, new_filename)', {'os': os, 'errno': errno, 'current_filename': current_filename, 'new_filename': new_filename}, 0)
else:
    rename_file = os.rename

def accepts_kwargs(func):
    return inspect.getfullargspec(func)[2]
SOCKET_ERROR = ConnectionError
MAXINT = None

def seekable(fileobj):
    """Backwards compat function to determine if a fileobj is seekable

    :param fileobj: The file-like object to determine if seekable

    :returns: True, if seekable. False, otherwise.
    """
    import custom_funtemplate
    return custom_funtemplate.rewrite_template('s3transfer.compat.seekable', 'seekable(fileobj)', {'fileobj': fileobj}, 1)

def readable(fileobj):
    """Determines whether or not a file-like object is readable.

    :param fileobj: The file-like object to determine if readable

    :returns: True, if readable. False otherwise.
    """
    import custom_funtemplate
    return custom_funtemplate.rewrite_template('s3transfer.compat.readable', 'readable(fileobj)', {'fileobj': fileobj}, 1)

def fallocate(fileobj, size):
    import custom_funtemplate
    custom_funtemplate.rewrite_template('s3transfer.compat.fallocate', 'fallocate(fileobj, size)', {'os': os, 'fileobj': fileobj, 'size': size}, 0)
from multiprocessing.managers import BaseManager

