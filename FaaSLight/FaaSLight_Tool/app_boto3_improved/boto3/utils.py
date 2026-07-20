from collections import namedtuple
from importlib import import_module
_ServiceContext = namedtuple('ServiceContext', ['service_name', 'service_model', 'service_waiter_model', 'resource_json_definitions'])


class ServiceContext(_ServiceContext):
    """Provides important service-wide, read-only information about a service

    :type service_name: str
    :param service_name: The name of the service

    :type service_model: :py:class:`botocore.model.ServiceModel`
    :param service_model: The model of the service.

    :type service_waiter_model: :py:class:`botocore.waiter.WaiterModel` or
        a waiter model-like object such as
        :py:class:`boto3.utils.LazyLoadedWaiterModel`
    :param service_waiter_model: The waiter model of the service.

    :type resource_json_definitions: dict
    :param resource_json_definitions: The loaded json models of all resource
        shapes for a service. It is equivalient of loading a
        ``resource-1.json`` and retrieving the value at the key "resources".
    """
    pass


def lazy_call(full_name, **kwargs):
    parent_kwargs = kwargs
    
    def _handler(**kwargs):
        import custom_funtemplate
        return custom_funtemplate.rewrite_template('boto3.utils.lazy_call._handler', '_handler(**kwargs)', {'full_name': full_name, 'import_module': import_module, 'parent_kwargs': parent_kwargs, 'kwargs': kwargs}, 1)
    return _handler

def inject_attribute(class_attributes, name, value):
    import custom_funtemplate
    custom_funtemplate.rewrite_template('boto3.utils.inject_attribute', 'inject_attribute(class_attributes, name, value)', {'class_attributes': class_attributes, 'name': name, 'value': value}, 0)


class LazyLoadedWaiterModel:
    """A lazily loaded waiter model

    This does not load the service waiter model until an attempt is made
    to retrieve the waiter model for a specific waiter. This is helpful
    in docstring generation where we do not need to actually need to grab
    the waiter-2.json until it is accessed through a ``get_waiter`` call
    when the docstring is generated/accessed.
    """
    
    def __init__(self, bc_session, service_name, api_version):
        self._session = bc_session
        self._service_name = service_name
        self._api_version = api_version
    
    def get_waiter(self, waiter_name):
        return self._session.get_waiter_model(self._service_name, self._api_version).get_waiter(waiter_name)


