import typing
import aiohttp
from typing import Union, Optional

if typing.TYPE_CHECKING:
    from ...client import GramBotPy

class UnpinChatMessage:
    """Method for unpinning messages in chats."""
    
    async def unpin_chat_message(
        self: "GramBotPy",
        chat_id: Union[int, str],
        message_id: Optional[int] = None
    ) -> bool:
        """Unpin a message in a chat.
        
        Parameters:
            chat_id (``int`` | ``str``):
                Unique identifier for the target chat or username.
                
            message_id (``int``, optional):
                Identifier of a message to unpin. If not specified, unpins the
                most recent pinned message (by default).
                
        Returns:
            ``bool``: True on success.
            
        Example:
            .. code-block:: python
            
                # Unpin a specific message
                await bot.unpin_chat_message(chat_id, message_id)
                
                # Unpin the most recent pinned message
                await bot.unpin_chat_message(chat_id)
        """
        self.logger.info(f"Unpinning message in chat {chat_id}")
        
        # Create params dictionary with required parameters
        params = {
            "chat_id": chat_id
        }
        
        # Add message_id if provided
        if message_id is not None:
            params["message_id"] = message_id
        
        # Make the API request
        return await self._unpin_message_request(params)
    
    async def _unpin_message_request(self, params: dict) -> bool:
        """Make the actual API request for unpinning a message.
        
        Parameters:
            params (``dict``):
                Parameters to send in the request.
                
        Returns:
            ``bool``: True on success.
        """
        async with aiohttp.ClientSession() as session:
            try:
                url = f"https://api.telegram.org/bot{self.token}/unpinChatMessage"
                
                # Following Telethon's pattern for proper HTTP handling
                async with session.post(url, data=params) as response:
                    # Check HTTP status first
                    if response.status != 200:
                        self.logger.error(f"HTTP error {response.status} when unpinning message: {await response.text()}")
                        return False
                    
                    # Parse the JSON response
                    result = await response.json()
                    
                    if not result.get("ok", False):
                        error_description = result.get('description', 'Unknown error')
                        self.logger.error(f"Error unpinning message: {error_description}")
                        self.logger.debug(f"Params used: {params}")
                        return False
                        
                    return True
                    
            except aiohttp.ClientError as e:
                self.logger.error(f"Network error making request to Telegram API: {e}", exc_info=True)
                return False
            except Exception as e:
                self.logger.error(f"Error making request to Telegram API: {e}", exc_info=True)
                return False
    
    async def unpin_all_chat_messages(
        self: "GramBotPy",
        chat_id: Union[int, str]
    ) -> bool:
        """Unpin all pinned messages in a chat.
        
        Parameters:
            chat_id (``int`` | ``str``):
                Unique identifier for the target chat or username.
                
        Returns:
            ``bool``: True on success.
            
        Example:
            .. code-block:: python
            
                # Unpin all messages in a chat
                await bot.unpin_all_chat_messages(chat_id)
        """
        self.logger.info(f"Unpinning all messages in chat {chat_id}")
        
        # Create params dictionary with required parameters
        params = {
            "chat_id": chat_id
        }
        
        # Make the API request
        async with aiohttp.ClientSession() as session:
            try:
                url = f"https://api.telegram.org/bot{self.token}/unpinAllChatMessages"
                
                # Following Telethon's pattern for proper HTTP handling
                async with session.post(url, data=params) as response:
                    # Check HTTP status first
                    if response.status != 200:
                        self.logger.error(f"HTTP error {response.status} when unpinning all messages: {await response.text()}")
                        return False
                    
                    # Parse the JSON response
                    result = await response.json()
                    
                    if not result.get("ok", False):
                        error_description = result.get('description', 'Unknown error')
                        self.logger.error(f"Error unpinning all messages: {error_description}")
                        self.logger.debug(f"Params used: {params}")
                        return False
                        
                    return True
                    
            except aiohttp.ClientError as e:
                self.logger.error(f"Network error making request to Telegram API: {e}", exc_info=True)
                return False
            except Exception as e:
                self.logger.error(f"Error making request to Telegram API: {e}", exc_info=True)
                return False 
            