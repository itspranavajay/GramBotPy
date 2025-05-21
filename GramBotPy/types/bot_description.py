from dataclasses import dataclass

@dataclass
class BotDescription:
    """This object represents a bot's description.
    
    Attributes:
        description (``str``):
            The bot's description.
    """
    
    description: str
    
    @classmethod
    def _parse(cls, client, description_data: dict):
        """Parse a BotDescription object from the Telegram API response."""
        if not description_data:
            return None
            
        return cls(
            description=description_data.get("description")
        )
        
    def to_dict(self):
        """Convert the BotDescription object to a dictionary."""
        return {
            "description": self.description
        } 