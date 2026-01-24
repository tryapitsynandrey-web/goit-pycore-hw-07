import shlex
import random
from functools import wraps
from typing import Callable, List, Dict, Optional, Tuple

from rich.table import Table
from rich.panel import Panel
from rich import box
from rich.align import Align

from assistant_bot.config import DEFAULT_BIRTHDAY_LOOKAHEAD_DAYS
from assistant_bot.storage import AddressBook
from assistant_bot.utils.console import console, print_error, print_success, print_info, print_warning, print_duplicate_error
from assistant_bot.utils.validators import validate_phone, validate_email, normalize_phone
from assistant_bot.features import birthdays, notes, tags, import_export
from assistant_bot.utils.ux_messages import (
    UNKNOWN_COMMAND_MESSAGES, MISSING_ARGS_MESSAGES,
    CONTACT_ADDED_MESSAGES, CONTACT_UPDATED_MESSAGES, PHONE_ADDED_MESSAGES,
    PHONE_UPDATED_MESSAGES, CONTACT_DELETED_MESSAGES, EMAIL_UPDATED_MESSAGES,
    BIRTHDAY_UPDATED_MESSAGES, NOTE_ADDED_MESSAGES, NOTE_UPDATED_MESSAGES,
    NOTE_DELETED_MESSAGES, TAG_ADDED_MESSAGES, TAG_REMOVED_MESSAGES,
    IMPORT_SUCCESS_MESSAGES, EXPORT_SUCCESS_MESSAGES, DELETE_ALL_MESSAGES,
    DUPLICATE_EMAIL_MESSAGES, DUPLICATE_PHONE_MESSAGES,
    CONTACT_NOT_FOUND_MESSAGES, INVALID_PHONE_MESSAGES, INVALID_EMAIL_MESSAGES,
    INVALID_BIRTHDAY_MESSAGES, INVALID_INDEX_MESSAGES
)

# Registry for commands.
COMMAND_REGISTRY: Dict[str, Tuple[Callable, str]] = {}


def command(name: str, help_text: str = ""):
    """Decorator to register a bot command."""
    def decorator(func: Callable):
        COMMAND_REGISTRY[name] = (func, help_text)
        @wraps(func)
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)
        return wrapper
    return decorator


# --- Command Handlers ---

@command("help", "Show available commands")
def handle_help(book: AddressBook, args: List[str]):
    """Displays commands grouped by category."""
    
    categories = {
        "📇 Contact Management": [
            "add", "all", "change", "add_phone", "phone", "delete", 
            "add_email", "add_birthday", "birthdays", "days_to_bday", 
            "search", "list"
        ],
        "📝 Notes": [
            "add_note", "edit_note", "delete_note", "search_notes", "list_notes"
        ],
        "🏷️ Tags": [
            "add_tag", "remove_tag", "list_tags", "filter_by_tag"
        ],
        "💾 System & Data": [
            "import", "export", "delete_all", "help", "exit", "close"
        ]
    }

    console.print(Align.center(Panel(
        "🤖 [bold magenta]Assistant Bot Help Menu[/bold magenta]", 
        border_style="magenta",
        subtitle="[dim]Type a command to proceed[/dim]",
        width=90,
        box=box.ROUNDED
    )))

    for category, cmds in categories.items():
        table = Table(
            title=category, 
            title_style="bold cyan", 
            show_header=True, 
            header_style="bold white", 
            box=box.ROUNDED,
            width=90,
            show_lines=True,
            border_style="bright_blue"
        )
        table.add_column("Command", style="cyan", width=35)
        table.add_column("Description", style="white")
        
        has_rows = False
        for name in cmds:
            if name in COMMAND_REGISTRY:
                _, help_text = COMMAND_REGISTRY[name]
                table.add_row(name, help_text)
                has_rows = True
        
        if has_rows:
            console.print(Align.center(table))
            console.print()


# --- CONTACT MANAGEMENT ---

