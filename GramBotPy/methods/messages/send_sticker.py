import typing
import json
import aiohttp
import os
from typing import Union, Optional, BinaryIO
from datetime import datetime

from ...types import Message

if typing.TYPE_CHECKING:
    from ...client import GramBotPy
    from ...types import InlineKeyboardMarkup, ReplyKeyboardMarkup
    from ...types import ReplyKeyboardRemove, ForceReply

class SendSticker:
    """Method for sending stickers."""
    
    async def send_sticker(
        self: "GramBotPy",
        chat_id: Union[int, str],
        sticker: Union[str, BinaryIO],
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
        """Send a sticker.
        
        Parameters:
            chat_id (``int`` | ``str``):
                Unique identifier for the target chat or username.
                
            sticker (``str`` | ``BinaryIO``):
                Sticker to send. Pass a file_id as string to send a sticker that 
                exists on the Telegram servers, pass an HTTP URL for Telegram 
                to get a sticker from the Internet, or pass a file object in binary mode.
                
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
            
                # Send a sticker by file_id
                await bot.send_sticker(chat_id, "CAACAgIAAxkBAAEJzE9kpI9AAx97U...")
                
                # Send a sticker by URL
                await bot.send_sticker(chat_id, "https://example.com/sticker.webp")
                
                # Send a sticker from disk
                with open("sticker.webp", "rb") as f:
                    await bot.send_sticker(chat_id, f)
        """
        self.logger.info(f"Sending sticker to {chat_id}")
        
        # Create form data and handle options
        form, is_file_upload = await self._prepare_sticker_upload(
            chat_id, sticker, disable_notification, protect_content,
            reply_to_message_id, allow_sending_without_reply, reply_markup
        )
        
        # Make the API request
        return await self._send_sticker_request(chat_id, form, is_file_upload)
    
    async def _prepare_sticker_upload(
        self,
        chat_id: Union[int, str],
        sticker: Union[str, BinaryIO],
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
    ) -> tuple:
        """Prepare the form data for sending a sticker.
        
        Returns:
            tuple: (form, is_file_upload) where form is the prepared form data
                and is_file_upload is a boolean indicating if we're uploading a file.
        """
        # Create data dict for form data
        data = {
            "chat_id": chat_id
        }
        
        # Add optional parameters if provided
        if disable_notification is not None:
            data["disable_notification"] = json.dumps(disable_notification)
            
        if protect_content is not None:
            data["protect_content"] = json.dumps(protect_content)
            
        if reply_to_message_id:
            data["reply_to_message_id"] = reply_to_message_id
            
        if allow_sending_without_reply is not None:
            data["allow_sending_without_reply"] = json.dumps(allow_sending_without_reply)
            
        if reply_markup:
            if hasattr(reply_markup, "to_dict"):
                data["reply_markup"] = json.dumps(reply_markup.to_dict())
            else:
                data["reply_markup"] = json.dumps(reply_markup)
            
        # Determine if we're uploading a file or using a file_id/URL
        is_file_upload = False
        form = aiohttp.FormData()
        
        if isinstance(sticker, str):
            # If sticker is a string, it's either a file_id or URL
            data["sticker"] = sticker
            for key, value in data.items():
                form.add_field(key, str(value))
        else:
            # If sticker is a file-like object
            is_file_upload = True
            for key, value in data.items():
                form.add_field(key, str(value))
                
            # Try to get filename from file object if possible
            filename = getattr(sticker, 'name', 'sticker.webp')
            if hasattr(sticker, 'name'):
                # Extract just the filename, not the full path
                filename = os.path.basename(filename)
                
            # Default content type for stickers is webp
            content_type = 'image/webp'
            if filename.lower().endswith(('.tgs')):
                content_type = 'application/x-tgsticker'  # Animated sticker
                
            form.add_field('sticker', sticker, filename=filename, content_type=content_type)
                
        return form, is_file_upload
    
    async def _send_sticker_request(
        self,
        chat_id: Union[int, str],
        form: aiohttp.FormData,
        is_file_upload: bool
    ) -> Message:
        """Send the actual request to the Telegram API.
        
        Returns:
            :obj:`Message`: The sent message or a placeholder in case of error.
        """
        # Make the API request
        async with aiohttp.ClientSession() as session:
            try:
                url = f"https://api.telegram.org/bot{self.token}/sendSticker"
                
                # Following Telethon's pattern for proper HTTP handling
                async with session.post(url, data=form) as response:
                    # Check HTTP status first
                    if response.status != 200:
                        self.logger.error(f"HTTP error {response.status} when sending sticker: {await response.text()}")
                        return self._get_fallback_message(chat_id)
                    
                    # Parse the JSON response
                    result = await response.json()
                
                    if not result.get("ok", False):
                        error_description = result.get('description', 'Unknown error')
                        self.logger.error(f"Error sending sticker: {error_description}")
                        
                        # More detailed errors for file uploads
                        if is_file_upload:
                            self.logger.debug(f"Failed to upload sticker file. Check file format and permissions.")
                            
                        return self._get_fallback_message(chat_id)
                
                    # Parse the response and create a Message object
                    message_data = result.get("result", {})
                    return Message._parse(self, message_data)
                
            except aiohttp.ClientError as e:
                self.logger.error(f"Network error sending sticker: {e}", exc_info=True)
                return self._get_fallback_message(chat_id)
            except Exception as e:
                self.logger.error(f"Error sending sticker: {e}", exc_info=True)
                return self._get_fallback_message(chat_id)
    
    def _get_fallback_message(self, chat_id: Union[int, str]) -> Message:
        """Create a fallback message object for error cases.
        
        Returns:
            :obj:`Message`: A placeholder message object.
        """
        return Message(
            message_id=-1,
            date=int(datetime.now().timestamp()),
            chat={"id": int(chat_id) if str(chat_id).lstrip('-').isdigit() else 0, "type": "private"},
            sticker={"file_id": "error", "width": 0, "height": 0, "file_size": 0}
        ) 