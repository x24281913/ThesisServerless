import json
import boto3

BUCKET = 'thesis-faaslight-results'
REGION = 'us-east-1'


def lambda_handler(event, context):
    headers = {
        'Access-Control-Allow-Origin': '*',
        'Content-Type': 'application/json'
    }

    path = event.get('path', '/')

    try:
        s3 = boto3.client('s3', region_name=REGION)

        # GET /coldstart
        if path == '/coldstart':
            obj = s3.get_object(
                Bucket=BUCKET,
                Key='lambda_coldstart_results.json')
            data = json.loads(obj['Body'].read())
            return {
                'statusCode': 200,
                'headers': headers,
                'body': json.dumps(data)
            }

        # GET /results
        all_results = []
        response = s3.list_objects_v2(Bucket=BUCKET)
        for obj in response.get('Contents', []):
            key = obj['Key']
            if key.endswith('_result.json'):
                file_obj = s3.get_object(
                    Bucket=BUCKET, Key=key)
                data = json.loads(
                    file_obj['Body'].read())
                all_results.append(data)

        return {
            'statusCode': 200,
            'headers': headers,
            'body': json.dumps(all_results)
        }

    except Exception as e:
        return {
            'statusCode': 500,
            'headers': headers,
            'body': json.dumps({'error': str(e)})
        }