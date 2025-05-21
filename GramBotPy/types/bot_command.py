from dataclasses import dataclass

@dataclass
class BotCommand:
    """This object represents a bot command.
    
    Attributes:
        command (``str``):
            Text of the command; 1-32 characters. Can contain only lowercase
            English letters, digits and underscores.
            
        description (``str``):
            Description of the command; 1-256 characters.
    """
    
    command: str
    description: str
    
    @classmethod
    def _parse(cls, client, command_data: dict):
        """Parse a BotCommand object from the Telegram API response."""
        if not command_data:
            return None
            
        return cls(
            command=command_data.get("command"),
            description=command_data.get("description")
        )
        
    def to_dict(self):
        """Convert the BotCommand object to a dictionary."""
        return {
            "command": self.command,
            "description": self.description
        } 