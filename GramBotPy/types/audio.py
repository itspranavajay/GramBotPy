from dataclasses import dataclass
from typing import Optional, Dict, Any

@dataclass
class Audio:
    """This object represents an audio file.
    
    Parameters:
        file_id (``str``):
            Identifier for this file, which can be used to download or reuse the file.
            
        file_unique_id (``str``):
            Unique identifier for this file, which is supposed to be the same over time and for different bots.
            Can't be used to download or reuse the file.
            
        duration (``int``):
            Duration of the audio in seconds as defined by sender.
            
        performer (``str``, optional):
            Performer of the audio as defined by sender or by audio tags.
            
        title (``str``, optional):
            Title of the audio as defined by sender or by audio tags.
            
        file_name (``str``, optional):
            Original filename as defined by sender.
            
        mime_type (``str``, optional):
            MIME type of the file as defined by sender.
            
        file_size (``int``, optional):
            File size.
            
        thumb (``dict``, optional):
            Thumbnail of the album cover to which the music file belongs.
    """
    
    file_id: str
    file_unique_id: str
    duration: int
    performer: Optional[str] = None
    title: Optional[str] = None
    file_name: Optional[str] = None
    mime_type: Optional[str] = None
    file_size: Optional[int] = None
    thumb: Optional[Dict[str, Any]] = None 