@command("add", "Add contact: add <name> [phone] [email] [birthday]")
def handle_add(book: AddressBook, args: List[str]):
    if not args:
        print_error(random.choice(MISSING_ARGS_MESSAGES).format(syntax="add <name> [phone] [email] [birthday]"))
        return
    
    name = args[0]
    phone = args[1] if len(args) > 1 else None
    email = args[2] if len(args) > 2 else None
    birthday = args[3] if len(args) > 3 else None

    # Validation
    if phone and not validate_phone(phone):
        print_error(random.choice(INVALID_PHONE_MESSAGES).format(phone=phone))
        return
    if email and not validate_email(email):
        print_error(random.choice(INVALID_EMAIL_MESSAGES).format(email=email))
        return

    # Uniqueness Check (Global)
    if phone:
        owner = book.find_phone_global(phone)
        if owner and owner != name:
            print_duplicate_error(owner, book.contacts[owner], normalize_phone(phone), DUPLICATE_PHONE_MESSAGES)
            return

    if email:
        owner = book.find_email_global(email)
        if owner and owner != name:
            print_duplicate_error(owner, book.contacts[owner], email, DUPLICATE_EMAIL_MESSAGES)
            return

    # Execution via Business Logic Layer
    result, status = book.add_contact(name, phone, email, birthday)
    
    if status == "new":
        print_success(random.choice(CONTACT_ADDED_MESSAGES).format(name=name))
    elif isinstance(status, list):
        if status:
            print_success(f"Updated contact '{name}': added/changed {', '.join(status)}.")
        else:
            print_info(f"Contact '{name}' already up to date.")


@command("change", "Change phone: change <name> <old_phone> <new_phone>")
def handle_change(book: AddressBook, args: List[str]):
    if len(args) < 3:
        print_error(random.choice(MISSING_ARGS_MESSAGES).format(syntax="change <name> <old_phone> <new_phone>"))
        return
    
    name, old_phone, new_phone = args[0], args[1], args[2]
    
    # Validation
    if not validate_phone(new_phone):
        print_error(random.choice(INVALID_PHONE_MESSAGES).format(phone=new_phone))
        return
        
    # Uniqueness Check
    owner = book.find_phone_global(new_phone)
    if owner and owner != name:
        print_duplicate_error(owner, book.contacts[owner], normalize_phone(new_phone), DUPLICATE_PHONE_MESSAGES)
        return

    try:
        book.update_phone(name, old_phone, new_phone)
        print_success(random.choice(PHONE_UPDATED_MESSAGES).format(name=name))
    except KeyError:
        print_error(random.choice(CONTACT_NOT_FOUND_MESSAGES).format(name=name))
    except ValueError:
        print_error(f"Phone {old_phone} not found for {name}.")


@command("add_phone", "Add extra phone: add_phone <name> <phone>")
def handle_add_phone(book: AddressBook, args: List[str]):
    if len(args) < 2:
        print_error(random.choice(MISSING_ARGS_MESSAGES).format(syntax="add_phone <name> <phone>"))
        return
    
    name, phone = args[0], args[1]

    if not validate_phone(phone):
        print_error(random.choice(INVALID_PHONE_MESSAGES).format(phone=phone))
        return
    
    owner = book.find_phone_global(phone)
    if owner and owner != name:
         print_duplicate_error(owner, book.contacts[owner], normalize_phone(phone), DUPLICATE_PHONE_MESSAGES)
         return
         
    try:
        book.add_phone(name, phone)
        print_success(random.choice(PHONE_ADDED_MESSAGES).format(name=name))
    except KeyError:
        print_error(random.choice(CONTACT_NOT_FOUND_MESSAGES).format(name=name))


@command("delete", "Delete contact: delete <name>")
def handle_delete(book: AddressBook, args: List[str]):
    if not args:
        print_error(random.choice(MISSING_ARGS_MESSAGES).format(syntax="delete <name>"))
        return
    
    name = args[0]
    if book.delete_contact(name):
        print_success(random.choice(CONTACT_DELETED_MESSAGES).format(name=name))
    else:
        print_error(random.choice(CONTACT_NOT_FOUND_MESSAGES).format(name=name))


