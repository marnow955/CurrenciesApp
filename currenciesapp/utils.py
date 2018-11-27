from datetime import datetime


def validate_date(date_str: str, pattern: str):
    try:
        datetime.strptime(date_str, pattern)
        return True
    except ValueError:
        return False
