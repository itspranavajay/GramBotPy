from dataclasses import dataclass
from typing import Optional
from datetime import datetime
from .chat import Chat
from .user import User
from .chat_invite_link import ChatInviteLink


@dataclass
class ChatJoinRequest:
    """
    Represents a join request sent to a chat.
    """
    chat: Chat
    """Chat to which the request was sent"""
    
    from_user: User
    """User that sent the join request"""
    
    date: int
    """Date the request was sent in Unix time"""
    
    bio: Optional[str] = None
    """Optional. Bio of the user"""
    
    invite_link: Optional[ChatInviteLink] = None
    """Optional. Chat invite link that was used by the user to send the join request""" 