@command("search", "Search contacts: search <query>")
def handle_search(book: AddressBook, args: List[str]):
    if not args:
        print_error(random.choice(MISSING_ARGS_MESSAGES).format(syntax="search <query>"))
        return
    
    query = args[0].lower()
    results = {}
    
    # Ideally search logic should be in AddressBook too, but keeping it simple for now
    for name, data in book.contacts.items():
        if query in name.lower():
            results[name] = data
            continue
        for phone in data.get('phones', []):
            if query in phone:
                results[name] = data
                break
        if data.get('email') and query in data['email'].lower():
            results[name] = data
    
    if not results:
        print_info(f"No contacts found matching '{query}'")
        return
        
    _print_contacts_table(results)


@command("phone", "Show phones: phone <name>")
def handle_phone(book: AddressBook, args: List[str]):
    if not args:
        print_error(random.choice(MISSING_ARGS_MESSAGES).format(syntax="phone <name>"))
        return
    
    name = args[0]
    contact = book.get_contact(name)
    if contact:
        phones = contact.get('phones', [])
        console.print(f"[bold]{name}[/bold]: {', '.join(phones) if phones else 'No phones'}")
    else:
        print_error(random.choice(CONTACT_NOT_FOUND_MESSAGES).format(name=name))


@command("add_email", "Add/Edit email: add_email <name> <email>")
def handle_add_email(book: AddressBook, args: List[str]):
    if len(args) < 2:
        print_error(random.choice(MISSING_ARGS_MESSAGES).format(syntax="add_email <name> <email>"))
        return
    
    name, email = args[0], args[1]
    
    if not validate_email(email):
        print_error(random.choice(INVALID_EMAIL_MESSAGES).format(email=email))
        return

    owner = book.find_email_global(email)
    if owner and owner != name:
         print_duplicate_error(owner, book.contacts[owner], email, DUPLICATE_EMAIL_MESSAGES)
         return
         
    contact = book.get_contact(name)
    if contact:
        contact['email'] = email # Direct update for now, or add update_email method
        print_success(random.choice(EMAIL_UPDATED_MESSAGES).format(name=name))
    else:
        print_error(random.choice(CONTACT_NOT_FOUND_MESSAGES).format(name=name))


@command("add_birthday", "Add/Edit birthday: add_birthday <name> <DD-MM-YYYY>")
def handle_add_birthday(book: AddressBook, args: List[str]):
    if len(args) < 2:
        print_error(random.choice(MISSING_ARGS_MESSAGES).format(syntax="add_birthday <name> <date>"))
        return
    
    name, bday = args[0], args[1]
    contact = book.get_contact(name)
    if not contact:
        print_error(random.choice(CONTACT_NOT_FOUND_MESSAGES).format(name=name))
        return
    
    try:
        birthdays.days_until_birthday(bday) # Validation
        contact['birthday'] = bday
        print_success(random.choice(BIRTHDAY_UPDATED_MESSAGES).format(name=name))
    except ValueError:
        print_error(random.choice(INVALID_BIRTHDAY_MESSAGES))


@command("all", "Show all contact info")
def handle_all(book: AddressBook, args: List[str]):
    if not book.contacts:
        print_info("No contacts found.")
        return

    table = Table(title="All Contacts Details")
    table.add_column("Full Name", style="cyan")
    table.add_column("Phone", style="green")
    table.add_column("Email", style="blue")
    table.add_column("Birthday", style="yellow")
    table.add_column("Days to B-day", style="magenta")
    table.add_column("Note", style="white")
    table.add_column("Tag", style="red")

    for name, data in book.contacts.items():
        phones = ", ".join(data.get('phones', []))
        email = data.get('email') or "-"
        bday_str = data.get('birthday') or "-"
        
        days_until = "-"
        if bday_str != "-":
            try:
                days = birthdays.days_until_birthday(bday_str)
                days_until = str(days)
            except ValueError:
                days_until = "Invalid Date"
        
        user_notes = book.notes.get(name, [])
        note_str = "\n".join(user_notes) if user_notes else "-"
        
        user_tags = book.tags.get(name, [])
        tag_str = ", ".join(user_tags) if user_tags else "-"
        
        table.add_row(name, phones, email, bday_str, days_until, note_str, tag_str)
    
    console.print(Align.center(table))


