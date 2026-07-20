import boto3
import json
from botocore.exceptions import ClientError
from boto3.session import Session

def lambda_handler(event, context):
    session = Session()
    client = session.client(
        service_name='s3',
        region_name='us-east-1'
    )
    bucket_name = event.get('bucket', 'my-bucket')
    key = event.get('key', 'test.txt')
    return {
        'statusCode': 200,
        'body': {
            'bucket': bucket_name,
            'key': key,
            'region': 'us-east-1'
        }
    }
