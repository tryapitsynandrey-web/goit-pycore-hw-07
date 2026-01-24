def add_tag(address_book, contact_name: str, tag: str):
    """Adds a tag to a contact if it doesn't already exist."""
    if contact_name not in address_book.contacts:
        raise KeyError('Contact not found')
    address_book.tags.setdefault(contact_name, [])
    if tag not in address_book.tags[contact_name]:
        address_book.tags[contact_name].append(tag)


def remove_tag(address_book, contact_name: str, tag: str):
    """Removes a specific tag from a contact."""
    tags = address_book.tags.get(contact_name, [])
    if tag in tags:
        tags.remove(tag)


def list_tags(address_book):
    """Returns the entire tags dictionary {name: [tags]}."""
    return address_book.tags


def filter_by_tag(address_book, tag: str):
    """Returns a list of contact names that have the specified tag."""
    return [name for name, tags in address_book.tags.items() if tag in tags]


__all__ = ['add_tag', 'remove_tag', 'list_tags', 'filter_by_tag']
