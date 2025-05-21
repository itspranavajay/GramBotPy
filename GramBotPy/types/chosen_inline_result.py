from dataclasses import dataclass
from typing import Optional
from .user import User
from .location import Location


@dataclass
class ChosenInlineResult:
    """
    Represents a result of an inline query that was chosen by the user and sent to their chat partner.
    """
    result_id: str
    """The unique identifier for the result that was chosen"""
    
    from_user: User
    """The user that chose the result"""
    
    query: str
    """The query that was used to obtain the result"""
    
    location: Optional[Location] = None
    """Optional. Sender location, only for bots that require user location"""
    
    inline_message_id: Optional[str] = None
    """Optional. Identifier of the sent inline message.
    Available only if there is an inline keyboard attached to the message.
    Will be also received in callback queries and can be used to edit the message.""" 