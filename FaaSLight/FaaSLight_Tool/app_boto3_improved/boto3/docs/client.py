from botocore.docs.client import ClientDocumenter


class Boto3ClientDocumenter(ClientDocumenter):
    
    def _add_client_creation_example(self, section):
        section.style.start_codeblock()
        section.style.new_line()
        section.write('import boto3')
        section.style.new_line()
        section.style.new_line()
        section.write(f"client = boto3.client('{self._service_name}')")
        section.style.end_codeblock()


