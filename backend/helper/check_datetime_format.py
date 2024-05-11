from datetime import datetime


def validate_datetime_format(date_string):
    try:
        datetime.strptime(date_string, '%Y-%m-%dT%H:%M:%S.%fZ')
        return True
    except ValueError as e:
        return False
