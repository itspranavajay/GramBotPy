from dataclasses import dataclass
from typing import Optional


@dataclass
class MessageEntity:
    """
    This object represents one special entity in a text message.
    For example, hashtags, usernames, URLs, etc.
    
    Parameters:
        type (``str``):
            Type of the entity. Currently, can be:
            "mention" (@username),
            "hashtag" (#hashtag),
            "cashtag" ($USD),
            "bot_command" (/start@jobs_bot),
            "url" (https://telegram.org),
            "email" (do-not-reply@telegram.org),
            "phone_number" (+1-212-555-0123),
            "bold" (bold text),
            "italic" (italic text),
            "underline" (underlined text),
            "strikethrough" (strikethrough text),
            "spoiler" (spoiler message),
            "code" (monowidth string),
            "pre" (monowidth block),
            "text_link" (for clickable text URLs),
            "text_mention" (for users without usernames),
            "custom_emoji" (for inline custom emoji stickers)
            
        offset (``int``):
            Offset in UTF-16 code units to the start of the entity.
            
        length (``int``):
            Length of the entity in UTF-16 code units.
            
        url (``str``, optional):
            For "text_link" only, URL that will be opened after user taps on the text.
            
        user (``User``, optional):
            For "text_mention" only, the mentioned user.
            
        language (``str``, optional):
            For "pre" only, the programming language of the entity text.
            
        custom_emoji_id (``str``, optional):
            For "custom_emoji" only, unique identifier of the custom emoji.
    """
    
    type: str
    """Type of the entity. Can be "mention", "hashtag", "cashtag", "bot_command", "url", "email", "phone_number",
    "bold", "italic", "underline", "strikethrough", "spoiler", "code", "pre", "text_link", "text_mention", "custom_emoji"."""
    
    offset: int
    """Offset in UTF-16 code units to the start of the entity"""
    
    length: int
    """Length of the entity in UTF-16 code units"""
    
    url: Optional[str] = None
    """Optional. For "text_link" only, url that will be opened after user taps on the text"""
    
    user: Optional['User'] = None
    """Optional. For "text_mention" only, the mentioned user"""
    
    language: Optional[str] = None
    """Optional. For "pre" only, the programming language of the entity text"""
    
    custom_emoji_id: Optional[str] = None
    """Optional. For "custom_emoji" only, unique identifier of the custom emoji""" 