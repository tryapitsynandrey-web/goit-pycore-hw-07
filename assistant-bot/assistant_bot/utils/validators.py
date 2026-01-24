import re


def normalize_phone(phone: str) -> str:
    if not phone:
        return ''
    
    # Remove all non-digits
    digits = re.sub(r"\D", "", phone)
    
    # Case 1: 10 digits (e.g. 0501234567) -> Add +38
    if len(digits) == 10:
        return f"+38{digits}"
    
    # Case 2: 12 digits (e.g. 380501234567) -> Add +
    if len(digits) == 12:
        return f"+{digits}"
        
    # Other cases (invalid length for strict UA) -> return simple +digits or raw
    # But for compatibility, let's just return +digits if it looks long enough, 
    # OR we can let validation fail.
    # The requirement implicitly asks to "record +38 and all 10 digits".
    return f"+{digits}"


def validate_phone(phone: str) -> bool:
    # 1. Normalize
    norm = normalize_phone(phone)
    
    # 2. Strict check: Must start with +38 and have 12 digits total (country code 38 + 10 digits)
    # Allows +380... (mobile) or +384... (landline/other) as long as length is correct.
    return bool(re.match(r"^\+38\d{10}$", norm))


def validate_email(email: str) -> bool:
    if not email:
        return False
    # Simple regex for validation
    pattern = r'^[^@\s]+@[^@\s]+\.[^@\s]+'
    return re.match(pattern, email) is not None


__all__ = ['normalize_phone', 'validate_phone', 'validate_email']
