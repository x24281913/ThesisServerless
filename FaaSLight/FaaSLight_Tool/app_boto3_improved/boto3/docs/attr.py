from botocore.docs.params import ResponseParamsDocumenter
from boto3.docs.utils import get_identifier_description


class ResourceShapeDocumenter(ResponseParamsDocumenter):
    EVENT_NAME = 'resource-shape'


def document_attribute(section, service_name, resource_name, attr_name, event_emitter, attr_model, include_signature=True):
    import custom_funtemplate
    custom_funtemplate.rewrite_template('boto3.docs.attr.document_attribute', 'document_attribute(section, service_name, resource_name, attr_name, event_emitter, attr_model, include_signature=True)', {'ResourceShapeDocumenter': ResourceShapeDocumenter, 'section': section, 'service_name': service_name, 'resource_name': resource_name, 'attr_name': attr_name, 'event_emitter': event_emitter, 'attr_model': attr_model, 'include_signature': include_signature}, 0)

def document_identifier(section, resource_name, identifier_model, include_signature=True):
    import custom_funtemplate
    custom_funtemplate.rewrite_template('boto3.docs.attr.document_identifier', 'document_identifier(section, resource_name, identifier_model, include_signature=True)', {'get_identifier_description': get_identifier_description, 'section': section, 'resource_name': resource_name, 'identifier_model': identifier_model, 'include_signature': include_signature}, 0)

def document_reference(section, reference_model, include_signature=True):
    import custom_funtemplate
    custom_funtemplate.rewrite_template('boto3.docs.attr.document_reference', 'document_reference(section, reference_model, include_signature=True)', {'section': section, 'reference_model': reference_model, 'include_signature': include_signature}, 0)

