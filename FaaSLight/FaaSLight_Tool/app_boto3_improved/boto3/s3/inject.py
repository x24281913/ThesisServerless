import copy as python_copy
import logging
from functools import partial
from botocore.exceptions import ClientError
from boto3 import utils
from boto3.compat import is_append_mode
from boto3.s3.transfer import ProgressCallbackInvoker, S3Transfer, TransferConfig, create_transfer_manager
try:
    from botocore.context import with_current_context
except ImportError:
    from functools import wraps
    
    def with_current_context(hook=None):
        import custom_funtemplate
        return custom_funtemplate.rewrite_template('boto3.s3.inject.with_current_context', 'with_current_context(hook=None)', {'wraps': wraps, 'hook': hook}, 1)
try:
    from botocore.useragent import register_feature_id
except ImportError:
    
    def register_feature_id(feature_id):
        pass
logger = logging.getLogger(__name__)

def inject_s3_transfer_methods(class_attributes, **kwargs):
    import custom_funtemplate
    custom_funtemplate.rewrite_template('boto3.s3.inject.inject_s3_transfer_methods', 'inject_s3_transfer_methods(class_attributes, **kwargs)', {'utils': utils, 'upload_file': upload_file, 'download_file': download_file, 'copy': copy, 'upload_fileobj': upload_fileobj, 'download_fileobj': download_fileobj, 'class_attributes': class_attributes, 'kwargs': kwargs}, 0)

def inject_bucket_methods(class_attributes, **kwargs):
    import custom_funtemplate
    custom_funtemplate.rewrite_template('boto3.s3.inject.inject_bucket_methods', 'inject_bucket_methods(class_attributes, **kwargs)', {'utils': utils, 'bucket_load': bucket_load, 'bucket_upload_file': bucket_upload_file, 'bucket_download_file': bucket_download_file, 'bucket_copy': bucket_copy, 'bucket_upload_fileobj': bucket_upload_fileobj, 'bucket_download_fileobj': bucket_download_fileobj, 'class_attributes': class_attributes, 'kwargs': kwargs}, 0)

def inject_object_methods(class_attributes, **kwargs):
    import custom_funtemplate
    custom_funtemplate.rewrite_template('boto3.s3.inject.inject_object_methods', 'inject_object_methods(class_attributes, **kwargs)', {'utils': utils, 'object_upload_file': object_upload_file, 'object_download_file': object_download_file, 'object_copy': object_copy, 'object_upload_fileobj': object_upload_fileobj, 'object_download_fileobj': object_download_fileobj, 'class_attributes': class_attributes, 'kwargs': kwargs}, 0)

def inject_object_summary_methods(class_attributes, **kwargs):
    utils.inject_attribute(class_attributes, 'load', object_summary_load)

def bucket_load(self, *args, **kwargs):
    """
    Calls s3.Client.list_buckets() to update the attributes of the Bucket
    resource.
    """
    import custom_funtemplate
    custom_funtemplate.rewrite_template('boto3.s3.inject.bucket_load', 'bucket_load(self, *args, **kwargs)', {'ClientError': ClientError, 'self': self, 'args': args, 'kwargs': kwargs}, 0)

def object_summary_load(self, *args, **kwargs):
    """
    Calls s3.Client.head_object to update the attributes of the ObjectSummary
    resource.
    """
    import custom_funtemplate
    custom_funtemplate.rewrite_template('boto3.s3.inject.object_summary_load', 'object_summary_load(self, *args, **kwargs)', {'self': self, 'args': args, 'kwargs': kwargs}, 0)

