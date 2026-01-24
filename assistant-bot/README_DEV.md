# 🛠 Assistant Bot - Developer Guide

## Architecture Overview
The project is structured as a modular Python package `assistant_bot` following a **Model-View-Controller (MVC)** inspired pattern, adapted for CLI.
- **Model (`storage.py`)**: `AddressBook` class holding state and enforcing business logic.
- **View (`console.py`, `commands.py`)**: Handles output validation and formatting.
- **Controller (`commands.py`, `app.py`)**: Routes input commands to model methods.

### Directory Structure
```
assistant_bot/
├── run.py                  # MAIN ENTRY POINT
├── assistant_bot/
│   ├── app.py              # Main Loop (PromptSession)
│   ├── config.py           # Centralized Configuration (Paths, Defaults)
│   ├── commands.py         # Command Handling & Presentation Layer
│   ├── storage.py          # Data Model & Persistence (JSON)
│   ├── features/           # pluggable Feature Modules
│   │   ├── birthdays.py    # Date calculations
│   │   ├── notes.py        # Notes logic
│   │   ├── tags.py         # Tagging logic
│   │   └── import_export.py# External file handling
│   └── utils/
│       ├── console.py      # Rich output
│       ├── ux_messages.py  # Gamified string constants
│       └── validators.py   # Regex patterns
```

## Storage Layer (`storage.py`)
- **Format**: Valid **JSON** (`contacts.json`).
- **Mechanism**: The `AddressBook` class uses `json.dump` / `json.load`.
- **Persistence**: Data is automatically saved upon exit via `save_address_book`.
- **Why JSON?**: It is human-readable, portable, and avoids the security risks of `pickle`.

## Business Logic Layer
Core logic is encapsulated in the `AddressBook` class in `storage.py`.
- **Validation**: Logic methods like `add_contact` or `update_phone` ensure data consistency.
- **Separation**: The `AddressBook` does *not* print to the console. It returns results or raises exceptions.
- **Smart Merge**: `add_contact` detects duplicates and merges new phones/emails instead of creating duplicates.

## Command Handling Layer (`commands.py`)
- **Role**: Validates user input arguments, calls method on `AddressBook`, and pretty-prints the result.
- **Gamification**: Catches exceptions (e.g. `KeyError`) and prints funny error messages from `ux_messages.py`.

## Configuration Management (`config.py`)
Centralized place for all tunable constants.
- `JSON_STORAGE_PATH`: Path to the DB file.
- `DEFAULT_BIRTHDAY_LOOKAHEAD_DAYS`: Default range for `birthdays` command (21).
- `AUTO_HELP_THRESHOLD`: How many errors before auto-showing help.

## Separation of Concerns
1. **Business Logic** (`storage.py`, `features/`): Pure Python functions/methods. No `print()`.
2. **Presentation** (`commands.py`, `utils/console.py`): Handles `Rich` tables, colors, and user feedback.

## Extending the Project
- **New Command**: Add a function in `commands.py` with `@command("name")`. Call a method on `book`.
- **New Config**: Add constant to `config.py`, import where needed. Do not hardcode values.
