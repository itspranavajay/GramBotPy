import typing
import json
import aiohttp
from typing import Union, Optional
from datetime import datetime, timedelta

from ...types import ChatMember

if typing.TYPE_CHECKING:
    from ...client import GramBotPy

class MuteChatMember:
    """Method for muting (restricting) a chat member from sending messages."""
    
    async def mute_chat_member(
        self: "GramBotPy",
        chat_id: Union[int, str],
        user_id: int,
        until_date: Optional[Union[int, datetime]] = None,
        revoke_messages: Optional[bool] = None
    ) -> bool:
        """Mute a user in a group chat.
        
        Parameters:
            chat_id (``int`` | ``str``):
                Unique identifier for the target chat or username.
                
            user_id (``int``):
                Unique identifier of the target user.
                
            until_date (``int`` | ``datetime``, optional):
                Date when the user will be unmuted. If not specified, the user will be muted forever.
                
            revoke_messages (``bool``, optional):
                Pass True to delete all messages from the user in this chat.
                
        Returns:
            ``bool``: True on success.
            
        Example:
            .. code-block:: python
            
                # Mute a user indefinitely
                await bot.mute_chat_member(chat_id, user_id)
                
                # Mute a user for 1 day
                from datetime import datetime, timedelta
                until_date = datetime.now() + timedelta(days=1)
                await bot.mute_chat_member(chat_id, user_id, until_date=until_date)
        """
        self.logger.info(f"Muting user {user_id} in chat {chat_id}")
        
        # Create permissions object with all message permissions set to False
        permissions = {
            "can_send_messages": False,
            "can_send_media_messages": False,
            "can_send_polls": False,
            "can_send_other_messages": False,
            "can_add_web_page_previews": False
        }
        
        # Convert datetime to timestamp if needed
        if isinstance(until_date, datetime):
            until_date = int(until_date.timestamp())
        
        # Create params dictionary with required parameters
        params = {
            "chat_id": chat_id,
            "user_id": user_id,
            "permissions": json.dumps(permissions)
        }
        
        # Add optional parameters
        if until_date is not None:
            params["until_date"] = until_date
            
        if revoke_messages is not None:
            params["revoke_messages"] = json.dumps(revoke_messages)
        
        # Make the API request
        return await self._mute_chat_member_request(params)
    
    async def _mute_chat_member_request(
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
                        self.logger.error(f"HTTP error {response.status} when muting member: {await response.text()}")
                        return False
                    
                    # Parse the JSON response
                    result = await response.json()
                    
                    if not result.get("ok", False):
                        error_description = result.get('description', 'Unknown error')
                        self.logger.error(f"Error muting member: {error_description}")
                        self.logger.debug(f"Params used: {params}")
                        return False
                    
                    return True
                    
            except aiohttp.ClientError as e:
                self.logger.error(f"Network error muting member: {e}", exc_info=True)
                return False
            except Exception as e:
                self.logger.error(f"Error muting member: {e}", exc_info=True)
                return False 