@with_current_context(partial(register_feature_id, 'S3_TRANSFER'))
def upload_file(self, Filename, Bucket, Key, ExtraArgs=None, Callback=None, Config=None):
    """Upload a file to an S3 object.

    Usage::

        import boto3
        s3 = boto3.client('s3')
        s3.upload_file('/tmp/hello.txt', 'amzn-s3-demo-bucket', 'hello.txt')

    Similar behavior as S3Transfer's upload_file() method, except that
    argument names are capitalized. Detailed examples can be found at
    :ref:`S3Transfer's Usage <ref_s3transfer_usage>`.

    :type Filename: str
    :param Filename: The path to the file to upload.

    :type Bucket: str
    :param Bucket: The name of the bucket to upload to.

    :type Key: str
    :param Key: The name of the key to upload to.

    :type ExtraArgs: dict
    :param ExtraArgs: Extra arguments that may be passed to the
        client operation. For allowed upload arguments see
        :py:attr:`boto3.s3.transfer.S3Transfer.ALLOWED_UPLOAD_ARGS`.

    :type Callback: function
    :param Callback: A method which takes a number of bytes transferred to
        be periodically called during the upload.

    :type Config: boto3.s3.transfer.TransferConfig
    :param Config: The transfer configuration to be used when performing the
        transfer.
    """
    with S3Transfer(self, Config) as transfer:
        return transfer.upload_file(filename=Filename, bucket=Bucket, key=Key, extra_args=ExtraArgs, callback=Callback)

@with_current_context(partial(register_feature_id, 'S3_TRANSFER'))
def download_file(self, Bucket, Key, Filename, ExtraArgs=None, Callback=None, Config=None):
    """Download an S3 object to a file.

    Usage::

        import boto3
        s3 = boto3.client('s3')
        s3.download_file('amzn-s3-demo-bucket', 'hello.txt', '/tmp/hello.txt')

    Similar behavior as S3Transfer's download_file() method,
    except that parameters are capitalized. Detailed examples can be found at
    :ref:`S3Transfer's Usage <ref_s3transfer_usage>`.

    :type Bucket: str
    :param Bucket: The name of the bucket to download from.

    :type Key: str
    :param Key: The name of the key to download from.

    :type Filename: str
    :param Filename: The path to the file to download to.

    :type ExtraArgs: dict
    :param ExtraArgs: Extra arguments that may be passed to the
        client operation. For allowed download arguments see
        :py:attr:`boto3.s3.transfer.S3Transfer.ALLOWED_DOWNLOAD_ARGS`.

    :type Callback: function
    :param Callback: A method which takes a number of bytes transferred to
        be periodically called during the download.

    :type Config: boto3.s3.transfer.TransferConfig
    :param Config: The transfer configuration to be used when performing the
        transfer.
    """
    with S3Transfer(self, Config) as transfer:
        return transfer.download_file(bucket=Bucket, key=Key, filename=Filename, extra_args=ExtraArgs, callback=Callback)

def bucket_upload_file(self, Filename, Key, ExtraArgs=None, Callback=None, Config=None):
    """Upload a file to an S3 object.

    Usage::

        import boto3
        s3 = boto3.resource('s3')
        s3.Bucket('amzn-s3-demo-bucket').upload_file('/tmp/hello.txt', 'hello.txt')

    Similar behavior as S3Transfer's upload_file() method,
    except that parameters are capitalized. Detailed examples can be found at
    :ref:`S3Transfer's Usage <ref_s3transfer_usage>`.

    :type Filename: str
    :param Filename: The path to the file to upload.

    :type Key: str
    :param Key: The name of the key to upload to.

    :type ExtraArgs: dict
    :param ExtraArgs: Extra arguments that may be passed to the
        client operation. For allowed upload arguments see
        :py:attr:`boto3.s3.transfer.S3Transfer.ALLOWED_UPLOAD_ARGS`.

    :type Callback: function
    :param Callback: A method which takes a number of bytes transferred to
        be periodically called during the upload.

    :type Config: boto3.s3.transfer.TransferConfig
    :param Config: The transfer configuration to be used when performing the
        transfer.
    """
    return self.meta.client.upload_file(Filename=Filename, Bucket=self.name, Key=Key, ExtraArgs=ExtraArgs, Callback=Callback, Config=Config)