@command("list", "List all contacts")
def handle_list(book: AddressBook, args: List[str]):
    if not book.contacts:
        print_info("No contacts found.")
        return
    _print_contacts_table(book.contacts)


def _print_contacts_table(contacts_dict: Dict):
    table = Table(title="Contacts List")
    table.add_column("Name", style="cyan")
    table.add_column("Phones", style="green")
    table.add_column("Email", style="blue")
    table.add_column("Birthday", style="yellow")

    for name, data in contacts_dict.items():
        phones = ", ".join(data.get('phones', []))
        email = data.get('email') or "-"
        birthday = data.get('birthday') or "-"
        table.add_row(name, phones, email, birthday)
    
    console.print(table)


# --- NOTES MANAGEMENT ---

@command("add_note", "Add note: add_note <name> <text>")
def handle_add_note(book: AddressBook, args: List[str]):
    if len(args) < 2:
        print_error(random.choice(MISSING_ARGS_MESSAGES).format(syntax="add_note <name> <text>"))
        return
    
    name = args[0]
    note = " ".join(args[1:])
    try:
        notes.add_note(book, name, note)
        print_success(random.choice(NOTE_ADDED_MESSAGES).format(name=name))
    except KeyError:
        print_error(random.choice(CONTACT_NOT_FOUND_MESSAGES).format(name=name))


@command("edit_note", "Edit note: edit_note <name> <index> <new_text>")
def handle_edit_note(book: AddressBook, args: List[str]):
    if len(args) < 3:
        print_error(random.choice(MISSING_ARGS_MESSAGES).format(syntax="edit_note <name> <index> <new_text>"))
        return
    
    name = args[0]
    try:
        index = int(args[1]) - 1
        new_text = " ".join(args[2:])
        
        user_notes = notes.list_notes(book, name)
        if not user_notes:
            print_error(f"No notes for {name}")
            return
            
        if 0 <= index < len(user_notes):
            notes.edit_note(book, name, index, new_text)
            print_success(random.choice(NOTE_UPDATED_MESSAGES).format(name=name))
        else:
            print_error(random.choice(INVALID_INDEX_MESSAGES))
    except ValueError:
        print_error("Index must be a number.")
    except KeyError:
        print_error(random.choice(CONTACT_NOT_FOUND_MESSAGES).format(name=name))


@command("delete_note", "Delete note: delete_note <name> <index>")
def handle_delete_note(book: AddressBook, args: List[str]):
    if len(args) < 2:
        print_error(random.choice(MISSING_ARGS_MESSAGES).format(syntax="delete_note <name> <index>"))
        return
    
    name, index_str = args[0], args[1]
    try:
        index = int(index_str) - 1
        notes.delete_note(book, name, index)
        print_success(random.choice(NOTE_DELETED_MESSAGES).format(name=name))
    except ValueError:
        print_error("Index must be a number.")
    except Exception:
         print_error("Could not delete note. Check contact and index.")


@command("search_notes", "Search notes: search_notes <query>")
def handle_search_notes(book: AddressBook, args: List[str]):
    if not args:
        print_error(random.choice(MISSING_ARGS_MESSAGES).format(syntax="search_notes <query>"))
        return
    
    query = args[0].lower()
    found = False
    
    for name, user_notes in book.notes.items():
        for i, note in enumerate(user_notes):
            if query in note.lower():
                console.print(f"[bold cyan]{name}[/bold cyan] (Note {i+1}): {note}")
                found = True
    
    if not found:
        print_info(f"No notes found matching '{query}'")


@command("list_notes", "List notes: list_notes [name]")
def handle_list_notes(book: AddressBook, args: List[str]):
    name = args[0] if args else None
    results = notes.list_notes(book, name)
    
    if not results:
        print_info(f"No notes found{' for ' + name if name else ''}.")
        return

    if isinstance(results, list):
         console.print(f"[bold]Notes for {name}:[/bold]")
         for i, note in enumerate(results, 1):
             console.print(f"{i}. {note}")
    elif isinstance(results, dict):
        for contact_name, note_list in results.items():
            if note_list:
                console.print(f"[bold]{contact_name}[/bold]:")
                for i, note in enumerate(note_list, 1):
                    console.print(f"  {i}. {note}")


