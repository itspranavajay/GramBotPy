import typing
import json
import aiohttp
from typing import Union, Optional, Dict, Any
from datetime import datetime

from ...types import User, ChatMember

if typing.TYPE_CHECKING:
    from ...client import GramBotPy

class GetUserInfo:
    """Method for getting detailed information about a user."""
    
    async def get_user_info(
        self: "GramBotPy",
        chat_id: Union[int, str],
        user_id: int,
        include_profile_photos: Optional[bool] = False,
        fetch_status: Optional[bool] = False
    ) -> Dict[str, Any]:
        """Get detailed information about a user.
        
        Parameters:
            chat_id (``int`` | ``str``):
                Unique identifier for the target chat or username
                where the bot can access user information.
                
            user_id (``int``):
                Unique identifier of the target user.
                
            include_profile_photos (``bool``, optional):
                Whether to fetch the user's profile photos.
                
            fetch_status (``bool``, optional):
                Whether to fetch the user's status (online, offline, etc.).
                
        Returns:
            ``dict``: User information including membership status, 
            profile photos (if requested), and other available details.
            
        Example:
            .. code-block:: python
            
                # Get basic user info
                user_info = await bot.get_user_info(chat_id, user_id)
                
                # Get detailed user info with profile photos
                detailed_info = await bot.get_user_info(
                    chat_id, user_id, 
                    include_profile_photos=True,
                    fetch_status=True
                )
        """
        self.logger.info(f"Getting information for user {user_id} in chat {chat_id}")
        
        # Get chat member info first
        try:
            member_info = await self.get_chat_member(chat_id, user_id)
            
            # Build the user info dictionary
            user_info = {
                "user": member_info.user._raw, 
                "status": member_info.status,
                "membership_data": {
                    "is_member": member_info.status not in ["left", "kicked"],
                    "joined_date": getattr(member_info, "joined_date", None),
                    "permissions": self._extract_permissions(member_info),
                    "admin_rights": self._extract_admin_rights(member_info),
                    "is_restricted": member_info.status == "restricted",
                    "can_send_messages": getattr(member_info, "can_send_messages", None)
                },
                "profile_photos": None,
                "online_status": None
            }
            
            # Fetch profile photos if requested
            if include_profile_photos:
                photos = await self._get_user_profile_photos(user_id)
                user_info["profile_photos"] = photos
                
            # Fetch online status if requested (requires user bot, not available for normal bots)
            if fetch_status:
                try:
                    status = await self._get_user_status(user_id)
                    user_info["online_status"] = status
                except Exception as e:
                    self.logger.warning(f"Failed to get user status (may require user bot): {e}")
                    user_info["online_status"] = {"error": "Status unavailable for bot API"}
            
            return user_info
            
        except Exception as e:
            self.logger.error(f"Error getting user info: {e}", exc_info=True)
            return {
                "error": str(e),
                "user_id": user_id,
                "chat_id": chat_id,
                "timestamp": int(datetime.now().timestamp())
            }
    
    def _extract_permissions(self, member: ChatMember) -> Dict[str, bool]:
        """Extract permissions from a ChatMember object.
        
        Returns:
            ``dict``: Dictionary of permission values.
        """
        permissions = {}
        
        for perm in [
            "can_send_messages", "can_send_media_messages", "can_send_polls",
            "can_send_other_messages", "can_add_web_page_previews",
            "can_change_info", "can_invite_users", "can_pin_messages"
        ]:
            permissions[perm] = getattr(member, perm, None)
            
        return permissions
    
    def _extract_admin_rights(self, member: ChatMember) -> Dict[str, bool]:
        """Extract admin rights from a ChatMember object.
        
        Returns:
            ``dict``: Dictionary of admin permission values.
        """
        rights = {}
        
        for right in [
            "can_be_edited", "can_manage_chat", "can_delete_messages",
            "can_manage_voice_chats", "can_restrict_members", 
            "can_promote_members", "can_change_info",
            "can_invite_users", "can_pin_messages"
        ]:
            rights[right] = getattr(member, right, None)
            
        # Additional information for administrators
        rights["is_anonymous"] = getattr(member, "is_anonymous", None)
        rights["custom_title"] = getattr(member, "custom_title", None)
            
        return rights
    
    async def _get_user_profile_photos(self, user_id: int) -> Dict[str, Any]:
        """Get a user's profile photos.
        
        Returns:
            ``dict``: User profile photos information.
        """
        try:
            # Create params dictionary
            params = {
                "user_id": user_id,
                "limit": 10  # Get up to 10 recent photos
            }
            
            async with aiohttp.ClientSession() as session:
                url = f"https://api.telegram.org/bot{self.token}/getUserProfilePhotos"
                
                async with session.post(url, data=params) as response:
                    if response.status != 200:
                        self.logger.error(f"HTTP error {response.status} when getting profile photos: {await response.text()}")
                        return {"error": "Failed to fetch profile photos", "count": 0, "photos": []}
                    
                    result = await response.json()
                    
                    if not result.get("ok", False):
                        return {"error": result.get("description", "Unknown error"), "count": 0, "photos": []}
                    
                    data = result.get("result", {})
                    return {
                        "count": data.get("total_count", 0),
                        "photos": data.get("photos", [])
                    }
                    
        except Exception as e:
            self.logger.error(f"Error fetching profile photos: {e}", exc_info=True)
            return {"error": str(e), "count": 0, "photos": []}
    
    async def _get_user_status(self, user_id: int) -> Dict[str, Any]:
        """Get a user's online status.
        
        Note: This method is not available for normal bots,
        only for user bots. It will always return empty data
        for regular bot accounts.
        
        Returns:
            ``dict``: User status information.
        """
        # Always return this for normal bots
        return {
            "status": "unknown",
            "note": "User status is unavailable through the Bot API"
        } 