def bucket_download_file(self, Key, Filename, ExtraArgs=None, Callback=None, Config=None):
    """Download an S3 object to a file.

    Usage::

        import boto3
        s3 = boto3.resource('s3')
        s3.Bucket('amzn-s3-demo-bucket').download_file('hello.txt', '/tmp/hello.txt')

    Similar behavior as S3Transfer's download_file() method,
    except that parameters are capitalized. Detailed examples can be found at
    :ref:`S3Transfer's Usage <ref_s3transfer_usage>`.

    :type Key: str
    :param Key: The name of the key to download from.

    :type Filename: str
    :param Filename: The path to the file to download to.

    :type ExtraArgs: dict
    :param ExtraArgs: Extra arguments that may be passed to the
        client operation. For allowed download arguments see
        :py:attr:`boto3.s3.transfer.S3Transfer.ALLOWED_DOWNLOAD_ARGS`.

    :type Callback: function
    :param Callback: A method which takes a number of bytes transferred to
        be periodically called during the download.

    :type Config: boto3.s3.transfer.TransferConfig
    :param Config: The transfer configuration to be used when performing the
        transfer.
    """
    return self.meta.client.download_file(Bucket=self.name, Key=Key, Filename=Filename, ExtraArgs=ExtraArgs, Callback=Callback, Config=Config)

def object_upload_file(self, Filename, ExtraArgs=None, Callback=None, Config=None):
    """Upload a file to an S3 object.

    Usage::

        import boto3
        s3 = boto3.resource('s3')
        s3.Object('amzn-s3-demo-bucket', 'hello.txt').upload_file('/tmp/hello.txt')

    Similar behavior as S3Transfer's upload_file() method,
    except that parameters are capitalized. Detailed examples can be found at
    :ref:`S3Transfer's Usage <ref_s3transfer_usage>`.

    :type Filename: str
    :param Filename: The path to the file to upload.

    :type ExtraArgs: dict
    :param ExtraArgs: Extra arguments that may be passed to the
        client operation. For allowed upload arguments see
        :py:attr:`boto3.s3.transfer.S3Transfer.ALLOWED_UPLOAD_ARGS`.

    :type Callback: function
    :param Callback: A method which takes a number of bytes transferred to
        be periodically called during the upload.

    :type Config: boto3.s3.transfer.TransferConfig
    :param Config: The transfer configuration to be used when performing the
        transfer.
    """
    return self.meta.client.upload_file(Filename=Filename, Bucket=self.bucket_name, Key=self.key, ExtraArgs=ExtraArgs, Callback=Callback, Config=Config)

def object_download_file(self, Filename, ExtraArgs=None, Callback=None, Config=None):
    """Download an S3 object to a file.

    Usage::

        import boto3
        s3 = boto3.resource('s3')
        s3.Object('amzn-s3-demo-bucket', 'hello.txt').download_file('/tmp/hello.txt')

    Similar behavior as S3Transfer's download_file() method,
    except that parameters are capitalized. Detailed examples can be found at
    :ref:`S3Transfer's Usage <ref_s3transfer_usage>`.

    :type Filename: str
    :param Filename: The path to the file to download to.

    :type ExtraArgs: dict
    :param ExtraArgs: Extra arguments that may be passed to the
        client operation. For allowed download arguments see
        :py:attr:`boto3.s3.transfer.S3Transfer.ALLOWED_DOWNLOAD_ARGS`.

    :type Callback: function
    :param Callback: A method which takes a number of bytes transferred to
        be periodically called during the download.

    :type Config: boto3.s3.transfer.TransferConfig
    :param Config: The transfer configuration to be used when performing the
        transfer.
    """
    return self.meta.client.download_file(Bucket=self.bucket_name, Key=self.key, Filename=Filename, ExtraArgs=ExtraArgs, Callback=Callback, Config=Config)

