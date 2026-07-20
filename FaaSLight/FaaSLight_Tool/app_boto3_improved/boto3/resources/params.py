import re
import jmespath
from botocore import xform_name
from ..exceptions import ResourceLoadException
INDEX_RE = re.compile('\\[(.*)\\]$')

def get_data_member(parent, path):
    """
    Get a data member from a parent using a JMESPath search query,
    loading the parent if required. If the parent cannot be loaded
    and no data is present then an exception is raised.

    :type parent: ServiceResource
    :param parent: The resource instance to which contains data we
                   are interested in.
    :type path: string
    :param path: The JMESPath expression to query
    :raises ResourceLoadException: When no data is present and the
                                   resource cannot be loaded.
    :returns: The queried data or ``None``.
    """
    if parent.meta.data is None:
        if hasattr(parent, 'load'):
            parent.load()
        else:
            raise ResourceLoadException(f'{parent.__class__.__name__} has no load method!')
    return jmespath.search(path, parent.meta.data)

def create_request_parameters(parent, request_model, params=None, index=None):
    """
    Handle request parameters that can be filled in from identifiers,
    resource data members or constants.

    By passing ``params``, you can invoke this method multiple times and
    build up a parameter dict over time, which is particularly useful
    for reverse JMESPath expressions that append to lists.

    :type parent: ServiceResource
    :param parent: The resource instance to which this action is attached.
    :type request_model: :py:class:`~boto3.resources.model.Request`
    :param request_model: The action request model.
    :type params: dict
    :param params: If set, then add to this existing dict. It is both
                   edited in-place and returned.
    :type index: int
    :param index: The position of an item within a list
    :rtype: dict
    :return: Pre-filled parameters to be sent to the request operation.
    """
    if params is None:
        params = {}
    for param in request_model.params:
        source = param.source
        target = param.target
        if source == 'identifier':
            value = getattr(parent, xform_name(param.name))
        elif source == 'data':
            value = get_data_member(parent, param.path)
        elif source in ['string', 'integer', 'boolean']:
            value = param.value
        elif source == 'input':
            continue
        else:
            raise NotImplementedError(f'Unsupported source type: {source}')
        build_param_structure(params, target, value, index)
    return params

def build_param_structure(params, target, value, index=None):
    """
    This method provides a basic reverse JMESPath implementation that
    lets you go from a JMESPath-like string to a possibly deeply nested
    object. The ``params`` are mutated in-place, so subsequent calls
    can modify the same element by its index.

        >>> build_param_structure(params, 'test[0]', 1)
        >>> print(params)
        {'test': [1]}

        >>> build_param_structure(params, 'foo.bar[0].baz', 'hello world')
        >>> print(params)
        {'test': [1], 'foo': {'bar': [{'baz': 'hello, world'}]}}

    """
    pos = params
    parts = target.split('.')
    for (i, part) in enumerate(parts):
        result = INDEX_RE.search(part)
        if result:
            if result.group(1):
                if result.group(1) == '*':
                    part = part[:-3]
                else:
                    index = int(result.group(1))
                    part = part[:-len(f'{index}[]')]
            else:
                index = None
                part = part[:-2]
            if (part not in pos or not isinstance(pos[part], list)):
                pos[part] = []
            if index is None:
                index = len(pos[part])
            while len(pos[part]) <= index:
                pos[part].append({})
            if i == len(parts) - 1:
                pos[part][index] = value
            else:
                pos = pos[part][index]
        else:
            if part not in pos:
                pos[part] = {}
            if i == len(parts) - 1:
                pos[part] = value
            else:
                pos = pos[part]

