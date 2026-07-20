import os
from botocore.docs import DEPRECATED_SERVICE_NAMES
from boto3.docs.service import ServiceDocumenter

def generate_docs(root_dir, session):
    """Generates the reference documentation for botocore

    This will go through every available AWS service and output ReSTructured
    text files documenting each service.

    :param root_dir: The directory to write the reference files to. Each
        service's reference documentation is located at
        root_dir/reference/services/service-name.rst

    :param session: The boto3 session
    """
    import custom_funtemplate
    custom_funtemplate.rewrite_template('boto3.docs.__init__.generate_docs', 'generate_docs(root_dir, session)', {'os': os, 'DEPRECATED_SERVICE_NAMES': DEPRECATED_SERVICE_NAMES, 'ServiceDocumenter': ServiceDocumenter, 'root_dir': root_dir, 'session': session}, 0)

