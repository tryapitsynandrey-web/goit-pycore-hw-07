import os
import json
from typing import Dict, Any, List

from assistant_bot.config import JSON_STORAGE_PATH, CSV_STORAGE_PATH, DATA_DIR
from assistant_bot.models import AddressBook, Record
from assistant_bot.utils.console import print_info

def load_address_book() -> AddressBook:
    """
    Loads data from JSON storage.
    Handles migration from legacy dict-based format to OOP Record format.
    """
    os.makedirs(DATA_DIR, exist_ok=True)
    book = AddressBook()
    
    if not os.path.exists(JSON_STORAGE_PATH):
        return book

    try:
        with open(JSON_STORAGE_PATH, 'r', encoding='utf-8') as f:
            raw_data = json.load(f)

        # Check for legacy format (dict with 'contacts' key) vs new format (dict of records)
        # We assume the new format will simply be the UserDict dump (keys are names, values are dicts of record data)
        # But wait, UserDict serialization usually requires custom encoding/decoding. 
        # We will standardize on saving a DICT where keys=names, values=Record.to_dict() equivalent.
        
        # Scenario 1: Legacy Format (Previous Refactor)
        # Structure was {name: {phones:[], email:..., notes:[], tags:[]}} (from the recent refactor)
        # Or even older: {contacts:{}, notes:{}, tags:{}} (from the very first version)
        
        # Let's handle the most recent "clean JSON" format we created:
        # { "Bob": { "phones": [...], "email": "...", "notes": [...], "tags": [...] } }
        
        if isinstance(raw_data, dict):
             for name, data in raw_data.items():
                 # Handle potentially mixed formats if any
                 if not isinstance(data, dict):
                     continue
                 
                 try:
                     record = Record(name)
                     
                     # Phones
                     for p in data.get('phones', []):
                         record.add_phone(p)
                         
                     # Email
                     email = data.get('email')
                     if email:
                         record.add_email(email)
                         
                     # Birthday
                     bday = data.get('birthday')
                     if bday:
                         record.add_birthday(bday)
                         
                     # Notes (Supported from both flat record and split architecture)
                     notes = data.get('notes', [])
                     for n in notes:
                         record.add_note(n)
                         
                     # Tags
                     tags = data.get('tags', [])
                     for t in tags:
                         record.add_tag(t)
                         
                     book.add_record(record)
                 except ValueError as e:
                     print(f"Skipping invalid record '{name}': {e}")

    except Exception as e:
        print_info(f"Warning: Failed to load data or starting fresh: {e}")
            
    return book


def save_address_book(book: AddressBook) -> None:
    """
    Saves AddressBook to JSON storage.
    Serializes Record objects to dictionaries.
    """
    os.makedirs(DATA_DIR, exist_ok=True)
    
    save_data = {}
    
    for name, record in book.data.items():
        record_data = {
            "phones": [p.value for p in record.phones],
            "email": record.email.value if record.email else None,
            "birthday": record.birthday.value if record.birthday else None,
            "notes": record.notes,
            "tags": record.tags
        }
        save_data[name] = record_data
        
    try:
        with open(JSON_STORAGE_PATH, 'w', encoding='utf-8') as f:
            json.dump(save_data, f, ensure_ascii=False, indent=2)
            
        # Optional: CSV backup
        # Requires adapting existing import_export if we want to keep it
        pass 
        
    except Exception as e:
        print(f"Error saving data: {e}")

# Backwards compatibility aliases
def load(): return load_address_book()
def save(ab): save_address_book(ab)

__all__ = ["load_address_book", "save_address_book"]
