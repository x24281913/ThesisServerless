"""Abstractions over S3's upload/download operations.

This module provides high level abstractions for efficient
uploads/downloads.  It handles several things for the user:

* Automatically switching to multipart transfers when
  a file is over a specific size threshold
* Uploading/downloading a file in parallel
* Progress callbacks to monitor transfers
* Retries.  While botocore handles retries for streaming uploads,
  it is not possible for it to handle retries for streaming
  downloads.  This module handles retries for both cases so
  you don't need to implement any retry logic yourself.

This module has a reasonable set of defaults.  It also allows you
to configure many aspects of the transfer process including:

* Multipart threshold size
* Max parallel downloads
* Socket timeouts
* Retry amounts

There is no support for s3->s3 multipart copies at this
time.


.. _ref_s3transfer_usage:

Usage
=====

The simplest way to use this module is:

.. code-block:: python

    client = boto3.client('s3', 'us-west-2')
    transfer = S3Transfer(client)
    # Upload /tmp/myfile to s3://bucket/key
    transfer.upload_file('/tmp/myfile', 'bucket', 'key')

    # Download s3://bucket/key to /tmp/myfile
    transfer.download_file('bucket', 'key', '/tmp/myfile')

The ``upload_file`` and ``download_file`` methods also accept
``**kwargs``, which will be forwarded through to the corresponding
client operation.  Here are a few examples using ``upload_file``::

    # Making the object public
    transfer.upload_file('/tmp/myfile', 'bucket', 'key',
                         extra_args={'ACL': 'public-read'})

    # Setting metadata
    transfer.upload_file('/tmp/myfile', 'bucket', 'key',
                         extra_args={'Metadata': {'a': 'b', 'c': 'd'}})

    # Setting content type
    transfer.upload_file('/tmp/myfile.json', 'bucket', 'key',
                         extra_args={'ContentType': "application/json"})


The ``S3Transfer`` class also supports progress callbacks so you can
provide transfer progress to users.  Both the ``upload_file`` and
``download_file`` methods take an optional ``callback`` parameter.
Here's an example of how to print a simple progress percentage
to the user:

.. code-block:: python

    class ProgressPercentage(object):
        def __init__(self, filename):
            self._filename = filename
            self._size = float(os.path.getsize(filename))
            self._seen_so_far = 0
            self._lock = threading.Lock()

        def __call__(self, bytes_amount):
            # To simplify we'll assume this is hooked up
            # to a single filename.
            with self._lock:
                self._seen_so_far += bytes_amount
                percentage = (self._seen_so_far / self._size) * 100
                sys.stdout.write(
                    "
%s  %s / %s  (%.2f%%)" % (
                        self._filename, self._seen_so_far, self._size,
                        percentage))
                sys.stdout.flush()


    transfer = S3Transfer(boto3.client('s3', 'us-west-2'))
    # Upload /tmp/myfile to s3://bucket/key and print upload progress.
    transfer.upload_file('/tmp/myfile', 'bucket', 'key',
                         callback=ProgressPercentage('/tmp/myfile'))



You can also provide a TransferConfig object to the S3Transfer
object that gives you more fine grained control over the
transfer.  For example:

.. code-block:: python

    client = boto3.client('s3', 'us-west-2')
    config = TransferConfig(
        multipart_threshold=8 * 1024 * 1024,
        max_concurrency=10,
        num_download_attempts=10,
    )
    transfer = S3Transfer(client, config)
    transfer.upload_file('/tmp/foo', 'bucket', 'key')


"""

import logging
import threading
from os import PathLike, fspath, getpid
from botocore.compat import HAS_CRT
from botocore.exceptions import ClientError, MissingDependencyException
from s3transfer.exceptions import RetriesExceededError as S3TransferRetriesExceededError
from s3transfer.futures import NonThreadedExecutor
from s3transfer.manager import TransferConfig as S3TransferConfig
from s3transfer.manager import TransferManager
from s3transfer.subscribers import BaseSubscriber
from s3transfer.utils import OSUtils
import boto3.s3.constants as constants
from boto3.compat import TRANSFER_CONFIG_SUPPORTS_CRT
from boto3.exceptions import RetriesExceededError, S3UploadFailedError
if HAS_CRT:
    import awscrt.s3
    from boto3.crt import create_crt_transfer_manager
KB = 1024
MB = KB * KB
logger = logging.getLogger(__name__)

def create_transfer_manager(client, config, osutil=None):
    """Creates a transfer manager based on configuration

    :type client: boto3.client
    :param client: The S3 client to use

    :type config: boto3.s3.transfer.TransferConfig
    :param config: The transfer config to use

    :type osutil: s3transfer.utils.OSUtils
    :param osutil: The os utility to use

    :rtype: s3transfer.manager.TransferManager
    :returns: A transfer manager based on parameters provided
    """
    import custom_funtemplate
    return custom_funtemplate.rewrite_template('boto3.s3.transfer.create_transfer_manager', 'create_transfer_manager(client, config, osutil=None)', {'_should_use_crt': _should_use_crt, 'create_crt_transfer_manager': create_crt_transfer_manager, 'logger': logger, 'getpid': getpid, 'threading': threading, '_create_default_transfer_manager': _create_default_transfer_manager, 'client': client, 'config': config, 'osutil': osutil}, 1)

