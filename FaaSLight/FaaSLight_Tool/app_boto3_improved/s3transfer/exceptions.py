from concurrent.futures import CancelledError


class RetriesExceededError(Exception):
    
    def __init__(self, last_exception, msg='Max Retries Exceeded'):
        super().__init__(msg)
        self.last_exception = last_exception



class S3UploadFailedError(Exception):
    pass



class S3DownloadFailedError(Exception):
    pass



class S3CopyFailedError(Exception):
    pass



class InvalidSubscriberMethodError(Exception):
    pass



class TransferNotDoneError(Exception):
    pass



class FatalError(CancelledError):
    """A CancelledError raised from an error in the TransferManager"""
    pass



class S3ValidationError(Exception):
    pass