@with_current_context(partial(register_feature_id, 'S3_TRANSFER'))
def copy(self, CopySource, Bucket, Key, ExtraArgs=None, Callback=None, SourceClient=None, Config=None):
    """Copy an object from one S3 location to another.

    This is a managed transfer which will perform a multipart copy in
    multiple threads if necessary.

    Usage::

        import boto3
        s3 = boto3.resource('s3')
        copy_source = {
            'Bucket': 'amzn-s3-demo-bucket1',
            'Key': 'mykey'
        }
        s3.meta.client.copy(copy_source, 'amzn-s3-demo-bucket2', 'otherkey')

    :type CopySource: dict
    :param CopySource: The name of the source bucket, key name of the
        source object, and optional version ID of the source object. The
        dictionary format is:
        ``{'Bucket': 'bucket', 'Key': 'key', 'VersionId': 'id'}``. Note
        that the ``VersionId`` key is optional and may be omitted.

    :type Bucket: str
    :param Bucket: The name of the bucket to copy to

    :type Key: str
    :param Key: The name of the key to copy to

    :type ExtraArgs: dict
    :param ExtraArgs: Extra arguments that may be passed to the
        client operation. For allowed copy arguments see
        :py:attr:`boto3.s3.transfer.S3Transfer.ALLOWED_COPY_ARGS`.

    :type Callback: function
    :param Callback: A method which takes a number of bytes transferred to
        be periodically called during the copy.

    :type SourceClient: botocore or boto3 Client
    :param SourceClient: The client to be used for operations that
        may happen at the source object. For example, this client is
        used for the head_object that determines the size of the copy.
        If no client is provided, the current client is used as the
        client for the source object.  The current client still
        requires IAM permissions to access both buckets.

    :type Config: boto3.s3.transfer.TransferConfig
    :param Config: The transfer configuration to be used when performing the
        copy.
    """
    import custom_funtemplate
    return custom_funtemplate.rewrite_template('boto3.s3.inject.copy', 'copy(self, CopySource, Bucket, Key, ExtraArgs=None, Callback=None, SourceClient=None, Config=None)', {'ProgressCallbackInvoker': ProgressCallbackInvoker, 'TransferConfig': TransferConfig, 'python_copy': python_copy, 'create_transfer_manager': create_transfer_manager, 'with_current_context': with_current_context, 'partial': partial, 'register_feature_id': register_feature_id, 'self': self, 'CopySource': CopySource, 'Bucket': Bucket, 'Key': Key, 'ExtraArgs': ExtraArgs, 'Callback': Callback, 'SourceClient': SourceClient, 'Config': Config}, 1)

def bucket_copy(self, CopySource, Key, ExtraArgs=None, Callback=None, SourceClient=None, Config=None):
    """Copy an object from one S3 location to an object in this bucket.

    This is a managed transfer which will perform a multipart copy in
    multiple threads if necessary.

    Usage::

        import boto3
        s3 = boto3.resource('s3')
        copy_source = {
            'Bucket': 'amzn-s3-demo-bucket1',
            'Key': 'mykey'
        }
        bucket = s3.Bucket('amzn-s3-demo-bucket2')
        bucket.copy(copy_source, 'otherkey')

    :type CopySource: dict
    :param CopySource: The name of the source bucket, key name of the
        source object, and optional version ID of the source object. The
        dictionary format is:
        ``{'Bucket': 'bucket', 'Key': 'key', 'VersionId': 'id'}``. Note
        that the ``VersionId`` key is optional and may be omitted.

    :type Key: str
    :param Key: The name of the key to copy to

    :type ExtraArgs: dict
    :param ExtraArgs: Extra arguments that may be passed to the
        client operation. For allowed copy arguments see
        :py:attr:`boto3.s3.transfer.S3Transfer.ALLOWED_COPY_ARGS`.

    :type Callback: function
    :param Callback: A method which takes a number of bytes transferred to
        be periodically called during the copy.

    :type SourceClient: botocore or boto3 Client
    :param SourceClient: The client to be used for operations that
        may happen at the source object. For example, this client is
        used for the head_object that determines the size of the copy.
        If no client is provided, the current client is used as the
        client for the source object.  The current client still
        requires IAM permissions to access both buckets.

    :type Config: boto3.s3.transfer.TransferConfig
    :param Config: The transfer configuration to be used when performing the
        copy.
    """
    return self.meta.client.copy(CopySource=CopySource, Bucket=self.name, Key=Key, ExtraArgs=ExtraArgs, Callback=Callback, SourceClient=SourceClient, Config=Config)

