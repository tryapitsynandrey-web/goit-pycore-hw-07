from collections import UserDict
from datetime import datetime, date
from typing import Optional, List, Any, Dict, Set
import re

from assistant_bot.utils.validators import validate_phone, normalize_phone, validate_email

class Field:
    """Base class for record fields."""
    def __init__(self, value: Any):
        self.value = value

    def __str__(self):
        return str(self.value)

class Name(Field):
    """Class for storing contact name. Mandatory field."""
    def __init__(self, value: str):
        if not value:
            raise ValueError("Name cannot be empty.")
        super().__init__(value)

class Phone(Field):
    """Class for storing phone number. Validates format."""
    def __init__(self, value: str):
        if not validate_phone(value):
            raise ValueError(f"Invalid phone number: {value}")
        super().__init__(normalize_phone(value))

class Email(Field):
    """Class for storing email address. Validates format."""
    def __init__(self, value: str):
        if not validate_email(value):
            raise ValueError(f"Invalid email: {value}")
        super().__init__(value)

class Birthday(Field):
    """Class for storing birthday. Validates format DD-MM-YYYY."""
    def __init__(self, value: str):
        try:
            self.date_obj = datetime.strptime(value, "%d-%m-%Y").date()
        except ValueError:
            raise ValueError("Invalid date format. Use DD-MM-YYYY")
        super().__init__(value)

class Record:
    """
    Class for storing contact information.
    Enforces strict encapsulation to prevent mutation hazards.
    """
    def __init__(self, name: str):
        self.name = Name(name)
        self._phones: List[Phone] = []
        self.email: Optional[Email] = None
        self.birthday: Optional[Birthday] = None
        self._notes: List[str] = []
        self._tags: List[str] = []

    # --- Properties (Read-Only Views) ---
    @property
    def phones(self) -> List[Phone]:
        """Returns a copy of the phones list to prevent direct mutation."""
        return self._phones[:]

    @property
    def notes(self) -> List[str]:
        """Returns a copy of the notes list."""
        return self._notes[:]

    @property
    def tags(self) -> List[str]:
        """Returns a copy of the tags list."""
        return self._tags[:]

    # --- Phone Management ---
    def add_phone(self, phone: str):
        # validation happens in Phone.__init__
        self._phones.append(Phone(phone))

    def remove_phone(self, phone: str):
        norm_phone = normalize_phone(phone)
        initial_len = len(self._phones)
        self._phones = [p for p in self._phones if p.value != norm_phone]
        # Verify removal happened if needed, but current logic mimics list.remove partly
        # Typically remove raises ValueError if x not in list, but here we filter.
        # Keeping existing behavior: if it's not there, nothing happens, no error?
        # Previous code: self.phones = [p for p in self.phones if p.value != norm_phone]
        # This silently ignored missing phones. Preserving behavior.

    def edit_phone(self, old_phone: str, new_phone: str):
        norm_old = normalize_phone(old_phone)
        for i, phone in enumerate(self._phones):
            if phone.value == norm_old:
                self._phones[i] = Phone(new_phone)
                return
        raise ValueError(f"Phone {old_phone} not found")

    def find_phone(self, phone: str) -> Optional[Phone]:
        norm_phone = normalize_phone(phone)
        for p in self._phones:
            if p.value == norm_phone:
                return p
        return None

    # --- Email Management ---
    def add_email(self, email: str):
        self.email = Email(email)


    # --- Birthday Management ---
    def add_birthday(self, birthday: str):
        self.birthday = Birthday(birthday)

    def days_to_birthday(self, today: Optional[date] = None) -> Optional[int]:
        """
        Calculates days until the next birthday.
        Returns:
            int: Days until birthday, or None if birthday is not set.
        """
        if not self.birthday:
            return None
        
        if today is None:
            today = date.today()

        bdate = self.birthday.date_obj
        
        # Calculate for this year
        this_year_bday = date(today.year, bdate.month, bdate.day)
        
        # If passed, move to next year
        if this_year_bday < today:
            this_year_bday = date(today.year + 1, bdate.month, bdate.day)
            
        return (this_year_bday - today).days

    # --- Notes Management ---
    def add_note(self, note: str):
        if note:
             self._notes.append(note)

    def edit_note(self, index: int, new_note: str):
        if 0 <= index < len(self._notes):
            self._notes[index] = new_note
        else:
            raise IndexError("Note index out of range")

    def remove_note(self, index: int):
        if 0 <= index < len(self._notes):
            self._notes.pop(index)
        else:
            raise IndexError("Note index out of range")

    # --- Tags Management ---
    def add_tag(self, tag: str):
        tag = self._normalize_tag(tag)
        if tag and tag not in self._tags:
            self._tags.append(tag)

    def remove_tag(self, tag: str):
        tag = self._normalize_tag(tag)
        if tag in self._tags:
            self._tags.remove(tag)

    def has_tag(self, tag: str) -> bool:
        """Checks if the record has a specific tag (case-insensitive)."""
        return self._normalize_tag(tag) in self._tags

    @staticmethod
    def _normalize_tag(tag: str) -> str:
        return tag.strip().casefold()

    def __str__(self):
        phones_str = '; '.join(p.value for p in self._phones)
        return f"Contact name: {self.name.value}, phones: {phones_str}"

class AddressBook(UserDict):
    """Class for storing and managing records."""
    
    def add_record(self, record: Record):
        self.data[record.name.value] = record

    def find(self, name: str) -> Optional[Record]:
        return self.data.get(name)

    def delete(self, name: str):
        if name in self.data:
            del self.data[name]
            return True
        return False

    def get_upcoming_birthdays(self, days: int = 7) -> List[dict]:
        """
        Finds contacts with birthdays in the upcoming 'days'.
        Returns a list of dicts: {'name': str, 'birthday': str, 'days_until': int}
        """
        upcoming = []
        today = date.today()
        
        for record in self.data.values():
            days_until = record.days_to_birthday(today)
            
            if days_until is not None and 0 <= days_until <= days:
                upcoming.append({
                    "name": record.name.value,
                    "birthday": record.birthday.value,  # type: ignore
                    "days_until": days_until
                })
                
        return sorted(upcoming, key=lambda x: x['days_until'])

    def find_by_tag(self, tag: str) -> List[str]:
        """Returns a list of contact names that have the specified tag."""
        # Delegating to Record's logic via shared normalization or just calling Record if possible
        # But Record doesn't expose generic normalization publicly easily.
        # We can reuse the same Logic or use has_tag if available.
        return [record.name.value for record in self.data.values() if record.has_tag(tag)]
        
    def get_all_tags(self) -> Dict[str, List[str]]:
        """Returns the entire tags dictionary {name: [tags]}."""
        return {name: r.tags for name, r in self.data.items() if r.tags}

    def get_unique_tags(self) -> Set[str]:
        """Returns a set of unique tags across all contacts."""
        unique_tags = set()
        for record in self.data.values():
            unique_tags.update(record.tags)
        return unique_tags

    # Helpers for global uniqueness checks
    def find_phone_global(self, phone: str) -> Optional[str]:
        norm = normalize_phone(phone)
        for record in self.data.values():
            # Accessing property which returns copy - slightly inefficient but safer
            # Optimized internal access? No, strict encapsulation preferred.
            for p in record.phones:
                if p.value == norm:
                    return record.name.value
        return None

    def find_email_global(self, email: str) -> Optional[str]:
        for record in self.data.values():
            if record.email and record.email.value == email:
                return record.name.value
        return None


