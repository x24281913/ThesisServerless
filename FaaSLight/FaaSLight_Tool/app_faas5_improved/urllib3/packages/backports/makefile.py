"""
backports.makefile
~~~~~~~~~~~~~~~~~~

Backports the Python 3 ``socket.makefile`` method for use with anything that
wants to create a "fake" socket object.
"""

import io
from socket import SocketIO

def backport_makefile(self, mode='r', buffering=None, encoding=None, errors=None, newline=None):
    """
    Backport of ``socket.makefile`` from Python 3.5.
    """
    import custom_funtemplate
    return custom_funtemplate.rewrite_template('urllib3.packages.backports.makefile.backport_makefile', "backport_makefile(self, mode='r', buffering=None, encoding=None, errors=None, newline=None)", {'SocketIO': SocketIO, 'io': io, 'self': self, 'mode': mode, 'buffering': buffering, 'encoding': encoding, 'errors': errors, 'newline': newline}, 1)

