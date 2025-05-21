import os
import typing
import aiohttp
import asyncio
from typing import Union, Optional, BinaryIO, Any, Dict

if typing.TYPE_CHECKING:
    from ...client import GramBotPy
    from ...types import Message

class DownloadMedia:
    """Method for downloading media from messages."""
    
    async def download_media(
        self: "GramBotPy",
        message: Union["Message", Any],
        file_name: Optional[str] = None,
        in_memory: Optional[bool] = None,
        block: Optional[bool] = True,
        progress: Optional[callable] = None,
        progress_args: Optional[tuple] = ()
    ) -> Optional[Union[str, bytes, BinaryIO]]:
        """Download the media from a message.
        
        Parameters:
            message (:obj:`Message` | ``object``):
                Message containing the media to be downloaded.
                
            file_name (``str``, optional):
                A custom path to save the file. If not specified,
                the file will be saved in the current working directory
                with its original name.
                
            in_memory (``bool``, optional):
                Whether to return the file as bytes instead of saving it to disk.
                
            block (``bool``, optional):
                Whether to block (wait) until the download is complete.
                
            progress (``callable``, optional):
                A callback function to report download progress.
                Takes four arguments: (current, total, file_name, progress_args).
                
            progress_args (``tuple``, optional):
                Extra arguments to pass to the progress callback.
                
        Returns:
            ``str`` | ``bytes`` | ``None``: On success, if file_name is given, the file path
            is returned. If in_memory is True, the file content is returned as bytes.
            Otherwise, None is returned.
            
        Example:
            .. code-block:: python
            
                # Download to a custom path
                file_path = await bot.download_media(message, "photo.jpg")
                
                # Download in memory
                file_bytes = await bot.download_media(message, in_memory=True)
                
                # Download with progress
                def progress_callback(current, total, file_name, args):
                    print(f"Downloaded {current} of {total} bytes for {file_name}")
                    
                file_path = await bot.download_media(message, progress=progress_callback)
        """
        self.logger.info(f"Downloading media from message")
        
        if not message:
            raise ValueError("Message not provided")
            
        # Extract file_id and determine media type
        file_id, media_type, file_size, file_unique_id = await self._extract_file_info(message)
        
        if not file_id:
            raise ValueError("Message does not contain downloadable media")
            
        self.logger.info(f"Downloading {media_type} with file_id {file_id}")
        
        # Get file path from Telegram to download
        file_path = await self._get_file_path(file_id)
        if not file_path:
            raise ValueError(f"Could not get download path for file {file_id}")
            
        # Determine the local file name/path for saving
        local_path = self._determine_file_path(file_id, file_path, media_type, file_name)
        
        # Download the file
        return await self._download_file(
            file_path, local_path, in_memory, 
            file_size, progress, progress_args
        )
    
    async def _extract_file_info(
        self, message: Union["Message", Any]
    ) -> tuple:
        """Extract file ID and type from a message.
        
        Returns:
            tuple: (file_id, media_type, file_size, file_unique_id)
        """
        file_id = None
        file_size = 0
        file_unique_id = None
        media_type = None
        
        # Handle various message types
        if hasattr(message, "photo") and message.photo:
            # Photos come as an array of PhotoSize, get the largest one
            media_type = "photo"
            if isinstance(message.photo, list) and len(message.photo) > 0:
                # Get the largest photo (last in array)
                photo = message.photo[-1]
                file_id = photo.get("file_id")
                file_size = photo.get("file_size", 0)
                file_unique_id = photo.get("file_unique_id")
                
        elif hasattr(message, "video") and message.video:
            media_type = "video"
            file_id = message.video.get("file_id")
            file_size = message.video.get("file_size", 0)
            file_unique_id = message.video.get("file_unique_id")
            
        elif hasattr(message, "audio") and message.audio:
            media_type = "audio"
            file_id = message.audio.get("file_id")
            file_size = message.audio.get("file_size", 0)
            file_unique_id = message.audio.get("file_unique_id")
            
        elif hasattr(message, "document") and message.document:
            media_type = "document"
            file_id = message.document.get("file_id")
            file_size = message.document.get("file_size", 0)
            file_unique_id = message.document.get("file_unique_id")
            
        elif hasattr(message, "voice") and message.voice:
            media_type = "voice"
            file_id = message.voice.get("file_id")
            file_size = message.voice.get("file_size", 0)
            file_unique_id = message.voice.get("file_unique_id")
            
        elif hasattr(message, "sticker") and message.sticker:
            media_type = "sticker"
            file_id = message.sticker.get("file_id")
            file_size = message.sticker.get("file_size", 0)
            file_unique_id = message.sticker.get("file_unique_id")
            
        elif hasattr(message, "animation") and message.animation:
            media_type = "animation"
            file_id = message.animation.get("file_id")
            file_size = message.animation.get("file_size", 0)
            file_unique_id = message.animation.get("file_unique_id")
            
        # Handle dict-like objects
        elif isinstance(message, dict) or hasattr(message, "get"):
            if message.get("photo"):
                media_type = "photo"
                if isinstance(message["photo"], list) and len(message["photo"]) > 0:
                    photo = message["photo"][-1]
                    file_id = photo.get("file_id")
                    file_size = photo.get("file_size", 0)
                    file_unique_id = photo.get("file_unique_id")
            elif message.get("video"):
                media_type = "video"
                file_id = message["video"].get("file_id")
                file_size = message["video"].get("file_size", 0)
                file_unique_id = message["video"].get("file_unique_id")
            elif message.get("audio"):
                media_type = "audio"
                file_id = message["audio"].get("file_id")
                file_size = message["audio"].get("file_size", 0)
                file_unique_id = message["audio"].get("file_unique_id")
            elif message.get("document"):
                media_type = "document"
                file_id = message["document"].get("file_id")
                file_size = message["document"].get("file_size", 0)
                file_unique_id = message["document"].get("file_unique_id")
            elif message.get("voice"):
                media_type = "voice"
                file_id = message["voice"].get("file_id")
                file_size = message["voice"].get("file_size", 0)
                file_unique_id = message["voice"].get("file_unique_id")
            elif message.get("sticker"):
                media_type = "sticker"
                file_id = message["sticker"].get("file_id")
                file_size = message["sticker"].get("file_size", 0)
                file_unique_id = message["sticker"].get("file_unique_id")
            elif message.get("animation"):
                media_type = "animation"
                file_id = message["animation"].get("file_id")
                file_size = message["animation"].get("file_size", 0)
                file_unique_id = message["animation"].get("file_unique_id")
                
        return file_id, media_type, file_size, file_unique_id
    
    async def _get_file_path(self, file_id: str) -> Optional[str]:
        """Get the file path from Telegram servers.
        
        Returns:
            Optional[str]: The file path on Telegram servers, or None on failure.
        """
        try:
            url = f"https://api.telegram.org/bot{self.token}/getFile"
            params = {"file_id": file_id}
            
            async with aiohttp.ClientSession() as session:
                async with session.get(url, params=params) as response:
                    if response.status != 200:
                        self.logger.error(f"HTTP error {response.status} when getting file path: {await response.text()}")
                        return None
                        
                    result = await response.json()
                    
                    if not result.get("ok", False):
                        error = result.get("description", "Unknown error")
                        self.logger.error(f"Error getting file path: {error}")
                        return None
                        
                    file_info = result.get("result", {})
                    return file_info.get("file_path")
                    
        except aiohttp.ClientError as e:
            self.logger.error(f"Network error getting file path: {e}", exc_info=True)
            return None
        except Exception as e:
            self.logger.error(f"Error getting file path: {e}", exc_info=True)
            return None
    
    def _determine_file_path(
        self, 
        file_id: str, 
        file_path: str, 
        media_type: str, 
        custom_path: Optional[str] = None
    ) -> str:
        """Determine the local file path for saving the downloaded file.
        
        Returns:
            str: The local file path.
        """
        if custom_path:
            if os.path.isdir(custom_path):
                # If custom_path is a directory, generate a filename
                filename = os.path.basename(file_path) if file_path else f"{media_type}_{file_id.split('_')[0]}"
                return os.path.join(custom_path, filename)
            return custom_path
            
        # Generate default filename
        if file_path:
            # Use the original filename from Telegram
            filename = os.path.basename(file_path)
        else:
            # Generate a filename based on media type
            ext = ".dat"
            if media_type == "photo":
                ext = ".jpg"
            elif media_type == "video":
                ext = ".mp4"
            elif media_type == "audio":
                ext = ".mp3"
            elif media_type == "voice":
                ext = ".ogg"
            elif media_type == "sticker":
                ext = ".webp"
            elif media_type == "animation":
                ext = ".mp4"
                
            filename = f"{media_type}_{file_id.split('_')[0]}{ext}"
            
        return filename
    
    async def _download_file(
        self,
        file_path: str,
        local_path: str,
        in_memory: Optional[bool] = None,
        file_size: int = 0,
        progress: Optional[callable] = None,
        progress_args: Optional[tuple] = ()
    ) -> Optional[Union[str, bytes]]:
        """Download a file from Telegram servers.
        
        Returns:
            Optional[Union[str, bytes]]: The file path or content.
        """
        url = f"https://api.telegram.org/file/bot{self.token}/{file_path}"
        self.logger.info(f"Downloading from URL: {url}")
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as response:
                    if response.status != 200:
                        self.logger.error(f"HTTP error {response.status} when downloading file: {await response.text()}")
                        return None
                        
                    # Get total file size if not provided
                    if not file_size:
                        file_size = int(response.headers.get("Content-Length", 0))
                        
                    if in_memory:
                        # Download to memory
                        if progress and callable(progress):
                            # Read with progress updates
                            data = b""
                            downloaded = 0
                            async for chunk in response.content.iter_chunked(8192):
                                data += chunk
                                downloaded += len(chunk)
                                progress(downloaded, file_size, local_path, progress_args)
                            return data
                        else:
                            # Read all at once
                            return await response.read()
                    else:
                        # Download to file
                        dir_path = os.path.dirname(os.path.abspath(local_path))
                        os.makedirs(dir_path, exist_ok=True)
                        
                        if progress and callable(progress):
                            # Write with progress updates
                            with open(local_path, "wb") as f:
                                downloaded = 0
                                async for chunk in response.content.iter_chunked(8192):
                                    f.write(chunk)
                                    downloaded += len(chunk)
                                    progress(downloaded, file_size, local_path, progress_args)
                        else:
                            # Write all at once
                            with open(local_path, "wb") as f:
                                f.write(await response.read())
                                
                        return local_path
                        
        except aiohttp.ClientError as e:
            self.logger.error(f"Network error downloading file: {e}", exc_info=True)
            return None
        except Exception as e:
            self.logger.error(f"Error downloading file: {e}", exc_info=True)
            return None 