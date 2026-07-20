import os
from botocore import xform_name
from botocore.compat import OrderedDict
from botocore.docs.bcdoc.restdoc import DocumentStructure
from botocore.docs.method import document_model_driven_method
from botocore.docs.utils import DocumentedShape
from botocore.utils import get_service_module_name


class PaginatorDocumenter:
    
    def __init__(self, client, service_paginator_model, root_docs_path):
        self._client = client
        self._client_class_name = self._client.__class__.__name__
        self._service_name = self._client.meta.service_model.service_name
        self._service_paginator_model = service_paginator_model
        self._root_docs_path = root_docs_path
        self._USER_GUIDE_LINK = 'https://docs.aws.amazon.com/boto3/latest/guide/paginators.html'
    
    def document_paginators(self, section):
        """Documents the various paginators for a service

        param section: The section to write to.
        """
        section.style.h2('Paginators')
        self._add_overview(section)
        section.style.new_line()
        section.writeln('The available paginators are:')
        section.style.toctree()
        paginator_names = sorted(self._service_paginator_model._paginator_config)
        for paginator_name in paginator_names:
            section.style.tocitem(f'{self._service_name}/paginator/{paginator_name}')
            paginator_doc_structure = DocumentStructure(paginator_name, target='html')
            self._add_paginator(paginator_doc_structure, paginator_name)
            paginator_dir_path = os.path.join(self._root_docs_path, self._service_name, 'paginator')
            paginator_doc_structure.write_to_file(paginator_dir_path, paginator_name)
    
    def _add_paginator(self, section, paginator_name):
        breadcrumb_section = section.add_new_section('breadcrumb')
        breadcrumb_section.style.ref(self._client_class_name, f'../../{self._service_name}')
        breadcrumb_section.write(f' / Paginator / {paginator_name}')
        section.add_title_section(paginator_name)
        paginator_section = section.add_new_section(paginator_name)
        paginator_section.style.start_sphinx_py_class(class_name=f'{self._client_class_name}.Paginator.{paginator_name}')
        paginator_section.style.start_codeblock()
        paginator_section.style.new_line()
        paginator_section.write(f"paginator = client.get_paginator('{xform_name(paginator_name)}')")
        paginator_section.style.end_codeblock()
        paginator_section.style.new_line()
        paginator_config = self._service_paginator_model.get_paginator(paginator_name)
        document_paginate_method(section=paginator_section, paginator_name=paginator_name, event_emitter=self._client.meta.events, service_model=self._client.meta.service_model, paginator_config=paginator_config)
    
    def _add_overview(self, section):
        section.style.new_line()
        section.write('Paginators are available on a client instance via the ``get_paginator`` method. For more detailed instructions and examples on the usage of paginators, see the paginators ')
        section.style.external_link(title='user guide', link=self._USER_GUIDE_LINK)
        section.write('.')
        section.style.new_line()


def document_paginate_method(section, paginator_name, event_emitter, service_model, paginator_config, include_signature=True):
    """Documents the paginate method of a paginator

    :param section: The section to write to

    :param paginator_name: The name of the paginator. It is snake cased.

    :param event_emitter: The event emitter to use to emit events

    :param service_model: The service model

    :param paginator_config: The paginator config associated to a particular
        paginator.

    :param include_signature: Whether or not to include the signature.
        It is useful for generating docstrings.
    """
    operation_model = service_model.operation_model(paginator_name)
    pagination_config_members = OrderedDict()
    pagination_config_members['MaxItems'] = DocumentedShape(name='MaxItems', type_name='integer', documentation='<p>The total number of items to return. If the total number of items available is more than the value specified in max-items then a <code>NextToken</code> will be provided in the output that you can use to resume pagination.</p>')
    if paginator_config.get('limit_key', None):
        pagination_config_members['PageSize'] = DocumentedShape(name='PageSize', type_name='integer', documentation='<p>The size of each page.<p>')
    pagination_config_members['StartingToken'] = DocumentedShape(name='StartingToken', type_name='string', documentation='<p>A token to specify where to start paginating. This is the <code>NextToken</code> from a previous response.</p>')
    botocore_pagination_params = [DocumentedShape(name='PaginationConfig', type_name='structure', documentation='<p>A dictionary that provides parameters to control pagination.</p>', members=pagination_config_members)]
    botocore_pagination_response_params = [DocumentedShape(name='NextToken', type_name='string', documentation='<p>A token to resume pagination.</p>')]
    service_pagination_params = []
    if isinstance(paginator_config['input_token'], list):
        service_pagination_params += paginator_config['input_token']
    else:
        service_pagination_params.append(paginator_config['input_token'])
    if paginator_config.get('limit_key', None):
        service_pagination_params.append(paginator_config['limit_key'])
    service_pagination_response_params = []
    if isinstance(paginator_config['output_token'], list):
        service_pagination_response_params += paginator_config['output_token']
    else:
        service_pagination_response_params.append(paginator_config['output_token'])
    paginate_description = f'Creates an iterator that will paginate through responses from :py:meth:`{get_service_module_name(service_model)}.Client.{xform_name(paginator_name)}`.'
    document_model_driven_method(section, 'paginate', operation_model, event_emitter=event_emitter, method_description=paginate_description, example_prefix='response_iterator = paginator.paginate', include_input=botocore_pagination_params, include_output=botocore_pagination_response_params, exclude_input=service_pagination_params, exclude_output=service_pagination_response_params, include_signature=include_signature)

