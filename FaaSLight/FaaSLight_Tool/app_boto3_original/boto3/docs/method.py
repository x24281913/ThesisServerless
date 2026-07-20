from botocore.docs.method import document_model_driven_method

def document_model_driven_resource_method(section, method_name, operation_model, event_emitter, method_description=None, example_prefix=None, include_input=None, include_output=None, exclude_input=None, exclude_output=None, document_output=True, resource_action_model=None, include_signature=True):
    import custom_funtemplate
    custom_funtemplate.rewrite_template('boto3.docs.method.document_model_driven_resource_method', 'document_model_driven_resource_method(section, method_name, operation_model, event_emitter, method_description=None, example_prefix=None, include_input=None, include_output=None, exclude_input=None, exclude_output=None, document_output=True, resource_action_model=None, include_signature=True)', {'document_model_driven_method': document_model_driven_method, '_method_returns_resource_list': _method_returns_resource_list, 'section': section, 'method_name': method_name, 'operation_model': operation_model, 'event_emitter': event_emitter, 'method_description': method_description, 'example_prefix': example_prefix, 'include_input': include_input, 'include_output': include_output, 'exclude_input': exclude_input, 'exclude_output': exclude_output, 'document_output': document_output, 'resource_action_model': resource_action_model, 'include_signature': include_signature}, 0)

def _method_returns_resource_list(resource):
    import custom_funtemplate
    return custom_funtemplate.rewrite_template('boto3.docs.method._method_returns_resource_list', '_method_returns_resource_list(resource)', {'resource': resource}, 1)

