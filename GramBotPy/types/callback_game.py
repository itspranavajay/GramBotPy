from dataclasses import dataclass

@dataclass
class CallbackGame:
    """A placeholder, currently holds no information.
    
    Use BotFather to set up your game.
    """
    
    @classmethod
    def _parse(cls, client, _):
        """Parse a callback game object from the Telegram API response."""
        return cls()
        
    def to_dict(self):
        """Convert the CallbackGame object to a dictionary."""
        return {} 