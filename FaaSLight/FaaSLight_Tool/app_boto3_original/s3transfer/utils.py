import functools
import logging
import math
import os
import random
import socket
import stat
import string
import threading
from collections import defaultdict
from botocore.exceptions import IncompleteReadError, ReadTimeoutError, ResponseStreamingError
from botocore.httpchecksum import DEFAULT_CHECKSUM_ALGORITHM, AwsChunkedWrapper
from botocore.utils import is_s3express_bucket
from s3transfer.compat import SOCKET_ERROR, fallocate, rename_file
from s3transfer.constants import FULL_OBJECT_CHECKSUM_ARGS
MAX_PARTS = 10000
MAX_SINGLE_UPLOAD_SIZE = 5 * 1024**3
MIN_UPLOAD_CHUNKSIZE = 5 * 1024**2
logger = logging.getLogger(__name__)
S3_RETRYABLE_DOWNLOAD_ERRORS = (socket.timeout, SOCKET_ERROR, ReadTimeoutError, IncompleteReadError, ResponseStreamingError)

def random_file_extension(num_digits=8):
    return ''.join((random.choice(string.hexdigits) for _ in range(num_digits)))

def signal_not_transferring(request, operation_name, **kwargs):
    if (operation_name in ['PutObject', 'UploadPart'] and hasattr(request.body, 'signal_not_transferring')):
        request.body.signal_not_transferring()

def signal_transferring(request, operation_name, **kwargs):
    import custom_funtemplate
    custom_funtemplate.rewrite_template('s3transfer.utils.signal_transferring', 'signal_transferring(request, operation_name, **kwargs)', {'AwsChunkedWrapper': AwsChunkedWrapper, 'request': request, 'operation_name': operation_name, 'kwargs': kwargs}, 0)

def calculate_num_parts(size, part_size):
    return int(math.ceil(size / float(part_size)))

def calculate_range_parameter(part_size, part_index, num_parts, total_size=None):
    """Calculate the range parameter for multipart downloads/copies

    :type part_size: int
    :param part_size: The size of the part

    :type part_index: int
    :param part_index: The index for which this parts starts. This index starts
        at zero

    :type num_parts: int
    :param num_parts: The total number of parts in the transfer

    :returns: The value to use for Range parameter on downloads or
        the CopySourceRange parameter for copies
    """
    import custom_funtemplate
    return custom_funtemplate.rewrite_template('s3transfer.utils.calculate_range_parameter', 'calculate_range_parameter(part_size, part_index, num_parts, total_size=None)', {'part_size': part_size, 'part_index': part_index, 'num_parts': num_parts, 'total_size': total_size}, 1)

def get_callbacks(transfer_future, callback_type):
    """Retrieves callbacks from a subscriber

    :type transfer_future: s3transfer.futures.TransferFuture
    :param transfer_future: The transfer future the subscriber is associated
        to.

    :type callback_type: str
    :param callback_type: The type of callback to retrieve from the subscriber.
        Valid types include:
            * 'queued'
            * 'progress'
            * 'done'

    :returns: A list of callbacks for the type specified. All callbacks are
        preinjected with the transfer future.
    """
    import custom_funtemplate
    return custom_funtemplate.rewrite_template('s3transfer.utils.get_callbacks', 'get_callbacks(transfer_future, callback_type)', {'functools': functools, 'transfer_future': transfer_future, 'callback_type': callback_type}, 1)

def invoke_progress_callbacks(callbacks, bytes_transferred):
    """Calls all progress callbacks

    :param callbacks: A list of progress callbacks to invoke
    :param bytes_transferred: The number of bytes transferred. This is passed
        to the callbacks. If no bytes were transferred the callbacks will not
        be invoked because no progress was achieved. It is also possible
        to receive a negative amount which comes from retrying a transfer
        request.
    """
    import custom_funtemplate
    custom_funtemplate.rewrite_template('s3transfer.utils.invoke_progress_callbacks', 'invoke_progress_callbacks(callbacks, bytes_transferred)', {'callbacks': callbacks, 'bytes_transferred': bytes_transferred}, 0)

def get_filtered_dict(original_dict, whitelisted_keys=None, blocklisted_keys=None):
    """Gets a dictionary filtered by whitelisted and blocklisted keys.

    :param original_dict: The original dictionary of arguments to source keys
        and values.
    :param whitelisted_key: A list of keys to include in the filtered
        dictionary.
    :param blocklisted_key: A list of keys to exclude in the filtered
        dictionary.

    :returns: A dictionary containing key/values from the original dictionary
        whose key was included in the whitelist and/or not included in the
        blocklist.
    """
    import custom_funtemplate
    return custom_funtemplate.rewrite_template('s3transfer.utils.get_filtered_dict', 'get_filtered_dict(original_dict, whitelisted_keys=None, blocklisted_keys=None)', {'original_dict': original_dict, 'whitelisted_keys': whitelisted_keys, 'blocklisted_keys': blocklisted_keys}, 1)


