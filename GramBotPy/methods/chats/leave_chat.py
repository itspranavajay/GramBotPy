import typing
import aiohttp
from typing import Union

if typing.TYPE_CHECKING:
    from ...client import GramBotPy

class LeaveChat:
    """Method for leaving a chat."""
    
    async def leave_chat(
        self: "GramBotPy",
        chat_id: Union[int, str]
    ) -> bool:
        """Leave a group, supergroup or channel.
        
        Parameters:
            chat_id (``int`` | ``str``):
                Unique identifier for the target chat or username.
                
        Returns:
            ``bool``: True on success.
            
        Example:
            .. code-block:: python
            
                # Leave a chat
                await bot.leave_chat(chat_id)
        """
        self.logger.info(f"Leaving chat {chat_id}")
        
        # Create params dictionary with required parameter
        params = {
            "chat_id": chat_id
        }
        
        # Make the API request
        return await self._leave_chat_request(params)
    
    async def _leave_chat_request(self, params: dict) -> bool:
        """Make the actual API request for leaving a chat.
        
        Parameters:
            params (``dict``):
                Parameters to send in the request.
                
        Returns:
            ``bool``: True on success.
        """
        async with aiohttp.ClientSession() as session:
            try:
                url = f"https://api.telegram.org/bot{self.token}/leaveChat"
                
                # Following Telethon's pattern for proper HTTP handling
                async with session.post(url, data=params) as response:
                    # Check HTTP status first
                    if response.status != 200:
                        self.logger.error(f"HTTP error {response.status} when leaving chat: {await response.text()}")
                        return False
                    
                    # Parse the JSON response
                    result = await response.json()
                    
                    if not result.get("ok", False):
                        error_description = result.get('description', 'Unknown error')
                        self.logger.error(f"Error leaving chat: {error_description}")
                        self.logger.debug(f"Params used: {params}")
                        return False
                        
                    return True
                    
            except aiohttp.ClientError as e:
                self.logger.error(f"Network error making request to Telegram API: {e}", exc_info=True)
                return False
            except Exception as e:
                self.logger.error(f"Error making request to Telegram API: {e}", exc_info=True)
                return False 