import typing
import json
import aiohttp
from typing import Union

if typing.TYPE_CHECKING:
    from ...client import GramBotPy

class UnmuteChatMember:
    """Method for unmuting a previously muted chat member."""
    
    async def unmute_chat_member(
        self: "GramBotPy",
        chat_id: Union[int, str],
        user_id: int
    ) -> bool:
        """Unmute a previously muted user in a group chat.
        
        Parameters:
            chat_id (``int`` | ``str``):
                Unique identifier for the target chat or username.
                
            user_id (``int``):
                Unique identifier of the target user.
                
        Returns:
            ``bool``: True on success.
            
        Example:
            .. code-block:: python
            
                # Unmute a user
                await bot.unmute_chat_member(chat_id, user_id)
        """
        self.logger.info(f"Unmuting user {user_id} in chat {chat_id}")
        
        # Create permissions object with default message permissions
        permissions = {
            "can_send_messages": True,
            "can_send_media_messages": True,
            "can_send_polls": True,
            "can_send_other_messages": True,
            "can_add_web_page_previews": True,
            "can_change_info": False,
            "can_invite_users": True,
            "can_pin_messages": False
        }
        
        # Create params dictionary with required parameters
        params = {
            "chat_id": chat_id,
            "user_id": user_id,
            "permissions": json.dumps(permissions)
        }
        
        # Make the API request
        return await self._unmute_chat_member_request(params)
    
    async def _unmute_chat_member_request(
        self,
        params: dict
    ) -> bool:
        """Send the actual request to the Telegram API.
        
        Returns:
            ``bool``: True on success.
        """
        async with aiohttp.ClientSession() as session:
            try:
                url = f"https://api.telegram.org/bot{self.token}/restrictChatMember"
                
                async with session.post(url, data=params) as response:
                    # Check HTTP status first
                    if response.status != 200:
                        self.logger.error(f"HTTP error {response.status} when unmuting member: {await response.text()}")
                        return False
                    
                    # Parse the JSON response
                    result = await response.json()
                    
                    if not result.get("ok", False):
                        error_description = result.get('description', 'Unknown error')
                        self.logger.error(f"Error unmuting member: {error_description}")
                        self.logger.debug(f"Params used: {params}")
                        return False
                    
                    return True
                    
            except aiohttp.ClientError as e:
                self.logger.error(f"Network error unmuting member: {e}", exc_info=True)
                return False
            except Exception as e:
                self.logger.error(f"Error unmuting member: {e}", exc_info=True)
                return False 