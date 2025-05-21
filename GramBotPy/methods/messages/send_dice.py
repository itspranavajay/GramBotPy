import typing
import json
import aiohttp
from typing import Union, Optional
from datetime import datetime

from ...types import Message

if typing.TYPE_CHECKING:
    from ...client import GramBotPy
    from ...types import InlineKeyboardMarkup, ReplyKeyboardMarkup
    from ...types import ReplyKeyboardRemove, ForceReply

class SendDice:
    """Method for sending animated dice that result in random values."""
    
    async def send_dice(
        self: "GramBotPy",
        chat_id: Union[int, str],
        emoji: Optional[str] = None,
        disable_notification: Optional[bool] = None,
        protect_content: Optional[bool] = None,
        reply_to_message_id: Optional[int] = None,
        allow_sending_without_reply: Optional[bool] = None,
        reply_markup: Optional[Union[
            "InlineKeyboardMarkup",
            "ReplyKeyboardMarkup",
            "ReplyKeyboardRemove",
            "ForceReply"
        ]] = None
    ) -> "Message":
        """Send a dice message.
        
        Parameters:
            chat_id (``int`` | ``str``):
                Unique identifier for the target chat or username.
                
            emoji (``str``, optional):
                Emoji on which the dice throw animation is based. 
                Currently, must be one of "🎲", "🎯", "🏀", "⚽", "🎳", or "🎰".
                Defaults to "🎲".
                
            disable_notification (``bool``, optional):
                Sends the message silently.
                
            protect_content (``bool``, optional):
                Protects the contents of the sent message from forwarding and saving.
                
            reply_to_message_id (``int``, optional):
                If the message is a reply, ID of the original message.
                
            allow_sending_without_reply (``bool``, optional):
                Pass True if the message should be sent even if the specified replied-to
                message is not found.
                
            reply_markup (:obj:`InlineKeyboardMarkup` | :obj:`ReplyKeyboardMarkup` | :obj:`ReplyKeyboardRemove` | :obj:`ForceReply`, optional):
                Additional interface options.
                
        Returns:
            :obj:`Message`: On success, the sent Message is returned.
            
        Example:
            .. code-block:: python
            
                # Send a dice (1-6)
                await bot.send_dice(chat_id)
                
                # Send a dartboard (1-6) 
                await bot.send_dice(chat_id, emoji="🎯")
                
                # Send a basketball (miss or hit, 0-5)
                await bot.send_dice(chat_id, emoji="🏀")
                
                # Send a football/soccer (1-5)
                await bot.send_dice(chat_id, emoji="⚽")
                
                # Send a slot machine (variable combination)
                await bot.send_dice(chat_id, emoji="🎰")
                
                # Send a bowling (strike or miss, 0-6)
                await bot.send_dice(chat_id, emoji="🎳")
        """
        self.logger.info(f"Sending dice to {chat_id}")
        
        # Create params dictionary with required parameters
        params = {
            "chat_id": chat_id
        }
        
        # Add emoji if provided
        if emoji:
            params["emoji"] = emoji
            
        # Add optional parameters if provided
        if disable_notification is not None:
            params["disable_notification"] = json.dumps(disable_notification)
            
        if protect_content is not None:
            params["protect_content"] = json.dumps(protect_content)
            
        if reply_to_message_id:
            params["reply_to_message_id"] = reply_to_message_id
            
        if allow_sending_without_reply is not None:
            params["allow_sending_without_reply"] = json.dumps(allow_sending_without_reply)
            
        if reply_markup:
            if hasattr(reply_markup, "to_dict"):
                params["reply_markup"] = json.dumps(reply_markup.to_dict())
            else:
                params["reply_markup"] = json.dumps(reply_markup)
        
        # Make the API request
        return await self._send_dice_request(chat_id, params)
    
    async def _send_dice_request(
        self,
        chat_id: Union[int, str],
        params: dict
    ) -> Message:
        """Send the actual request to the Telegram API.
        
        Returns:
            :obj:`Message`: The sent message or a placeholder in case of error.
        """
        async with aiohttp.ClientSession() as session:
            try:
                url = f"https://api.telegram.org/bot{self.token}/sendDice"
                
                # Following Telethon's pattern for proper HTTP handling
                async with session.post(url, data=params) as response:
                    # Check HTTP status first
                    if response.status != 200:
                        self.logger.error(f"HTTP error {response.status} when sending dice: {await response.text()}")
                        return self._get_dice_fallback_message(chat_id)
                    
                    # Parse the JSON response
                    result = await response.json()
                
                    if not result.get("ok", False):
                        error_description = result.get('description', 'Unknown error')
                        self.logger.error(f"Error sending dice: {error_description}")
                        self.logger.debug(f"Params used: {params}")
                        return self._get_dice_fallback_message(chat_id)
                
                    # Parse the response and create a Message object
                    message_data = result.get("result", {})
                    return Message._parse(self, message_data)
                
            except aiohttp.ClientError as e:
                self.logger.error(f"Network error sending dice: {e}", exc_info=True)
                return self._get_dice_fallback_message(chat_id)
            except Exception as e:
                self.logger.error(f"Error sending dice: {e}", exc_info=True)
                return self._get_dice_fallback_message(chat_id)
    
    def _get_dice_fallback_message(self, chat_id: Union[int, str]) -> Message:
        """Create a fallback message object for error cases.
        
        Returns:
            :obj:`Message`: A placeholder message object.
        """
        return Message(
            message_id=-1,
            date=int(datetime.now().timestamp()),
            chat={"id": int(chat_id) if str(chat_id).lstrip('-').isdigit() else 0, "type": "private"},
            dice={"emoji": "🎲", "value": 1}
        ) 