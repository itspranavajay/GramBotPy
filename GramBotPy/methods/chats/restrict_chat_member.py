import typing
import aiohttp
import json
from typing import Union, Optional, Dict, Any
from datetime import datetime

if typing.TYPE_CHECKING:
    from ...client import GramBotPy

class RestrictChatMember:
    """Method to restrict a user in a chat."""
    
    async def restrict_chat_member(
        self: "GramBotPy",
        chat_id: Union[int, str],
        user_id: int,
        permissions: Dict[str, bool],
        until_date: Optional[datetime] = None
    ) -> bool:
        """Restrict a user in a supergroup.
        
        Parameters:
            chat_id (``int`` | ``str``):
                Unique identifier for the target chat or username.
                
            user_id (``int``):
                Unique identifier of the target user.
                
            permissions (``dict``):
                New user permissions. A dictionary containing the following keys:
                    - can_send_messages (``bool``, optional)
                    - can_send_media_messages (``bool``, optional)
                    - can_send_polls (``bool``, optional)
                    - can_send_other_messages (``bool``, optional)
                    - can_add_web_page_previews (``bool``, optional)
                    - can_change_info (``bool``, optional)
                    - can_invite_users (``bool``, optional)
                    - can_pin_messages (``bool``, optional)
                
            until_date (:py:obj:`~datetime.datetime`, optional):
                Date when restrictions will be lifted. If not specified, 
                restrictions will be applied forever.
                
        Returns:
            ``bool``: True on success.
            
        Example:
            .. code-block:: python
            
                # Restrict a user from sending messages
                permissions = {
                    "can_send_messages": False,
                    "can_send_media_messages": False,
                    "can_send_polls": False,
                    "can_send_other_messages": False,
                    "can_add_web_page_previews": False,
                    "can_change_info": False,
                    "can_invite_users": False,
                    "can_pin_messages": False
                }
                await bot.restrict_chat_member(chat_id, user_id, permissions)
                
                # Restrict a user for 24 hours
                from datetime import datetime, timedelta
                restrict_until = datetime.now() + timedelta(days=1)
                await bot.restrict_chat_member(chat_id, user_id, permissions, until_date=restrict_until)
        """
        self.logger.info(f"Restricting user {user_id} in chat {chat_id}")
        self.logger.info(f"Permissions: {permissions}")
        
        # Create params dictionary with required parameters
        params = {
            "chat_id": chat_id,
            "user_id": user_id,
            "permissions": json.dumps(permissions)
        }
        
        # Convert datetime to Unix timestamp if provided
        if until_date:
            until_date_ts = int(until_date.timestamp())
            params["until_date"] = until_date_ts
            self.logger.info(f"Restrict until: {until_date} ({until_date_ts})")
        
        # Make the API request
        return await self._restrict_chat_member_request(params)
    
    async def _restrict_chat_member_request(self, params: dict) -> bool:
        """Make the actual API request for restricting a user.
        
        Parameters:
            params (``dict``):
                Parameters to send in the request.
                
        Returns:
            ``bool``: True on success.
        """
        async with aiohttp.ClientSession() as session:
            try:
                url = f"https://api.telegram.org/bot{self.token}/restrictChatMember"
                
                # Following Telethon's pattern for proper HTTP handling
                async with session.post(url, data=params) as response:
                    # Check HTTP status first
                    if response.status != 200:
                        self.logger.error(f"HTTP error {response.status} when restricting user: {await response.text()}")
                        return False
                    
                    # Parse the JSON response
                    result = await response.json()
                    
                    if not result.get("ok", False):
                        error_description = result.get('description', 'Unknown error')
                        self.logger.error(f"Error restricting user: {error_description}")
                        self.logger.debug(f"Params used: {params}")
                        return False
                        
                    return True
                    
            except aiohttp.ClientError as e:
                self.logger.error(f"Network error making request to Telegram API: {e}", exc_info=True)
                return False
            except Exception as e:
                self.logger.error(f"Error making request to Telegram API: {e}", exc_info=True)
                return False 