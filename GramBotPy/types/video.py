from dataclasses import dataclass
from typing import Optional, Dict, Any

@dataclass
class Video:
    """This object represents a video file.
    
    Parameters:
        file_id (``str``):
            Identifier for this file, which can be used to download or reuse the file.
            
        file_unique_id (``str``):
            Unique identifier for this file, which is supposed to be the same over time and for different bots.
            Can't be used to download or reuse the file.
            
        width (``int``):
            Video width as defined by sender.
            
        height (``int``):
            Video height as defined by sender.
            
        duration (``int``):
            Duration of the video in seconds as defined by sender.
            
        thumb (``dict``, optional):
            Video thumbnail.
            
        file_name (``str``, optional):
            Original filename as defined by sender.
            
        mime_type (``str``, optional):
            MIME type of the file as defined by sender.
            
        file_size (``int``, optional):
            File size.
    """
    
    file_id: str
    file_unique_id: str
    width: int
    height: int
    duration: int
    thumb: Optional[Dict[str, Any]] = None
    file_name: Optional[str] = None
    mime_type: Optional[str] = None
    file_size: Optional[int] = None 