import asyncio
import logging
import typing
import aiohttp
import json

if typing.TYPE_CHECKING:
    from ...client import GramBotPy

class ReadBusinessMessage:
    """Method for marking business messages as read."""
    
    async def read_business_message(
        self: "GramBotPy",
        business_connection_id: str,
        chat_id: typing.Union[int, str],
        message_id: int
    ) -> bool:
        """Mark incoming messages as read on behalf of a business account.
        
        Parameters:
            business_connection_id (``str``):
                Unique identifier of the business connection on behalf of which messages will be marked as read.
                
            chat_id (``int`` | ``str``):
                Unique identifier for the target chat or username of the target channel.
                
            message_id (``int``):
                Identifier of the message to mark as read.
                
        Returns:
            ``bool``: True on success.
            
        Example:
            .. code-block:: python
            
                # Mark a message as read
                await bot.read_business_message(business_connection_id, chat_id, message_id)
        """
        self.logger.info(f"Marking business message as read: {message_id} in chat {chat_id}")
        
        # Create the params dictionary with required parameters
        params = {
            "business_connection_id": business_connection_id,
            "chat_id": chat_id,
            "message_id": message_id
        }
        
        # Make the API request to mark the message as read
        async with aiohttp.ClientSession() as session:
            try:
                url = f"https://api.telegram.org/bot{self.token}/readBusinessMessage"
                async with session.post(url, data=params) as response:
                    result = await response.json()
                    
                    if not result.get("ok", False):
                        error_description = result.get('description', 'Unknown error')
                        self.logger.error(f"Error marking business message as read: {error_description}")
                        
                        # More detailed error logging
                        self.logger.debug(f"Params used: {params}")
                        return False
                    
                    return True
                    
            except aiohttp.ClientError as e:
                self.logger.error(f"Network error making request to Telegram API: {e}", exc_info=True)
                return False
            except Exception as e:
                self.logger.error(f"Error making request to Telegram API: {e}", exc_info=True)
                return False 