
import json
import csv
import random
from datetime import date, timedelta

# Constants based on requirements
COUNT = 400
TAGS_POOL = [
    "work", "friend", "family", "gym", "cigar club", "tennis club", 
    "school mate", "neighbor", "colleague", "vip", "client", 
    "football team", "book club", "gaming buddy"
]  # 14 distinct tags

FIRST_NAMES = [
    "John", "Jane", "Alice", "Bob", "Charlie", "David", "Eve", "Frank", "Grace", "Hannah",
    "Ivan", "Jack", "Kathy", "Leo", "Mike", "Nina", "Oscar", "Paul", "Quinn", "Rose",
    "Steve", "Tom", "Uma", "Victor", "Wendy", "Xander", "Yara", "Zack",
    "Liam", "Noah", "Oliver", "Elijah", "James", "William", "Benjamin", "Lucas",
    "Henry", "Alexander", "Mason", "Michael", "Ethan", "Daniel", "Jacob", "Logan",
    "Sophia", "Emma", "Olivia", "Ava", "Isabella", "Mia", "Amelia", "Harper",
    "Evelyn", "Abigail", "Emily", "Ella", "Scarlett", "Victoria", "Aria",
    "Samuel", "Joseph", "Matthew", "Andrew", "Joshua", "Christopher", "Ryan",
    "Nathan", "Aaron", "Caleb", "Dylan", "Isaac", "Julian", "Sebastian"
]

LAST_NAMES = [
    "Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller", "Davis",
    "Rodriguez", "Martinez", "Hernandez", "Lopez", "Gonzalez", "Wilson", "Anderson",
    "Thomas", "Taylor", "Moore", "Jackson", "Martin", "Lee", "Perez", "Thompson",
    "White", "Harris", "Sanchez", "Clark", "Ramirez", "Lewis", "Robinson",
    "Walker", "Young", "Allen", "King", "Wright", "Scott", "Torres", "Nguyen",
    "Hill", "Flores", "Green", "Adams", "Nelson", "Baker", "Hall",
    "Rivera", "Campbell", "Mitchell", "Carter", "Roberts", "Gomez",
    "Phillips", "Evans", "Turner", "Diaz", "Parker", "Cruz", "Edwards"
]

NOTES_LONG = [
    "Enjoys psychological thrillers like Shutter Island and Inception. Big fan of Christopher Nolan.",
    "Favorite color is azure blue. Loves 80s synth-pop, especially Depeche Mode.",
    "Prefers single malt scotch, especially Lagavulin 16. Strong dislike for gin.",
    "Dedicated Beatles fan who listens only on vinyl. Considers Abbey Road their best work.",
    "Passionate about gardening and growing exotic orchids. Maintains a small greenhouse.",
    "Collects vintage cameras from the 1960s, especially Leica models. Practices darkroom development.",
    "Loves Italian cuisine and makes homemade pasta regularly. Enjoys experimenting with recipes.",
    "Avid Stephen King reader and collector. Owns a first edition of The Shining.",
    "Enjoys hiking in the Swiss Alps and has visited Zermatt multiple times.",
    "Passionate about specialty coffee and roasts Ethiopian beans at home."
]

NOTES_SHORT = [
    "Call back later.", "Meeting next week.", " owe him $5.", "Nice guy.", 
    "Met at conference.", "Don't forget birthday.", "Sent invoice.", 
    "Needs updated contract.", "New phone number.", "Discuss project."
]

DOMAINS = [
    "gmail.com", "yahoo.com", "outlook.com", "hotmail.com",
    "icloud.com", "ukr.net", "proton.me", "aol.com",
    "live.com", "msn.com", "zoho.com", "mail.com", "yandex.com",
    "pm.me", "tutanota.com", "gmx.com",
    "protonmail.com", "fastmail.com", "hey.com", "inbox.com",
    "orange.fr", "bluewin.ch", "web.de"
]

