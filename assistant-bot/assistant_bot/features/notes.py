def add_note(address_book, contact_name: str, note_text: str):
    """Adds a new text note to the specified contact."""
    if contact_name not in address_book.contacts:
        raise KeyError('Contact not found')
    address_book.notes.setdefault(contact_name, []).append(note_text)


def edit_note(address_book, contact_name: str, index: int, new_text: str):
    """
    Edits an existing note by its index (0-based).
    Raises IndexError/ValueError implicitly if index is invalid (handled by caller).
    """
    notes = address_book.notes.get(contact_name, [])
    notes[index] = new_text


def delete_note(address_book, contact_name: str, index: int):
    """Deletes a note at the specified index."""
    notes = address_book.notes.get(contact_name, [])
    if 0 <= index < len(notes):
        notes.pop(index)


def list_notes(address_book, contact_name: str):
    """
    Returns notes for a specific contact, or all notes if contact_name is None.
    Structure: {name: [notes]}
    """
    if contact_name:
        return address_book.notes.get(contact_name, [])
    return address_book.notes


__all__ = ['add_note', 'edit_note', 'delete_note', 'list_notes']
