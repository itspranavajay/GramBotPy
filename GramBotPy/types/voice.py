from dataclasses import dataclass
from typing import Optional

@dataclass
class Voice:
    """This object represents a voice note.
    
    Parameters:
        file_id (``str``):
            Identifier for this file, which can be used to download or reuse the file.
            
        file_unique_id (``str``):
            Unique identifier for this file, which is supposed to be the same over time and for different bots.
            Can't be used to download or reuse the file.
            
        duration (``int``):
            Duration of the audio in seconds as defined by sender.
            
        mime_type (``str``, optional):
            MIME type of the file as defined by sender.
            
        file_size (``int``, optional):
            File size.
    """
    
    file_id: str
    file_unique_id: str
    duration: int
    mime_type: Optional[str] = None
    file_size: Optional[int] = None 