def _should_use_crt(config):
    import custom_funtemplate
    return custom_funtemplate.rewrite_template('boto3.s3.transfer._should_use_crt', '_should_use_crt(config)', {'HAS_CRT': HAS_CRT, 'has_minimum_crt_version': has_minimum_crt_version, 'awscrt': awscrt, 'constants': constants, 'MissingDependencyException': MissingDependencyException, 'logger': logger, 'config': config}, 1)

def has_minimum_crt_version(minimum_version):
    """Not intended for use outside boto3."""
    import custom_funtemplate
    return custom_funtemplate.rewrite_template('boto3.s3.transfer.has_minimum_crt_version', 'has_minimum_crt_version(minimum_version)', {'HAS_CRT': HAS_CRT, 'awscrt': awscrt, 'minimum_version': minimum_version}, 1)

def _create_default_transfer_manager(client, config, osutil):
    """Create the default TransferManager implementation for s3transfer."""
    import custom_funtemplate
    return custom_funtemplate.rewrite_template('boto3.s3.transfer._create_default_transfer_manager', '_create_default_transfer_manager(client, config, osutil)', {'NonThreadedExecutor': NonThreadedExecutor, 'TransferManager': TransferManager, 'client': client, 'config': config, 'osutil': osutil}, 1)


class TransferConfig(S3TransferConfig):
    ALIAS = {'max_concurrency': 'max_request_concurrency', 'max_io_queue': 'max_io_queue_size'}
    DEFAULTS = {'multipart_threshold': 8 * MB, 'max_concurrency': 10, 'max_request_concurrency': 10, 'multipart_chunksize': 8 * MB, 'num_download_attempts': 5, 'max_io_queue': 100, 'max_io_queue_size': 100, 'io_chunksize': 256 * KB, 'use_threads': True, 'max_bandwidth': None, 'preferred_transfer_client': constants.AUTO_RESOLVE_TRANSFER_CLIENT}
    
    def __init__(self, multipart_threshold=None, max_concurrency=None, multipart_chunksize=None, num_download_attempts=None, max_io_queue=None, io_chunksize=None, use_threads=None, max_bandwidth=None, preferred_transfer_client=None):
        """Configuration object for managed S3 transfers

        :param multipart_threshold: The transfer size threshold for which
            multipart uploads, downloads, and copies will automatically be
            triggered.

        :param max_concurrency: The maximum number of threads that will be
            making requests to perform a transfer. If ``use_threads`` is
            set to ``False``, the value provided is ignored as the transfer
            will only ever use the current thread.

        :param multipart_chunksize: The partition size of each part for a
            multipart transfer.

        :param num_download_attempts: The number of download attempts that
            will be retried upon errors with downloading an object in S3.
            Note that these retries account for errors that occur when
            streaming  down the data from s3 (i.e. socket errors and read
            timeouts that occur after receiving an OK response from s3).
            Other retryable exceptions such as throttling errors and 5xx
            errors are already retried by botocore (this default is 5). This
            does not take into account the number of exceptions retried by
            botocore. Note: This value is ignored when resolved transfer
            manager type is CRTTransferManager.

        :param max_io_queue: The maximum amount of read parts that can be
            queued in memory to be written for a download. The size of each
            of these read parts is at most the size of ``io_chunksize``.
            Note: This value is ignored when resolved transfer manager type
            is CRTTransferManager.

        :param io_chunksize: The max size of each chunk in the io queue.
            Currently, this is size used when ``read`` is called on the
            downloaded stream as well. Note: This value is ignored when
            resolved transfer manager type is CRTTransferManager.

        :param use_threads: If True, threads will be used when performing
            S3 transfers. If False, no threads will be used in
            performing transfers; all logic will be run in the current thread.
            Note: This value is ignored when resolved transfer manager type is
            CRTTransferManager.

        :param max_bandwidth: The maximum bandwidth that will be consumed
            in uploading and downloading file content. The value is an integer
            in terms of bytes per second. Note: This value is ignored when
            resolved transfer manager type is CRTTransferManager.

        :param preferred_transfer_client: String specifying preferred transfer
            client for transfer operations.

            Current supported settings are:
              * auto (default) - Use the CRTTransferManager when calls
                  are made with supported environment and settings.
              * classic - Only use the origin S3TransferManager with
                  requests. Disables possible CRT upgrade on requests.
              * crt - Only use the CRTTransferManager with requests.
        """
        init_args = {'multipart_threshold': multipart_threshold, 'max_concurrency': max_concurrency, 'multipart_chunksize': multipart_chunksize, 'num_download_attempts': num_download_attempts, 'max_io_queue': max_io_queue, 'io_chunksize': io_chunksize, 'use_threads': use_threads, 'max_bandwidth': max_bandwidth, 'preferred_transfer_client': preferred_transfer_client}
        resolved = self._resolve_init_args(init_args)
        super().__init__(multipart_threshold=resolved['multipart_threshold'], max_request_concurrency=resolved['max_concurrency'], multipart_chunksize=resolved['multipart_chunksize'], num_download_attempts=resolved['num_download_attempts'], max_io_queue_size=resolved['max_io_queue'], io_chunksize=resolved['io_chunksize'], max_bandwidth=resolved['max_bandwidth'])
        for alias in self.ALIAS:
            setattr(self, alias, object.__getattribute__(self, self.ALIAS[alias]))
        self.use_threads = resolved['use_threads']
        self.preferred_transfer_client = resolved['preferred_transfer_client']
    
    def __setattr__(self, name, value):
        if name in self.ALIAS:
            super().__setattr__(self.ALIAS[name], value)
        super().__setattr__(name, value)
    
    def __getattribute__(self, item):
        value = object.__getattribute__(self, item)
        if not TRANSFER_CONFIG_SUPPORTS_CRT:
            return value
        defaults = object.__getattribute__(self, 'DEFAULTS')
        if item not in defaults:
            return value
        if value is self.UNSET_DEFAULT:
            return defaults[item]
        return value
    
    def _resolve_init_args(self, init_args):
        resolved = {}
        for (init_arg, val) in init_args.items():
            if val is not None:
                resolved[init_arg] = val
            elif TRANSFER_CONFIG_SUPPORTS_CRT:
                resolved[init_arg] = self.UNSET_DEFAULT
            else:
                resolved[init_arg] = self.DEFAULTS[init_arg]
        return resolved



