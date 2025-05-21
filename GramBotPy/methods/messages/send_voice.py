import typing
import json
import aiohttp
import os
from typing import Union, Optional, BinaryIO, List
from datetime import datetime

from ...types import Message

if typing.TYPE_CHECKING:
    from ...client import GramBotPy
    from ...types import InlineKeyboardMarkup, ReplyKeyboardMarkup
    from ...types import ReplyKeyboardRemove, ForceReply

class SendVoice:
    """Method for sending voice messages."""
    
    async def send_voice(
        self: "GramBotPy",
        chat_id: Union[int, str],
        voice: Union[str, BinaryIO],
        caption: Optional[str] = None,
        parse_mode: Optional[str] = None,
        caption_entities: Optional[List[dict]] = None,
        duration: Optional[int] = None,
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
        """Send a voice message.
        
        Parameters:
            chat_id (``int`` | ``str``):
                Unique identifier for the target chat or username.
                
            voice (``str`` | ``BinaryIO``):
                Voice message to send. Pass a file_id as string to send a voice message that 
                exists on the Telegram servers, pass an HTTP URL for Telegram 
                to get a voice message from the Internet, or pass a file object in binary mode.
                
            caption (``str``, optional):
                Voice message caption, 0-1024 characters.
                
            parse_mode (``str``, optional):
                Mode for parsing entities in the voice message caption.
                
            caption_entities (``list``, optional):
                List of special entities that appear in the caption.
                
            duration (``int``, optional):
                Duration of the voice message in seconds.
                
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
            
                # Send a voice message by file_id
                await bot.send_voice(chat_id, "AwACAgEAAxkBAAIBs2RoKXAKq9...")
                
                # Send a voice message by URL
                await bot.send_voice(chat_id, "https://example.com/voice.ogg", 
                                    caption="Voice message sent via URL")
                
                # Send a voice message from disk
                with open("voice.ogg", "rb") as f:
                    await bot.send_voice(chat_id, f, caption="Local voice message")
        """
        self.logger.info(f"Sending voice message to {chat_id}")
        
        # Create form data and handle options
        form, is_file_upload = await self._prepare_voice_upload(
            chat_id, voice, caption, parse_mode, caption_entities,
            duration, disable_notification, protect_content,
            reply_to_message_id, allow_sending_without_reply, reply_markup
        )
        
        # Make the API request
        return await self._send_voice_request(chat_id, form, is_file_upload)
    
    async def _prepare_voice_upload(
        self,
        chat_id: Union[int, str],
        voice: Union[str, BinaryIO],
        caption: Optional[str] = None,
        parse_mode: Optional[str] = None,
        caption_entities: Optional[List[dict]] = None,
        duration: Optional[int] = None,
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
        """Prepare the form data for sending a voice message.
        
        Returns:
            tuple: (form, is_file_upload) where form is the prepared form data
                and is_file_upload is a boolean indicating if we're uploading a file.
        """
        # Create data dict for form data
        data = {
            "chat_id": chat_id
        }
        
        # Add optional parameters if provided
        if caption:
            data["caption"] = caption
            
        if parse_mode:
            data["parse_mode"] = parse_mode
            
        if caption_entities:
            data["caption_entities"] = json.dumps(caption_entities)
            
        if duration:
            data["duration"] = duration
            
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
        
        if isinstance(voice, str):
            # If voice is a string, it's either a file_id or URL
            data["voice"] = voice
            for key, value in data.items():
                form.add_field(key, str(value))
        else:
            # If voice is a file-like object
            is_file_upload = True
            for key, value in data.items():
                form.add_field(key, str(value))
                
            # Try to get filename from file object if possible
            filename = getattr(voice, 'name', 'voice.ogg')
            if hasattr(voice, 'name'):
                # Extract just the filename, not the full path
                filename = os.path.basename(filename)
                
            # Default content type for voice is ogg
            content_type = 'audio/ogg'
            if filename.lower().endswith(('.mp3')):
                content_type = 'audio/mpeg'
                
            form.add_field('voice', voice, filename=filename, content_type=content_type)
                
        return form, is_file_upload
    
    async def _send_voice_request(
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
                url = f"https://api.telegram.org/bot{self.token}/sendVoice"
                
                # Following Telethon's pattern for proper HTTP handling
                async with session.post(url, data=form) as response:
                    # Check HTTP status first
                    if response.status != 200:
                        self.logger.error(f"HTTP error {response.status} when sending voice: {await response.text()}")
                        return self._get_voice_fallback_message(chat_id)
                    
                    # Parse the JSON response
                    result = await response.json()
                
                    if not result.get("ok", False):
                        error_description = result.get('description', 'Unknown error')
                        self.logger.error(f"Error sending voice: {error_description}")
                        
                        # More detailed errors for file uploads
                        if is_file_upload:
                            self.logger.debug(f"Failed to upload voice file. Check file format and permissions.")
                            
                        return self._get_voice_fallback_message(chat_id)
                
                    # Parse the response and create a Message object
                    message_data = result.get("result", {})
                    return Message._parse(self, message_data)
                
            except aiohttp.ClientError as e:
                self.logger.error(f"Network error sending voice: {e}", exc_info=True)
                return self._get_voice_fallback_message(chat_id)
            except Exception as e:
                self.logger.error(f"Error sending voice: {e}", exc_info=True)
                return self._get_voice_fallback_message(chat_id)
    
    def _get_voice_fallback_message(self, chat_id: Union[int, str]) -> Message:
        """Create a fallback message object for error cases.
        
        Returns:
            :obj:`Message`: A placeholder message object.
        """
        return Message(
            message_id=-1,
            date=int(datetime.now().timestamp()),
            chat={"id": int(chat_id) if str(chat_id).lstrip('-').isdigit() else 0, "type": "private"},
            voice={"file_id": "error", "file_unique_id": "error", "duration": 0, "file_size": 0, "mime_type": "audio/ogg"}
        ) 