def object_copy(self, CopySource, ExtraArgs=None, Callback=None, SourceClient=None, Config=None):
    """Copy an object from one S3 location to this object.

    This is a managed transfer which will perform a multipart copy in
    multiple threads if necessary.

    Usage::

        import boto3
        s3 = boto3.resource('s3')
        copy_source = {
            'Bucket': 'amzn-s3-demo-bucket1',
            'Key': 'mykey'
        }
        bucket = s3.Bucket('amzn-s3-demo-bucket2')
        obj = bucket.Object('otherkey')
        obj.copy(copy_source)

    :type CopySource: dict
    :param CopySource: The name of the source bucket, key name of the
        source object, and optional version ID of the source object. The
        dictionary format is:
        ``{'Bucket': 'bucket', 'Key': 'key', 'VersionId': 'id'}``. Note
        that the ``VersionId`` key is optional and may be omitted.

    :type ExtraArgs: dict
    :param ExtraArgs: Extra arguments that may be passed to the
        client operation. For allowed copy arguments see
        :py:attr:`boto3.s3.transfer.S3Transfer.ALLOWED_COPY_ARGS`.

    :type Callback: function
    :param Callback: A method which takes a number of bytes transferred to
        be periodically called during the copy.

    :type SourceClient: botocore or boto3 Client
    :param SourceClient: The client to be used for operations that
        may happen at the source object. For example, this client is
        used for the head_object that determines the size of the copy.
        If no client is provided, the current client is used as the
        client for the source object.  The current client still
        requires IAM permissions to access both buckets.

    :type Config: boto3.s3.transfer.TransferConfig
    :param Config: The transfer configuration to be used when performing the
        copy.
    """
    return self.meta.client.copy(CopySource=CopySource, Bucket=self.bucket_name, Key=self.key, ExtraArgs=ExtraArgs, Callback=Callback, SourceClient=SourceClient, Config=Config)

@with_current_context(partial(register_feature_id, 'S3_TRANSFER'))
def upload_fileobj(self, Fileobj, Bucket, Key, ExtraArgs=None, Callback=None, Config=None):
    """Upload a file-like object to S3.

    The file-like object must be in binary mode.

    This is a managed transfer which will perform a multipart upload in
    multiple threads if necessary.

    Usage::

        import boto3
        s3 = boto3.client('s3')

        with open('filename', 'rb') as data:
            s3.upload_fileobj(data, 'amzn-s3-demo-bucket', 'mykey')

    :type Fileobj: a file-like object
    :param Fileobj: A file-like object to upload. At a minimum, it must
        implement the `read` method, and must return bytes.

    :type Bucket: str
    :param Bucket: The name of the bucket to upload to.

    :type Key: str
    :param Key: The name of the key to upload to.

    :type ExtraArgs: dict
    :param ExtraArgs: Extra arguments that may be passed to the
        client operation. For allowed upload arguments see
        :py:attr:`boto3.s3.transfer.S3Transfer.ALLOWED_UPLOAD_ARGS`.

    :type Callback: function
    :param Callback: A method which takes a number of bytes transferred to
        be periodically called during the upload.

    :type Config: boto3.s3.transfer.TransferConfig
    :param Config: The transfer configuration to be used when performing the
        upload.
    """
    import custom_funtemplate
    return custom_funtemplate.rewrite_template('boto3.s3.inject.upload_fileobj', 'upload_fileobj(self, Fileobj, Bucket, Key, ExtraArgs=None, Callback=None, Config=None)', {'ProgressCallbackInvoker': ProgressCallbackInvoker, 'TransferConfig': TransferConfig, 'create_transfer_manager': create_transfer_manager, 'with_current_context': with_current_context, 'partial': partial, 'register_feature_id': register_feature_id, 'self': self, 'Fileobj': Fileobj, 'Bucket': Bucket, 'Key': Key, 'ExtraArgs': ExtraArgs, 'Callback': Callback, 'Config': Config}, 1)

