import typing
import aiohttp
import json
from typing import Union, Optional
from datetime import datetime

if typing.TYPE_CHECKING:
    from ...client import GramBotPy

class BanChatMember:
    """Method to ban a user from a chat."""
    
    async def ban_chat_member(
        self: "GramBotPy",
        chat_id: Union[int, str],
        user_id: int,
        until_date: Optional[datetime] = None,
        revoke_messages: Optional[bool] = None
    ) -> bool:
        """Ban a user from a chat.
        
        Parameters:
            chat_id (``int`` | ``str``):
                Unique identifier for the target chat or username.
                
            user_id (``int``):
                Unique identifier of the target user.
                
            until_date (:py:obj:`~datetime.datetime`, optional):
                Date when the user will be unbanned. If not specified, the user will be banned forever.
                
            revoke_messages (``bool``, optional):
                Pass True to delete all messages from the chat for the user that is being removed.
                
        Returns:
            ``bool``: True on success.
            
        Example:
            .. code-block:: python
            
                # Ban a user permanently
                await bot.ban_chat_member(chat_id, user_id)
                
                # Ban a user for 24 hours
                from datetime import datetime, timedelta
                ban_until = datetime.now() + timedelta(days=1)
                await bot.ban_chat_member(chat_id, user_id, until_date=ban_until)
        """
        self.logger.info(f"Banning user {user_id} from chat {chat_id}")
        
        # Create params dictionary with required parameters
        params = {
            "chat_id": chat_id,
            "user_id": user_id
        }
        
        # Convert datetime to Unix timestamp if provided
        if until_date:
            until_date_ts = int(until_date.timestamp())
            params["until_date"] = until_date_ts
            self.logger.info(f"Ban until: {until_date} ({until_date_ts})")
        
        # Add optional parameters if provided
        if revoke_messages is not None:
            params["revoke_messages"] = json.dumps(revoke_messages)
        
        # Make the API request
        return await self._ban_chat_member_request(params)
    
    async def _ban_chat_member_request(self, params: dict) -> bool:
        """Make the actual API request for banning a user.
        
        Parameters:
            params (``dict``):
                Parameters to send in the request.
                
        Returns:
            ``bool``: True on success.
        """
        async with aiohttp.ClientSession() as session:
            try:
                url = f"https://api.telegram.org/bot{self.token}/banChatMember"
                
                # Following Telethon's pattern for proper HTTP handling
                async with session.post(url, data=params) as response:
                    # Check HTTP status first
                    if response.status != 200:
                        self.logger.error(f"HTTP error {response.status} when banning user: {await response.text()}")
                        return False
                    
                    # Parse the JSON response
                    result = await response.json()
                    
                    if not result.get("ok", False):
                        error_description = result.get('description', 'Unknown error')
                        self.logger.error(f"Error banning user: {error_description}")
                        self.logger.debug(f"Params used: {params}")
                        return False
                        
                    return True
                    
            except aiohttp.ClientError as e:
                self.logger.error(f"Network error making request to Telegram API: {e}", exc_info=True)
                return False
            except Exception as e:
                self.logger.error(f"Error making request to Telegram API: {e}", exc_info=True)
                return False 