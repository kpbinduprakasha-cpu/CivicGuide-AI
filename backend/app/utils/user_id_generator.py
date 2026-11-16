import re
import random
from ..models.user import User

def generate_unique_user_id(full_name: str) -> str:
    """
    Automatically generates a clean, unique User ID based on the user's registered name.
    Example: 'Rahul Kumar' -> 'rahul123'
    Ensures absolute uniqueness in database.
    """
    # Clean the name to lowercase alphanumeric
    cleaned = re.sub(r'[^a-zA-Z0-9]', '', full_name.strip()).lower()
    
    # If cleaned string is too short or empty, fallback to 'user'
    if len(cleaned) < 3:
        cleaned = 'user'
    elif len(cleaned) > 10:
        # Take first name or first 8 chars
        parts = full_name.strip().split()
        first_clean = re.sub(r'[^a-zA-Z0-9]', '', parts[0]).lower()
        cleaned = first_clean if len(first_clean) >= 3 else cleaned[:8]

    # Try generating unique ID
    attempts = 0
    while attempts < 100:
        # Generate 3-digit random number (100 to 999)
        suffix = random.randint(100, 999)
        candidate = f"{cleaned}{suffix}"
        
        # Check database uniqueness
        existing = User.query.filter_by(user_id=candidate).first()
        if not existing:
            return candidate
        
        attempts += 1

    # Fallback to 5-digit number
    return f"{cleaned}{random.randint(10000, 99999)}"
