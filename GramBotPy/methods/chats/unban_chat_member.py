import typing
import aiohttp
import json
from typing import Union, Optional

if typing.TYPE_CHECKING:
    from ...client import GramBotPy

class UnbanChatMember:
    """Method to unban a user from a chat."""
    
    async def unban_chat_member(
        self: "GramBotPy",
        chat_id: Union[int, str],
        user_id: int,
        only_if_banned: Optional[bool] = None
    ) -> bool:
        """Unban a previously banned user in a supergroup or channel.
        
        Parameters:
            chat_id (``int`` | ``str``):
                Unique identifier for the target chat or username.
                
            user_id (``int``):
                Unique identifier of the target user.
                
            only_if_banned (``bool``, optional):
                Do nothing if the user is not banned.
                
        Returns:
            ``bool``: True on success.
            
        Example:
            .. code-block:: python
            
                # Unban a user
                await bot.unban_chat_member(chat_id, user_id)
                
                # Unban a user only if they are currently banned
                await bot.unban_chat_member(chat_id, user_id, only_if_banned=True)
        """
        self.logger.info(f"Unbanning user {user_id} from chat {chat_id}")
        
        # Create params dictionary with required parameters
        params = {
            "chat_id": chat_id,
            "user_id": user_id
        }
        
        # Add optional parameters if provided
        if only_if_banned is not None:
            params["only_if_banned"] = json.dumps(only_if_banned)
            self.logger.info(f"Only if banned: {only_if_banned}")
        
        # Make the API request
        return await self._unban_chat_member_request(params)
    
    async def _unban_chat_member_request(self, params: dict) -> bool:
        """Make the actual API request for unbanning a user.
        
        Parameters:
            params (``dict``):
                Parameters to send in the request.
                
        Returns:
            ``bool``: True on success.
        """
        async with aiohttp.ClientSession() as session:
            try:
                url = f"https://api.telegram.org/bot{self.token}/unbanChatMember"
                
                # Following Telethon's pattern for proper HTTP handling
                async with session.post(url, data=params) as response:
                    # Check HTTP status first
                    if response.status != 200:
                        self.logger.error(f"HTTP error {response.status} when unbanning user: {await response.text()}")
                        return False
                    
                    # Parse the JSON response
                    result = await response.json()
                    
                    if not result.get("ok", False):
                        error_description = result.get('description', 'Unknown error')
                        self.logger.error(f"Error unbanning user: {error_description}")
                        self.logger.debug(f"Params used: {params}")
                        return False
                        
                    return True
                    
            except aiohttp.ClientError as e:
                self.logger.error(f"Network error making request to Telegram API: {e}", exc_info=True)
                return False
            except Exception as e:
                self.logger.error(f"Error making request to Telegram API: {e}", exc_info=True)
                return False 