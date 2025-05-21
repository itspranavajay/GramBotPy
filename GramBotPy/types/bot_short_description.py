from dataclasses import dataclass

@dataclass
class BotShortDescription:
    """This object represents a bot's short description.
    
    Attributes:
        short_description (``str``):
            The bot's short description.
    """
    
    short_description: str
    
    @classmethod
    def _parse(cls, client, description_data: dict):
        """Parse a BotShortDescription object from the Telegram API response."""
        if not description_data:
            return None
            
        return cls(
            short_description=description_data.get("short_description")
        )
        
    def to_dict(self):
        """Convert the BotShortDescription object to a dictionary."""
        return {
            "short_description": self.short_description
        } 