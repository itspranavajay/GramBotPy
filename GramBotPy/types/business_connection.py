import typing
from dataclasses import dataclass
from .business_bot_rights import BusinessBotRights

@dataclass
class BusinessConnection:
    """This object represents a connection between a bot and a business account.
    
    Attributes:
        id (``str``):
            Unique identifier of the business connection.
            
        user_id (``int``):
            Identifier of the business account user.
            
        rights (``BusinessBotRights``):
            Rights that the bot has in the business account.
    """
    
    id: str
    user_id: int
    rights: BusinessBotRights
    
    @classmethod
    def _parse(cls, client, connection_data: dict):
        """Parse a BusinessConnection object from the Telegram API response."""
        if not connection_data:
            return None
            
        rights = BusinessBotRights._parse(client, connection_data.get("rights", {}))
        
        return cls(
            id=connection_data.get("id"),
            user_id=connection_data.get("user_id"),
            rights=rights
        )
        
    def to_dict(self):
        """Convert the BusinessConnection object to a dictionary."""
        return {
            "id": self.id,
            "user_id": self.user_id,
            "rights": self.rights.to_dict() if self.rights else None
        } 