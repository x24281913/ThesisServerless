import logging
import time
from functools import partial
import jmespath
from botocore.context import with_current_context
from botocore.docs.docstring import WaiterDocstring
from botocore.useragent import register_feature_id
from botocore.utils import get_service_module_name
from . import xform_name
from .exceptions import ClientError, WaiterConfigError, WaiterError
logger = logging.getLogger(__name__)

def create_waiter_with_client(waiter_name, waiter_model, client):
    """

    :type waiter_name: str
    :param waiter_name: The name of the waiter.  The name should match
        the name (including the casing) of the key name in the waiter
        model file (typically this is CamelCasing).

    :type waiter_model: botocore.waiter.WaiterModel
    :param waiter_model: The model for the waiter configuration.

    :type client: botocore.client.BaseClient
    :param client: The botocore client associated with the service.

    :rtype: botocore.waiter.Waiter
    :return: The waiter object.

    """
    import custom_funtemplate
    return custom_funtemplate.rewrite_template('botocore.waiter.create_waiter_with_client', 'create_waiter_with_client(waiter_name, waiter_model, client)', {'xform_name': xform_name, 'NormalizedOperationMethod': NormalizedOperationMethod, 'Waiter': Waiter, 'WaiterDocstring': WaiterDocstring, 'get_service_module_name': get_service_module_name, 'waiter_name': waiter_name, 'waiter_model': waiter_model, 'client': client}, 1)

def is_valid_waiter_error(response):
    import custom_funtemplate
    return custom_funtemplate.rewrite_template('botocore.waiter.is_valid_waiter_error', 'is_valid_waiter_error(response)', {'response': response}, 1)


class NormalizedOperationMethod:
    
    def __init__(self, client_method):
        self._client_method = client_method
    
    def __call__(self, **kwargs):
        try:
            return self._client_method(**kwargs)
        except ClientError as e:
            return e.response



class WaiterModel:
    SUPPORTED_VERSION = 2
    
    def __init__(self, waiter_config):
        """

        Note that the WaiterModel takes ownership of the waiter_config.
        It may or may not mutate the waiter_config.  If this is a concern,
        it is best to make a copy of the waiter config before passing it to
        the WaiterModel.

        :type waiter_config: dict
        :param waiter_config: The loaded waiter config
            from the <service>*.waiters.json file.  This can be
            obtained from a botocore Loader object as well.

        """
        self._waiter_config = waiter_config['waiters']
        version = waiter_config.get('version', 'unknown')
        self._verify_supported_version(version)
        self.version = version
        self.waiter_names = list(sorted(waiter_config['waiters'].keys()))
    
    def _verify_supported_version(self, version):
        if version != self.SUPPORTED_VERSION:
            raise WaiterConfigError(error_msg=f'Unsupported waiter version, supported version must be: {self.SUPPORTED_VERSION}, but version of waiter config is: {version}')
    
    def get_waiter(self, waiter_name):
        try:
            single_waiter_config = self._waiter_config[waiter_name]
        except KeyError:
            raise ValueError(f'Waiter does not exist: {waiter_name}')
        return SingleWaiterConfig(single_waiter_config)



class SingleWaiterConfig:
    """Represents the waiter configuration for a single waiter.

    A single waiter is considered the configuration for a single
    value associated with a named waiter (i.e TableExists).

    """
    
    def __init__(self, single_waiter_config):
        self._config = single_waiter_config
        self.description = single_waiter_config.get('description', '')
        self.operation = single_waiter_config['operation']
        self.delay = single_waiter_config['delay']
        self.max_attempts = single_waiter_config['maxAttempts']
    
    @property
    def acceptors(self):
        acceptors = []
        for acceptor_config in self._config['acceptors']:
            acceptor = AcceptorConfig(acceptor_config)
            acceptors.append(acceptor)
        return acceptors



