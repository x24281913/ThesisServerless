import logging
import boto3
logger = logging.getLogger(__name__)


class ResourceMeta:
    """
    An object containing metadata about a resource.
    """
    
    def __init__(self, service_name, identifiers=None, client=None, data=None, resource_model=None):
        self.service_name = service_name
        if identifiers is None:
            identifiers = []
        self.identifiers = identifiers
        self.client = client
        self.data = data
        self.resource_model = resource_model
    
    def __repr__(self):
        return f"ResourceMeta('{self.service_name}', identifiers={self.identifiers})"
    
    def __eq__(self, other):
        if other.__class__.__name__ != self.__class__.__name__:
            return False
        return self.__dict__ == other.__dict__
    
    def copy(self):
        """
        Create a copy of this metadata object.
        """
        params = self.__dict__.copy()
        service_name = params.pop('service_name')
        return ResourceMeta(service_name, **params)



class ServiceResource:
    """
    A base class for resources.

    :type client: botocore.client
    :param client: A low-level Botocore client instance
    """
    meta = None
    "\n    Stores metadata about this resource instance, such as the\n    ``service_name``, the low-level ``client`` and any cached ``data``\n    from when the instance was hydrated. For example::\n\n        # Get a low-level client from a resource instance\n        client = resource.meta.client\n        response = client.operation(Param='foo')\n\n        # Print the resource instance's service short name\n        print(resource.meta.service_name)\n\n    See :py:class:`ResourceMeta` for more information.\n    "
    
    def __init__(self, *args, **kwargs):
        self.meta = self.meta.copy()
        if kwargs.get('client') is not None:
            self.meta.client = kwargs.get('client')
        else:
            self.meta.client = boto3.client(self.meta.service_name)
        for (i, value) in enumerate(args):
            setattr(self, f'_{self.meta.identifiers[i]}', value)
        for (name, value) in kwargs.items():
            if name == 'client':
                continue
            if name not in self.meta.identifiers:
                raise ValueError(f'Unknown keyword argument: {name}')
            setattr(self, f'_{name}', value)
        for identifier in self.meta.identifiers:
            if getattr(self, identifier) is None:
                raise ValueError(f'Required parameter {identifier} not set')
    
    def __repr__(self):
        identifiers = [f'{identifier}={repr(getattr(self, identifier))}' for identifier in self.meta.identifiers]
        return f"{self.__class__.__name__}({', '.join(identifiers)})"
    
    def __eq__(self, other):
        if other.__class__.__name__ != self.__class__.__name__:
            return False
        for identifier in self.meta.identifiers:
            if getattr(self, identifier) != getattr(other, identifier):
                return False
        return True
    
    def __hash__(self):
        identifiers = []
        for identifier in self.meta.identifiers:
            identifiers.append(getattr(self, identifier))
        return hash((self.__class__.__name__, tuple(identifiers)))


