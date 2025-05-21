import typing
import aiohttp
from typing import Union, Optional

if typing.TYPE_CHECKING:
    from ...client import GramBotPy

class PinChatMessage:
    """Method for pinning messages in chats."""
    
    async def pin_chat_message(
        self: "GramBotPy",
        chat_id: Union[int, str],
        message_id: int,
        disable_notification: Optional[bool] = None
    ) -> bool:
        """Pin a message in a chat.
        
        Parameters:
            chat_id (``int`` | ``str``):
                Unique identifier for the target chat or username.
                
            message_id (``int``):
                Identifier of a message to pin.
                
            disable_notification (``bool``, optional):
                Pass True to pin the message silently. Users will receive a notification
                without sound.
                
        Returns:
            ``bool``: True on success.
            
        Example:
            .. code-block:: python
            
                # Pin a message
                await bot.pin_chat_message(chat_id, message_id)
                
                # Pin silently
                await bot.pin_chat_message(chat_id, message_id, disable_notification=True)
        """
        self.logger.info(f"Pinning message {message_id} in chat {chat_id}")
        
        # Create params dictionary with required parameters
        params = {
            "chat_id": chat_id,
            "message_id": message_id
        }
        
        # Add optional parameters if provided
        if disable_notification is not None:
            params["disable_notification"] = disable_notification
        
        # Make the API request
        return await self._pin_message_request(params)
    
    async def _pin_message_request(self, params: dict) -> bool:
        """Make the actual API request for pinning a message.
        
        Parameters:
            params (``dict``):
                Parameters to send in the request.
                
        Returns:
            ``bool``: True on success.
        """
        async with aiohttp.ClientSession() as session:
            try:
                url = f"https://api.telegram.org/bot{self.token}/pinChatMessage"
                
                # Following Telethon's pattern for proper HTTP handling
                async with session.post(url, data=params) as response:
                    # Check HTTP status first
                    if response.status != 200:
                        self.logger.error(f"HTTP error {response.status} when pinning message: {await response.text()}")
                        return False
                    
                    # Parse the JSON response
                    result = await response.json()
                    
                    if not result.get("ok", False):
                        error_description = result.get('description', 'Unknown error')
                        self.logger.error(f"Error pinning message: {error_description}")
                        self.logger.debug(f"Params used: {params}")
                        return False
                        
                    return True
                    
            except aiohttp.ClientError as e:
                self.logger.error(f"Network error making request to Telegram API: {e}", exc_info=True)
                return False
            except Exception as e:
                self.logger.error(f"Error making request to Telegram API: {e}", exc_info=True)
                return False 