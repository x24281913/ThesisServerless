import os
from botocore import xform_name
from botocore.docs.bcdoc.restdoc import DocumentStructure
from botocore.docs.method import get_instance_public_methods
from botocore.docs.utils import DocumentedShape
from boto3.docs.base import NestedDocumenter
from boto3.docs.method import document_model_driven_resource_method
from boto3.docs.utils import add_resource_type_overview, get_resource_ignore_params


class CollectionDocumenter(NestedDocumenter):
    
    def document_collections(self, section):
        collections = self._resource.meta.resource_model.collections
        collections_list = []
        add_resource_type_overview(section=section, resource_type='Collections', description='Collections provide an interface to iterate over and manipulate groups of resources. ', intro_link='guide_collections')
        self.member_map['collections'] = collections_list
        for collection in collections:
            collections_list.append(collection.name)
            collection_doc = DocumentStructure(collection.name, target='html')
            breadcrumb_section = collection_doc.add_new_section('breadcrumb')
            breadcrumb_section.style.ref(self._resource_class_name, 'index')
            breadcrumb_section.write(f' / Collection / {collection.name}')
            collection_doc.add_title_section(collection.name)
            collection_section = collection_doc.add_new_section(collection.name, context={'qualifier': f'{self.class_name}.'})
            self._document_collection(collection_section, collection)
            collections_dir_path = os.path.join(self._root_docs_path, f'{self._service_name}', f'{self._resource_sub_path}')
            collection_doc.write_to_file(collections_dir_path, collection.name)
    
    def _document_collection(self, section, collection):
        methods = get_instance_public_methods(getattr(self._resource, collection.name))
        document_collection_object(section, collection)
        batch_actions = {}
        for batch_action in collection.batch_actions:
            batch_actions[batch_action.name] = batch_action
        for method in sorted(methods):
            method_section = section.add_new_section(method)
            if method in batch_actions:
                document_batch_action(section=method_section, resource_name=self._resource_name, event_emitter=self._resource.meta.client.meta.events, batch_action_model=batch_actions[method], collection_model=collection, service_model=self._resource.meta.client.meta.service_model)
            else:
                document_collection_method(section=method_section, resource_name=self._resource_name, action_name=method, event_emitter=self._resource.meta.client.meta.events, collection_model=collection, service_model=self._resource.meta.client.meta.service_model)


def document_collection_object(section, collection_model, include_signature=True):
    """Documents a collection resource object

    :param section: The section to write to

    :param collection_model: The model of the collection

    :param include_signature: Whether or not to include the signature.
        It is useful for generating docstrings.
    """
    import custom_funtemplate
    custom_funtemplate.rewrite_template('boto3.docs.collection.document_collection_object', 'document_collection_object(section, collection_model, include_signature=True)', {'section': section, 'collection_model': collection_model, 'include_signature': include_signature}, 0)

def document_batch_action(section, resource_name, event_emitter, batch_action_model, service_model, collection_model, include_signature=True):
    """Documents a collection's batch action

    :param section: The section to write to

    :param resource_name: The name of the resource

    :param action_name: The name of collection action. Currently only
        can be all, filter, limit, or page_size

    :param event_emitter: The event emitter to use to emit events

    :param batch_action_model: The model of the batch action

    :param collection_model: The model of the collection

    :param service_model: The model of the service

    :param include_signature: Whether or not to include the signature.
        It is useful for generating docstrings.
    """
    import custom_funtemplate
    custom_funtemplate.rewrite_template('boto3.docs.collection.document_batch_action', 'document_batch_action(section, resource_name, event_emitter, batch_action_model, service_model, collection_model, include_signature=True)', {'get_resource_ignore_params': get_resource_ignore_params, 'xform_name': xform_name, 'document_model_driven_resource_method': document_model_driven_resource_method, 'section': section, 'resource_name': resource_name, 'event_emitter': event_emitter, 'batch_action_model': batch_action_model, 'service_model': service_model, 'collection_model': collection_model, 'include_signature': include_signature}, 0)

def document_collection_method(section, resource_name, action_name, event_emitter, collection_model, service_model, include_signature=True):
    """Documents a collection method

    :param section: The section to write to

    :param resource_name: The name of the resource

    :param action_name: The name of collection action. Currently only
        can be all, filter, limit, or page_size

    :param event_emitter: The event emitter to use to emit events

    :param collection_model: The model of the collection

    :param service_model: The model of the service

    :param include_signature: Whether or not to include the signature.
        It is useful for generating docstrings.
    """
    import custom_funtemplate
    custom_funtemplate.rewrite_template('boto3.docs.collection.document_collection_method', 'document_collection_method(section, resource_name, action_name, event_emitter, collection_model, service_model, include_signature=True)', {'xform_name': xform_name, 'get_resource_ignore_params': get_resource_ignore_params, 'DocumentedShape': DocumentedShape, 'document_model_driven_resource_method': document_model_driven_resource_method, 'section': section, 'resource_name': resource_name, 'action_name': action_name, 'event_emitter': event_emitter, 'collection_model': collection_model, 'service_model': service_model, 'include_signature': include_signature}, 0)