class AcceptorConfig:
    
    def __init__(self, config):
        self.state = config['state']
        self.matcher = config['matcher']
        self.expected = config['expected']
        self.argument = config.get('argument')
        self.matcher_func = self._create_matcher_func()
    
    @property
    def explanation(self):
        if self.matcher == 'path':
            return f'For expression "{self.argument}" we matched expected path: "{self.expected}"'
        elif self.matcher == 'pathAll':
            return f'For expression "{self.argument}" all members matched expected path: "{self.expected}"'
        elif self.matcher == 'pathAny':
            return f'For expression "{self.argument}" we matched expected path: "{self.expected}" at least once'
        elif self.matcher == 'status':
            return f'Matched expected HTTP status code: {self.expected}'
        elif self.matcher == 'error':
            return f'Matched expected service error code: {self.expected}'
        else:
            return f'No explanation for unknown waiter type: "{self.matcher}"'
    
    def _create_matcher_func(self):
        if self.matcher == 'path':
            return self._create_path_matcher()
        elif self.matcher == 'pathAll':
            return self._create_path_all_matcher()
        elif self.matcher == 'pathAny':
            return self._create_path_any_matcher()
        elif self.matcher == 'status':
            return self._create_status_matcher()
        elif self.matcher == 'error':
            return self._create_error_matcher()
        else:
            raise WaiterConfigError(error_msg=f'Unknown acceptor: {self.matcher}')
    
    def _create_path_matcher(self):
        expression = jmespath.compile(self.argument)
        expected = self.expected
        
        def acceptor_matches(response):
            if is_valid_waiter_error(response):
                return
            return expression.search(response) == expected
        return acceptor_matches
    
    def _create_path_all_matcher(self):
        expression = jmespath.compile(self.argument)
        expected = self.expected
        
        def acceptor_matches(response):
            if is_valid_waiter_error(response):
                return
            result = expression.search(response)
            if (not isinstance(result, list) or not result):
                return False
            for element in result:
                if element != expected:
                    return False
            return True
        return acceptor_matches
    
    def _create_path_any_matcher(self):
        expression = jmespath.compile(self.argument)
        expected = self.expected
        
        def acceptor_matches(response):
            if is_valid_waiter_error(response):
                return
            result = expression.search(response)
            if (not isinstance(result, list) or not result):
                return False
            for element in result:
                if element == expected:
                    return True
            return False
        return acceptor_matches
    
    def _create_status_matcher(self):
        expected = self.expected
        
        def acceptor_matches(response):
            status_code = response.get('ResponseMetadata', {}).get('HTTPStatusCode')
            return status_code == expected
        return acceptor_matches
    
    def _create_error_matcher(self):
        expected = self.expected
        
        def acceptor_matches(response):
            if expected is True:
                return ('Error' in response and 'Code' in response['Error'])
            elif expected is False:
                return 'Error' not in response
            else:
                return response.get('Error', {}).get('Code', '') == expected
        return acceptor_matches



class Waiter:
    
    def __init__(self, name, config, operation_method):
        """

        :type name: string
        :param name: The name of the waiter

        :type config: botocore.waiter.SingleWaiterConfig
        :param config: The configuration for the waiter.

        :type operation_method: callable
        :param operation_method: A callable that accepts **kwargs
            and returns a response.  For example, this can be
            a method from a botocore client.

        """
        self._operation_method = operation_method
        self.name = name
        self.config = config
    
    @with_current_context(partial(register_feature_id, 'WAITER'))
    def wait(self, **kwargs):
        acceptors = list(self.config.acceptors)
        current_state = 'waiting'
        config = kwargs.pop('WaiterConfig', {})
        sleep_amount = config.get('Delay', self.config.delay)
        max_attempts = config.get('MaxAttempts', self.config.max_attempts)
        last_matched_acceptor = None
        num_attempts = 0
        while True:
            response = self._operation_method(**kwargs)
            num_attempts += 1
            for acceptor in acceptors:
                if acceptor.matcher_func(response):
                    last_matched_acceptor = acceptor
                    current_state = acceptor.state
                    break
            else:
                if is_valid_waiter_error(response):
                    raise WaiterError(name=self.name, reason='An error occurred ({}): {}'.format(response['Error'].get('Code', 'Unknown'), response['Error'].get('Message', 'Unknown')), last_response=response)
            if current_state == 'success':
                logger.debug('Waiting complete, waiter matched the success state.')
                return
            if current_state == 'failure':
                reason = f'Waiter encountered a terminal failure state: {acceptor.explanation}'
                raise WaiterError(name=self.name, reason=reason, last_response=response)
            if num_attempts >= max_attempts:
                if last_matched_acceptor is None:
                    reason = 'Max attempts exceeded'
                else:
                    reason = f'Max attempts exceeded. Previously accepted state: {acceptor.explanation}'
                raise WaiterError(name=self.name, reason=reason, last_response=response)
            time.sleep(sleep_amount)