# --- TAGS MANAGEMENT ---

@command("add_tag", "Add tag: add_tag <name> <tag>")
def handle_add_tag(book: AddressBook, args: List[str]):
    if len(args) < 2:
        print_error(random.choice(MISSING_ARGS_MESSAGES).format(syntax="add_tag <name> <tag>"))
        return
    
    name, tag = args[0], args[1]
    try:
        tags.add_tag(book, name, tag)
        print_success(random.choice(TAG_ADDED_MESSAGES).format(name=name, tag=tag))
    except KeyError:
        print_error(random.choice(CONTACT_NOT_FOUND_MESSAGES).format(name=name))


@command("remove_tag", "Remove tag: remove_tag <name> <tag>")
def handle_remove_tag(book: AddressBook, args: List[str]):
    if len(args) < 2:
        print_error(random.choice(MISSING_ARGS_MESSAGES).format(syntax="remove_tag <name> <tag>"))
        return
    
    name, tag = args[0], args[1]
    tags.remove_tag(book, name, tag)
    print_success(random.choice(TAG_REMOVED_MESSAGES).format(name=name))


@command("list_tags", "List all tags")
def handle_list_tags(book: AddressBook, args: List[str]):
    results = tags.list_tags(book)
    if not results:
        print_info("No tags found.")
        return
    
    for name, t_list in results.items():
        if t_list:
            console.print(f"[bold]{name}[/bold]: {', '.join(t_list)}")


@command("filter_by_tag", "Find contacts by tag: filter_by_tag <tag>")
def handle_filter_by_tag(book: AddressBook, args: List[str]):
    if not args:
        print_error(random.choice(MISSING_ARGS_MESSAGES).format(syntax="filter_by_tag <tag>"))
        return
    
    tag = args[0]
    names = tags.filter_by_tag(book, tag)
    if not names:
        print_info(f"No contacts found with tag '{tag}'")
        return

    table = Table(title=f"Contacts with Tag: {tag}")
    table.add_column("Tag", style="red")
    table.add_column("Full Name", style="cyan")
    table.add_column("Days to B-day", style="magenta")
    table.add_column("Phone", style="green")
    table.add_column("Email", style="blue")
    table.add_column("Birthday", style="yellow")
    table.add_column("Note", style="white")

    for name in names:
        data = book.contacts.get(name)
        if not data: 
            continue
            
        phones = ", ".join(data.get('phones', []))
        email = data.get('email') or "-"
        bday = data.get('birthday') or "-"
        
        days_until = "-"
        if bday != "-":
            try:
                days_until = str(birthdays.days_until_birthday(bday))
            except ValueError:
                days_until = "Invalid Date"
        
        user_notes = book.notes.get(name, [])
        note_str = "\n".join(user_notes) if user_notes else "-"
        
        table.add_row(tag, name, days_until, phones, email, bday, note_str)
    
    console.print(Align.center(table))


# --- BIRTHDAYS ---

@command("days_to_bday", "Days until birthday (one contact)")
def handle_days_to_bday(book: AddressBook, args: List[str]):
    if not args:
        print_error(random.choice(MISSING_ARGS_MESSAGES).format(syntax="days_to_bday <name>"))
        return
    
    name = args[0]
    contact = book.get_contact(name)
    if not contact:
        print_error(random.choice(CONTACT_NOT_FOUND_MESSAGES).format(name=name))
        return
    
    bday_str = contact.get('birthday')
    if not bday_str:
        print_warning(f"No birthday set for {name}.")
        return

    try:
        days = birthdays.days_until_birthday(bday_str)
        print_info(f"Days until {name}'s birthday: [bold]{days}[/bold]")
    except ValueError:
        print_error(random.choice(INVALID_BIRTHDAY_MESSAGES))


