import copy
from botocore.utils import merge_dicts

def build_retry_config(endpoint_prefix, retry_model, definitions, client_retry_config=None):
    service_config = retry_model.get(endpoint_prefix, {})
    resolve_references(service_config, definitions)
    final_retry_config = {'__default__': copy.deepcopy(retry_model.get('__default__', {}))}
    resolve_references(final_retry_config, definitions)
    merge_dicts(final_retry_config, service_config)
    if client_retry_config is not None:
        _merge_client_retry_config(final_retry_config, client_retry_config)
    return final_retry_config

def _merge_client_retry_config(retry_config, client_retry_config):
    max_retry_attempts_override = client_retry_config.get('max_attempts')
    if max_retry_attempts_override is not None:
        retry_config['__default__']['max_attempts'] = max_retry_attempts_override + 1

def resolve_references(config, definitions):
    """Recursively replace $ref keys.

    To cut down on duplication, common definitions can be declared
    (and passed in via the ``definitions`` attribute) and then
    references as {"$ref": "name"}, when this happens the reference
    dict is placed with the value from the ``definition`` dict.

    This is recursively done.

    """
    for (key, value) in config.items():
        if isinstance(value, dict):
            if (len(value) == 1 and list(value.keys())[0] == '$ref'):
                config[key] = definitions[list(value.values())[0]]
            else:
                resolve_references(value, definitions)

