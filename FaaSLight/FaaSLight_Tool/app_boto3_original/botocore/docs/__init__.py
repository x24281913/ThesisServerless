import os
from botocore.docs.service import ServiceDocumenter
DEPRECATED_SERVICE_NAMES = {'sms-voice'}

def generate_docs(root_dir, session):
    """Generates the reference documentation for botocore

    This will go through every available AWS service and output ReSTructured
    text files documenting each service.

    :param root_dir: The directory to write the reference files to. Each
        service's reference documentation is loacated at
        root_dir/reference/services/service-name.rst
    """
    services_dir_path = os.path.join(root_dir, 'reference', 'services')
    if not os.path.exists(services_dir_path):
        os.makedirs(services_dir_path)
    available_services = [service for service in session.get_available_services() if service not in DEPRECATED_SERVICE_NAMES]
    for service_name in available_services:
        docs = ServiceDocumenter(service_name, session, services_dir_path).document_service()
        service_file_path = os.path.join(services_dir_path, f'{service_name}.rst')
        with open(service_file_path, 'wb') as f:
            f.write(docs)

