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

class SendAnimation:
    """Method for sending animations (GIFs)."""
    
    async def send_animation(
        self: "GramBotPy",
        chat_id: Union[int, str],
        animation: Union[str, BinaryIO],
        thumb: Optional[Union[str, BinaryIO]] = None,
        caption: Optional[str] = None,
        parse_mode: Optional[str] = None,
        caption_entities: Optional[List[dict]] = None,
        duration: Optional[int] = None,
        width: Optional[int] = None,
        height: Optional[int] = None,
        disable_notification: Optional[bool] = None,
        protect_content: Optional[bool] = None,
        reply_to_message_id: Optional[int] = None,
        allow_sending_without_reply: Optional[bool] = None,
        reply_markup: Optional[Union[
            "InlineKeyboardMarkup",
            "ReplyKeyboardMarkup",
            "ReplyKeyboardRemove",
            "ForceReply"
        ]] = None,
        has_spoiler: Optional[bool] = None
    ) -> "Message":
        """Send an animation (GIF).
        
        Parameters:
            chat_id (``int`` | ``str``):
                Unique identifier for the target chat or username.
                
            animation (``str`` | ``BinaryIO``):
                Animation to send. Pass a file_id as string to send an animation that 
                exists on the Telegram servers, pass an HTTP URL for Telegram 
                to get an animation from the Internet, or pass a file object in binary mode.
                
            thumb (``str`` | ``BinaryIO``, optional):
                Thumbnail of the file.
                
            caption (``str``, optional):
                Animation caption, 0-1024 characters.
                
            parse_mode (``str``, optional):
                Mode for parsing entities in the animation caption.
                
            caption_entities (``list``, optional):
                List of special entities that appear in the caption.
                
            duration (``int``, optional):
                Duration of animation in seconds.
                
            width (``int``, optional):
                Animation width.
                
            height (``int``, optional):
                Animation height.
                
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

            has_spoiler (``bool``, optional):
                Pass True if the animation needs to be covered with a spoiler animation.
                
        Returns:
            :obj:`Message`: On success, the sent Message is returned.
            
        Example:
            .. code-block:: python
            
                # Send an animation by file_id
                await bot.send_animation(chat_id, "CgACAgEAAxkBAAIBs2RoKXAKq9...")
                
                # Send an animation by URL
                await bot.send_animation(chat_id, "https://example.com/animation.gif", 
                                       caption="Animation sent via URL")
                
                # Send an animation from disk
                with open("animation.gif", "rb") as f:
                    await bot.send_animation(chat_id, f, caption="Local animation")
        """
        self.logger.info(f"Sending animation to {chat_id}")
        
        # Create form data and handle options
        form, is_file_upload = await self._prepare_animation_upload(
            chat_id, animation, thumb, caption, parse_mode, caption_entities,
            duration, width, height, disable_notification, protect_content,
            reply_to_message_id, allow_sending_without_reply, reply_markup, has_spoiler
        )
        
        # Make the API request
        return await self._send_animation_request(chat_id, form, is_file_upload)
    
    async def _prepare_animation_upload(
        self,
        chat_id: Union[int, str],
        animation: Union[str, BinaryIO],
        thumb: Optional[Union[str, BinaryIO]] = None,
        caption: Optional[str] = None,
        parse_mode: Optional[str] = None,
        caption_entities: Optional[List[dict]] = None,
        duration: Optional[int] = None,
        width: Optional[int] = None,
        height: Optional[int] = None,
        disable_notification: Optional[bool] = None,
        protect_content: Optional[bool] = None,
        reply_to_message_id: Optional[int] = None,
        allow_sending_without_reply: Optional[bool] = None,
        reply_markup: Optional[Union[
            "InlineKeyboardMarkup",
            "ReplyKeyboardMarkup",
            "ReplyKeyboardRemove",
            "ForceReply"
        ]] = None,
        has_spoiler: Optional[bool] = None
    ) -> tuple:
        """Prepare the form data for sending an animation.
        
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
            
        if width:
            data["width"] = width
            
        if height:
            data["height"] = height
            
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
        
        if has_spoiler is not None:
            data["has_spoiler"] = json.dumps(has_spoiler)
            
        # Determine if we're uploading a file or using a file_id/URL
        is_file_upload = False
        form = aiohttp.FormData()
        
        if isinstance(animation, str):
            # If animation is a string, it's either a file_id or URL
            data["animation"] = animation
            for key, value in data.items():
                form.add_field(key, str(value))
        else:
            # If animation is a file-like object
            is_file_upload = True
            for key, value in data.items():
                form.add_field(key, str(value))
                
            # Try to get filename from file object if possible
            filename = getattr(animation, 'name', 'animation.gif')
            if hasattr(animation, 'name'):
                # Extract just the filename, not the full path
                filename = os.path.basename(filename)
                
            # Set content type based on extension
            content_type = 'image/gif'
            if filename.lower().endswith(('.mp4')):
                content_type = 'video/mp4'
                
            form.add_field('animation', animation, filename=filename, content_type=content_type)
                
        # Handle thumbnail if provided
        if thumb:
            if isinstance(thumb, str):
                # If thumb is a string, it's either a file_id or URL
                form.add_field('thumb', thumb)
            else:
                # If thumb is a file-like object
                thumb_filename = getattr(thumb, 'name', 'thumb.jpg')
                if hasattr(thumb, 'name'):
                    thumb_filename = os.path.basename(thumb_filename)
                form.add_field('thumb', thumb, filename=thumb_filename, content_type='image/jpeg')
                
        return form, is_file_upload
    
    async def _send_animation_request(
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
                url = f"https://api.telegram.org/bot{self.token}/sendAnimation"
                
                # Following Telethon's pattern for proper HTTP handling
                async with session.post(url, data=form) as response:
                    # Check HTTP status first
                    if response.status != 200:
                        self.logger.error(f"HTTP error {response.status} when sending animation: {await response.text()}")
                        return self._get_animation_fallback_message(chat_id)
                    
                    # Parse the JSON response
                    result = await response.json()
                
                    if not result.get("ok", False):
                        error_description = result.get('description', 'Unknown error')
                        self.logger.error(f"Error sending animation: {error_description}")
                        
                        # More detailed errors for file uploads
                        if is_file_upload:
                            self.logger.debug(f"Failed to upload animation file. Check file format and permissions.")
                            
                        return self._get_animation_fallback_message(chat_id)
                
                    # Parse the response and create a Message object
                    message_data = result.get("result", {})
                    return Message._parse(self, message_data)
                
            except aiohttp.ClientError as e:
                self.logger.error(f"Network error sending animation: {e}", exc_info=True)
                return self._get_animation_fallback_message(chat_id)
            except Exception as e:
                self.logger.error(f"Error sending animation: {e}", exc_info=True)
                return self._get_animation_fallback_message(chat_id)
    
    def _get_animation_fallback_message(self, chat_id: Union[int, str]) -> Message:
        """Create a fallback message object for error cases.
        
        Returns:
            :obj:`Message`: A placeholder message object.
        """
        return Message(
            message_id=-1,
            date=int(datetime.now().timestamp()),
            chat={"id": int(chat_id) if str(chat_id).lstrip('-').isdigit() else 0, "type": "private"},
            animation={"file_id": "error", "file_unique_id": "error", "width": 0, "height": 0, "duration": 0, "file_size": 0}
        ) 