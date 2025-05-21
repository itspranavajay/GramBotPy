from dataclasses import dataclass

@dataclass
class BusinessBotRights:
    """This object represents a bot's rights in a business account.
    
    Attributes:
        can_manage_chat (``bool``):
            True, if the bot can manage the business account's chat settings.
            
        can_manage_messages (``bool``):
            True, if the bot can read and manage messages in the business account.
            
        can_delete_messages (``bool``):
            True, if the bot can delete messages in the business account.
            
        can_manage_stories (``bool``):
            True, if the bot can create and manage stories for the business account.
            
        can_manage_profile (``bool``):
            True, if the bot can manage the business account's profile information.
            
        can_manage_gifts (``bool``):
            True, if the bot can manage gifts received by the business account.
            
        can_manage_stars (``bool``):
            True, if the bot can manage and transfer Telegram Stars from the business account.
    """
    
    can_manage_chat: bool
    can_manage_messages: bool
    can_delete_messages: bool
    can_manage_stories: bool
    can_manage_profile: bool
    can_manage_gifts: bool
    can_manage_stars: bool
    
    @classmethod
    def _parse(cls, client, rights_data: dict):
        """Parse a BusinessBotRights object from the Telegram API response."""
        if not rights_data:
            return None
            
        return cls(
            can_manage_chat=rights_data.get("can_manage_chat", False),
            can_manage_messages=rights_data.get("can_manage_messages", False),
            can_delete_messages=rights_data.get("can_delete_messages", False),
            can_manage_stories=rights_data.get("can_manage_stories", False),
            can_manage_profile=rights_data.get("can_manage_profile", False),
            can_manage_gifts=rights_data.get("can_manage_gifts", False),
            can_manage_stars=rights_data.get("can_manage_stars", False)
        )
        
    def to_dict(self):
        """Convert the BusinessBotRights object to a dictionary."""
        return {
            "can_manage_chat": self.can_manage_chat,
            "can_manage_messages": self.can_manage_messages,
            "can_delete_messages": self.can_delete_messages,
            "can_manage_stories": self.can_manage_stories,
            "can_manage_profile": self.can_manage_profile,
            "can_manage_gifts": self.can_manage_gifts,
            "can_manage_stars": self.can_manage_stars
        } 