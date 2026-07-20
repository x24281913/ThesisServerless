import botocore.exceptions


class Boto3Error(Exception):
    """Base class for all Boto3 errors."""
    



class ResourceLoadException(Boto3Error):
    pass



class NoVersionFound(Boto3Error):
    pass



class UnknownAPIVersionError(Boto3Error, botocore.exceptions.DataNotFoundError):
    
    def __init__(self, service_name, bad_api_version, available_api_versions):
        msg = f"The '{service_name}' resource does not support an API version of: {bad_api_version}\nValid API versions are: {available_api_versions}"
        Boto3Error.__init__(self, msg)



class ResourceNotExistsError(Boto3Error, botocore.exceptions.DataNotFoundError):
    """Raised when you attempt to create a resource that does not exist."""
    
    def __init__(self, service_name, available_services, has_low_level_client):
        msg = "The '{}' resource does not exist.\nThe available resources are:\n   - {}\n".format(service_name, '\n   - '.join(available_services))
        if has_low_level_client:
            msg = f"{msg}\nConsider using a boto3.client('{service_name}') instead of a resource for '{service_name}'"
        Boto3Error.__init__(self, msg)



class RetriesExceededError(Boto3Error):
    
    def __init__(self, last_exception, msg='Max Retries Exceeded'):
        super().__init__(msg)
        self.last_exception = last_exception



class S3TransferFailedError(Boto3Error):
    pass



class S3UploadFailedError(Boto3Error):
    pass



class DynamoDBOperationNotSupportedError(Boto3Error):
    """Raised for operations that are not supported for an operand."""
    
    def __init__(self, operation, value):
        msg = f'{operation} operation cannot be applied to value {value} of type {type(value)} directly. Must use AttributeBase object methods (i.e. Attr().eq()). to generate ConditionBase instances first.'
        Exception.__init__(self, msg)

DynanmoDBOperationNotSupportedError = DynamoDBOperationNotSupportedError


class DynamoDBNeedsConditionError(Boto3Error):
    """Raised when input is not a condition"""
    
    def __init__(self, value):
        msg = f'Expecting a ConditionBase object. Got {value} of type {type(value)}. Use AttributeBase object methods (i.e. Attr().eq()). to generate ConditionBase instances.'
        Exception.__init__(self, msg)



class DynamoDBNeedsKeyConditionError(Boto3Error):
    pass



class PythonDeprecationWarning(Warning):
    """
    Python version being used is scheduled to become unsupported
    in an future release. See warning for specifics.
    """
    pass



class InvalidCrtTransferConfigError(Boto3Error):
    pass


