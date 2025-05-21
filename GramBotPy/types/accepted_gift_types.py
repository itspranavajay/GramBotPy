from dataclasses import dataclass

@dataclass
class AcceptedGiftTypes:
    """This object represents the types of gifts that are accepted by a user or chat.
    
    Attributes:
        regular (``bool``):
            True, if the user accepts regular gifts.
            
        unique (``bool``):
            True, if the user accepts unique gifts.
    """
    
    regular: bool
    unique: bool
    
    @classmethod
    def _parse(cls, client, types_data: dict):
        """Parse an AcceptedGiftTypes object from the Telegram API response."""
        if not types_data:
            return None
            
        return cls(
            regular=types_data.get("regular", False),
            unique=types_data.get("unique", False)
        )
        
    def to_dict(self):
        """Convert the AcceptedGiftTypes object to a dictionary."""
        return {
            "regular": self.regular,
            "unique": self.unique
        } 