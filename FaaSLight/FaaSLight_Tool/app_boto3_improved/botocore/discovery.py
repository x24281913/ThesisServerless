import logging
import time
import weakref
from botocore import xform_name
from botocore.exceptions import BotoCoreError, ConnectionError, HTTPClientError
from botocore.model import OperationNotFoundError
from botocore.utils import CachedProperty
logger = logging.getLogger(__name__)


class EndpointDiscoveryException(BotoCoreError):
    pass



class EndpointDiscoveryRequired(EndpointDiscoveryException):
    """Endpoint Discovery is disabled but is required for this operation."""
    fmt = 'Endpoint Discovery is not enabled but this operation requires it.'



class EndpointDiscoveryRefreshFailed(EndpointDiscoveryException):
    """Endpoint Discovery failed to the refresh the known endpoints."""
    fmt = 'Endpoint Discovery failed to refresh the required endpoints.'


def block_endpoint_discovery_required_operations(model, **kwargs):
    endpoint_discovery = model.endpoint_discovery
    if (endpoint_discovery and endpoint_discovery.get('required')):
        raise EndpointDiscoveryRequired()


class EndpointDiscoveryModel:
    
    def __init__(self, service_model):
        self._service_model = service_model
    
    @CachedProperty
    def discovery_operation_name(self):
        discovery_operation = self._service_model.endpoint_discovery_operation
        return xform_name(discovery_operation.name)
    
    @CachedProperty
    def discovery_operation_keys(self):
        discovery_operation = self._service_model.endpoint_discovery_operation
        keys = []
        if discovery_operation.input_shape:
            keys = list(discovery_operation.input_shape.members.keys())
        return keys
    
    def discovery_required_for(self, operation_name):
        try:
            operation_model = self._service_model.operation_model(operation_name)
            return operation_model.endpoint_discovery.get('required', False)
        except OperationNotFoundError:
            return False
    
    def discovery_operation_kwargs(self, **kwargs):
        input_keys = self.discovery_operation_keys
        if not kwargs.get('Identifiers'):
            kwargs.pop('Operation', None)
            kwargs.pop('Identifiers', None)
        return {k: v for (k, v) in kwargs.items() if k in input_keys}
    
    def gather_identifiers(self, operation, params):
        return self._gather_ids(operation.input_shape, params)
    
    def _gather_ids(self, shape, params, ids=None):
        if ids is None:
            ids = {}
        for (member_name, member_shape) in shape.members.items():
            if member_shape.metadata.get('endpointdiscoveryid'):
                ids[member_name] = params[member_name]
            elif (member_shape.type_name == 'structure' and member_name in params):
                self._gather_ids(member_shape, params[member_name], ids)
        return ids



