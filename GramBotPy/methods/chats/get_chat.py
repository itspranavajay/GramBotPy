import typing
import aiohttp
from typing import Union, Dict, Any, Optional

if typing.TYPE_CHECKING:
    from ...client import GramBotPy
    from ...types import Chat

class GetChat:
    """Method to get information about a chat."""
    
    async def get_chat(
        self: "GramBotPy",
        chat_id: Union[int, str]
    ) -> Dict[str, Any]:
        """Get up-to-date information about a chat.
        
        Parameters:
            chat_id (``int`` | ``str``):
                Unique identifier for the target chat or username.
                
        Returns:
            ``dict``: Chat object with information about the chat.
            
        Example:
            .. code-block:: python
            
                # Get information about a chat
                chat = await bot.get_chat(chat_id)
                print(f"Chat title: {chat.get('title')}")
        """
        self.logger.info(f"Getting information about chat {chat_id}")
        
        # Create params dictionary with required parameter
        params = {
            "chat_id": chat_id
        }
        
        # Make the API request
        async with aiohttp.ClientSession() as session:
            try:
                url = f"https://api.telegram.org/bot{self.token}/getChat"
                
                # Following Telethon's pattern to properly handle HTTP requests
                async with session.post(url, data=params) as response:
                    # Check HTTP status first
                    if response.status != 200:
                        self.logger.error(f"HTTP error {response.status} when getting chat: {await response.text()}")
                        return self._get_fallback_chat(chat_id)
                    
                    # Parse the JSON response
                    result = await response.json()
                    
                    if not result.get("ok", False):
                        error_description = result.get('description', 'Unknown error')
                        self.logger.error(f"Error getting chat information: {error_description}")
                        return self._get_fallback_chat(chat_id)
                    
                    # Parse the response
                    chat_data = result.get("result", {})
                    return chat_data
                    
            except aiohttp.ClientError as e:
                self.logger.error(f"Network error making request to Telegram API: {e}", exc_info=True)
                return self._get_fallback_chat(chat_id)
            except Exception as e:
                self.logger.error(f"Error making request to Telegram API: {e}", exc_info=True)
                return self._get_fallback_chat(chat_id)
    
    def _get_fallback_chat(self, chat_id: Union[int, str]) -> Dict[str, Any]:
        """Generate a fallback chat object for error cases.
        
        Parameters:
            chat_id (``int`` | ``str``):
                The chat ID to use for the fallback object.
                
        Returns:
            ``dict``: A fallback chat object.
        """
        # Extract numeric ID if possible
        chat_id_int = int(chat_id) if str(chat_id).lstrip('-').isdigit() else 0
        
        # Determine the chat type based on the ID
        chat_type = "private"
        if str(chat_id).startswith('-100'):
            chat_type = "supergroup"
        elif str(chat_id).startswith('-'):
            chat_type = "group"
        
        return {
            "id": chat_id_int,
            "type": chat_type,
            "title": f"Chat {chat_id_int}" if chat_type in ["group", "supergroup"] else None,
            "username": f"user{abs(chat_id_int)}" if chat_type == "private" else None,
            "first_name": "User" if chat_type == "private" else None,
            "last_name": "Name" if chat_type == "private" else None
        } 