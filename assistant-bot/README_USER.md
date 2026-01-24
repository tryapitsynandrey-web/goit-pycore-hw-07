# 🤖 Assistant Bot (CLI v5)

Welcome to the **Assistant Bot**, your professional CLI companion for managing contacts, notes, and tasks. This version is fully refactored for robustness, valid data handling, and a premium user experience.

## 🚀 Installation & Launch

### Prerequisites
- Python 3.8 or higher
- `pip` package manager

### Setup
1. **Clone or Download** the repository.
2. **Install Dependencies** (Critical for the Beautiful UI 🎨):
   To see the colorful tables, panels, and interactive menus (just like in the screenshots), you **must** install the libraries listed in the requirements file.
   ```bash
   pip install -r assistant-bot/requirements.txt
   ```
   *Included Libraries:*
   - `rich`: Renders the beautiful tables, colors, and panels.
   - `prompt_toolkit`: Handles the interactive input.

### Running the Bot
The only entry point is `run.py`. Execute it from the project root:
```bash
python run.py
```
You will see the interactive prompt: `bot>`.

---

## 📖 Feature Guide

### 📇 Contact Management
Manage your personal address book with validation.

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
| **search** | `search <query>` | Search contacts by name, phone, or email. |
| **list** | `list` | Show a beautiful **Rich Table** of all contacts. |
| **filter_by_tag**| `filter_by_tag <tag>` | Show a rich table of contacts with this tag (includes days to bday!). |

> **Note on Merging:** If you `add` a contact that already exists (e.g., "John"), the bot will **smartly update** them by adding the new phone/email instead of showing an error. Duplicate phones for *different* people are still blocked.

### 📝 Notes Management
Keep track of ideas and tasks.

| Command | Usage | Description |
|:---|:---|:---|
| **add_note** | `add_note <name> <text>` | Add a note to a contact. |
| **edit_note** | `edit_note <name> <idx> <text>` | Edit a specific note (by index). |
| **delete_note** | `delete_note <name> <idx>` | Delete a specific note. |
| **search_notes**| `search_notes <query>` | Search through all notes text. |
| **list_notes** | `list_notes [name]` | List notes for a person (or all). |

### 🏷️ Tags & Extras
Organize contacts and check events.

| Command | Usage | Description |
|:---|:---|:---|
| **add_tag** | `add_tag <name> <tag>` | Tag a contact (e.g., "work", "friend"). |
| **remove_tag** | `remove_tag <name> <tag>` | Remove a tag. |
| **filter_by_tag**| `filter_by_tag <tag>` | List all contacts with a specific tag. |
| **days_to_bday**| `days_to_bday <name>` | Check days until a specific birthday. |
| **days_to_bday**| `days_to_bday <name>` | Check days until a specific birthday. |
| **birthdays** | `birthdays [days]` | Show rich table of upcoming birthdays (default 21 days). Includes tags! |

### 💾 Data & System
| Command | Usage | Description |
|:---|:---|:---|
| **import** | `import <file.json/csv>` | Import data from a file. |
| **export** | `export <file.json/csv>` | Export address book to file. |
| **help** | `help` | Show the interactive command menu. |
| **exit / close**| `exit` | Save data and close the bot. |

---

## 🎭 Gamified Experience
Errors don't have to be boring! This bot features a **Gamified Error System**. 
If you make a typo or enter invalid data, the bot will respond with one of **50+ unique, funny messages** chosen at random. 
- *Alien frequencies for bad phones* 👽
- *Sherlock Holmes missing contacts* 🕵️‍♂️
- *Time travel paradoxes for bad dates* 🕰️

## ⚠️ Common Errors & Tips
- **Validation**: Phones must be 7-15 digits. Emails must be valid format. Dates must be `DD-MM-YYYY`.
- **Search**: Search is case-insensitive.
- **Persistence**: Data is **automatically saved** to `user_address_book/contacts.json` and `contacts.csv` when you exit. Do not force close the terminal if possible.
