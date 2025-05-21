from typing import Union, Optional, Dict, List, Any

from .get_chat import GetChat
from .get_chat_member import GetChatMember
from .get_chat_members import GetChatMembers
from .get_chat_information import GetChatInformation

async def get_chat(
    self,
    chat_id: Union[int, str]
) -> Dict[str, Any]:
    """Get up-to-date information about the chat.
    
    Parameters:
        chat_id (``int`` | ``str``):
            Unique identifier for the target chat or username.
            
    Returns:
        ``Dict[str, Any]``: Chat information.
    """
    get_chat_obj = GetChat(
        chat_id=chat_id
    )
    
    return await get_chat_obj._call(self)

async def get_chat_member(
    self,
    chat_id: Union[int, str],
    user_id: int
) -> Dict[str, Any]:
    """Get information about a member of a chat.
    
    Parameters:
        chat_id (``int`` | ``str``):
            Unique identifier for the target chat or username.
            
        user_id (``int``):
            Unique identifier of the target user.
            
    Returns:
        ``Dict[str, Any]``: Information about the chat member.
    """
    get_chat_member_obj = GetChatMember(
        chat_id=chat_id,
        user_id=user_id
    )
    
    return await get_chat_member_obj._call(self)

async def get_chat_members(
    self,
    chat_id: Union[int, str],
    offset: int = 0,
    limit: int = 100,
    filter: str = None
) -> List[Dict[str, Any]]:
    """Get a list of members in a chat.
    
    Parameters:
        chat_id (``int`` | ``str``):
            Unique identifier for the target chat or username.
            
        offset (``int``, optional):
            Number of members to skip.
            
        limit (``int``, optional):
            Limit number of members to return.
            
        filter (``str``, optional):
            Filter to apply to the list.
            
    Returns:
        ``List[Dict[str, Any]]``: List of chat members.
    """
    get_chat_members_obj = GetChatMembers(
        chat_id=chat_id,
        offset=offset,
        limit=limit,
        filter=filter
    )
    
    return await get_chat_members_obj._call(self)

async def get_chat_member_count(
    self,
    chat_id: Union[int, str]
) -> int:
    """Get the number of members in a chat.
    
    Parameters:
        chat_id (``int`` | ``str``):
            Unique identifier for the target chat or username.
            
    Returns:
        ``int``: Number of members in the chat.
    """
    params = {"chat_id": chat_id}
    
    result = await self.send_request(
        "getChatMemberCount",
        params
    )
    
    return result or 0

async def get_chat_administrators(
    self,
    chat_id: Union[int, str]
) -> List[Dict[str, Any]]:
    """Get a list of administrators in a chat.
    
    Parameters:
        chat_id (``int`` | ``str``):
            Unique identifier for the target chat or username.
            
    Returns:
        ``List[Dict[str, Any]]``: List of administrators.
    """
    params = {"chat_id": chat_id}
    
    result = await self.send_request(
        "getChatAdministrators",
        params
    )
    
    return result or []

async def get_me(self) -> Dict[str, Any]:
    """Get basic information about the bot.
    
    Returns:
        ``Dict[str, Any]``: Bot information.
    """
    result = await self.send_request(
        "getMe",
        {}
    )
    
    return result or {}

async def set_chat_title(
    self,
    chat_id: Union[int, str],
    title: str
) -> bool:
    """Change the title of a chat.
    
    Parameters:
        chat_id (``int`` | ``str``):
            Unique identifier for the target chat or username.
            
        title (``str``):
            New chat title, 1-255 characters.
            
    Returns:
        ``bool``: True on success.
    """
    params = {
        "chat_id": chat_id,
        "title": title
    }
    
    result = await self.send_request(
        "setChatTitle",
        params
    )
    
    return result or False

async def set_chat_description(
    self,
    chat_id: Union[int, str],
    description: Optional[str] = None
) -> bool:
    """Change the description of a chat.
    
    Parameters:
        chat_id (``int`` | ``str``):
            Unique identifier for the target chat or username.
            
        description (``str``, optional):
            New chat description, 0-255 characters. Pass None to remove the description.
            
    Returns:
        ``bool``: True on success.
    """
    params = {
        "chat_id": chat_id
    }
    
    if description is not None:
        params["description"] = description
    
    result = await self.send_request(
        "setChatDescription",
        params
    )
    
    return result or False

async def set_chat_photo(
    self,
    chat_id: Union[int, str],
    photo: Union[str, bytes]
) -> bool:
    """Set a new profile photo for the chat.
    
    Parameters:
        chat_id (``int`` | ``str``):
            Unique identifier for the target chat or username.
            
        photo (``str`` | ``bytes``):
            New chat photo. Pass a file_id as string to send a photo that exists on the 
            Telegram servers, pass an HTTP URL as a string for Telegram to get a photo 
            from the Internet, or pass bytes for uploading a new photo.
            
    Returns:
        ``bool``: True on success.
    """
    # This requires special handling for file upload
    # For now, return a placeholder implementation
    return False 