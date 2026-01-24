import os
import json
from dataclasses import dataclass, field
from typing import Dict, Any, List, Optional

from assistant_bot.config import JSON_STORAGE_PATH, CSV_STORAGE_PATH, DATA_DIR
from assistant_bot.utils.validators import normalize_phone

@dataclass
class AddressBook:
    contacts: Dict[str, Dict[str, Any]] = field(default_factory=dict)
    notes: Dict[str, list] = field(default_factory=dict)
    tags: Dict[str, list] = field(default_factory=dict)

    # --- Business Logic: Contacts ---

    def add_contact(self, name: str, phone: Optional[str] = None, email: Optional[str] = None, birthday: Optional[str] = None):
        """Adds or updates a contact. Merges data if contact exists."""
        if name not in self.contacts:
            self.contacts[name] = {
                'phones': [normalize_phone(phone)] if phone else [],
                'email': email,
                'birthday': birthday
            }
            return True, "new" # Created
        else:
            # Smart Merge
            contact = self.contacts[name]
            updated_fields = []
            
            if phone:
                norm = normalize_phone(phone)
                if norm not in contact['phones']:
                    contact['phones'].append(norm)
                    updated_fields.append('phone')
            
            if email and email != contact['email']:
                contact['email'] = email
                updated_fields.append('email')
                
            if birthday and birthday != contact['birthday']:
                contact['birthday'] = birthday
                updated_fields.append('birthday')
            
            return True, updated_fields # Updated

    def delete_contact(self, name: str):
        """Deletes a contact and all associated data."""
        if name in self.contacts:
            del self.contacts[name]
            self.notes.pop(name, None)
            self.tags.pop(name, None)
            return True
        return False

    def get_contact(self, name: str) -> Optional[Dict]:
        return self.contacts.get(name)

    def find_phone_global(self, phone: str) -> Optional[str]:
        """Returns the name of the contact who owns this phone, if any."""
        norm = normalize_phone(phone)
        for name, data in self.contacts.items():
            if norm in data.get('phones', []):
                return name
        return None

    def find_email_global(self, email: str) -> Optional[str]:
        """Returns the name of the contact who owns this email, if any."""
        for name, data in self.contacts.items():
            if data.get('email') == email:
                return name
        return None

    # --- Business Logic: Phones ---
    
    def add_phone(self, name: str, phone: str):
         contact = self.get_contact(name)
         if not contact:
             raise KeyError(f"Contact {name} not found")
         
         norm = normalize_phone(phone)
         if norm not in contact['phones']:
             contact['phones'].append(norm)
    
    def update_phone(self, name: str, old_phone: str, new_phone: str):
        contact = self.get_contact(name)
        if not contact:
             raise KeyError(f"Contact {name} not found")
        
        phones = contact['phones']
        norm_old = normalize_phone(old_phone)
        norm_new = normalize_phone(new_phone)
        
        # Try finding exact or normalized match
        target = old_phone if old_phone in phones else norm_old
        
        if target in phones:
            idx = phones.index(target)
            phones[idx] = norm_new
        else:
            raise ValueError(f"Phone {old_phone} not found")

    # --- Business Logic: Validation wrappers ---
    # (Optional: Logic checks can go here, calling validators internally)


def load_address_book() -> AddressBook:
    """Loads data from JSON storage."""
    os.makedirs(DATA_DIR, exist_ok=True)
    book = AddressBook()
    
    if os.path.exists(JSON_STORAGE_PATH):
        try:
            with open(JSON_STORAGE_PATH, 'r', encoding='utf-8') as f:
                data = json.load(f)
                
            for name, entry in data.items():
                # Extract separated stores
                notes_data = entry.pop('notes', [])
                tags_data = entry.pop('tags', [])
                
                book.contacts[name] = entry
                if notes_data:
                    book.notes[name] = notes_data
                if tags_data:
                    book.tags[name] = tags_data
        except Exception as e:
            print(f"Warning: Failed to load data: {e}")
            
    return book


def save_address_book(book: AddressBook) -> None:
    """Saves data to JSON storage."""
    os.makedirs(DATA_DIR, exist_ok=True)
    
    # Structure for saving: Dictionary of contacts with notes/tags embedded
    # This matches the schema expected by import/export and previous versions
    save_data = {}
    for name, data in book.contacts.items():
        entry = data.copy()
        entry['notes'] = book.notes.get(name, [])
        entry['tags'] = book.tags.get(name, [])
        save_data[name] = entry
        
    try:
        with open(JSON_STORAGE_PATH, 'w', encoding='utf-8') as f:
            json.dump(save_data, f, ensure_ascii=False, indent=2)
            
        # Optional: CSV backup (as per original requirement)
        # We can leverage the existing feature module for CSV to avoid code duplication
        from assistant_bot.features.import_export import export_file
        export_file(book, CSV_STORAGE_PATH)
        
    except Exception as e:
        print(f"Error saving data: {e}")

# Backwards compatibility aliases
def load(): return load_address_book()
def save(ab): save_address_book(ab)

__all__ = ["AddressBook", "load_address_book", "save_address_book"]
