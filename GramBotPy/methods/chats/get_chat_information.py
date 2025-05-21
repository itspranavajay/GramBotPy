import typing
import json
import aiohttp
from typing import Union, Optional, Dict, Any
from datetime import datetime

if typing.TYPE_CHECKING:
    from ...client import GramBotPy

class GetChatInformation:
    """Method for getting detailed information about a chat."""
    
    async def get_chat_information(
        self: "GramBotPy",
        chat_id: Union[int, str],
        include_member_count: Optional[bool] = True,
        include_admins: Optional[bool] = True,
        include_invite_link: Optional[bool] = True
    ) -> Dict[str, Any]:
        """Get detailed information about a chat.
        
        Parameters:
            chat_id (``int`` | ``str``):
                Unique identifier for the target chat or username.
                
            include_member_count (``bool``, optional):
                Whether to include the member count in the result.
                
            include_admins (``bool``, optional):
                Whether to include the list of administrators.
                
            include_invite_link (``bool``, optional):
                Whether to include the chat invite link, if available.
                
        Returns:
            ``dict``: Detailed chat information including requested components.
            
        Example:
            .. code-block:: python
            
                # Get basic chat information
                chat_info = await bot.get_chat_information(chat_id)
                
                # Get detailed chat information without admin list
                chat_info = await bot.get_chat_information(
                    chat_id, 
                    include_admins=False
                )
        """
        self.logger.info(f"Getting detailed information for chat {chat_id}")
        
        try:
            # Get basic chat information
            chat = await self.get_chat(chat_id)
            
            # Initialize the result dictionary with base chat info
            chat_info = {
                "id": chat.id,
                "type": chat.type,
                "title": getattr(chat, "title", None),
                "username": getattr(chat, "username", None),
                "first_name": getattr(chat, "first_name", None),
                "last_name": getattr(chat, "last_name", None),
                "description": getattr(chat, "description", None),
                "photo": getattr(chat, "photo", None),
                "permissions": getattr(chat, "permissions", None),
                "invite_link": None,
                "member_count": None,
                "administrators": None,
                "is_forum": getattr(chat, "is_forum", False),
                "has_protected_content": getattr(chat, "has_protected_content", False),
                "sticker_set_name": getattr(chat, "sticker_set_name", None),
                "can_set_sticker_set": getattr(chat, "can_set_sticker_set", False),
                "linked_chat_id": getattr(chat, "linked_chat_id", None),
                "slow_mode_delay": getattr(chat, "slow_mode_delay", None),
                "message_auto_delete_time": getattr(chat, "message_auto_delete_time", None),
                "join_to_send_messages": getattr(chat, "join_to_send_messages", None),
                "join_by_request": getattr(chat, "join_by_request", None)
            }
            
            # Get member count if requested
            if include_member_count and chat.type in ["group", "supergroup", "channel"]:
                chat_info["member_count"] = await self._get_chat_member_count(chat_id)
            
            # Get administrators if requested
            if include_admins and chat.type in ["group", "supergroup", "channel"]:
                chat_info["administrators"] = await self._get_chat_administrators(chat_id)
            
            # Get invite link if requested
            if include_invite_link and chat.type in ["group", "supergroup", "channel"]:
                chat_info["invite_link"] = await self._get_chat_invite_link(chat_id)
                
            return chat_info
            
        except Exception as e:
            self.logger.error(f"Error getting chat information: {e}", exc_info=True)
            return {
                "error": str(e),
                "chat_id": chat_id,
                "timestamp": int(datetime.now().timestamp())
            }
    
    async def _get_chat_member_count(self, chat_id: Union[int, str]) -> int:
        """Get the number of members in a chat.
        
        Returns:
            ``int``: Number of members or None if failed.
        """
        try:
            params = {"chat_id": chat_id}
            
            async with aiohttp.ClientSession() as session:
                url = f"https://api.telegram.org/bot{self.token}/getChatMemberCount"
                
                async with session.post(url, data=params) as response:
                    if response.status != 200:
                        self.logger.error(f"HTTP error {response.status} when getting member count: {await response.text()}")
                        return None
                    
                    result = await response.json()
                    
                    if not result.get("ok", False):
                        self.logger.error(f"Error getting member count: {result.get('description', 'Unknown error')}")
                        return None
                    
                    return result.get("result", 0)
                    
        except Exception as e:
            self.logger.error(f"Error fetching member count: {e}", exc_info=True)
            return None
    
    async def _get_chat_administrators(self, chat_id: Union[int, str]) -> list:
        """Get a list of administrators in a chat.
        
        Returns:
            ``list``: List of administrator information or empty list if failed.
        """
        try:
            params = {"chat_id": chat_id}
            
            async with aiohttp.ClientSession() as session:
                url = f"https://api.telegram.org/bot{self.token}/getChatAdministrators"
                
                async with session.post(url, data=params) as response:
                    if response.status != 200:
                        self.logger.error(f"HTTP error {response.status} when getting administrators: {await response.text()}")
                        return []
                    
                    result = await response.json()
                    
                    if not result.get("ok", False):
                        self.logger.error(f"Error getting administrators: {result.get('description', 'Unknown error')}")
                        return []
                    
                    # Process the result to extract just the necessary information
                    admins = result.get("result", [])
                    admin_info = []
                    
                    for admin in admins:
                        user = admin.get("user", {})
                        admin_data = {
                            "user_id": user.get("id"),
                            "username": user.get("username"),
                            "first_name": user.get("first_name"),
                            "last_name": user.get("last_name"),
                            "status": admin.get("status"),
                            "custom_title": admin.get("custom_title"),
                            "is_anonymous": admin.get("is_anonymous", False),
                            "can_manage_chat": admin.get("can_manage_chat", False),
                            "can_delete_messages": admin.get("can_delete_messages", False),
                            "can_manage_voice_chats": admin.get("can_manage_voice_chats", False),
                            "can_restrict_members": admin.get("can_restrict_members", False),
                            "can_promote_members": admin.get("can_promote_members", False),
                            "can_change_info": admin.get("can_change_info", False),
                            "can_invite_users": admin.get("can_invite_users", False),
                            "can_pin_messages": admin.get("can_pin_messages", False)
                        }
                        admin_info.append(admin_data)
                    
                    return admin_info
                    
        except Exception as e:
            self.logger.error(f"Error fetching administrators: {e}", exc_info=True)
            return []
    
    async def _get_chat_invite_link(self, chat_id: Union[int, str]) -> str:
        """Get the invite link for a chat.
        
        Returns:
            ``str``: Invite link or None if failed.
        """
        try:
            params = {"chat_id": chat_id}
            
            async with aiohttp.ClientSession() as session:
                url = f"https://api.telegram.org/bot{self.token}/exportChatInviteLink"
                
                async with session.post(url, data=params) as response:
                    if response.status != 200:
                        self.logger.debug(f"HTTP error {response.status} when getting invite link: {await response.text()}")
                        return None
                    
                    result = await response.json()
                    
                    if not result.get("ok", False):
                        self.logger.debug(f"Error getting invite link: {result.get('description', 'Unknown error')}")
                        return None
                    
                    return result.get("result", "")
                    
        except Exception as e:
            self.logger.debug(f"Error fetching invite link: {e}")
            return None 