class CallArgs:
    
    def __init__(self, **kwargs):
        """A class that records call arguments

        The call arguments must be passed as keyword arguments. It will set
        each keyword argument as an attribute of the object along with its
        associated value.
        """
        for (arg, value) in kwargs.items():
            setattr(self, arg, value)



class FunctionContainer:
    """An object that contains a function and any args or kwargs to call it

    When called the provided function will be called with provided args
    and kwargs.
    """
    
    def __init__(self, func, *args, **kwargs):
        self._func = func
        self._args = args
        self._kwargs = kwargs
    
    def __repr__(self):
        return f'Function: {self._func} with args {self._args} and kwargs {self._kwargs}'
    
    def __call__(self):
        return self._func(*self._args, **self._kwargs)



class CountCallbackInvoker:
    """An abstraction to invoke a callback when a shared count reaches zero

    :param callback: Callback invoke when finalized count reaches zero
    """
    
    def __init__(self, callback):
        self._lock = threading.Lock()
        self._callback = callback
        self._count = 0
        self._is_finalized = False
    
    @property
    def current_count(self):
        with self._lock:
            return self._count
    
    def increment(self):
        """Increment the count by one"""
        with self._lock:
            if self._is_finalized:
                raise RuntimeError('Counter has been finalized it can no longer be incremented.')
            self._count += 1
    
    def decrement(self):
        """Decrement the count by one"""
        with self._lock:
            if self._count == 0:
                raise RuntimeError('Counter is at zero. It cannot dip below zero')
            self._count -= 1
            if (self._is_finalized and self._count == 0):
                self._callback()
    
    def finalize(self):
        """Finalize the counter

        Once finalized, the counter never be incremented and the callback
        can be invoked once the count reaches zero
        """
        with self._lock:
            self._is_finalized = True
            if self._count == 0:
                self._callback()



class OSUtils:
    _MAX_FILENAME_LEN = 255
    
    def get_file_size(self, filename):
        return os.path.getsize(filename)
    
    def open_file_chunk_reader(self, filename, start_byte, size, callbacks):
        return ReadFileChunk.from_filename(filename, start_byte, size, callbacks, enable_callbacks=False)
    
    def open_file_chunk_reader_from_fileobj(self, fileobj, chunk_size, full_file_size, callbacks, close_callbacks=None):
        return ReadFileChunk(fileobj, chunk_size, full_file_size, callbacks=callbacks, enable_callbacks=False, close_callbacks=close_callbacks)
    
    def open(self, filename, mode):
        return open(filename, mode)
    
    def remove_file(self, filename):
        """Remove a file, noop if file does not exist."""
        try:
            os.remove(filename)
        except OSError:
            pass
    
    def rename_file(self, current_filename, new_filename):
        rename_file(current_filename, new_filename)
    
    def is_special_file(cls, filename):
        """Checks to see if a file is a special UNIX file.

        It checks if the file is a character special device, block special
        device, FIFO, or socket.

        :param filename: Name of the file

        :returns: True if the file is a special file. False, if is not.
        """
        if not os.path.exists(filename):
            return False
        mode = os.stat(filename).st_mode
        if stat.S_ISCHR(mode):
            return True
        if stat.S_ISBLK(mode):
            return True
        if stat.S_ISFIFO(mode):
            return True
        if stat.S_ISSOCK(mode):
            return True
        return False
    
    def get_temp_filename(self, filename):
        suffix = os.extsep + random_file_extension()
        path = os.path.dirname(filename)
        name = os.path.basename(filename)
        temp_filename = name[:self._MAX_FILENAME_LEN - len(suffix)] + suffix
        return os.path.join(path, temp_filename)
    
    def allocate(self, filename, size):
        try:
            with self.open(filename, 'wb') as f:
                fallocate(f, size)
        except OSError:
            self.remove_file(filename)
            raise



