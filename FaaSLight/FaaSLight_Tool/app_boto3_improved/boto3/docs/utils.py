import inspect
import jmespath

def get_resource_ignore_params(params):
    """Helper method to determine which parameters to ignore for actions

    :returns: A list of the parameter names that does not need to be
        included in a resource's method call for documentation purposes.
    """
    import custom_funtemplate
    return custom_funtemplate.rewrite_template('boto3.docs.utils.get_resource_ignore_params', 'get_resource_ignore_params(params)', {'jmespath': jmespath, 'params': params}, 1)

def is_resource_action(action_handle):
    return inspect.isfunction(action_handle)

def get_resource_public_actions(resource_class):
    import custom_funtemplate
    return custom_funtemplate.rewrite_template('boto3.docs.utils.get_resource_public_actions', 'get_resource_public_actions(resource_class)', {'inspect': inspect, 'is_resource_action': is_resource_action, 'resource_class': resource_class}, 1)

def get_identifier_values_for_example(identifier_names):
    return ','.join([f"'{identifier}'" for identifier in identifier_names])

def get_identifier_args_for_signature(identifier_names):
    return ','.join(identifier_names)

def get_identifier_description(resource_name, identifier_name):
    return f"The {resource_name}'s {identifier_name} identifier. This **must** be set."

def add_resource_type_overview(section, resource_type, description, intro_link=None):
    import custom_funtemplate
    custom_funtemplate.rewrite_template('boto3.docs.utils.add_resource_type_overview', 'add_resource_type_overview(section, resource_type, description, intro_link=None)', {'section': section, 'resource_type': resource_type, 'description': description, 'intro_link': intro_link}, 0)


class DocumentModifiedShape:
    
    def __init__(self, shape_name, new_type, new_description, new_example_value):
        self._shape_name = shape_name
        self._new_type = new_type
        self._new_description = new_description
        self._new_example_value = new_example_value
    
    def replace_documentation_for_matching_shape(self, event_name, section, **kwargs):
        if self._shape_name == section.context.get('shape'):
            self._replace_documentation(event_name, section)
        for section_name in section.available_sections:
            sub_section = section.get_section(section_name)
            if self._shape_name == sub_section.context.get('shape'):
                self._replace_documentation(event_name, sub_section)
            else:
                self.replace_documentation_for_matching_shape(event_name, sub_section)
    
    def _replace_documentation(self, event_name, section):
        if (event_name.startswith('docs.request-example') or event_name.startswith('docs.response-example')):
            section.remove_all_sections()
            section.clear_text()
            section.write(self._new_example_value)
        if (event_name.startswith('docs.request-params') or event_name.startswith('docs.response-params')):
            allowed_sections = ('param-name', 'param-documentation', 'end-structure', 'param-type', 'end-param')
            for section_name in section.available_sections:
                if section_name not in allowed_sections:
                    section.delete_section(section_name)
            description_section = section.get_section('param-documentation')
            description_section.clear_text()
            description_section.write(self._new_description)
            type_section = section.get_section('param-type')
            if type_section.getvalue().decode('utf-8').startswith(':type'):
                type_section.clear_text()
                type_section.write(f':type {section.name}: {self._new_type}')
            else:
                type_section.clear_text()
                type_section.style.italics(f'({self._new_type}) -- ')


