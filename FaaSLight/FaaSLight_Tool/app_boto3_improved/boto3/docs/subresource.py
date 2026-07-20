import os
from botocore import xform_name
from botocore.docs.bcdoc.restdoc import DocumentStructure
from botocore.utils import get_service_module_name
from boto3.docs.base import NestedDocumenter
from boto3.docs.utils import add_resource_type_overview, get_identifier_args_for_signature, get_identifier_description, get_identifier_values_for_example


class SubResourceDocumenter(NestedDocumenter):
    
    def document_sub_resources(self, section):
        add_resource_type_overview(section=section, resource_type='Sub-resources', description="Sub-resources are methods that create a new instance of a child resource. This resource's identifiers get passed along to the child.", intro_link='subresources_intro')
        sub_resources = sorted(self._resource.meta.resource_model.subresources, key=lambda sub_resource: sub_resource.name)
        sub_resources_list = []
        self.member_map['sub-resources'] = sub_resources_list
        for sub_resource in sub_resources:
            sub_resources_list.append(sub_resource.name)
            sub_resource_doc = DocumentStructure(sub_resource.name, target='html')
            breadcrumb_section = sub_resource_doc.add_new_section('breadcrumb')
            breadcrumb_section.style.ref(self._resource_class_name, 'index')
            breadcrumb_section.write(f' / Sub-Resource / {sub_resource.name}')
            sub_resource_doc.add_title_section(sub_resource.name)
            sub_resource_section = sub_resource_doc.add_new_section(sub_resource.name, context={'qualifier': f'{self.class_name}.'})
            document_sub_resource(section=sub_resource_section, resource_name=self._resource_name, sub_resource_model=sub_resource, service_model=self._service_model)
            sub_resources_dir_path = os.path.join(self._root_docs_path, f'{self._service_name}', f'{self._resource_sub_path}')
            sub_resource_doc.write_to_file(sub_resources_dir_path, sub_resource.name)


def document_sub_resource(section, resource_name, sub_resource_model, service_model, include_signature=True):
    """Documents a resource action

    :param section: The section to write to

    :param resource_name: The name of the resource

    :param sub_resource_model: The model of the subresource

    :param service_model: The model of the service

    :param include_signature: Whether or not to include the signature.
        It is useful for generating docstrings.
    """
    import custom_funtemplate
    custom_funtemplate.rewrite_template('boto3.docs.subresource.document_sub_resource', 'document_sub_resource(section, resource_name, sub_resource_model, service_model, include_signature=True)', {'xform_name': xform_name, 'get_identifier_args_for_signature': get_identifier_args_for_signature, 'get_identifier_values_for_example': get_identifier_values_for_example, 'get_identifier_description': get_identifier_description, 'get_service_module_name': get_service_module_name, 'section': section, 'resource_name': resource_name, 'sub_resource_model': sub_resource_model, 'service_model': service_model, 'include_signature': include_signature}, 0)

