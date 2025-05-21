import asyncio
import logging
import typing
import aiohttp
import json

from ...types import Message

if typing.TYPE_CHECKING:
    from ...client import GramBotPy

class GetChannelMessages:
    """Method for getting messages from a channel."""
    
    async def get_channel_messages(
        self: "GramBotPy",
        chat_id: typing.Union[int, str],
        offset: int = 0,
        limit: int = 100
    ) -> typing.List[dict]:
        """Get messages from a channel.
        
        Parameters:
            chat_id (``int`` | ``str``):
                Unique identifier for the target chat or username of the
                target channel (in the format @channelusername).
                
            offset (``int``, optional):
                Sequential number of the first message to be returned. Defaults to 0.
                
            limit (``int``, optional):
                Limits the number of messages to be retrieved. Defaults to 100.
                Values between 1-100 are accepted.
                
        Returns:
            List of ``dict``: List of messages or empty list on failure.
        """
        self.logger.info(f"Getting messages from channel {chat_id}")
        
        # Create the params dictionary with required parameters
        params = {
            "chat_id": chat_id,
            "offset": offset,
            "limit": min(limit, 100)  # Ensure limit is within allowed range
        }
        
        # Make the API request to get the messages
        async with aiohttp.ClientSession() as session:
            try:
                url = f"https://api.telegram.org/bot{self.token}/getMessages"
                async with session.post(url, data=params) as response:
                    result = await response.json()
                    
                    if not result.get("ok", False):
                        error_description = result.get('description', 'Unknown error')
                        self.logger.error(f"Error getting channel messages: {error_description}")
                        
                        # More detailed error logging
                        self.logger.debug(f"Params used: {params}")
                        return []
                    
                    # Return the raw message data
                    return result.get("result", [])
                    
            except aiohttp.ClientError as e:
                self.logger.error(f"Network error making request to Telegram API: {e}", exc_info=True)
                return []
            except Exception as e:
                self.logger.error(f"Error making request to Telegram API: {e}", exc_info=True)
                return [] 