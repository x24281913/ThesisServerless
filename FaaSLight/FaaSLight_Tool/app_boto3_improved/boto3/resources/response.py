import jmespath
from botocore import xform_name
from .params import get_data_member

def all_not_none(iterable):
    """
    Return True if all elements of the iterable are not None (or if the
    iterable is empty). This is like the built-in ``all``, except checks
    against None, so 0 and False are allowable values.
    """
    import custom_funtemplate
    return custom_funtemplate.rewrite_template('boto3.resources.response.all_not_none', 'all_not_none(iterable)', {'iterable': iterable}, 1)

def build_identifiers(identifiers, parent, params=None, raw_response=None):
    """
    Builds a mapping of identifier names to values based on the
    identifier source location, type, and target. Identifier
    values may be scalars or lists depending on the source type
    and location.

    :type identifiers: list
    :param identifiers: List of :py:class:`~boto3.resources.model.Parameter`
                        definitions
    :type parent: ServiceResource
    :param parent: The resource instance to which this action is attached.
    :type params: dict
    :param params: Request parameters sent to the service.
    :type raw_response: dict
    :param raw_response: Low-level operation response.
    :rtype: list
    :return: An ordered list of ``(name, value)`` identifier tuples.
    """
    import custom_funtemplate
    return custom_funtemplate.rewrite_template('boto3.resources.response.build_identifiers', 'build_identifiers(identifiers, parent, params=None, raw_response=None)', {'jmespath': jmespath, 'xform_name': xform_name, 'get_data_member': get_data_member, 'identifiers': identifiers, 'parent': parent, 'params': params, 'raw_response': raw_response}, 1)

def build_empty_response(search_path, operation_name, service_model):
    """
    Creates an appropriate empty response for the type that is expected,
    based on the service model's shape type. For example, a value that
    is normally a list would then return an empty list. A structure would
    return an empty dict, and a number would return None.

    :type search_path: string
    :param search_path: JMESPath expression to search in the response
    :type operation_name: string
    :param operation_name: Name of the underlying service operation.
    :type service_model: :ref:`botocore.model.ServiceModel`
    :param service_model: The Botocore service model
    :rtype: dict, list, or None
    :return: An appropriate empty value
    """
    import custom_funtemplate
    return custom_funtemplate.rewrite_template('boto3.resources.response.build_empty_response', 'build_empty_response(search_path, operation_name, service_model)', {'search_path': search_path, 'operation_name': operation_name, 'service_model': service_model}, 1)


class RawHandler:
    """
    A raw action response handler. This passed through the response
    dictionary, optionally after performing a JMESPath search if one
    has been defined for the action.

    :type search_path: string
    :param search_path: JMESPath expression to search in the response
    :rtype: dict
    :return: Service response
    """
    
    def __init__(self, search_path):
        self.search_path = search_path
    
    def __call__(self, parent, params, response):
        """
        :type parent: ServiceResource
        :param parent: The resource instance to which this action is attached.
        :type params: dict
        :param params: Request parameters sent to the service.
        :type response: dict
        :param response: Low-level operation response.
        """
        if (self.search_path and self.search_path != '$'):
            response = jmespath.search(self.search_path, response)
        return response



class ResourceHandler:
    """
    Creates a new resource or list of new resources from the low-level
    response based on the given response resource definition.

    :type search_path: string
    :param search_path: JMESPath expression to search in the response

    :type factory: ResourceFactory
    :param factory: The factory that created the resource class to which
                    this action is attached.

    :type resource_model: :py:class:`~boto3.resources.model.ResponseResource`
    :param resource_model: Response resource model.

    :type service_context: :py:class:`~boto3.utils.ServiceContext`
    :param service_context: Context about the AWS service

    :type operation_name: string
    :param operation_name: Name of the underlying service operation, if it
                           exists.

    :rtype: ServiceResource or list
    :return: New resource instance(s).
    """
    
    def __init__(self, search_path, factory, resource_model, service_context, operation_name=None):
        self.search_path = search_path
        self.factory = factory
        self.resource_model = resource_model
        self.operation_name = operation_name
        self.service_context = service_context
    
    def __call__(self, parent, params, response):
        """
        :type parent: ServiceResource
        :param parent: The resource instance to which this action is attached.
        :type params: dict
        :param params: Request parameters sent to the service.
        :type response: dict
        :param response: Low-level operation response.
        """
        resource_name = self.resource_model.type
        json_definition = self.service_context.resource_json_definitions.get(resource_name)
        resource_cls = self.factory.load_from_definition(resource_name=resource_name, single_resource_json_definition=json_definition, service_context=self.service_context)
        raw_response = response
        search_response = None
        if self.search_path:
            search_response = jmespath.search(self.search_path, raw_response)
        identifiers = dict(build_identifiers(self.resource_model.identifiers, parent, params, raw_response))
        plural = [v for v in identifiers.values() if isinstance(v, list)]
        if plural:
            response = []
            for i in range(len(plural[0])):
                response_item = None
                if search_response:
                    response_item = search_response[i]
                response.append(self.handle_response_item(resource_cls, parent, identifiers, response_item))
        elif all_not_none(identifiers.values()):
            response = self.handle_response_item(resource_cls, parent, identifiers, search_response)
        else:
            response = None
            if self.operation_name is not None:
                response = build_empty_response(self.search_path, self.operation_name, self.service_context.service_model)
        return response
    
    def handle_response_item(self, resource_cls, parent, identifiers, resource_data):
        """
        Handles the creation of a single response item by setting
        parameters and creating the appropriate resource instance.

        :type resource_cls: ServiceResource subclass
        :param resource_cls: The resource class to instantiate.
        :type parent: ServiceResource
        :param parent: The resource instance to which this action is attached.
        :type identifiers: dict
        :param identifiers: Map of identifier names to value or values.
        :type resource_data: dict or None
        :param resource_data: Data for resource attributes.
        :rtype: ServiceResource
        :return: New resource instance.
        """
        kwargs = {'client': parent.meta.client}
        for (name, value) in identifiers.items():
            if isinstance(value, list):
                value = value.pop(0)
            kwargs[name] = value
        resource = resource_cls(**kwargs)
        if resource_data is not None:
            resource.meta.data = resource_data
        return resource