class S3Transfer:
    ALLOWED_DOWNLOAD_ARGS = TransferManager.ALLOWED_DOWNLOAD_ARGS
    ALLOWED_UPLOAD_ARGS = TransferManager.ALLOWED_UPLOAD_ARGS
    ALLOWED_COPY_ARGS = TransferManager.ALLOWED_COPY_ARGS
    
    def __init__(self, client=None, config=None, osutil=None, manager=None):
        if (not client and not manager):
            raise ValueError('Either a boto3.Client or s3transfer.manager.TransferManager must be provided')
        if (manager and any([client, config, osutil])):
            raise ValueError('Manager cannot be provided with client, config, nor osutil. These parameters are mutually exclusive.')
        if config is None:
            config = TransferConfig()
        if osutil is None:
            osutil = OSUtils()
        if manager:
            self._manager = manager
        else:
            self._manager = create_transfer_manager(client, config, osutil)
    
    def upload_file(self, filename, bucket, key, callback=None, extra_args=None):
        """Upload a file to an S3 object.

        Variants have also been injected into S3 client, Bucket and Object.
        You don't have to use S3Transfer.upload_file() directly.

        .. seealso::
            :py:meth:`S3.Client.upload_file`
            :py:meth:`S3.Client.upload_fileobj`
        """
        if isinstance(filename, PathLike):
            filename = fspath(filename)
        if not isinstance(filename, str):
            raise ValueError('Filename must be a string or a path-like object')
        subscribers = self._get_subscribers(callback)
        future = self._manager.upload(filename, bucket, key, extra_args, subscribers)
        try:
            future.result()
        except ClientError as e:
            raise S3UploadFailedError(f'Failed to upload {filename} to {bucket}/{key}: {e}')
    
    def download_file(self, bucket, key, filename, extra_args=None, callback=None):
        """Download an S3 object to a file.

        Variants have also been injected into S3 client, Bucket and Object.
        You don't have to use S3Transfer.download_file() directly.

        .. seealso::
            :py:meth:`S3.Client.download_file`
            :py:meth:`S3.Client.download_fileobj`
        """
        if isinstance(filename, PathLike):
            filename = fspath(filename)
        if not isinstance(filename, str):
            raise ValueError('Filename must be a string or a path-like object')
        subscribers = self._get_subscribers(callback)
        future = self._manager.download(bucket, key, filename, extra_args, subscribers)
        try:
            future.result()
        except S3TransferRetriesExceededError as e:
            raise RetriesExceededError(e.last_exception)
    
    def _get_subscribers(self, callback):
        if not callback:
            return None
        return [ProgressCallbackInvoker(callback)]
    
    def __enter__(self):
        return self
    
    def __exit__(self, *args):
        self._manager.__exit__(*args)



class ProgressCallbackInvoker(BaseSubscriber):
    """A back-compat wrapper to invoke a provided callback via a subscriber

    :param callback: A callable that takes a single positional argument for
        how many bytes were transferred.
    """
    
    def __init__(self, callback):
        self._callback = callback
    
    def on_progress(self, bytes_transferred, **kwargs):
        self._callback(bytes_transferred)