class DeferredOpenFile:
    
    def __init__(self, filename, start_byte=0, mode='rb', open_function=open):
        """A class that defers the opening of a file till needed

        This is useful for deferring opening of a file till it is needed
        in a separate thread, as there is a limit of how many open files
        there can be in a single thread for most operating systems. The
        file gets opened in the following methods: ``read()``, ``seek()``,
        and ``__enter__()``

        :type filename: str
        :param filename: The name of the file to open

        :type start_byte: int
        :param start_byte: The byte to seek to when the file is opened.

        :type mode: str
        :param mode: The mode to use to open the file

        :type open_function: function
        :param open_function: The function to use to open the file
        """
        self._filename = filename
        self._fileobj = None
        self._start_byte = start_byte
        self._mode = mode
        self._open_function = open_function
    
    def _open_if_needed(self):
        if self._fileobj is None:
            self._fileobj = self._open_function(self._filename, self._mode)
            if self._start_byte != 0:
                self._fileobj.seek(self._start_byte)
    
    @property
    def name(self):
        return self._filename
    
    def read(self, amount=None):
        self._open_if_needed()
        return self._fileobj.read(amount)
    
    def write(self, data):
        self._open_if_needed()
        self._fileobj.write(data)
    
    def seek(self, where, whence=0):
        self._open_if_needed()
        self._fileobj.seek(where, whence)
    
    def tell(self):
        if self._fileobj is None:
            return self._start_byte
        return self._fileobj.tell()
    
    def close(self):
        if self._fileobj:
            self._fileobj.close()
    
    def __enter__(self):
        self._open_if_needed()
        return self
    
    def __exit__(self, *args, **kwargs):
        self.close()



class ReadFileChunk:
    
    def __init__(self, fileobj, chunk_size, full_file_size, callbacks=None, enable_callbacks=True, close_callbacks=None):
        """

        Given a file object shown below::

            |___________________________________________________|
            0          |                 |                 full_file_size
                       |----chunk_size---|
                    f.tell()

        :type fileobj: file
        :param fileobj: File like object

        :type chunk_size: int
        :param chunk_size: The max chunk size to read.  Trying to read
            pass the end of the chunk size will behave like you've
            reached the end of the file.

        :type full_file_size: int
        :param full_file_size: The entire content length associated
            with ``fileobj``.

        :type callbacks: A list of function(amount_read)
        :param callbacks: Called whenever data is read from this object in the
            order provided.

        :type enable_callbacks: boolean
        :param enable_callbacks: True if to run callbacks. Otherwise, do not
            run callbacks

        :type close_callbacks: A list of function()
        :param close_callbacks: Called when close is called. The function
            should take no arguments.
        """
        self._fileobj = fileobj
        self._start_byte = self._fileobj.tell()
        self._size = self._calculate_file_size(self._fileobj, requested_size=chunk_size, start_byte=self._start_byte, actual_file_size=full_file_size)
        self._amount_read = 0
        self._callbacks = callbacks
        if callbacks is None:
            self._callbacks = []
        self._callbacks_enabled = enable_callbacks
        self._close_callbacks = close_callbacks
        if close_callbacks is None:
            self._close_callbacks = close_callbacks
    
    @classmethod
    def from_filename(cls, filename, start_byte, chunk_size, callbacks=None, enable_callbacks=True):
        """Convenience factory function to create from a filename.

        :type start_byte: int
        :param start_byte: The first byte from which to start reading.

        :type chunk_size: int
        :param chunk_size: The max chunk size to read.  Trying to read
            pass the end of the chunk size will behave like you've
            reached the end of the file.

        :type full_file_size: int
        :param full_file_size: The entire content length associated
            with ``fileobj``.

        :type callbacks: function(amount_read)
        :param callbacks: Called whenever data is read from this object.

        :type enable_callbacks: bool
        :param enable_callbacks: Indicate whether to invoke callback
            during read() calls.

        :rtype: ``ReadFileChunk``
        :return: A new instance of ``ReadFileChunk``

        """
        f = open(filename, 'rb')
        f.seek(start_byte)
        file_size = os.fstat(f.fileno()).st_size
        return cls(f, chunk_size, file_size, callbacks, enable_callbacks)
    
    def _calculate_file_size(self, fileobj, requested_size, start_byte, actual_file_size):
        max_chunk_size = actual_file_size - start_byte
        return min(max_chunk_size, requested_size)
    
    def read(self, amount=None):
        amount_left = max(self._size - self._amount_read, 0)
        if amount is None:
            amount_to_read = amount_left
        else:
            amount_to_read = min(amount_left, amount)
        data = self._fileobj.read(amount_to_read)
        self._amount_read += len(data)
        if (self._callbacks is not None and self._callbacks_enabled):
            invoke_progress_callbacks(self._callbacks, len(data))
        return data
    
    def signal_transferring(self):
        self.enable_callback()
        if hasattr(self._fileobj, 'signal_transferring'):
            self._fileobj.signal_transferring()
    
    def signal_not_transferring(self):
        self.disable_callback()
        if hasattr(self._fileobj, 'signal_not_transferring'):
            self._fileobj.signal_not_transferring()
    
    def enable_callback(self):
        self._callbacks_enabled = True
    
    def disable_callback(self):
        self._callbacks_enabled = False
    
    def seek(self, where, whence=0):
        if whence not in (0, 1, 2):
            raise ValueError(f'invalid whence ({whence}, should be 0, 1 or 2)')
        where += self._start_byte
        if whence == 1:
            where += self._amount_read
        elif whence == 2:
            where += self._size
        self._fileobj.seek(max(where, self._start_byte))
        if (self._callbacks is not None and self._callbacks_enabled):
            bounded_where = max(min(where - self._start_byte, self._size), 0)
            bounded_amount_read = min(self._amount_read, self._size)
            amount = bounded_where - bounded_amount_read
            invoke_progress_callbacks(self._callbacks, bytes_transferred=amount)
        self._amount_read = max(where - self._start_byte, 0)
    
    def close(self):
        if (self._close_callbacks is not None and self._callbacks_enabled):
            for callback in self._close_callbacks:
                callback()
        self._fileobj.close()
    
    def tell(self):
        return self._amount_read
    
    def __len__(self):
        return self._size
    
    def __enter__(self):
        return self
    
    def __exit__(self, *args, **kwargs):
        self.close()
    
    def __iter__(self):
        return iter([])



