import typing
import aiohttp
from typing import Union, List

if typing.TYPE_CHECKING:
    from ...client import GramBotPy

class DeleteMessages:
    """Method for deleting messages."""
    
    async def delete_messages(
        self: "GramBotPy",
        chat_id: Union[int, str],
        message_ids: Union[int, List[int]],
        revoke: bool = True
    ) -> bool:
        """Delete messages.
        
        Parameters:
            chat_id (``int`` | ``str``):
                Unique identifier for the target chat or username.
                
            message_ids (``int`` | ``list``):
                ID or list of IDs of the messages to delete.
                
            revoke (``bool``, optional):
                Pass True to delete messages for all participants, including the message sender.
                Always True for channels and supergroups.
                
        Returns:
            ``bool``: True on success.
            
        Example:
            .. code-block:: python
            
                # Delete a single message
                await bot.delete_messages(chat_id, message_id)
                
                # Delete multiple messages at once
                await bot.delete_messages(chat_id, [message_id1, message_id2, message_id3])
        """
        # Convert single message_id to list for consistent handling
        if isinstance(message_ids, int):
            message_ids = [message_ids]
        
        # Make a copy of the list to avoid modifying the original
        message_ids = list(message_ids)
            
        self.logger.info(f"Deleting {len(message_ids)} messages from chat {chat_id}")
        
        # Following Telethon's pattern: process messages in chunks for efficiency
        chunk_size = 100  # Telegram limit
        success = True
        
        # Process messages in chunks
        for i in range(0, len(message_ids), chunk_size):
            chunk = message_ids[i:i + chunk_size]
            
            # Create params dictionary for this chunk
            params = {
                "chat_id": chat_id,
                "message_ids": chunk
            }
            
            chunk_result = await self._delete_messages_chunk(params)
            success = success and chunk_result
            
        return success
    
    async def _delete_messages_chunk(self, params: dict) -> bool:
        """Delete a chunk of messages using the Telegram API.
        
        Parameters:
            params (``dict``):
                Parameters for the request.
                
        Returns:
            ``bool``: True if all messages in the chunk were deleted successfully.
        """
        chat_id = params["chat_id"]
        message_ids = params["message_ids"]
        
        # Try to use the deleteMessages API for batch deletion first
        async with aiohttp.ClientSession() as session:
            try:
                url = f"https://api.telegram.org/bot{self.token}/deleteMessages"
                data = {
                    "chat_id": chat_id,
                    "message_ids": message_ids
                }
                
                async with session.post(url, json=data) as response:
                    # If the API exists, process the result
                    if response.status == 200:
                        result = await response.json()
                        if result.get("ok", False):
                            return True
                        else:
                            self.logger.warning(f"Batch delete failed, falling back to individual deletion. Error: {result.get('description', 'Unknown error')}")
                    else:
                        self.logger.warning(f"Batch delete API not available (HTTP {response.status}), falling back to individual deletion")
            
            except Exception as e:
                self.logger.warning(f"Error with batch deletion, falling back to individual deletion: {e}")
        
        # Fall back to individual deletion if batch deletion fails or isn't available
        success = True
        for message_id in message_ids:
            # Process individual messages
            msg_success = await self._delete_single_message(chat_id, message_id)
            success = success and msg_success
                    
        return success
    
    async def _delete_single_message(self, chat_id: Union[int, str], message_id: int) -> bool:
        """Delete a single message using the Telegram API.
        
        Parameters:
            chat_id (``int`` | ``str``):
                Chat ID.
            message_id (``int``):
                Message ID.
                
        Returns:
            ``bool``: True if the message was deleted successfully.
        """
        # Create params dictionary for this message
        params = {
            "chat_id": chat_id,
            "message_id": message_id
        }
        
        # Make the API request
        async with aiohttp.ClientSession() as session:
            try:
                url = f"https://api.telegram.org/bot{self.token}/deleteMessage"
                
                async with session.post(url, data=params) as response:
                    # Check HTTP status first
                    if response.status != 200:
                        self.logger.error(f"HTTP error {response.status} when deleting message {message_id}: {await response.text()}")
                        return False
                    
                    # Parse the response
                    result = await response.json()
                    
                    if not result.get("ok", False):
                        error_description = result.get('description', 'Unknown error')
                        self.logger.error(f"Error deleting message {message_id}: {error_description}")
                        return False
                        
                    return True
                    
            except aiohttp.ClientError as e:
                self.logger.error(f"Network error deleting message {message_id}: {e}", exc_info=True)
                return False
            except Exception as e:
                self.logger.error(f"Error deleting message {message_id}: {e}", exc_info=True)
                return False 