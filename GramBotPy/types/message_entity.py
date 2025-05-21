from dataclasses import dataclass
from typing import Optional


@dataclass
class MessageEntity:
    """
    This object represents one special entity in a text message.
    For example, hashtags, usernames, URLs, etc.
    """
    type: str  # Type of the entity
    offset: int  # Offset in UTF-16 code units to the start of the entity
    length: int  # Length of the entity in UTF-16 code units
    url: Optional[str] = None  # Optional. For "text_link" only, url that will be opened
    user: Optional[dict] = None  # Optional. For "text_mention" only, the mentioned user
    language: Optional[str] = None  # Optional. For "pre" only, the programming language
    custom_emoji_id: Optional[str] = None  # Optional. For "custom_emoji" only