class StreamReaderProgress:
    """Wrapper for a read only stream that adds progress callbacks."""
    
    def __init__(self, stream, callbacks=None):
        self._stream = stream
        self._callbacks = callbacks
        if callbacks is None:
            self._callbacks = []
    
    def read(self, *args, **kwargs):
        value = self._stream.read(*args, **kwargs)
        invoke_progress_callbacks(self._callbacks, len(value))
        return value



class NoResourcesAvailable(Exception):
    pass



class TaskSemaphore:
    
    def __init__(self, count):
        """A semaphore for the purpose of limiting the number of tasks

        :param count: The size of semaphore
        """
        self._semaphore = threading.Semaphore(count)
    
    def acquire(self, tag, blocking=True):
        """Acquire the semaphore

        :param tag: A tag identifying what is acquiring the semaphore. Note
            that this is not really needed to directly use this class but is
            needed for API compatibility with the SlidingWindowSemaphore
            implementation.
        :param block: If True, block until it can be acquired. If False,
            do not block and raise an exception if cannot be acquired.

        :returns: A token (can be None) to use when releasing the semaphore
        """
        logger.debug('Acquiring %s', tag)
        if not self._semaphore.acquire(blocking):
            raise NoResourcesAvailable(f"Cannot acquire tag '{tag}'")
    
    def release(self, tag, acquire_token):
        """Release the semaphore

        :param tag: A tag identifying what is releasing the semaphore
        :param acquire_token:  The token returned from when the semaphore was
            acquired. Note that this is not really needed to directly use this
            class but is needed for API compatibility with the
            SlidingWindowSemaphore implementation.
        """
        logger.debug(f'Releasing acquire {tag}/{acquire_token}')
        self._semaphore.release()



