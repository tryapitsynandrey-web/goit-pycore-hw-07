# 🛠 Assistant Bot - Developer Guide

## Architecture Overview
The project follows a **Domain-Driven Design (DDD)** approach adapted for a CLI application. It emphasizes strict separation of concerns, data integrity via encapsulation, and a clear "Model-View-Controller" flow.

### Layers
1.  **Domain Model (`models.py`)**: The core logic. Defines `Record`, `AddressBook`, and `Field` variants.
    *   **Responsibility**: Data structure, validation, invariants, business logic (e.g., `days_to_birthday`).
    *   **Encapsulation**: Critical lists (`_phones`, `_tags`) are private. Access is provided via read-only properties (`self.phones`) to prevent external mutation.
2.  **Infrastructure / Persistence (`storage.py`)**: Handles saving and loading data.
    *   **Responsibility**: Serializing `AddressBook` to JSON. Mapped to `user_address_book/contacts.json`.
3.  **Controller (`commands.py`, `app.py`)**:
    *   `app.py`: Main event loop using `prompt_toolkit`. Handles autocomplete and session management.
    *   `commands.py`: Command handlers. Parses input, calls Model methods, and handles exceptions.
4.  **Presentation / View (`utils/console.py`, `utils/ux_messages.py`)**:
    *   **Responsibility**: Formatting output (Rich tables), printing success/error messages.
    *   **Gamification**: Error messages are randomized from `ux_messages.py` to provide a fun UX.

### Directory Structure
```
assistant_bot/
├── run.py                 # MAIN ENTRY POINT
├── assistant_bot/
│   ├── app.py             # Application Loop & Autocomplete
│   ├── config.py          # Configuration Constants
│   ├── commands.py        # Command Handlers & Dispatcher
│   ├── models.py          # DOMAIN MODEL (DDD)
│   ├── storage.py         # Persistence (JSON)
│   ├── features/
│   │   └── import_export.py # CSV/JSON Import/Export logic
│   └── utils/
│       ├── console.py     # Rich Console Wrappers
│       ├── ux_messages.py # Message Constants
│       └── validators.py  # Regex Helpers
```

## Domain Model (`models.py`)
This is the heart of the application.
*   **Record**: Represents a contact.
    *   **Invariants**: Name cannot be empty.
    *   **Strict Encapsulation**: `add_phone`, `remove_tag` etc. are the *only* way to modify state. valid `Phone` and `Email` objects are created internally.
*   **AddressBook**: A container for records (inherits `UserDict`).
    *   **Methods**: `find_by_tag`, `get_upcoming_birthdays`, `get_unique_tags` (optimized for autocomplete).

## Data Flow
1.  **User Input** (`bot> add Bob`) -> **App** (`prompt_toolkit`).
2.  **App** passes input to `commands.dispatch`.
3.  **Dispatcher** finds handler (`handle_add`).
4.  **Handler** calls **Model** (`book.add_record`).
5.  **Model** validates and updates state.
6.  **Handler** gets success/error -> calls **Console** (`print_success`).
7.  **Console** picks random message from `ux_messages.py` and renders it.

## Development Standards
*   **Type Hinting**: All functions must have Python 3.10+ type hints.
*   **Docstrings**: Mandatory for all public classes/functions.
*   **Encapsulation**: Never access `_private` attributes outside the class. Use strict methods.
*   **Output**: Do not use `print()`. Use `assistant_bot.utils.console` functions.

## Adding Features
1.  **Model**: Add logic to `Record` or `AddressBook` in `models.py`.
2.  **Command**: Create a handler in `commands.py` decorated with `@command`.
3.  **UI**: Add new message constants to `ux_messages.py` if needed.

## Testing & Verification
Currently, the project relies on **manual verification**. When modifying code, run the following smoke tests:
1.  **Startup**: Run `python run.py`. Ensure no import errors.
2.  **Add Contact**: `add TestUser +380501234567`. Check for success message.
3.  **Tags**: `add_tag TestUser "Test Tag"`. Verify via `filter_by_tag`.
4.  **Persistence**: `exit` the bot, restart, and `list` to ensure data remains.