@command("birthdays", "Upcoming birthdays: birthdays [days]")
def handle_birthdays(book: AddressBook, args: List[str]):
    days = DEFAULT_BIRTHDAY_LOOKAHEAD_DAYS
    if args:
        try:
            days = int(args[0])
        except ValueError:
            print_error("Days must be a number.")
            return

    upcoming = birthdays.get_upcoming_birthdays(book.contacts, days)
    if not upcoming:
        print_info(f"No birthdays in the next {days} days.")
        return

    console.print(f"[bold]Birthdays in the next {days} days:[/bold]")
    
    table = Table(title=f"Upcoming Birthdays (Next {days} days)")
    table.add_column("Birthday", style="yellow")
    table.add_column("Days to B-day", style="magenta")
    table.add_column("Full Name", style="cyan")
    table.add_column("Tag", style="red")
    table.add_column("Phone", style="green")
    table.add_column("Email", style="blue")
    table.add_column("Note", style="white")
    
    for item in upcoming:
        name = item['name']
        data = book.contacts.get(name)
        if not data:
            continue
            
        phones = ", ".join(data.get('phones', []))
        email = data.get('email') or "-"
        
        user_notes = book.notes.get(name, [])
        note_str = "\n".join(user_notes) if user_notes else "-"
        
        user_tags = book.tags.get(name, [])
        tag_str = ", ".join(user_tags) if user_tags else "-"
        
        table.add_row(
            item['birthday'], 
            str(item['days_until']), 
            name,
            tag_str,
            phones, 
            email, 
            note_str
        )
        
    console.print(Align.center(table))


# --- IMPORT/EXPORT ---

@command("import", "Import data: import <file.json|csv>")
def handle_import(book: AddressBook, args: List[str]):
    if not args:
        print_error(random.choice(MISSING_ARGS_MESSAGES).format(syntax="import <path>"))
        return
    
    path = args[0]
    try:
        import_export.import_file(book, path)
        print_success(random.choice(IMPORT_SUCCESS_MESSAGES).format(path=path))
    except Exception as e:
        print_error(f"Import failed: {e}")


@command("export", "Export data: export <file.json|csv>")
def handle_export(book: AddressBook, args: List[str]):
    if not args:
        print_error(random.choice(MISSING_ARGS_MESSAGES).format(syntax="export <path>"))
        return
    
    path = args[0]
    try:
        import_export.export_file(book, path)
        print_success(random.choice(EXPORT_SUCCESS_MESSAGES).format(path=path))
    except Exception as e:
        print_error(f"Export failed: {e}")


@command("delete_all", "Delete ALL content: delete_all")
def handle_delete_all(book: AddressBook, args: List[str]):
    console.print("[bold red]⚠️  WARNING: This will delete ALL contacts, notes, and tags![/bold red]")
    confirm = console.input("[bold yellow]Are you sure? Type 'YES' to confirm: [/bold yellow]")
    
    if confirm == "YES":
        book.contacts.clear()
        book.notes.clear()
        book.tags.clear()
        print_success(random.choice(DELETE_ALL_MESSAGES))
    else:
        print_info("Operation canceled. Your data is safe.")


@command("exit", "Exit the application")
def handle_exit(book: AddressBook, args: List[str]):
    pass

@command("close", "Exit the application")
def handle_close(book: AddressBook, args: List[str]):
    pass


# --- Parser & Dispatcher ---

def parse(raw: str) -> Tuple[Optional[str], List[str]]:
    try:
        parts = shlex.split(raw)
        if not parts:
            return None, []
        return parts[0].lower(), parts[1:]
    except ValueError:
        return None, []

def dispatch(book: AddressBook, raw_input: str) -> bool:
    """Parses and executes a command."""
    cmd, args = parse(raw_input)
    
    if not cmd:
        return True

    if cmd in ('exit', 'close'):
        return False
    
    if cmd in COMMAND_REGISTRY:
        handler, _ = COMMAND_REGISTRY[cmd]
        try:
            handler(book, args)
        except Exception as e:
            print_error(f"Error executing '{cmd}': {e}")
    else:
        from assistant_bot.utils.ux_messages import UNKNOWN_COMMAND_MESSAGES
        msg = random.choice(UNKNOWN_COMMAND_MESSAGES).format(cmd=cmd)
        print_error(msg)
    
    return True
