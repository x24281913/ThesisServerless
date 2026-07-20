import copy
import logging
from s3transfer.utils import get_callbacks
try:
    from botocore.context import start_as_current_context
except ImportError:
    from contextlib import nullcontext as start_as_current_context
logger = logging.getLogger(__name__)


class Task:
    """A task associated to a TransferFuture request

    This is a base class for other classes to subclass from. All subclassed
    classes must implement the main() method.
    """
    
    def __init__(self, transfer_coordinator, main_kwargs=None, pending_main_kwargs=None, done_callbacks=None, is_final=False):
        """
        :type transfer_coordinator: s3transfer.futures.TransferCoordinator
        :param transfer_coordinator: The context associated to the
            TransferFuture for which this Task is associated with.

        :type main_kwargs: dict
        :param main_kwargs: The keyword args that can be immediately supplied
            to the _main() method of the task

        :type pending_main_kwargs: dict
        :param pending_main_kwargs: The keyword args that are depended upon
            by the result from a dependent future(s). The result returned by
            the future(s) will be used as the value for the keyword argument
            when _main() is called. The values for each key can be:
                * a single future - Once completed, its value will be the
                  result of that single future
                * a list of futures - Once all of the futures complete, the
                  value used will be a list of each completed future result
                  value in order of when they were originally supplied.

        :type done_callbacks: list of callbacks
        :param done_callbacks: A list of callbacks to call once the task is
            done completing. Each callback will be called with no arguments
            and will be called no matter if the task succeeds or an exception
            is raised.

        :type is_final: boolean
        :param is_final: True, to indicate that this task is the final task
            for the TransferFuture request. By setting this value to True, it
            will set the result of the entire TransferFuture to the result
            returned by this task's main() method.
        """
        self._transfer_coordinator = transfer_coordinator
        self._main_kwargs = main_kwargs
        if self._main_kwargs is None:
            self._main_kwargs = {}
        self._pending_main_kwargs = pending_main_kwargs
        if pending_main_kwargs is None:
            self._pending_main_kwargs = {}
        self._done_callbacks = done_callbacks
        if self._done_callbacks is None:
            self._done_callbacks = []
        self._is_final = is_final
    
    def __repr__(self):
        params_to_display = ['bucket', 'key', 'part_number', 'final_filename', 'transfer_future', 'offset', 'extra_args']
        main_kwargs_to_display = self._get_kwargs_with_params_to_include(self._main_kwargs, params_to_display)
        return f'{self.__class__.__name__}(transfer_id={self._transfer_coordinator.transfer_id}, {main_kwargs_to_display})'
    
    @property
    def transfer_id(self):
        """The id for the transfer request that the task belongs to"""
        return self._transfer_coordinator.transfer_id
    
    def _get_kwargs_with_params_to_include(self, kwargs, include):
        filtered_kwargs = {}
        for param in include:
            if param in kwargs:
                filtered_kwargs[param] = kwargs[param]
        return filtered_kwargs
    
    def _get_kwargs_with_params_to_exclude(self, kwargs, exclude):
        filtered_kwargs = {}
        for (param, value) in kwargs.items():
            if param in exclude:
                continue
            filtered_kwargs[param] = value
        return filtered_kwargs
    
    def __call__(self, ctx=None):
        """The callable to use when submitting a Task to an executor"""
        with start_as_current_context(ctx):
            try:
                try:
                    self._wait_on_dependent_futures()
                    kwargs = self._get_all_main_kwargs()
                    if not self._transfer_coordinator.done():
                        return self._execute_main(kwargs)
                except Exception as e:
                    self._log_and_set_exception(e)
            finally:
                for done_callback in self._done_callbacks:
                    done_callback()
                if self._is_final:
                    self._transfer_coordinator.announce_done()
    
    def _execute_main(self, kwargs):
        params_to_exclude = ['data']
        kwargs_to_display = self._get_kwargs_with_params_to_exclude(kwargs, params_to_exclude)
        logger.debug(f'Executing task {self} with kwargs {kwargs_to_display}')
        return_value = self._main(**kwargs)
        if self._is_final:
            self._transfer_coordinator.set_result(return_value)
        return return_value
    
    def _log_and_set_exception(self, exception):
        logger.debug('Exception raised.', exc_info=True)
        self._transfer_coordinator.set_exception(exception)
    
    def _main(self, **kwargs):
        """The method that will be ran in the executor

        This method must be implemented by subclasses from Task. main() can
        be implemented with any arguments decided upon by the subclass.
        """
        raise NotImplementedError('_main() must be implemented')
    
    def _wait_on_dependent_futures(self):
        futures_to_wait_on = []
        for (_, future) in self._pending_main_kwargs.items():
            if isinstance(future, list):
                futures_to_wait_on.extend(future)
            else:
                futures_to_wait_on.append(future)
        self._wait_until_all_complete(futures_to_wait_on)
    
    def _wait_until_all_complete(self, futures):
        logger.debug('%s about to wait for the following futures %s', self, futures)
        for future in futures:
            try:
                logger.debug('%s about to wait for %s', self, future)
                future.result()
            except Exception:
                pass
        logger.debug('%s done waiting for dependent futures', self)
    
    def _get_all_main_kwargs(self):
        kwargs = copy.copy(self._main_kwargs)
        for (key, pending_value) in self._pending_main_kwargs.items():
            if isinstance(pending_value, list):
                result = []
                for future in pending_value:
                    result.append(future.result())
            else:
                result = pending_value.result()
            kwargs[key] = result
        return kwargs



