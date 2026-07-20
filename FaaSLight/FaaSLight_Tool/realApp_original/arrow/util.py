"""Helpful functions used internally within arrow."""

import datetime
from typing import Any, Optional, cast
from dateutil.rrule import WEEKLY, rrule
from arrow.constants import MAX_ORDINAL, MAX_TIMESTAMP, MAX_TIMESTAMP_MS, MAX_TIMESTAMP_US, MIN_ORDINAL

def next_weekday(start_date: Optional[datetime.date], weekday: int) -> datetime.datetime:
    """Get next weekday from the specified start date.

    :param start_date: Datetime object representing the start date.
    :param weekday: Next weekday to obtain. Can be a value between 0 (Monday) and 6 (Sunday).
    :return: Datetime object corresponding to the next weekday after start_date.

    Usage::

        # Get first Monday after epoch
        >>> next_weekday(datetime(1970, 1, 1), 0)
        1970-01-05 00:00:00

        # Get first Thursday after epoch
        >>> next_weekday(datetime(1970, 1, 1), 3)
        1970-01-01 00:00:00

        # Get first Sunday after epoch
        >>> next_weekday(datetime(1970, 1, 1), 6)
        1970-01-04 00:00:00
    """
    import custom_funtemplate
    return custom_funtemplate.rewrite_template('arrow.util.next_weekday', 'next_weekday(start_date, weekday)', {'datetime': datetime, 'rrule': rrule, 'WEEKLY': WEEKLY, 'start_date': start_date, 'weekday': weekday, 'Optional': Optional, 'datetime': datetime, 'datetime': datetime}, 1)

def is_timestamp(value: Any) -> bool:
    """Check if value is a valid timestamp."""
    import custom_funtemplate
    return custom_funtemplate.rewrite_template('arrow.util.is_timestamp', 'is_timestamp(value)', {'value': value}, 1)

def validate_ordinal(value: Any) -> None:
    """Raise an exception if value is an invalid Gregorian ordinal.

    :param value: the input to be checked

    """
    import custom_funtemplate
    custom_funtemplate.rewrite_template('arrow.util.validate_ordinal', 'validate_ordinal(value)', {'MIN_ORDINAL': MIN_ORDINAL, 'MAX_ORDINAL': MAX_ORDINAL, 'value': value}, 0)

def normalize_timestamp(timestamp: float) -> float:
    """Normalize millisecond and microsecond timestamps into normal timestamps."""
    import custom_funtemplate
    return custom_funtemplate.rewrite_template('arrow.util.normalize_timestamp', 'normalize_timestamp(timestamp)', {'MAX_TIMESTAMP': MAX_TIMESTAMP, 'MAX_TIMESTAMP_MS': MAX_TIMESTAMP_MS, 'MAX_TIMESTAMP_US': MAX_TIMESTAMP_US, 'timestamp': timestamp}, 1)

def iso_to_gregorian(iso_year: int, iso_week: int, iso_day: int) -> datetime.date:
    """Converts an ISO week date into a datetime object.

    :param iso_year: the year
    :param iso_week: the week number, each year has either 52 or 53 weeks
    :param iso_day: the day numbered 1 through 7, beginning with Monday

    """
    import custom_funtemplate
    return custom_funtemplate.rewrite_template('arrow.util.iso_to_gregorian', 'iso_to_gregorian(iso_year, iso_week, iso_day)', {'datetime': datetime, 'iso_year': iso_year, 'iso_week': iso_week, 'iso_day': iso_day, 'datetime': datetime}, 1)

def validate_bounds(bounds: str) -> None:
    if (bounds != '()' and bounds != '(]' and bounds != '[)' and bounds != '[]'):
        raise ValueError("Invalid bounds. Please select between '()', '(]', '[)', or '[]'.")
__all__ = ['next_weekday', 'is_timestamp', 'validate_ordinal', 'iso_to_gregorian']