PREFIXES = [
    "050", "066", "095", "099",
    "067", "068", "096", "097", "098",
    "063", "093", "073",

    # added – additional valid Ukrainian ranges
    "091",  # 3Mob
    "092",  # PEOPLEnet
    "094",  # Intertelecom (legacy but still встречается в данных)
    "089",  # Lycamobile Ukraine
    "090"   # corporate / MVNO
]


def generate_phone(index):
    # Generate random realistic phone: +38 + Prefix + 7 random digits
    prefix = random.choice(PREFIXES)
    # Generate 7 digits. Pad with zeros if needed (though randint(0,9999999) isn't safe for leading zeros visually if we cast to int first)
    # Better: ''.join(random.choices('0123456789', k=7))
    suffix = ''.join(random.choices('0123456789', k=7))
    return f"+38{prefix}{suffix}"

def generate_email(name, index):
    # Unique email
    clean_name = name.lower().replace(" ", ".")
    domain = random.choice(DOMAINS)
    return f"{clean_name}.{index}@{domain}"

def generate_birthday(index):
    # random year 1940-2007
    # 58 people have duplicate birthdays? 
    # Actually random collision naturally happens, but let's just do pure random within range.
    # To force 58 duplicates we'd need complex logic, but "as much as possible... but can overlap" 
    # typically means just random is fine, or we can pick a few fixed dates.
    # The prompt says "different as much as possible but can repeat for 58 people".
    # Let's interpret: mostly unique, but some collisions are fine.
    
    start_date = date(1940, 1, 1)
    end_date = date(2007, 12, 31)
    days_range = (end_date - start_date).days
    
    # We can pre-generate a list of dates to ensure high variance?
    # Or just random. Random 1940-2007 (67 years * 365 = ~24k days) vs 400 people.
    # Collisions will be rare natively. We can force some if strict. 
    # "can repeat for 58 people" -> maybe means exactly 58 people share bdays?
    # Let's just use random, it fits "different as much as possible".
    
    rand_days = random.randint(0, days_range)
    bday = start_date + timedelta(days=rand_days)
    return bday.strftime("%d-%m-%Y")

