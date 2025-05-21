from dataclasses import dataclass
from typing import Optional, Dict, Any, List

@dataclass
class Chat:
    """This object represents a chat.
    
    Parameters:
        id (``int``):
            Unique identifier for this chat.
            
        type (``str``):
            Type of chat, can be "private", "group", "supergroup", or "channel".
            
        title (``str``, optional):
            Title, for supergroups, channels and group chats.
            
        username (``str``, optional):
            Username, for private chats, supergroups and channels if available.
            
        first_name (``str``, optional):
            First name of the other party in a private chat.
            
        last_name (``str``, optional):
            Last name of the other party in a private chat.
            
        photo (``dict``, optional):
            Chat photo. Returned only in getChat.
            
        bio (``str``, optional):
            Bio of the other party in a private chat. Returned only in getChat.
            
        description (``str``, optional):
            Description, for supergroups and channel chats. Returned only in getChat.
            
        invite_link (``str``, optional):
            Chat invite link, for supergroups and channel chats. Returned only in getChat.
            
        pinned_message (``dict``, optional):
            The most recent pinned message. Returned only in getChat.
            
        permissions (``dict``, optional):
            Default chat member permissions. Returned only in getChat.
            
        slow_mode_delay (``int``, optional):
            For supergroups, the minimum allowed delay between consecutive messages.
            
        message_auto_delete_time (``int``, optional):
            The time after which all messages sent to the chat will be automatically deleted.
            
        has_protected_content (``bool``, optional):
            True, if messages from the chat can't be forwarded to other chats.
            
        sticker_set_name (``str``, optional):
            For supergroups, name of the group sticker set.
            
        can_set_sticker_set (``bool``, optional):
            True, if the bot can change the group sticker set.
            
        linked_chat_id (``int``, optional):
            For supergroups, the linked chat ID.
            
        location (``dict``, optional):
            For supergroups, the location to which the supergroup is connected.
    """
    
    id: int
    type: str
    title: Optional[str] = None
    username: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    photo: Optional[Dict[str, Any]] = None
    bio: Optional[str] = None
    description: Optional[str] = None
    invite_link: Optional[str] = None
    pinned_message: Optional[Dict[str, Any]] = None
    permissions: Optional[Dict[str, Any]] = None
    slow_mode_delay: Optional[int] = None
    message_auto_delete_time: Optional[int] = None
    has_protected_content: Optional[bool] = None
    sticker_set_name: Optional[str] = None
    can_set_sticker_set: Optional[bool] = None
    linked_chat_id: Optional[int] = None
    location: Optional[Dict[str, Any]] = None
    
    def __post_init__(self):
        # Convert pinned_message to Message object if needed
        # This would happen in a real implementation
        pass
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Chat":
        """Create a Chat object from a dictionary.
        
        Parameters:
            data (``dict``):
                The dictionary containing the chat data.
                
        Returns:
            :obj:`Chat`: The chat object.
        """
        return cls(**data)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert the object to a dict suitable for JSON serialization."""
        return {k: v for k, v in self.__dict__.items() if v is not None and not k.startswith('_')} 