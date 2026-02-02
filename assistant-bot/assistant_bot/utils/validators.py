import re

# Constants
# Strict Ukrainian phone format: +38 followed by 10 digits
PHONE_VALIDATION_PATTERN = r'^\+38\d{10}$'
# Basic email validation: Must contain @ and . with no spaces
EMAIL_VALIDATION_PATTERN = r'^[^@\s]+@[^@\s]+\.[^@\s]+$'


def normalize_phone(phone: str) -> str:
    """
    Normalizes a phone number to the standard +38 format.
    
    Args:
        phone: Raw phone number string.
        
    Returns:
        Normalized phone string starting with '+'.
    """
    if not phone:
        return ''
    
    # Remove all non-digit characters
    digits = re.sub(r"\D", "", phone)
    
    # Case 1: 10 digits (e.g. 0501234567) -> Add +38 (Implicit UA)
    if len(digits) == 10:
        return f"+38{digits}"
    
    # Case 2: 12 digits (e.g. 380501234567) -> Add + (Explicit UA or other)
    if len(digits) == 12:
        return f"+{digits}"
        
    # Fallback: Return with '+' prefix to attempt validation later
    return f"+{digits}"


def validate_phone(phone: str) -> bool:
    """
    Validates if a phone number matches the strict strict Ukrainian format (+380...).
    
    Args:
        phone: Raw phone number string.
        
    Returns:
        True if valid, False otherwise.
    """
    normalized_phone = normalize_phone(phone)
    return bool(re.match(PHONE_VALIDATION_PATTERN, normalized_phone))


def validate_email(email: str) -> bool:
    """
    Validates an email address using a strict regex pattern.
    
    Args:
        email: Email address string.
        
    Returns:
        True if valid, False otherwise.
    """
    if not email:
        return False
        
    return bool(re.match(EMAIL_VALIDATION_PATTERN, email))


__all__ = ['normalize_phone', 'validate_phone', 'validate_email']
