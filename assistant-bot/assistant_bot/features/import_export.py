import json
import csv


def export_file(address_book, path: str):
    if not path:
        raise ValueError('Path required')
    
    # Prepare data structure including notes and tags embedded
    export_data = {}
    for name, c in address_book.contacts.items():
        entry = c.copy()
        entry['notes'] = address_book.notes.get(name, [])
        entry['tags'] = address_book.tags.get(name, [])
        export_data[name] = entry

    if path.lower().endswith('.json'):
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(export_data, f, ensure_ascii=False, indent=2)
    elif path.lower().endswith('.csv'):
        with open(path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['name', 'phones', 'email', 'birthday', 'notes', 'tags'])
            for name, c in export_data.items():
                phones_str = '|'.join(c.get('phones', []))
                email_str = c.get('email', '')
                bday_str = c.get('birthday', '')
                # Join multiple notes with ' ; ' separator to fit in one CSV cell reasonably
                notes_str = ' ; '.join(c.get('notes', []))
                tags_str = ','.join(c.get('tags', []))
                writer.writerow([name, phones_str, email_str, bday_str, notes_str, tags_str])
    else:
        raise ValueError('Unsupported export format')


def import_file(address_book, path: str):
    if not path:
        raise ValueError('Path required')
    
    if path.lower().endswith('.json'):
        with open(path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            for name, c in data.items():
                # Extract extras
                notes = c.pop('notes', [])
                tags = c.pop('tags', [])
                
                # Save contact
                address_book.contacts[name] = c
                
                # Save extras
                if notes:
                    address_book.notes[name] = notes
                if tags:
                    address_book.tags[name] = tags
                    
    elif path.lower().endswith('.csv'):
        with open(path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                name = row.get('name')
                if not name:
                    continue
                    
                phones = row.get('phones', '').split('|') if row.get('phones') else []
                email = row.get('email')
                birthday = row.get('birthday')
                
                notes_raw = row.get('notes')
                notes = notes_raw.split(' ; ') if notes_raw else []
                
                tags_raw = row.get('tags')
                tags = tags_raw.split(',') if tags_raw else []
                
                # Save
                address_book.contacts[name] = {'phones': phones, 'email': email, 'birthday': birthday}
                if notes:
                    address_book.notes[name] = notes
                if tags:
                    address_book.tags[name] = tags
    else:
        raise ValueError('Unsupported import format')


__all__ = ['export_file', 'import_file']
