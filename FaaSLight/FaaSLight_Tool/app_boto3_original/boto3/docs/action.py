import os
from botocore import xform_name
from botocore.docs.bcdoc.restdoc import DocumentStructure
from botocore.docs.method import document_custom_method, document_model_driven_method
from botocore.model import OperationModel
from botocore.utils import get_service_module_name
from boto3.docs.base import NestedDocumenter
from boto3.docs.method import document_model_driven_resource_method
from boto3.docs.utils import add_resource_type_overview, get_resource_ignore_params, get_resource_public_actions
PUT_DATA_WARNING_MESSAGE = "\n.. warning::\n    It is recommended to use the :py:meth:`put_metric_data`\n    :doc:`client method <../../cloudwatch/client/put_metric_data>`\n    instead. If you would still like to use this resource method,\n    please make sure that ``MetricData[].MetricName`` is equal to\n    the metric resource's ``name`` attribute.\n"
WARNING_MESSAGES = {'Metric': {'put_data': PUT_DATA_WARNING_MESSAGE}}
IGNORE_PARAMS = {'Metric': {'put_data': ['Namespace']}}


class ActionDocumenter(NestedDocumenter):
    
    def document_actions(self, section):
        modeled_actions_list = self._resource_model.actions
        modeled_actions = {}
        for modeled_action in modeled_actions_list:
            modeled_actions[modeled_action.name] = modeled_action
        resource_actions = get_resource_public_actions(self._resource.__class__)
        self.member_map['actions'] = sorted(resource_actions)
        add_resource_type_overview(section=section, resource_type='Actions', description='Actions call operations on resources.  They may automatically handle the passing in of arguments set from identifiers and some attributes.', intro_link='actions_intro')
        resource_warnings = WARNING_MESSAGES.get(self._resource_name, {})
        for action_name in sorted(resource_actions):
            action_doc = DocumentStructure(action_name, target='html')
            breadcrumb_section = action_doc.add_new_section('breadcrumb')
            breadcrumb_section.style.ref(self._resource_class_name, 'index')
            breadcrumb_section.write(f' / Action / {action_name}')
            action_doc.add_title_section(action_name)
            warning_message = resource_warnings.get(action_name)
            if warning_message is not None:
                action_doc.add_new_section('warning').write(warning_message)
            action_section = action_doc.add_new_section(action_name, context={'qualifier': f'{self.class_name}.'})
            if (action_name in ['load', 'reload'] and self._resource_model.load):
                document_load_reload_action(section=action_section, action_name=action_name, resource_name=self._resource_name, event_emitter=self._resource.meta.client.meta.events, load_model=self._resource_model.load, service_model=self._service_model)
            elif action_name in modeled_actions:
                document_action(section=action_section, resource_name=self._resource_name, event_emitter=self._resource.meta.client.meta.events, action_model=modeled_actions[action_name], service_model=self._service_model)
            else:
                document_custom_method(action_section, action_name, resource_actions[action_name])
            actions_dir_path = os.path.join(self._root_docs_path, f'{self._service_name}', f'{self._resource_sub_path}')
            action_doc.write_to_file(actions_dir_path, action_name)


def document_action(section, resource_name, event_emitter, action_model, service_model, include_signature=True):
    """Documents a resource action

    :param section: The section to write to

    :param resource_name: The name of the resource

    :param event_emitter: The event emitter to use to emit events

    :param action_model: The model of the action

    :param service_model: The model of the service

    :param include_signature: Whether or not to include the signature.
        It is useful for generating docstrings.
    """
    import custom_funtemplate
    custom_funtemplate.rewrite_template('boto3.docs.action.document_action', 'document_action(section, resource_name, event_emitter, action_model, service_model, include_signature=True)', {'IGNORE_PARAMS': IGNORE_PARAMS, 'get_resource_ignore_params': get_resource_ignore_params, 'xform_name': xform_name, 'document_model_driven_resource_method': document_model_driven_resource_method, 'section': section, 'resource_name': resource_name, 'event_emitter': event_emitter, 'action_model': action_model, 'service_model': service_model, 'include_signature': include_signature}, 0)

def document_load_reload_action(section, action_name, resource_name, event_emitter, load_model, service_model, include_signature=True):
    """Documents the resource load action

    :param section: The section to write to

    :param action_name: The name of the loading action should be load or reload

    :param resource_name: The name of the resource

    :param event_emitter: The event emitter to use to emit events

    :param load_model: The model of the load action

    :param service_model: The model of the service

    :param include_signature: Whether or not to include the signature.
        It is useful for generating docstrings.
    """
    import custom_funtemplate
    custom_funtemplate.rewrite_template('boto3.docs.action.document_load_reload_action', 'document_load_reload_action(section, action_name, resource_name, event_emitter, load_model, service_model, include_signature=True)', {'get_service_module_name': get_service_module_name, 'xform_name': xform_name, 'document_model_driven_method': document_model_driven_method, 'OperationModel': OperationModel, 'section': section, 'action_name': action_name, 'resource_name': resource_name, 'event_emitter': event_emitter, 'load_model': load_model, 'service_model': service_model, 'include_signature': include_signature}, 0)