class SlidingWindowSemaphore(TaskSemaphore):
    """A semaphore used to coordinate sequential resource access.

    This class is similar to the stdlib BoundedSemaphore:

    * It's initialized with a count.
    * Each call to ``acquire()`` decrements the counter.
    * If the count is at zero, then ``acquire()`` will either block until the
      count increases, or if ``blocking=False``, then it will raise
      a NoResourcesAvailable exception indicating that it failed to acquire the
      semaphore.

    The main difference is that this semaphore is used to limit
    access to a resource that requires sequential access.  For example,
    if I want to access resource R that has 20 subresources R_0 - R_19,
    this semaphore can also enforce that you only have a max range of
    10 at any given point in time.  You must also specify a tag name
    when you acquire the semaphore.  The sliding window semantics apply
    on a per tag basis.  The internal count will only be incremented
    when the minimum sequence number for a tag is released.

    """
    
    def __init__(self, count):
        self._count = count
        self._tag_sequences = defaultdict(int)
        self._lowest_sequence = {}
        self._lock = threading.Lock()
        self._condition = threading.Condition(self._lock)
        self._pending_release = {}
    
    def current_count(self):
        with self._lock:
            return self._count
    
    def acquire(self, tag, blocking=True):
        logger.debug('Acquiring %s', tag)
        self._condition.acquire()
        try:
            if self._count == 0:
                if not blocking:
                    raise NoResourcesAvailable(f"Cannot acquire tag '{tag}'")
                else:
                    while self._count == 0:
                        self._condition.wait()
            sequence_number = self._tag_sequences[tag]
            if sequence_number == 0:
                self._lowest_sequence[tag] = sequence_number
            self._tag_sequences[tag] += 1
            self._count -= 1
            return sequence_number
        finally:
            self._condition.release()
    
    def release(self, tag, acquire_token):
        sequence_number = acquire_token
        logger.debug('Releasing acquire %s/%s', tag, sequence_number)
        self._condition.acquire()
        try:
            if tag not in self._tag_sequences:
                raise ValueError(f'Attempted to release unknown tag: {tag}')
            max_sequence = self._tag_sequences[tag]
            if self._lowest_sequence[tag] == sequence_number:
                self._lowest_sequence[tag] += 1
                self._count += 1
                self._condition.notify()
                queued = self._pending_release.get(tag, [])
                while queued:
                    if self._lowest_sequence[tag] == queued[-1]:
                        queued.pop()
                        self._lowest_sequence[tag] += 1
                        self._count += 1
                    else:
                        break
            elif self._lowest_sequence[tag] < sequence_number < max_sequence:
                self._pending_release.setdefault(tag, []).append(sequence_number)
                self._pending_release[tag].sort(reverse=True)
            else:
                raise ValueError(f'Attempted to release unknown sequence number {sequence_number} for tag: {tag}')
        finally:
            self._condition.release()



class ChunksizeAdjuster:
    
    def __init__(self, max_size=MAX_SINGLE_UPLOAD_SIZE, min_size=MIN_UPLOAD_CHUNKSIZE, max_parts=MAX_PARTS):
        self.max_size = max_size
        self.min_size = min_size
        self.max_parts = max_parts
    
    def adjust_chunksize(self, current_chunksize, file_size=None):
        """Get a chunksize close to current that fits within all S3 limits.

        :type current_chunksize: int
        :param current_chunksize: The currently configured chunksize.

        :type file_size: int or None
        :param file_size: The size of the file to upload. This might be None
            if the object being transferred has an unknown size.

        :returns: A valid chunksize that fits within configured limits.
        """
        chunksize = current_chunksize
        if file_size is not None:
            chunksize = self._adjust_for_max_parts(chunksize, file_size)
        return self._adjust_for_chunksize_limits(chunksize)
    
    def _adjust_for_chunksize_limits(self, current_chunksize):
        if current_chunksize > self.max_size:
            logger.debug(f'Chunksize greater than maximum chunksize. Setting to {self.max_size} from {current_chunksize}.')
            return self.max_size
        elif current_chunksize < self.min_size:
            logger.debug(f'Chunksize less than minimum chunksize. Setting to {self.min_size} from {current_chunksize}.')
            return self.min_size
        else:
            return current_chunksize
    
    def _adjust_for_max_parts(self, current_chunksize, file_size):
        chunksize = current_chunksize
        num_parts = int(math.ceil(file_size / float(chunksize)))
        while num_parts > self.max_parts:
            chunksize *= 2
            num_parts = int(math.ceil(file_size / float(chunksize)))
        if chunksize != current_chunksize:
            logger.debug(f'Chunksize would result in the number of parts exceeding the maximum. Setting to {chunksize} from {current_chunksize}.')
        return chunksize


def add_s3express_defaults(bucket, extra_args):
    """
    This function has been deprecated, but is kept for backwards compatibility.
    This function is subject to removal in a future release.
    """
    if (is_s3express_bucket(bucket) and 'ChecksumAlgorithm' not in extra_args):
        extra_args['ChecksumAlgorithm'] = 'crc32'

def set_default_checksum_algorithm(extra_args):
    """Set the default algorithm to CRC32 if not specified by the user."""
    import custom_funtemplate
    return custom_funtemplate.rewrite_template('s3transfer.utils.set_default_checksum_algorithm', 'set_default_checksum_algorithm(extra_args)', {'FULL_OBJECT_CHECKSUM_ARGS': FULL_OBJECT_CHECKSUM_ARGS, 'DEFAULT_CHECKSUM_ALGORITHM': DEFAULT_CHECKSUM_ALGORITHM, 'extra_args': extra_args}, 1)
try:
    from botocore.utils import create_nested_client as create_client
except ImportError:
    
    def create_client(session, *args, **kwargs):
        return session.create_client(*args, **kwargs)

def create_nested_client(session, service_name, **kwargs):
    return create_client(session, service_name, **kwargs)

