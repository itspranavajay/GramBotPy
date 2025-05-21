from dataclasses import dataclass
from typing import Optional

@dataclass
class Contact:
    """This object represents a phone contact.
    
    Parameters:
        phone_number (``str``):
            Contact's phone number.
            
        first_name (``str``):
            Contact's first name.
            
        last_name (``str``, optional):
            Contact's last name.
            
        user_id (``int``, optional):
            Contact's user identifier in Telegram.
            
        vcard (``str``, optional):
            Additional data about the contact in the form of a vCard.
    """
    
    phone_number: str
    first_name: str
    last_name: Optional[str] = None
    user_id: Optional[int] = None
    vcard: Optional[str] = None 