def bucket_upload_fileobj(self, Fileobj, Key, ExtraArgs=None, Callback=None, Config=None):
    """Upload a file-like object to this bucket.

    The file-like object must be in binary mode.

    This is a managed transfer which will perform a multipart upload in
    multiple threads if necessary.

    Usage::

        import boto3
        s3 = boto3.resource('s3')
        bucket = s3.Bucket('amzn-s3-demo-bucket')

        with open('filename', 'rb') as data:
            bucket.upload_fileobj(data, 'mykey')

    :type Fileobj: a file-like object
    :param Fileobj: A file-like object to upload. At a minimum, it must
        implement the `read` method, and must return bytes.

    :type Key: str
    :param Key: The name of the key to upload to.

    :type ExtraArgs: dict
    :param ExtraArgs: Extra arguments that may be passed to the
        client operation. For allowed upload arguments see
        :py:attr:`boto3.s3.transfer.S3Transfer.ALLOWED_UPLOAD_ARGS`.

    :type Callback: function
    :param Callback: A method which takes a number of bytes transferred to
        be periodically called during the upload.

    :type Config: boto3.s3.transfer.TransferConfig
    :param Config: The transfer configuration to be used when performing the
        upload.
    """
    return self.meta.client.upload_fileobj(Fileobj=Fileobj, Bucket=self.name, Key=Key, ExtraArgs=ExtraArgs, Callback=Callback, Config=Config)

def object_upload_fileobj(self, Fileobj, ExtraArgs=None, Callback=None, Config=None):
    """Upload a file-like object to this object.

    The file-like object must be in binary mode.

    This is a managed transfer which will perform a multipart upload in
    multiple threads if necessary.

    Usage::

        import boto3
        s3 = boto3.resource('s3')
        bucket = s3.Bucket('amzn-s3-demo-bucket')
        obj = bucket.Object('mykey')

        with open('filename', 'rb') as data:
            obj.upload_fileobj(data)

    :type Fileobj: a file-like object
    :param Fileobj: A file-like object to upload. At a minimum, it must
        implement the `read` method, and must return bytes.

    :type ExtraArgs: dict
    :param ExtraArgs: Extra arguments that may be passed to the
        client operation. For allowed upload arguments see
        :py:attr:`boto3.s3.transfer.S3Transfer.ALLOWED_UPLOAD_ARGS`.

    :type Callback: function
    :param Callback: A method which takes a number of bytes transferred to
        be periodically called during the upload.

    :type Config: boto3.s3.transfer.TransferConfig
    :param Config: The transfer configuration to be used when performing the
        upload.
    """
    return self.meta.client.upload_fileobj(Fileobj=Fileobj, Bucket=self.bucket_name, Key=self.key, ExtraArgs=ExtraArgs, Callback=Callback, Config=Config)

def disable_threading_if_append_mode(config, fileobj):
    """Set `TransferConfig.use_threads` to `False` if file-like
        object is in append mode.

    :type config: boto3.s3.transfer.TransferConfig
    :param config: The transfer configuration to be used when performing the
        download.

    :type fileobj: A file-like object
    :param fileobj: A file-like object to inspect for append mode.
    """
    import custom_funtemplate
    custom_funtemplate.rewrite_template('boto3.s3.inject.disable_threading_if_append_mode', 'disable_threading_if_append_mode(config, fileobj)', {'is_append_mode': is_append_mode, 'logger': logger, 'config': config, 'fileobj': fileobj}, 0)

