# 🤖 Assistant Bot (CLI v6)

Welcome to the **Assistant Bot**, your professional CLI companion for managing contacts, notes, and tasks. This version features a robust architecture, strict data validation, and a polished, gamified user experience.

## 🚀 Installation & Launch

### Prerequisites
- Python 3.10 or higher
- `pip` package manager

### Setup
1. **Clone** the repository.
2. **Create a Virtual Environment** (Recommended):
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```
3. **Install Dependencies** (Critical for UI & Autocomplete):
   ```bash
   pip install -r assistant-bot/requirements.txt
   ```
   *Required:* `rich` (UI), `prompt_toolkit` (Autocomplete).

### Running the Bot
Execute the entry point from the project root:
```bash
python assistant-bot/run.py
```
You will see the interactive prompt: `bot>`.

---

## 📖 Feature Guide

### 📇 Contact Management
Manage your personal address book with strict validation.

| Command | Usage | Description |
|:---|:---|:---|
| **add** | `add <name> [phone] [email] [bday]` | Create a new contact. |
| **change** | `change <name> <old> <new>` | Update an existing phone number. |
| **add_phone** | `add_phone <name> <phone>` | Add an additional phone to a contact. |
| **phone** | `phone <name>` | Show all phone numbers for a contact. |
| **delete** | `delete <name>` | **Delete** a contact permanently. |
| **add_email** | `add_email <name> <email>` | Add or update email. |
| **add_birthday** | `add_birthday <name> <date>` | Add or update birthday (DD-MM-YYYY). |
| **search** | `search <query>` | Search contacts by name, phone, or email. |
| **list** | `list` | Show a beautiful **Rich Table** of all contacts. |

> **Note on Merging:** If you `add` a contact that already exists, the bot will smartly **update** them by adding the new phone/email instead of creating a duplicate.

### 🏷️ Tags Management
Organize contacts with tags. Multi-word tags are fully supported!

| Command | Usage | Description |
|:---|:---|:---|
| **add_tag** | `add_tag <name> <tag>` | Add a tag. Supports spaces! |
| **remove_tag** | `remove_tag <name> <tag>` | Remove a specific tag. |
| **list_tags** | `list_tags` | List all unique tags used in the system. |
| **filter_by_tag**| `filter_by_tag <tag>` | List all contacts with a specific tag. |

**Tag Examples:**
- Simple: `add_tag Alice Friend`
- Multi-word (Quoted): `add_tag Bob "Cigar Club"`
- Multi-word (Auto-join): `add_tag Bob Cigar Club` (Ending arguments are joined)

### 📝 Notes Management
Keep track of ideas and tasks linked to contacts.

| Command | Usage | Description |
|:---|:---|:---|
| **add_note** | `add_note <name> <text>` | Add a note to a contact. |
| **edit_note** | `edit_note <name> <idx> <text>` | Edit a specific note (by index 1..N). |
| **delete_note** | `delete_note <name> <idx>` | Delete a specific note. |
| **search_notes**| `search_notes <query>` | Search through all notes text. |
| **list_notes** | `list_notes [name]` | List notes for a person (or all). |

### 🎂 Birthdays
Never miss an event.

| Command | Usage | Description |
|:---|:---|:---|
| **days_to_bday**| `days_to_bday <name>` | Check days until a specific birthday. |
| **birthdays** | `birthdays [days]` | Show rich table of upcoming birthdays (default 7 days). |

### 💾 System & Data
| Command | Usage | Description |
|:---|:---|:---|
| **import** | `import <file.json/csv>` | Import data from a file. |
| **export** | `export <file.json/csv>` | Export address book to file. |
| **delete_all** | `delete_all` | **Wipe** all data (requires confirmation). |
| **help** | `help` | Show the interactive command menu. |
| **exit / close**| `exit` | Save data and close the bot. |

---

## 🎭 Gamified Experience
Errors don't have to be boring! This bot features a **Gamified Error System**. 
If you enter invalid data (like a bad phone number), the bot handles it gracefully with a unique, randomized message:
- *Alien frequencies for bad phones* 👽
- *Sherlock Holmes missing contacts* 🕵️‍♂️
- *Time travel paradoxes for bad dates* 🕰️

## ⚠️ Common Rules
- **Phones**: Must be 10-12 digits. International format `+380...` is preferred.
- **Emails**: Validated against standard email patterns.
- **Dates**: Strict `DD-MM-YYYY` format.
- **Persistence**: Data is **automatically saved** to `user_address_book/contacts.json` on exit.