class SubmissionTask(Task):
    """A base class for any submission task

    Submission tasks are the top-level task used to submit a series of tasks
    to execute a particular transfer.
    """
    
    def _main(self, transfer_future, **kwargs):
        """
        :type transfer_future: s3transfer.futures.TransferFuture
        :param transfer_future: The transfer future associated with the
            transfer request that tasks are being submitted for

        :param kwargs: Any additional kwargs that you may want to pass
            to the _submit() method
        """
        try:
            self._transfer_coordinator.set_status_to_queued()
            on_queued_callbacks = get_callbacks(transfer_future, 'queued')
            for on_queued_callback in on_queued_callbacks:
                on_queued_callback()
            self._transfer_coordinator.set_status_to_running()
            self._submit(transfer_future=transfer_future, **kwargs)
        except BaseException as e:
            self._log_and_set_exception(e)
            self._wait_for_all_submitted_futures_to_complete()
            self._transfer_coordinator.announce_done()
    
    def _submit(self, transfer_future, **kwargs):
        """The submission method to be implemented

        :type transfer_future: s3transfer.futures.TransferFuture
        :param transfer_future: The transfer future associated with the
            transfer request that tasks are being submitted for

        :param kwargs: Any additional keyword arguments you want to be passed
            in
        """
        raise NotImplementedError('_submit() must be implemented')
    
    def _wait_for_all_submitted_futures_to_complete(self):
        submitted_futures = self._transfer_coordinator.associated_futures
        while submitted_futures:
            self._wait_until_all_complete(submitted_futures)
            possibly_more_submitted_futures = self._transfer_coordinator.associated_futures
            if submitted_futures == possibly_more_submitted_futures:
                break
            submitted_futures = possibly_more_submitted_futures



class CreateMultipartUploadTask(Task):
    """Task to initiate a multipart upload"""
    
    def _main(self, client, bucket, key, extra_args):
        """
        :param client: The client to use when calling CreateMultipartUpload
        :param bucket: The name of the bucket to upload to
        :param key: The name of the key to upload to
        :param extra_args: A dictionary of any extra arguments that may be
            used in the initialization.

        :returns: The upload id of the multipart upload
        """
        response = client.create_multipart_upload(Bucket=bucket, Key=key, **extra_args)
        upload_id = response['UploadId']
        self._transfer_coordinator.add_failure_cleanup(client.abort_multipart_upload, Bucket=bucket, Key=key, UploadId=upload_id)
        return upload_id



class CompleteMultipartUploadTask(Task):
    """Task to complete a multipart upload"""
    
    def _main(self, client, bucket, key, upload_id, parts, extra_args):
        """
        :param client: The client to use when calling CompleteMultipartUpload
        :param bucket: The name of the bucket to upload to
        :param key: The name of the key to upload to
        :param upload_id: The id of the upload
        :param parts: A list of parts to use to complete the multipart upload::

            [{'Etag': etag_value, 'PartNumber': part_number}, ...]

            Each element in the list consists of a return value from
            ``UploadPartTask.main()``.
        :param extra_args:  A dictionary of any extra arguments that may be
            used in completing the multipart transfer.
        """
        client.complete_multipart_upload(Bucket=bucket, Key=key, UploadId=upload_id, MultipartUpload={'Parts': parts}, **extra_args)