class EndpointDiscoveryManager:
    
    def __init__(self, client, cache=None, current_time=None, always_discover=True):
        if cache is None:
            cache = {}
        self._cache = cache
        self._failed_attempts = {}
        if current_time is None:
            current_time = time.time
        self._time = current_time
        self._always_discover = always_discover
        self._client = weakref.proxy(client)
        self._model = EndpointDiscoveryModel(client.meta.service_model)
    
    def _parse_endpoints(self, response):
        endpoints = response['Endpoints']
        current_time = self._time()
        for endpoint in endpoints:
            cache_time = endpoint.get('CachePeriodInMinutes')
            endpoint['Expiration'] = current_time + cache_time * 60
        return endpoints
    
    def _cache_item(self, value):
        if isinstance(value, dict):
            return tuple(sorted(value.items()))
        else:
            return value
    
    def _create_cache_key(self, **kwargs):
        kwargs = self._model.discovery_operation_kwargs(**kwargs)
        return tuple((self._cache_item(v) for (k, v) in sorted(kwargs.items())))
    
    def gather_identifiers(self, operation, params):
        return self._model.gather_identifiers(operation, params)
    
    def delete_endpoints(self, **kwargs):
        cache_key = self._create_cache_key(**kwargs)
        if cache_key in self._cache:
            del self._cache[cache_key]
    
    def _describe_endpoints(self, **kwargs):
        kwargs = self._model.discovery_operation_kwargs(**kwargs)
        operation_name = self._model.discovery_operation_name
        discovery_operation = getattr(self._client, operation_name)
        logger.debug('Discovering endpoints with kwargs: %s', kwargs)
        return discovery_operation(**kwargs)
    
    def _get_current_endpoints(self, key):
        if key not in self._cache:
            return None
        now = self._time()
        return [e for e in self._cache[key] if now < e['Expiration']]
    
    def _refresh_current_endpoints(self, **kwargs):
        cache_key = self._create_cache_key(**kwargs)
        try:
            response = self._describe_endpoints(**kwargs)
            endpoints = self._parse_endpoints(response)
            self._cache[cache_key] = endpoints
            self._failed_attempts.pop(cache_key, None)
            return endpoints
        except (ConnectionError, HTTPClientError):
            self._failed_attempts[cache_key] = self._time() + 60
            return None
    
    def _recently_failed(self, cache_key):
        if cache_key in self._failed_attempts:
            now = self._time()
            if now < self._failed_attempts[cache_key]:
                return True
            del self._failed_attempts[cache_key]
        return False
    
    def _select_endpoint(self, endpoints):
        return endpoints[0]['Address']
    
    def describe_endpoint(self, **kwargs):
        operation = kwargs['Operation']
        discovery_required = self._model.discovery_required_for(operation)
        if (not self._always_discover and not discovery_required):
            logger.debug('Optional discovery disabled. Skipping discovery for Operation: %s', operation)
            return None
        cache_key = self._create_cache_key(**kwargs)
        endpoints = self._get_current_endpoints(cache_key)
        if endpoints:
            return self._select_endpoint(endpoints)
        recently_failed = self._recently_failed(cache_key)
        if not recently_failed:
            endpoints = self._refresh_current_endpoints(**kwargs)
            if endpoints:
                return self._select_endpoint(endpoints)
        logger.debug('Endpoint Discovery has failed for: %s', kwargs)
        stale_entries = self._cache.get(cache_key, None)
        if stale_entries:
            return self._select_endpoint(stale_entries)
        if discovery_required:
            if recently_failed:
                endpoints = self._refresh_current_endpoints(**kwargs)
                if endpoints:
                    return self._select_endpoint(endpoints)
            raise EndpointDiscoveryRefreshFailed()
        return None



class EndpointDiscoveryHandler:
    
    def __init__(self, manager):
        self._manager = manager
    
    def register(self, events, service_id):
        events.register(f'before-parameter-build.{service_id}', self.gather_identifiers)
        events.register_first(f'request-created.{service_id}', self.discover_endpoint)
        events.register(f'needs-retry.{service_id}', self.handle_retries)
    
    def gather_identifiers(self, params, model, context, **kwargs):
        endpoint_discovery = model.endpoint_discovery
        if endpoint_discovery is None:
            return
        ids = self._manager.gather_identifiers(model, params)
        context['discovery'] = {'identifiers': ids}
    
    def discover_endpoint(self, request, operation_name, **kwargs):
        ids = request.context.get('discovery', {}).get('identifiers')
        if ids is None:
            return
        endpoint = self._manager.describe_endpoint(Operation=operation_name, Identifiers=ids)
        if endpoint is None:
            logger.debug('Failed to discover and inject endpoint')
            return
        if not endpoint.startswith('http'):
            endpoint = 'https://' + endpoint
        logger.debug('Injecting discovered endpoint: %s', endpoint)
        request.url = endpoint
    
    def handle_retries(self, request_dict, response, operation, **kwargs):
        if response is None:
            return None
        (_, response) = response
        status = response.get('ResponseMetadata', {}).get('HTTPStatusCode')
        error_code = response.get('Error', {}).get('Code')
        if (status != 421 and error_code != 'InvalidEndpointException'):
            return None
        context = request_dict.get('context', {})
        ids = context.get('discovery', {}).get('identifiers')
        if ids is None:
            return None
        self._manager.delete_endpoints(Operation=operation.name, Identifiers=ids)
        return 0


