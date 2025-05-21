from dataclasses import dataclass
from typing import Optional, Dict, Any

@dataclass
class Document:
    """This object represents a general file.
    
    Parameters:
        file_id (``str``):
            Identifier for this file, which can be used to download or reuse the file.
            
        file_unique_id (``str``):
            Unique identifier for this file, which is supposed to be the same over time and for different bots.
            Can't be used to download or reuse the file.
            
        thumb (``dict``, optional):
            Document thumbnail as defined by sender.
            
        file_name (``str``, optional):
            Original filename as defined by sender.
            
        mime_type (``str``, optional):
            MIME type of the file as defined by sender.
            
        file_size (``int``, optional):
            File size.
    """
    
    file_id: str
    file_unique_id: str
    thumb: Optional[Dict[str, Any]] = None
    file_name: Optional[str] = None
    mime_type: Optional[str] = None
    file_size: Optional[int] = None 