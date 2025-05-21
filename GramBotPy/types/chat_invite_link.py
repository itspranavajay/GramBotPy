from dataclasses import dataclass
import typing
from datetime import datetime

@dataclass
class ChatInviteLink:
    """This object represents an invite link for a chat.
    
    Attributes:
        invite_link (``str``):
            The invite link. If the link was created by another chat administrator, 
            then the second part of the link will be replaced with "...".
            
        creator (``User``):
            Creator of the link.
            
        creates_join_request (``bool``):
            True, if users joining the chat via the link need to be approved 
            by chat administrators.
            
        is_primary (``bool``):
            True, if the link is primary.
            
        is_revoked (``bool``):
            True, if the link is revoked.
            
        name (``str``, optional):
            Invite link name.
            
        expire_date (``datetime``, optional):
            Point in time (Unix timestamp) when the link will expire or has been expired.
            
        member_limit (``int``, optional):
            The maximum number of users that can be members of the chat 
            simultaneously after joining the chat via this invite link; 1-99999.
            
        pending_join_request_count (``int``, optional):
            Number of pending join requests created using this link.
    """
    
    invite_link: str
    creator: "User"
    creates_join_request: bool
    is_primary: bool
    is_revoked: bool
    name: str = None
    expire_date: datetime = None
    member_limit: int = None
    pending_join_request_count: int = None
    
    @classmethod
    def _parse(cls, client, link_data: dict):
        """Parse a ChatInviteLink object from the Telegram API response."""
        if not link_data:
            return None
            
        # Import here to avoid circular import
        from .user import User
        
        # Convert expire_date from unix timestamp to datetime if present
        expire_date = link_data.get("expire_date")
        if expire_date:
            expire_date = datetime.fromtimestamp(expire_date)
            
        return cls(
            invite_link=link_data.get("invite_link"),
            creator=User._parse(client, link_data.get("creator")),
            creates_join_request=link_data.get("creates_join_request"),
            is_primary=link_data.get("is_primary"),
            is_revoked=link_data.get("is_revoked"),
            name=link_data.get("name"),
            expire_date=expire_date,
            member_limit=link_data.get("member_limit"),
            pending_join_request_count=link_data.get("pending_join_request_count")
        )
    
    def to_dict(self):
        """Convert the ChatInviteLink object to a dictionary."""
        result = {
            "invite_link": self.invite_link,
            "creator": self.creator.to_dict(),
            "creates_join_request": self.creates_join_request,
            "is_primary": self.is_primary,
            "is_revoked": self.is_revoked
        }
        
        if self.name:
            result["name"] = self.name
            
        if self.expire_date:
            result["expire_date"] = int(self.expire_date.timestamp())
            
        if self.member_limit is not None:
            result["member_limit"] = self.member_limit
            
        if self.pending_join_request_count is not None:
            result["pending_join_request_count"] = self.pending_join_request_count
            
        return result 