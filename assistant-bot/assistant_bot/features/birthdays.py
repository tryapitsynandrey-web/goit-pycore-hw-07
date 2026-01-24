from datetime import datetime, date
from assistant_bot.utils.datetime_format import parse_datetime_str


def get_days_from_today(target_date: date) -> int:
    today = date.today()
    delta = target_date - today
    return delta.days


def _parse_birthdate_str(birthdate_str: str) -> date:
    # expect DD-MM-YYYY
    dt = parse_datetime_str(birthdate_str)
    return dt.date()


def days_until_birthday(birthdate_str: str) -> int:
    try:
        bdate = _parse_birthdate_str(birthdate_str)
    except Exception:
        raise ValueError('Invalid date format')

    today = date.today()
    this_year_bday = date(today.year, bdate.month, bdate.day)
    if this_year_bday < today:
        this_year_bday = date(today.year + 1, bdate.month, bdate.day)
    return (this_year_bday - today).days


def get_upcoming_birthdays(contacts: dict, days: int = 7) -> list:
    upcoming = []
    today = date.today()
    
    for name, data in contacts.items():
        bday_str = data.get('birthday')
        if not bday_str:
            continue
        try:
            bdate = _parse_birthdate_str(bday_str)
            this_year_bday = date(today.year, bdate.month, bdate.day)
            
            if this_year_bday < today:
                this_year_bday = date(today.year + 1, bdate.month, bdate.day)
            
            delta = (this_year_bday - today).days
            
            if 0 <= delta <= days:
                upcoming.append({"name": name, "birthday": bday_str, "days_until": delta})
        except Exception:
            continue
            
    return sorted(upcoming, key=lambda x: x['days_until'])


__all__ = ['get_days_from_today', 'days_until_birthday', 'get_upcoming_birthdays']
