import asyncio
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

class SendVideo:
    """Method for sending videos."""
    
    async def send_video(
        self: "GramBotPy",
        chat_id: Union[int, str],
        video: Union[str, BinaryIO],
        caption: Optional[str] = None,
        parse_mode: Optional[str] = None,
        caption_entities: Optional[List[dict]] = None,
        duration: Optional[int] = None,
        width: Optional[int] = None,
        height: Optional[int] = None,
        thumb: Optional[Union[str, BinaryIO]] = None,
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
        supports_streaming: Optional[bool] = None,
        nosound_video: Optional[bool] = None
    ) -> "Message":
        """Send a video.
        
        Parameters:
            chat_id (``int`` | ``str``):
                Unique identifier for the target chat or username.
                
            video (``str`` | ``BinaryIO``):
                Video to send. Pass a file_id as string to send a video that 
                exists on the Telegram servers, pass an HTTP URL for Telegram 
                to get a video from the Internet, or pass a file object in binary mode.
                
            caption (``str``, optional):
                Video caption, 0-1024 characters.
                
            parse_mode (``str``, optional):
                Mode for parsing entities in the video caption.
                
            caption_entities (``list``, optional):
                List of special entities that appear in the caption.
                
            duration (``int``, optional):
                Duration of sent video in seconds.
                
            width (``int``, optional):
                Video width.
                
            height (``int``, optional):
                Video height.
                
            thumb (``str`` | ``BinaryIO``, optional):
                Thumbnail of the video.
                
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
                
            supports_streaming (``bool``, optional):
                Pass True if the uploaded video is suitable for streaming.
                
            nosound_video (``bool``, optional):
                Pass True if the video doesn't have sound. Requires format change in some clients.
                
        Returns:
            :obj:`Message`: On success, the sent Message is returned.
            
        Example:
            .. code-block:: python
            
                # Send a video by file_id
                await bot.send_video(chat_id, "BAACAgEAAxkBAAIBs2RoKXAKq9KnG...")
                
                # Send a video by URL
                await bot.send_video(chat_id, "https://example.com/video.mp4", 
                                    caption="Video sent via URL")
                
                # Send a video from disk
                with open("video.mp4", "rb") as f:
                    await bot.send_video(chat_id, f, caption="Local video")
        """
        self.logger.info(f"Sending video to {chat_id}")
        
        # Create form data and handle options
        form, is_file_upload = await self._prepare_video_upload(
            chat_id, video, caption, parse_mode, caption_entities,
            duration, width, height, thumb, disable_notification,
            protect_content, reply_to_message_id, allow_sending_without_reply,
            reply_markup, supports_streaming, nosound_video
        )
        
        # Make the API request
        return await self._send_video_request(chat_id, caption, form, is_file_upload)
    
    async def _prepare_video_upload(
        self,
        chat_id: Union[int, str],
        video: Union[str, BinaryIO],
        caption: Optional[str] = None,
        parse_mode: Optional[str] = None,
        caption_entities: Optional[List[dict]] = None,
        duration: Optional[int] = None,
        width: Optional[int] = None,
        height: Optional[int] = None,
        thumb: Optional[Union[str, BinaryIO]] = None,
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
        supports_streaming: Optional[bool] = None,
        nosound_video: Optional[bool] = None
    ) -> tuple:
        """Prepare the form data for sending a video.
        
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
                
        if supports_streaming is not None:
            data["supports_streaming"] = json.dumps(supports_streaming)
            
        if nosound_video is not None:
            data["has_spoiler"] = json.dumps(nosound_video)
            
        # Determine if we're uploading a file or using a file_id/URL
        is_file_upload = False
        form = aiohttp.FormData()
        
        if isinstance(video, str):
            # If video is a string, it's either a file_id or URL
            data["video"] = video
            for key, value in data.items():
                form.add_field(key, str(value))
        else:
            # If video is a file-like object
            is_file_upload = True
            for key, value in data.items():
                form.add_field(key, str(value))
                
            # Try to get filename from file object if possible
            filename = getattr(video, 'name', 'video.mp4')
            if hasattr(video, 'name'):
                # Extract just the filename, not the full path
                filename = os.path.basename(video.name)
                
            form.add_field('video', video, filename=filename, content_type='video/mp4')
            
        # Handle thumbnail if provided
        if thumb:
            if isinstance(thumb, str):
                form.add_field("thumb", thumb)
            else:
                is_file_upload = True
                thumb_filename = getattr(thumb, 'name', 'thumb.jpg')
                if hasattr(thumb, 'name'):
                    thumb_filename = os.path.basename(thumb.name)
                form.add_field('thumb', thumb, filename=thumb_filename, content_type='image/jpeg')
                
        return form, is_file_upload
    
    async def _send_video_request(
        self,
        chat_id: Union[int, str],
        caption: Optional[str],
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
                url = f"https://api.telegram.org/bot{self.token}/sendVideo"
                
                # Following Telethon's pattern for proper HTTP handling
                async with session.post(url, data=form) as response:
                    # Check HTTP status first
                    if response.status != 200:
                        self.logger.error(f"HTTP error {response.status} when sending video: {await response.text()}")
                        return self._get_fallback_message(chat_id, caption)
                    
                    # Parse the JSON response
                    result = await response.json()
                
                    if not result.get("ok", False):
                        error_description = result.get('description', 'Unknown error')
                        self.logger.error(f"Error sending video: {error_description}")
                        
                        # More detailed errors for file uploads
                        if is_file_upload:
                            self.logger.debug(f"Failed to upload video file. Check file format and permissions.")
                            
                        return self._get_fallback_message(chat_id, caption)
                
                    # Parse the response and create a Message object
                    message_data = result.get("result", {})
                    return Message._parse(self, message_data)
                
            except aiohttp.ClientError as e:
                self.logger.error(f"Network error sending video: {e}", exc_info=True)
                return self._get_fallback_message(chat_id, caption)
            except Exception as e:
                self.logger.error(f"Error sending video: {e}", exc_info=True)
                return self._get_fallback_message(chat_id, caption)
    
    def _get_fallback_message(self, chat_id: Union[int, str], caption: Optional[str]) -> Message:
        """Create a fallback message object for error cases.
        
        Returns:
            :obj:`Message`: A placeholder message object.
        """
        return Message(
            message_id=-1,
            date=int(datetime.now().timestamp()),
            chat={"id": int(chat_id) if str(chat_id).lstrip('-').isdigit() else 0, "type": "private"},
            caption=caption
        ) 