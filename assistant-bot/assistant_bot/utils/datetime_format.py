from datetime import datetime

FORMAT = "%d-%m-%Y %H:%M"
SHORT_DATE = "%d-%m-%Y"


def parse_datetime_str(s: str) -> datetime:
    # Accept either full or date-only strings. For date-only, set time to 00:00.
    s = s.strip()
    if not s:
        raise ValueError('Empty date')
    try:
        return datetime.strptime(s, FORMAT)
    except ValueError:
        return datetime.strptime(s, SHORT_DATE)


def format_datetime(dt: datetime) -> str:
    return dt.strftime(FORMAT)


__all__ = ['parse_datetime_str', 'format_datetime', 'FORMAT', 'SHORT_DATE']
