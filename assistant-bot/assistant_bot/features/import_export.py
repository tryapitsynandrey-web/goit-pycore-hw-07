import json
import csv


from assistant_bot.models import Record, AddressBook

def export_file(address_book: AddressBook, path: str):
    if not path:
        raise ValueError('Path required')
    
    # Prepare data structure including notes and tags embedded
    export_data = {}
    for name, record in address_book.data.items():
        entry = {
            "phones": [p.value for p in record.phones],
            "email": record.email.value if record.email else "",
            "birthday": record.birthday.value if record.birthday else "",
            "notes": record.notes,
            "tags": record.tags
        }
        export_data[name] = entry

    if path.lower().endswith('.json'):
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(export_data, f, ensure_ascii=False, indent=2)
    elif path.lower().endswith('.csv'):
        with open(path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['name', 'phones', 'email', 'birthday', 'notes', 'tags'])
            for name, entry in export_data.items():
                phones_str = '|'.join(entry['phones'])
                email_str = entry['email']
                bday_str = entry['birthday']
                # Join multiple notes with ' ; ' separator to fit in one CSV cell reasonably
                notes_str = ' ; '.join(entry['notes'])
                tags_str = ','.join(entry['tags'])
                writer.writerow([name, phones_str, email_str, bday_str, notes_str, tags_str])
    else:
        raise ValueError('Unsupported export format')


def import_file(address_book: AddressBook, path: str):
    if not path:
        raise ValueError('Path required')
    
    if path.lower().endswith('.json'):
        with open(path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            for name, entry in data.items():
                record = Record(name)
                
                # Phones
                # Support both list of strings or list of dicts if legacy?
                # Assuming standardized export format above.
                phones = entry.get('phones', [])
                if isinstance(phones, list):
                    for p in phones:
                        record.add_phone(p)

                # Email
                email = entry.get('email')
                if email:
                    record.add_email(email)

                # Birthday
                bday = entry.get('birthday')
                if bday:
                    record.add_birthday(bday)

                # Notes
                notes = entry.get('notes', [])
                for n in notes:
                    record.add_note(n)

                # Tags
                tags = entry.get('tags', [])
                for t in tags:
                    record.add_tag(t)

                address_book.add_record(record)
                    
    elif path.lower().endswith('.csv'):
        with open(path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                name = row.get('name')
                if not name:
                    continue
                
                record = Record(name)
                
                phones_str = row.get('phones')
                if phones_str:
                    for p in phones_str.split('|'):
                        if p: record.add_phone(p)

                email = row.get('email')
                if email:
                    record.add_email(email)

                birthday = row.get('birthday')
                if birthday:
                     record.add_birthday(birthday)
                
                notes_raw = row.get('notes')
                if notes_raw:
                    for n in notes_raw.split(' ; '):
                        if n: record.add_note(n)
                
                tags_raw = row.get('tags')
                if tags_raw:
                    for t in tags_raw.split(','):
                        if t: record.add_tag(t)
                
                address_book.add_record(record)
    else:
        raise ValueError('Unsupported import format')


__all__ = ['export_file', 'import_file']
