import typing
import json
import aiohttp
from typing import Union, List, Optional, Dict, Any
from datetime import datetime

if typing.TYPE_CHECKING:
    from ...client import GramBotPy
    from ...types import Message

class ForwardMessages:
    """Method for forwarding messages."""
    
    async def forward_messages(
        self: "GramBotPy",
        chat_id: Union[int, str],
        from_chat_id: Union[int, str],
        message_ids: Union[int, List[int]],
        disable_notification: Optional[bool] = None,
        protect_content: Optional[bool] = None
    ) -> Union[List["Message"], "Message"]:
        """Forward messages of any kind.
        
        Parameters:
            chat_id (``int`` | ``str``):
                Unique identifier for the target chat or username.
                
            from_chat_id (``int`` | ``str``):
                Unique identifier for the chat where the original message was sent.
                
            message_ids (``int`` | ``list``):
                Message identifier(s) in the chat specified in from_chat_id.
                
            disable_notification (``bool``, optional):
                Sends the message silently. Users will receive a notification with no sound.
                
            protect_content (``bool``, optional):
                Protects the contents of the forwarded message from forwarding and saving.
                
        Returns:
            :obj:`Message` | ``list``: On success, the forwarded message(s) are returned.
            
        Example:
            .. code-block:: python
            
                # Forward a single message
                await bot.forward_messages(chat_id, from_chat_id, message_id)
                
                # Forward multiple messages
                await bot.forward_messages(chat_id, from_chat_id, [message_id1, message_id2])
        """
        # Convert single message_id to list for consistent handling
        single_message = False
        if isinstance(message_ids, int):
            message_ids = [message_ids]
            single_message = True
            
        # Make a copy of the list to avoid modifying the original
        message_ids = list(message_ids)
            
        self.logger.info(f"Forwarding {len(message_ids)} messages from {from_chat_id} to {chat_id}")
        
        # Try to use the forwardMessages API for batch forwarding if available
        if len(message_ids) > 1:
            batch_result = await self._forward_messages_batch(
                chat_id, from_chat_id, message_ids, disable_notification, protect_content
            )
            if batch_result:
                # If batch forwarding succeeded, return the result
                return batch_result[0] if single_message else batch_result
        
        # If batch forwarding is not available or failed, forward messages individually
        from ...types import Message
        forwarded_messages = []
        
        # Process each message individually
        for message_id in message_ids:
            message = await self._forward_single_message(
                chat_id, from_chat_id, message_id, disable_notification, protect_content
            )
            forwarded_messages.append(message)
        
        # Return a single message or a list depending on the input
        if single_message:
            return forwarded_messages[0]
        return forwarded_messages
    
    async def _forward_messages_batch(
        self,
        chat_id: Union[int, str],
        from_chat_id: Union[int, str],
        message_ids: List[int],
        disable_notification: Optional[bool] = None,
        protect_content: Optional[bool] = None
    ) -> Optional[List["Message"]]:
        """Try to forward multiple messages in a single batch.
        
        Returns:
            List of Message objects if successful, None if the API doesn't support batch forwarding.
        """
        # Create the params dictionary
        params = {
            "chat_id": chat_id,
            "from_chat_id": from_chat_id,
            "message_ids": json.dumps(message_ids)
        }
        
        # Add optional parameters if provided
        if disable_notification is not None:
            params["disable_notification"] = json.dumps(disable_notification)
            
        if protect_content is not None:
            params["protect_content"] = json.dumps(protect_content)
        
        # Try the batch forward API
        from ...types import Message
        try:
            async with aiohttp.ClientSession() as session:
                url = f"https://api.telegram.org/bot{self.token}/forwardMessages"
                async with session.post(url, data=params) as response:
                    # Check if the API exists and works
                    if response.status != 200:
                        self.logger.debug("Batch forward API not available, falling back to individual forwards")
                        return None
                    
                    result = await response.json()
                    
                    if not result.get("ok", False):
                        self.logger.debug(f"Batch forward failed: {result.get('description', 'Unknown error')}")
                        return None
                    
                    # Parse the response and create Message objects
                    message_datas = result.get("result", [])
                    return [Message._parse(self, msg_data) for msg_data in message_datas]
                    
        except Exception as e:
            self.logger.debug(f"Error using batch forward: {e}, falling back to individual forwards")
            return None
    
    async def _forward_single_message(
        self,
        chat_id: Union[int, str],
        from_chat_id: Union[int, str],
        message_id: int,
        disable_notification: Optional[bool] = None,
        protect_content: Optional[bool] = None
    ) -> "Message":
        """Forward a single message.
        
        Returns:
            A Message object.
        """
        # Create the params for this message
        params = {
            "chat_id": chat_id,
            "from_chat_id": from_chat_id,
            "message_id": message_id
        }
        
        # Add optional parameters if provided
        if disable_notification is not None:
            params["disable_notification"] = json.dumps(disable_notification)
            
        if protect_content is not None:
            params["protect_content"] = json.dumps(protect_content)
        
        # Make the API request
        from ...types import Message
        async with aiohttp.ClientSession() as session:
            try:
                url = f"https://api.telegram.org/bot{self.token}/forwardMessage"
                
                # Following Telethon's pattern for proper HTTP handling
                async with session.post(url, data=params) as response:
                    # Check HTTP status first
                    if response.status != 200:
                        self.logger.error(f"HTTP error {response.status} when forwarding message: {await response.text()}")
                        return self._get_fallback_message(chat_id, from_chat_id, message_id)
                    
                    # Parse the JSON response
                    result = await response.json()
                    
                    if not result.get("ok", False):
                        error_description = result.get('description', 'Unknown error')
                        self.logger.error(f"Error forwarding message {message_id}: {error_description}")
                        self.logger.debug(f"Params used: {params}")
                        return self._get_fallback_message(chat_id, from_chat_id, message_id)
                    
                    # Parse the response and create a Message object
                    message_data = result.get("result", {})
                    return Message._parse(self, message_data)
                        
            except aiohttp.ClientError as e:
                self.logger.error(f"Network error making request to Telegram API: {e}", exc_info=True)
                return self._get_fallback_message(chat_id, from_chat_id, message_id)
            except Exception as e:
                self.logger.error(f"Error making request to Telegram API: {e}", exc_info=True)
                return self._get_fallback_message(chat_id, from_chat_id, message_id)
    
    def _get_fallback_message(
        self, 
        chat_id: Union[int, str], 
        from_chat_id: Union[int, str], 
        message_id: int
    ) -> "Message":
        """Create a fallback message for error cases.
        
        Returns:
            A placeholder Message object.
        """
        from ...types import Message
        return Message(
            message_id=-1,
            date=int(datetime.now().timestamp()),
            chat={"id": int(chat_id) if str(chat_id).lstrip('-').isdigit() else 0, "type": "private"},
            forward_from_chat={"id": int(from_chat_id) if str(from_chat_id).lstrip('-').isdigit() else 0},
            forward_from_message_id=message_id
        ) 