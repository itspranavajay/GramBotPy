from dataclasses import dataclass
from typing import Optional, List
from .user import User
from .location import Location


@dataclass
class InlineQuery:
    """
    This object represents an incoming inline query.
    When the user sends an empty query, your bot could return some default or trending results.
    """
    id: str
    """Unique identifier for this query"""
    
    from_user: User
    """Sender"""
    
    query: str
    """Text of the query (up to 256 characters)"""
    
    offset: str
    """Offset of the results to be returned, can be controlled by the bot"""
    
    chat_type: Optional[str] = None
    """Optional. Type of the chat, from which the inline query was sent."""
    
    location: Optional[Location] = None
    """Optional. Sender location, only for bots that request user location""" 