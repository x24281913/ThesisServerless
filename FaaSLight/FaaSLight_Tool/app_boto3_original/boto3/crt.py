"""
This file contains private functionality for interacting with the AWS
Common Runtime library (awscrt) in boto3.

All code contained within this file is for internal usage within this
project and is not intended for external consumption. All interfaces
contained within are subject to abrupt breaking changes.
"""

import logging
import threading
import botocore.exceptions
from botocore.session import Session
from s3transfer.crt import BotocoreCRTCredentialsWrapper, BotocoreCRTRequestSerializer, CRTTransferManager, acquire_crt_s3_process_lock, create_s3_crt_client
from boto3.compat import TRANSFER_CONFIG_SUPPORTS_CRT
from boto3.exceptions import InvalidCrtTransferConfigError
from boto3.s3.constants import CRT_TRANSFER_CLIENT
logger = logging.getLogger(__name__)
CRT_S3_CLIENT = None
BOTOCORE_CRT_SERIALIZER = None
CLIENT_CREATION_LOCK = threading.Lock()
PROCESS_LOCK_NAME = 'boto3'
_ALLOWED_CRT_TRANSFER_CONFIG_OPTIONS = {'multipart_threshold', 'max_concurrency', 'max_request_concurrency', 'multipart_chunksize', 'preferred_transfer_client'}

def _create_crt_client(session, config, region_name, cred_provider):
    """Create a CRT S3 Client for file transfer.

    Instantiating many of these may lead to degraded performance or
    system resource exhaustion.
    """
    create_crt_client_kwargs = {'region': region_name, 'use_ssl': True, 'crt_credentials_provider': cred_provider}
    return create_s3_crt_client(**create_crt_client_kwargs)

def _create_crt_request_serializer(session, region_name):
    return BotocoreCRTRequestSerializer(session, {'region_name': region_name, 'endpoint_url': None})

def _create_crt_s3_client(session, config, region_name, credentials, lock, **kwargs):
    """Create boto3 wrapper class to manage crt lock reference and S3 client."""
    import custom_funtemplate
    return custom_funtemplate.rewrite_template('boto3.crt._create_crt_s3_client', '_create_crt_s3_client(session, config, region_name, credentials, lock, **kwargs)', {'BotocoreCRTCredentialsWrapper': BotocoreCRTCredentialsWrapper, 'CRTS3Client': CRTS3Client, '_create_crt_client': _create_crt_client, 'session': session, 'config': config, 'region_name': region_name, 'credentials': credentials, 'lock': lock, 'kwargs': kwargs}, 1)

def _initialize_crt_transfer_primatives(client, config):
    import custom_funtemplate
    return custom_funtemplate.rewrite_template('boto3.crt._initialize_crt_transfer_primatives', '_initialize_crt_transfer_primatives(client, config)', {'acquire_crt_s3_process_lock': acquire_crt_s3_process_lock, 'PROCESS_LOCK_NAME': PROCESS_LOCK_NAME, 'Session': Session, '_create_crt_request_serializer': _create_crt_request_serializer, '_create_crt_s3_client': _create_crt_s3_client, 'client': client, 'config': config}, 2)

def get_crt_s3_client(client, config):
    import custom_funtemplate
    return custom_funtemplate.rewrite_template('boto3.crt.get_crt_s3_client', 'get_crt_s3_client(client, config)', {'CLIENT_CREATION_LOCK': CLIENT_CREATION_LOCK, '_initialize_crt_transfer_primatives': _initialize_crt_transfer_primatives, 'client': client, 'config': config}, 1)


class CRTS3Client:
    """
    This wrapper keeps track of our underlying CRT client, the lock used to
    acquire it and the region we've used to instantiate the client.

    Due to limitations in the existing CRT interfaces, we can only make calls
    in a single region and does not support redirects. We track the region to
    ensure we don't use the CRT client when a successful request cannot be made.
    """
    
    def __init__(self, crt_client, process_lock, region, cred_provider):
        self.crt_client = crt_client
        self.process_lock = process_lock
        self.region = region
        self.cred_provider = cred_provider


def is_crt_compatible_request(client, crt_s3_client):
    """
    Boto3 client must use same signing region and credentials
    as the CRT_S3_CLIENT singleton. Otherwise fallback to classic.
    """
    import custom_funtemplate
    return custom_funtemplate.rewrite_template('boto3.crt.is_crt_compatible_request', 'is_crt_compatible_request(client, crt_s3_client)', {'compare_identity': compare_identity, 'client': client, 'crt_s3_client': crt_s3_client}, 1)

def compare_identity(boto3_creds, crt_s3_creds):
    import custom_funtemplate
    return custom_funtemplate.rewrite_template('boto3.crt.compare_identity', 'compare_identity(boto3_creds, crt_s3_creds)', {'botocore': botocore, 'boto3_creds': boto3_creds, 'crt_s3_creds': crt_s3_creds}, 1)

def _validate_crt_transfer_config(config):
    import custom_funtemplate
    return custom_funtemplate.rewrite_template('boto3.crt._validate_crt_transfer_config', '_validate_crt_transfer_config(config)', {'CRT_TRANSFER_CLIENT': CRT_TRANSFER_CLIENT, '_ALLOWED_CRT_TRANSFER_CONFIG_OPTIONS': _ALLOWED_CRT_TRANSFER_CONFIG_OPTIONS, 'InvalidCrtTransferConfigError': InvalidCrtTransferConfigError, 'config': config}, 1)

def create_crt_transfer_manager(client, config):
    """Create a CRTTransferManager for optimized data transfer."""
    import custom_funtemplate
    return custom_funtemplate.rewrite_template('boto3.crt.create_crt_transfer_manager', 'create_crt_transfer_manager(client, config)', {'get_crt_s3_client': get_crt_s3_client, 'is_crt_compatible_request': is_crt_compatible_request, 'BOTOCORE_CRT_SERIALIZER': BOTOCORE_CRT_SERIALIZER, 'TRANSFER_CONFIG_SUPPORTS_CRT': TRANSFER_CONFIG_SUPPORTS_CRT, '_validate_crt_transfer_config': _validate_crt_transfer_config, 'logger': logger, 'CRTTransferManager': CRTTransferManager, 'client': client, 'config': config}, 1)

