import logging
from logging import NullHandler
from boto3.compat import _warn_deprecated_python
from boto3.session import Session
__author__ = 'Amazon Web Services'
__version__ = '1.42.97'
DEFAULT_SESSION = None

def setup_default_session(**kwargs):
    """
    Set up a default session, passing through any parameters to the session
    constructor. There is no need to call this unless you wish to pass custom
    parameters, because a default session will be created for you.
    """
    global DEFAULT_SESSION
    DEFAULT_SESSION = Session(**kwargs)

def set_stream_logger(name='boto3', level=logging.DEBUG, format_string=None):
    """
    Add a stream handler for the given name and level to the logging module.
    By default, this logs all boto3 messages to ``stdout``.

        >>> import boto3
        >>> boto3.set_stream_logger('boto3.resources', logging.INFO)

    For debugging purposes a good choice is to set the stream logger to ``''``
    which is equivalent to saying "log everything".

    .. WARNING::
       Be aware that when logging anything from ``'botocore'`` the full wire
       trace will appear in your logs. If your payloads contain sensitive data
       this should not be used in production.

    :type name: string
    :param name: Log name
    :type level: int
    :param level: Logging level, e.g. ``logging.INFO``
    :type format_string: str
    :param format_string: Log message format
    """
    import custom_funtemplate
    custom_funtemplate.rewrite_template('boto3.__init__.set_stream_logger', "set_stream_logger(name='boto3', level=logging.DEBUG, format_string=None)", {'logging': logging, 'name': name, 'level': level, 'format_string': format_string}, 0)

def _get_default_session():
    """
    Get the default session, creating one if needed.

    :rtype: :py:class:`~boto3.session.Session`
    :return: The default session
    """
    import custom_funtemplate
    return custom_funtemplate.rewrite_template('boto3.__init__._get_default_session', '_get_default_session()', {'DEFAULT_SESSION': DEFAULT_SESSION, 'setup_default_session': setup_default_session, '_warn_deprecated_python': _warn_deprecated_python}, 1)

def client(*args, **kwargs):
    """
    Create a low-level service client by name using the default session.

    See :py:meth:`boto3.session.Session.client`.
    """
    return _get_default_session().client(*args, **kwargs)

def resource(*args, **kwargs):
    """
    Create a resource service client by name using the default session.

    See :py:meth:`boto3.session.Session.resource`.
    """
    return _get_default_session().resource(*args, **kwargs)
logging.getLogger('boto3').addHandler(NullHandler())

