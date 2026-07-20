from dateutil import parser
from dateutil import tz
from dateutil import relativedelta
from dateutil import easter
from dateutil import rrule
from dateutil.relativedelta import relativedelta as rd

def lambda_handler(event, context):
    date_str = event.get('date', '2026-07-01 12:00:00')
    parsed = parser.parse(date_str)
    utc_zone = tz.tzutc()
    local_zone = tz.tzlocal()
    delta = rd(months=1, days=5)
    new_date = parsed + delta
    easter_date = easter.easter(2026)
    utc_date = parsed.astimezone(utc_zone)
    return {
        'statusCode': 200,
        'body': {
            'parsed': str(parsed),
            'new_date': str(new_date),
            'easter': str(easter_date),
            'utc': str(utc_date)
        }
    }
