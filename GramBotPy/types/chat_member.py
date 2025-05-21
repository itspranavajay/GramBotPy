from dataclasses import dataclass
from typing import Optional, Dict, Any, Union

@dataclass
class ChatMember:
    """This object contains information about one member of a chat.
    
    Parameters:
        status (``str``):
            The member's status in the chat, can be "creator", "administrator", 
            "member", "restricted", "left" or "kicked".
            
        user (``dict``):
            Information about the user.
            
        custom_title (``str``, optional):
            Owner and administrators only. Custom title for this user.
            
        is_anonymous (``bool``, optional):
            Owner and administrators only. True, if the user's presence in the chat is hidden.
            
        can_be_edited (``bool``, optional):
            Administrators only. True, if the bot is allowed to edit administrator privileges of that user.
            
        can_manage_chat (``bool``, optional):
            Administrators only. True, if the administrator can access the chat event log, 
            chat statistics, etc.
            
        can_post_messages (``bool``, optional):
            Administrators only. True, if the administrator can post in the channel.
            
        can_edit_messages (``bool``, optional):
            Administrators only. True, if the administrator can edit messages of other users.
            
        can_delete_messages (``bool``, optional):
            Administrators only. True, if the administrator can delete messages of other users.
            
        can_restrict_members (``bool``, optional):
            Administrators only. True, if the administrator can restrict, ban or unban chat members.
            
        can_promote_members (``bool``, optional):
            Administrators only. True, if the administrator can add new administrators.
            
        can_change_info (``bool``, optional):
            Administrators and restricted only. True, if the user is allowed to change the chat title, 
            photo and other settings.
            
        can_invite_users (``bool``, optional):
            Administrators and restricted only. True, if the user is allowed to invite new users to the chat.
            
        can_pin_messages (``bool``, optional):
            Administrators and restricted only. True, if the user is allowed to pin messages.
            
        can_manage_voice_chats (``bool``, optional):
            Administrators only. True, if the administrator can manage voice chats.
            
        is_member (``bool``, optional):
            Restricted only. True, if the user is a member of the chat at the moment of the request.
            
        can_send_messages (``bool``, optional):
            Restricted only. True, if the user is allowed to send text messages, contacts, 
            locations and venues.
            
        can_send_media_messages (``bool``, optional):
            Restricted only. True, if the user is allowed to send audios, documents, photos, 
            videos, video notes and voice notes.
            
        can_send_polls (``bool``, optional):
            Restricted only. True, if the user is allowed to send polls.
            
        can_send_other_messages (``bool``, optional):
            Restricted only. True, if the user is allowed to send animations, games, stickers 
            and use inline bots.
            
        can_add_web_page_previews (``bool``, optional):
            Restricted only. True, if the user is allowed to add web page previews to their messages.
            
        until_date (``int``, optional):
            Restricted and kicked only. Date when restrictions will be lifted for this user, 
            unix time.
    """
    
    status: str
    user: Dict[str, Any]
    custom_title: Optional[str] = None
    is_anonymous: Optional[bool] = None
    can_be_edited: Optional[bool] = None
    can_manage_chat: Optional[bool] = None
    can_post_messages: Optional[bool] = None
    can_edit_messages: Optional[bool] = None
    can_delete_messages: Optional[bool] = None
    can_restrict_members: Optional[bool] = None
    can_promote_members: Optional[bool] = None
    can_change_info: Optional[bool] = None
    can_invite_users: Optional[bool] = None
    can_pin_messages: Optional[bool] = None
    can_manage_voice_chats: Optional[bool] = None
    is_member: Optional[bool] = None
    can_send_messages: Optional[bool] = None
    can_send_media_messages: Optional[bool] = None
    can_send_polls: Optional[bool] = None
    can_send_other_messages: Optional[bool] = None
    can_add_web_page_previews: Optional[bool] = None
    until_date: Optional[int] = None
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "ChatMember":
        """Create a ChatMember object from a dictionary.
        
        Parameters:
            data (``dict``):
                The dictionary containing the chat member data.
                
        Returns:
            :obj:`ChatMember`: The chat member object.
        """
        return cls(**data)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert the object to a dict suitable for JSON serialization."""
        return {k: v for k, v in self.__dict__.items() if v is not None} 