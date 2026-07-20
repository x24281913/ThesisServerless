import sys
import os
import errno
import socket
import warnings
from boto3.exceptions import PythonDeprecationWarning
from s3transfer.manager import TransferConfig
SOCKET_ERROR = ConnectionError
_APPEND_MODE_CHAR = 'a'
import collections.abc as collections_abc
TRANSFER_CONFIG_SUPPORTS_CRT = hasattr(TransferConfig, 'UNSET_DEFAULT')
if sys.platform.startswith('win'):
    
    def rename_file(current_filename, new_filename):
        import custom_funtemplate
        custom_funtemplate.rewrite_template('boto3.compat.rename_file', 'rename_file(current_filename, new_filename)', {'os': os, 'errno': errno, 'current_filename': current_filename, 'new_filename': new_filename}, 0)
else:
    rename_file = os.rename

def filter_python_deprecation_warnings():
    """
    Invoking this filter acknowledges your runtime will soon be deprecated
    at which time you will stop receiving all updates to your client.
    """
    warnings.filterwarnings('ignore', message='.*Boto3 will no longer support Python.*', category=PythonDeprecationWarning, module='.*boto3\\.compat')

def _warn_deprecated_python():
    """Use this template for future deprecation campaigns as needed."""
    import custom_funtemplate
    custom_funtemplate.rewrite_template('boto3.compat._warn_deprecated_python', '_warn_deprecated_python()', {'sys': sys, 'warnings': warnings, 'PythonDeprecationWarning': PythonDeprecationWarning}, 0)

def is_append_mode(fileobj):
    return (hasattr(fileobj, 'mode') and isinstance(fileobj.mode, str) and _APPEND_MODE_CHAR in fileobj.mode)

