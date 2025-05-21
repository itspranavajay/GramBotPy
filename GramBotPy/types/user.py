from dataclasses import dataclass
from typing import Optional

@dataclass
class User:
    """This object represents a Telegram user or bot.
    
    Parameters:
        id (``int``):
            Unique identifier for this user or bot.
            
        is_bot (``bool``):
            True, if this user is a bot.
            
        first_name (``str``):
            User's or bot's first name.
            
        last_name (``str``, optional):
            User's or bot's last name.
            
        username (``str``, optional):
            User's or bot's username.
            
        language_code (``str``, optional):
            IETF language tag of the user's language.
            
        is_premium (``bool``, optional):
            True, if this user is a Telegram Premium user.
            
        added_to_attachment_menu (``bool``, optional):
            True, if this user added the bot to the attachment menu.
            
        can_join_groups (``bool``, optional):
            True, if the bot can be invited to groups. Returned only in getMe.
            
        can_read_all_group_messages (``bool``, optional):
            True, if privacy mode is disabled for the bot. Returned only in getMe.
            
        supports_inline_queries (``bool``, optional):
            True, if the bot supports inline queries. Returned only in getMe.
    """
    
    id: int
    is_bot: bool
    first_name: str
    last_name: Optional[str] = None
    username: Optional[str] = None
    language_code: Optional[str] = None
    is_premium: Optional[bool] = None
    added_to_attachment_menu: Optional[bool] = None
    can_join_groups: Optional[bool] = None
    can_read_all_group_messages: Optional[bool] = None
    supports_inline_queries: Optional[bool] = None
    
    def __str__(self) -> str:
        """Return a string representation of the user."""
        if self.username:
            return f"@{self.username}"
        else:
            return self.full_name
    
    @property
    def full_name(self) -> str:
        """Get the user's full name.
        
        Returns:
            ``str``: The user's full name.
        """
        if self.last_name:
            return f"{self.first_name} {self.last_name}"
        return self.first_name
    
    @property
    def mention(self) -> str:
        """Get a text mention for this user.
        
        Returns:
            ``str``: The text mention for this user.
        """
        return f"[{self.full_name}](tg://user?id={self.id})" 