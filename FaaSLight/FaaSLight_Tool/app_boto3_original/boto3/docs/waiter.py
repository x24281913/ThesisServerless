import os
from botocore import xform_name
from botocore.docs.bcdoc.restdoc import DocumentStructure
from botocore.docs.method import document_model_driven_method
from botocore.utils import get_service_module_name
from boto3.docs.base import NestedDocumenter
from boto3.docs.utils import add_resource_type_overview, get_resource_ignore_params


class WaiterResourceDocumenter(NestedDocumenter):
    
    def __init__(self, resource, service_waiter_model, root_docs_path):
        super().__init__(resource, root_docs_path)
        self._service_waiter_model = service_waiter_model
    
    def document_resource_waiters(self, section):
        waiters = self._resource.meta.resource_model.waiters
        add_resource_type_overview(section=section, resource_type='Waiters', description='Waiters provide an interface to wait for a resource to reach a specific state.', intro_link='waiters_intro')
        waiter_list = []
        self.member_map['waiters'] = waiter_list
        for waiter in waiters:
            waiter_list.append(waiter.name)
            waiter_doc = DocumentStructure(waiter.name, target='html')
            breadcrumb_section = waiter_doc.add_new_section('breadcrumb')
            breadcrumb_section.style.ref(self._resource_class_name, 'index')
            breadcrumb_section.write(f' / Waiter / {waiter.name}')
            waiter_doc.add_title_section(waiter.name)
            waiter_section = waiter_doc.add_new_section(waiter.name, context={'qualifier': f'{self.class_name}.'})
            document_resource_waiter(section=waiter_section, resource_name=self._resource_name, event_emitter=self._resource.meta.client.meta.events, service_model=self._service_model, resource_waiter_model=waiter, service_waiter_model=self._service_waiter_model)
            waiters_dir_path = os.path.join(self._root_docs_path, f'{self._service_name}', f'{self._resource_sub_path}')
            waiter_doc.write_to_file(waiters_dir_path, waiter.name)


def document_resource_waiter(section, resource_name, event_emitter, service_model, resource_waiter_model, service_waiter_model, include_signature=True):
    import custom_funtemplate
    custom_funtemplate.rewrite_template('boto3.docs.waiter.document_resource_waiter', 'document_resource_waiter(section, resource_name, event_emitter, service_model, resource_waiter_model, service_waiter_model, include_signature=True)', {'get_resource_ignore_params': get_resource_ignore_params, 'get_service_module_name': get_service_module_name, 'xform_name': xform_name, 'document_model_driven_method': document_model_driven_method, 'section': section, 'resource_name': resource_name, 'event_emitter': event_emitter, 'service_model': service_model, 'resource_waiter_model': resource_waiter_model, 'service_waiter_model': service_waiter_model, 'include_signature': include_signature}, 0)