@with_current_context(partial(register_feature_id, 'S3_TRANSFER'))
def download_fileobj(self, Bucket, Key, Fileobj, ExtraArgs=None, Callback=None, Config=None):
    """Download an object from S3 to a file-like object.

    The file-like object must be in binary mode.

    This is a managed transfer which will perform a multipart download in
    multiple threads if necessary.

    Usage::

        import boto3
        s3 = boto3.client('s3')

        with open('filename', 'wb') as data:
            s3.download_fileobj('amzn-s3-demo-bucket', 'mykey', data)

    :type Bucket: str
    :param Bucket: The name of the bucket to download from.

    :type Key: str
    :param Key: The name of the key to download from.

    :type Fileobj: a file-like object
    :param Fileobj: A file-like object to download into. At a minimum, it must
        implement the `write` method and must accept bytes.

    :type ExtraArgs: dict
    :param ExtraArgs: Extra arguments that may be passed to the
        client operation. For allowed download arguments see
        :py:attr:`boto3.s3.transfer.S3Transfer.ALLOWED_DOWNLOAD_ARGS`.

    :type Callback: function
    :param Callback: A method which takes a number of bytes transferred to
        be periodically called during the download.

    :type Config: boto3.s3.transfer.TransferConfig
    :param Config: The transfer configuration to be used when performing the
        download.
    """
    import custom_funtemplate
    return custom_funtemplate.rewrite_template('boto3.s3.inject.download_fileobj', 'download_fileobj(self, Bucket, Key, Fileobj, ExtraArgs=None, Callback=None, Config=None)', {'ProgressCallbackInvoker': ProgressCallbackInvoker, 'TransferConfig': TransferConfig, 'python_copy': python_copy, 'disable_threading_if_append_mode': disable_threading_if_append_mode, 'create_transfer_manager': create_transfer_manager, 'with_current_context': with_current_context, 'partial': partial, 'register_feature_id': register_feature_id, 'self': self, 'Bucket': Bucket, 'Key': Key, 'Fileobj': Fileobj, 'ExtraArgs': ExtraArgs, 'Callback': Callback, 'Config': Config}, 1)

def bucket_download_fileobj(self, Key, Fileobj, ExtraArgs=None, Callback=None, Config=None):
    """Download an object from this bucket to a file-like-object.

    The file-like object must be in binary mode.

    This is a managed transfer which will perform a multipart download in
    multiple threads if necessary.

    Usage::

        import boto3
        s3 = boto3.resource('s3')
        bucket = s3.Bucket('amzn-s3-demo-bucket')

        with open('filename', 'wb') as data:
            bucket.download_fileobj('mykey', data)

    :type Fileobj: a file-like object
    :param Fileobj: A file-like object to download into. At a minimum, it must
        implement the `write` method and must accept bytes.

    :type Key: str
    :param Key: The name of the key to download from.

    :type ExtraArgs: dict
    :param ExtraArgs: Extra arguments that may be passed to the
        client operation. For allowed download arguments see
        :py:attr:`boto3.s3.transfer.S3Transfer.ALLOWED_DOWNLOAD_ARGS`.

    :type Callback: function
    :param Callback: A method which takes a number of bytes transferred to
        be periodically called during the download.

    :type Config: boto3.s3.transfer.TransferConfig
    :param Config: The transfer configuration to be used when performing the
        download.
    """
    return self.meta.client.download_fileobj(Bucket=self.name, Key=Key, Fileobj=Fileobj, ExtraArgs=ExtraArgs, Callback=Callback, Config=Config)

def object_download_fileobj(self, Fileobj, ExtraArgs=None, Callback=None, Config=None):
    """Download this object from S3 to a file-like object.

    The file-like object must be in binary mode.

    This is a managed transfer which will perform a multipart download in
    multiple threads if necessary.

    Usage::

        import boto3
        s3 = boto3.resource('s3')
        bucket = s3.Bucket('amzn-s3-demo-bucket')
        obj = bucket.Object('mykey')

        with open('filename', 'wb') as data:
            obj.download_fileobj(data)

    :type Fileobj: a file-like object
    :param Fileobj: A file-like object to download into. At a minimum, it must
        implement the `write` method and must accept bytes.

    :type ExtraArgs: dict
    :param ExtraArgs: Extra arguments that may be passed to the
        client operation. For allowed download arguments see
        :py:attr:`boto3.s3.transfer.S3Transfer.ALLOWED_DOWNLOAD_ARGS`.

    :type Callback: function
    :param Callback: A method which takes a number of bytes transferred to
        be periodically called during the download.

    :type Config: boto3.s3.transfer.TransferConfig
    :param Config: The transfer configuration to be used when performing the
        download.
    """
    return self.meta.client.download_fileobj(Bucket=self.bucket_name, Key=self.key, Fileobj=Fileobj, ExtraArgs=ExtraArgs, Callback=Callback, Config=Config)

