import arrow

def lambda_handler(event, context):
    current = arrow.now()
    utc = arrow.utcnow()
    formatted = current.format('YYYY-MM-DD HH:mm:ss')
    human = current.humanize()
    shifted = current.shift(hours=+1)
    return {'statusCode': 200, 'body': {'current': formatted, 'utc': str(utc), 'human': human, 'shifted': str(shifted)}}

