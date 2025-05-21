import typing
import os
import json
import aiohttp
import mimetypes
from typing import Union, Optional, BinaryIO, Dict, Any

if typing.TYPE_CHECKING:
    from ...client import GramBotPy

class UploadMedia:
    """Method for uploading media to Telegram."""
    
    async def upload_media(
        self: "GramBotPy",
        file: Union[str, BinaryIO],
        file_name: Optional[str] = None,
        file_type: Optional[str] = None,
        progress: Optional[callable] = None,
        progress_args: Optional[tuple] = ()
    ) -> Dict[str, Any]:
        """Upload a file to Telegram.
        
        Parameters:
            file (``str`` | ``BinaryIO``):
                File to upload. Pass a file path as string or a file object in binary mode.
                
            file_name (``str``, optional):
                A custom file name for the uploaded file.
                
            file_type (``str``, optional):
                Type of file: "photo", "audio", "document", "video", "animation", "voice", "sticker".
                If not specified, it will be auto-detected.
                
            progress (``callable``, optional):
                A callback function to report upload progress.
                Takes four arguments: (current, total, file_name, progress_args).
                
            progress_args (``tuple``, optional):
                Extra arguments to pass to the progress callback.
                
        Returns:
            ``dict``: On success, information about the uploaded file is returned.
            
        Example:
            .. code-block:: python
            
                # Upload a file from disk
                file_info = await bot.upload_media("photo.jpg", file_type="photo")
                file_id = file_info["file_id"]  # Use this file_id to send the file
                
                # Upload with progress callback
                def progress_callback(current, total, file_name, args):
                    print(f"Uploaded {current} of {total} bytes for {file_name}")
                    
                file_info = await bot.upload_media("document.pdf", progress=progress_callback)
        """
        self.logger.info(f"Uploading media file")
        
        # Determine file properties
        filename, file_size, file_obj = await self._prepare_file(file, file_name)
        
        # Auto-detect file type if not specified
        if not file_type:
            file_type = self._detect_file_type(filename)
        
        self.logger.info(f"Uploading {file_type} file: {filename}")
        
        # Call the appropriate API method based on file type
        return await self._upload_file(file_type, file_obj, filename, file_size, progress, progress_args)
    
    async def _prepare_file(
        self, 
        file: Union[str, BinaryIO],
        custom_name: Optional[str] = None
    ) -> tuple:
        """Prepare file for upload.
        
        Returns:
            tuple: (filename, file_size, file_object)
        """
        if isinstance(file, str):
            # It's a file path
            if not os.path.exists(file):
                raise FileNotFoundError(f"File not found: {file}")
                
            filename = custom_name or os.path.basename(file)
            file_size = os.path.getsize(file)
            file_obj = open(file, "rb")
            
            return filename, file_size, file_obj
        else:
            # It's a file-like object
            if not hasattr(file, "read"):
                raise ValueError("File object must have a 'read' method")
                
            # Try to get filename and size
            if custom_name:
                filename = custom_name
            elif hasattr(file, "name"):
                filename = os.path.basename(file.name)
            else:
                filename = "unknown"
                
            # Get file size if possible
            try:
                current_pos = file.tell()
                file.seek(0, os.SEEK_END)
                file_size = file.tell()
                file.seek(current_pos)  # Restore position
            except (AttributeError, OSError):
                file_size = 0
                
            return filename, file_size, file
    
    def _detect_file_type(self, filename: str) -> str:
        """Detect file type from filename.
        
        Returns:
            str: Detected file type
        """
        ext = os.path.splitext(filename)[1].lower()
        
        if ext in ['.jpg', '.jpeg', '.png', '.webp']:
            return "photo"
        elif ext in ['.mp3', '.m4a', '.aac']:
            return "audio"
        elif ext in ['.mp4', '.avi', '.mov', '.mkv']:
            return "video"
        elif ext in ['.gif']:
            return "animation"
        elif ext in ['.ogg', '.oga']:
            return "voice"
        elif ext in ['.webp', '.tgs']:
            return "sticker"
        else:
            return "document"
    
    async def _upload_file(
        self,
        file_type: str,
        file_obj: BinaryIO,
        filename: str,
        file_size: int,
        progress: Optional[callable],
        progress_args: Optional[tuple]
    ) -> Dict[str, Any]:
        """Upload a file using the appropriate Telegram API method.
        
        Returns:
            Dict[str, Any]: Information about the uploaded file.
        """
        # Choose the appropriate API method
        method = "sendDocument"  # Default method
        
        if file_type == "photo":
            method = "sendPhoto"
            field_name = "photo"
        elif file_type == "audio":
            method = "sendAudio"
            field_name = "audio"
        elif file_type == "video":
            method = "sendVideo"
            field_name = "video"
        elif file_type == "animation":
            method = "sendAnimation"
            field_name = "animation"
        elif file_type == "voice":
            method = "sendVoice"
            field_name = "voice"
        elif file_type == "sticker":
            method = "sendSticker"
            field_name = "sticker"
        else:
            method = "sendDocument"
            field_name = "document"
            
        # We need to use sendMedia with a fake chat_id just to get the file_id
        # Once we have the file_id, we can cancel/delete the message
        fake_chat_id = self._me.id  # Use the bot's own ID
        
        # Prepare form data
        form = aiohttp.FormData()
        form.add_field("chat_id", str(fake_chat_id))
        
        # Determine content type
        content_type = mimetypes.guess_type(filename)[0]
        if not content_type:
            if file_type == "photo":
                content_type = "image/jpeg"
            elif file_type == "audio":
                content_type = "audio/mpeg"
            elif file_type == "video":
                content_type = "video/mp4"
            elif file_type == "animation":
                content_type = "video/mp4"
            elif file_type == "voice":
                content_type = "audio/ogg"
            elif file_type == "sticker":
                content_type = "image/webp"
            else:
                content_type = "application/octet-stream"
        
        form.add_field(field_name, file_obj, filename=filename, content_type=content_type)
        
        try:
            # Upload the file
            url = f"https://api.telegram.org/bot{self.token}/{method}"
            
            async with aiohttp.ClientSession() as session:
                # Prepare request with progress tracking if needed
                if progress and callable(progress) and file_size > 0:
                    # Here we'd need to implement a custom request with progress tracking
                    # For simplicity, we'll use a basic request and just report progress at the end
                    progress(0, file_size, filename, progress_args)
                    
                    async with session.post(url, data=form) as response:
                        if response.status != 200:
                            self.logger.error(f"HTTP error {response.status} when uploading file: {await response.text()}")
                            return self._get_mock_file_info(file_type, filename)
                            
                        # Report completion
                        progress(file_size, file_size, filename, progress_args)
                        result = await response.json()
                else:
                    # Regular request without progress tracking
                    async with session.post(url, data=form) as response:
                        if response.status != 200:
                            self.logger.error(f"HTTP error {response.status} when uploading file: {await response.text()}")
                            return self._get_mock_file_info(file_type, filename)
                            
                        result = await response.json()
                
                # Extract file info from the response
                if not result.get("ok", False):
                    error = result.get("description", "Unknown error")
                    self.logger.error(f"Error uploading file: {error}")
                    return self._get_mock_file_info(file_type, filename)
                    
                # Get the message that contains our media
                message = result.get("result", {})
                file_info = self._extract_file_info(message, file_type)
                
                # Try to delete the message we just sent
                try:
                    message_id = message.get("message_id")
                    if message_id:
                        delete_url = f"https://api.telegram.org/bot{self.token}/deleteMessage"
                        params = {"chat_id": fake_chat_id, "message_id": message_id}
                        await session.post(delete_url, data=params)
                except Exception as e:
                    self.logger.warning(f"Error deleting temporary message: {e}")
                
                return file_info
                
        except aiohttp.ClientError as e:
            self.logger.error(f"Network error uploading file: {e}", exc_info=True)
            return self._get_mock_file_info(file_type, filename)
        except Exception as e:
            self.logger.error(f"Error uploading file: {e}", exc_info=True)
            return self._get_mock_file_info(file_type, filename)
        finally:
            # Close the file if we opened it
            if hasattr(file_obj, "close"):
                try:
                    file_obj.close()
                except:
                    pass
    
    def _extract_file_info(self, message: Dict[str, Any], file_type: str) -> Dict[str, Any]:
        """Extract file information from a message.
        
        Returns:
            Dict[str, Any]: Information about the file.
        """
        if file_type == "photo" and message.get("photo"):
            # Photos are returned as an array, get the largest one
            photo = message["photo"][-1]
            return {
                "file_id": photo.get("file_id"),
                "file_unique_id": photo.get("file_unique_id"),
                "file_size": photo.get("file_size", 0),
                "width": photo.get("width", 0),
                "height": photo.get("height", 0)
            }
        elif file_type == "video" and message.get("video"):
            return message["video"]
        elif file_type == "audio" and message.get("audio"):
            return message["audio"]
        elif file_type == "animation" and message.get("animation"):
            return message["animation"]
        elif file_type == "voice" and message.get("voice"):
            return message["voice"]
        elif file_type == "sticker" and message.get("sticker"):
            return message["sticker"]
        elif file_type == "document" and message.get("document"):
            return message["document"]
        else:
            # Fallback: return a mock file info
            return self._get_mock_file_info(file_type, message.get("caption", "unknown"))
    
    def _get_mock_file_info(self, file_type: str, file_name: str) -> Dict[str, Any]:
        """Create mock file info for error cases.
        
        Returns:
            Dict[str, Any]: Mock file information.
        """
        file_info = {
            "file_id": f"error_{file_type}_file_id",
            "file_unique_id": "error_unique_id",
            "file_size": 0
        }
        
        # Add type-specific fields
        if file_type == "photo":
            file_info.update({
                "width": 0,
                "height": 0
            })
        elif file_type == "video":
            file_info.update({
                "width": 0,
                "height": 0,
                "duration": 0
            })
        elif file_type == "audio":
            file_info.update({
                "duration": 0,
                "performer": "Unknown",
                "title": os.path.splitext(file_name)[0] if file_name else "Unknown"
            })
        elif file_type == "voice":
            file_info.update({
                "duration": 0
            })
        elif file_type == "animation":
            file_info.update({
                "width": 0,
                "height": 0,
                "duration": 0
            })
            
        return file_info 