def generate_data():
    data_list = []
    
    # Pre-assignments to meet exact percentages if needed, or probablistic.
    # 400 items.
    # 50% name+surname (200), 50% name (200)
    # 87% notes (348). Of these 348, 30% long (104), rest short (244).
    # 76% tags (304).
    
    for i in range(COUNT):
        # 1. Name
        if i < 200: # First 200: Name + Surname
            name = f"{random.choice(FIRST_NAMES)} {random.choice(LAST_NAMES)}"
        else: # Next 200: Only Name
            name = random.choice(FIRST_NAMES)
            # Ensure unique name to avoid overwrite in dict-based system?
            # The system uses Name as key. So names MUST be unique.
            # Simple "John" vs "John Smith". 
            # If we create duplicates, the last one overwrites. 
            # We must ensure 400 UNIQUE names.
            # Strategy: Append index if duplicate or just always append specific id?
            # User said "50% name+surname, 50% name". 
            # It's hard to have 200 unique single first names if list is short.
            # We will append a number if single name, or just use more distinct names?
            # Let's append index to all names relative to their group to ensure uniqueness if needed,
            # Or assume the prompt implies "unique contacts" -> unique names.
            # To be safe and clean, let's treat "Name" as the visible name.
            # If "John" implies just "John", we can only have one "John".
            # Hack: "John 1", "John 2"? Or "John_A"?
            # Prompt: "50% with name and surname, 50% only with name".
            # This is tricky for a system where Name is ID. 
            # I will use "Unique Name" strategy: Name + (i if needed).
            pass

    # Better Strategy for Names:
    # Generate 400 unique keys first.
    # Set 1 (200): First + Last. (Permutations of 40 first * 30 last = 1200 combos). Should be fine.
    # Set 2 (200): First. (Only 40 names). Impossible to have 200 unique single names from 40 list.
    # I will add a middle initial or numeric suffix to single names to satisfy "only name" style 
    # while keeping extended uniqueness? OR check if user system supports IDs separate from Name?
    # System uses `book.contacts[name]`. Name IS key.
    # So we cannot have 200 distinct contacts named just "John", "Mary" etc if we only have 40 names.
    # I will expand the source list or allow "John-1" style. 
    # Let's try to generate unique First+Last first.
    
    generated_names = set()
    rows = []

    for i in range(COUNT):
        entry = {}
        
        # --- NAME ---
        while True:
            # First 50% (0-199) -> Full Name
            if i < 200:
                fn = random.choice(FIRST_NAMES)
                ln = random.choice(LAST_NAMES)
                candidate = f"{fn} {ln}"
            else:
                # Second 50% (200-399) -> Single Name style
                # To make unique, we might need suffixes if collision
                fn = random.choice(FIRST_NAMES)
                candidate = fn
            
            # Helper to make unique if collision
            if candidate in generated_names:
                # Collision. 
                # If it's a "single name", we MUST differentiate.
                # User constraint "only with name" might allow "John B."?
                # or maybe just "John" but different phone? 
                # Code overwrites if name exists.
                # So we MUST have unique names.
                # I will add a subtle suffix like numeric ID for single names if collision.
                # "John 2", "John 3". It technically is "Name" (no surname).
                candidate = f"{candidate} {i}"
            
            if candidate not in generated_names:
                generated_names.add(candidate)
                entry['name'] = candidate
                break
        
        # --- PHONE ---
        # Unique phone per user
        while True:
             phone = generate_phone(i)
             # Check global uniqueness across already generated rows
             # (This is O(N^2) effectively but for 400 items it's instant)
             if not any(phone in r['phones'] for r in rows):
                 entry['phones'] = [phone]
                 break
        
        # --- EMAIL ---
        entry['email'] = generate_email(entry['name'], i)
        
        # --- BIRTHDAY ---
        entry['birthday'] = generate_birthday(i)
        
        # --- NOTES ---
        # 87% have notes. (i < 348 approx)
        if i < 348:
            # 30% of these (104) long.
            if i < 104:
                entry['notes'] = [random.choice(NOTES_LONG)]
            else:
                entry['notes'] = [random.choice(NOTES_SHORT)]
        else:
            entry['notes'] = []

        # --- TAGS ---
        # 76% have tags. (i < 304 approx)
        if i < 304:
            entry['tags'] = [random.choice(TAGS_POOL)]
        else:
            entry['tags'] = []
            
        rows.append(entry)

    # Shuffle rows so the "types" are mixed in the file? 
    # Or keep them ordered for easier verification of 50/50 split?
    # User didn't specify order. Random shuffle makes it look more natural.
    random.shuffle(rows)
    
    return rows

def save_files(data_rows):
    # JSON Structure: {name: {phones, email, birthday, notes, tags}, ...}
    json_data = {}
    for row in data_rows:
        name = row['name']
        json_data[name] = {
            'phones': row['phones'],
            'email': row['email'],
            'birthday': row['birthday'],
            'notes': row['notes'],
            'tags': row['tags']
        }
        
    with open('test_addressbook/test_data_400.json', 'w', encoding='utf-8') as f:
        json.dump(json_data, f, ensure_ascii=False, indent=2)
    print("Generated test_addressbook/test_data_400.json")

    # CSV Structure: name, phones, email, birthday, notes, tags
    with open('test_addressbook/test_data_400.csv', 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['name', 'phones', 'email', 'birthday', 'notes', 'tags'])
        for row in data_rows:
            phones_str = '|'.join(row['phones'])
            notes_str = ' ; '.join(row['notes']) # Match import format
            tags_str = ','.join(row['tags'])
            writer.writerow([
                row['name'], 
                phones_str, 
                row['email'], 
                row['birthday'], 
                notes_str, 
                tags_str
            ])
    print("Generated test_addressbook/test_data_400.csv")


if __name__ == "__main__":
    print("Generating 400 contacts...")
    data = generate_data()
    save_files(data)
    print("Done.")

