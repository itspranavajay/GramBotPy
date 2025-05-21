import asyncio
import logging
import typing
import aiohttp
import json
from datetime import datetime

from ...types import ChatInviteLink

if typing.TYPE_CHECKING:
    from ...client import GramBotPy

class CreateChatInviteLink:
    """Method for creating chat invite links."""
    
    async def create_chat_invite_link(
        self: "GramBotPy",
        chat_id: typing.Union[int, str],
        name: str = None,
        expire_date: typing.Union[int, datetime] = None,
        member_limit: int = None,
        creates_join_request: bool = None
    ) -> ChatInviteLink:
        """Create an additional invite link for a chat.
        
        The bot must be an administrator in the chat for this to work and must have
        the appropriate administrator rights.
        
        Parameters:
            chat_id (``int`` | ``str``):
                Unique identifier for the target chat or username of the
                target channel/supergroup (in the format @channelusername).
                
            name (``str``, optional):
                Invite link name; 0-32 characters.
                
            expire_date (``int`` | ``datetime``, optional):
                Point in time when the link will expire. Pass a Unix timestamp or
                a datetime object. If not specified, the link will be eternal.
                
            member_limit (``int``, optional):
                The maximum number of users that can be members of the chat
                simultaneously after joining the chat via this invite link; 1-99999.
                
            creates_join_request (``bool``, optional):
                True, if users joining the chat via the link need to be approved
                by chat administrators. If True, member_limit can't be specified.
                
        Returns:
            :obj:`ChatInviteLink`: The new invite link as ChatInviteLink object.
            
        Example:
            .. code-block:: python
            
                # Create a basic invite link
                link = await bot.create_chat_invite_link(chat_id=-1001234567890)
                print(f"New link: {link.invite_link}")
                
                # Create a named invite link
                link = await bot.create_chat_invite_link(
                    chat_id=-1001234567890,
                    name="June Event"
                )
                
                # Create an invite link that expires in 24 hours
                from datetime import datetime, timedelta
                
                expire_date = datetime.now() + timedelta(days=1)
                link = await bot.create_chat_invite_link(
                    chat_id=-1001234567890,
                    expire_date=expire_date
                )
                
                # Create an invite link with member limit
                link = await bot.create_chat_invite_link(
                    chat_id=-1001234567890,
                    member_limit=10
                )
                
                # Create an invite link that requires admin approval
                link = await bot.create_chat_invite_link(
                    chat_id=-1001234567890,
                    creates_join_request=True
                )
        """
        self.logger.info(f"Creating chat invite link for {chat_id}")
        
        # Create the params dictionary with required parameters
        params = {
            "chat_id": chat_id
        }
        
        # Add optional parameters if they are provided
        if name is not None:
            params["name"] = name
            
        if expire_date is not None:
            # Convert datetime to Unix timestamp if needed
            if isinstance(expire_date, datetime):
                expire_date = int(expire_date.timestamp())
            params["expire_date"] = expire_date
            
        if member_limit is not None:
            params["member_limit"] = member_limit
            
        if creates_join_request is not None:
            params["creates_join_request"] = creates_join_request
        
        # Make the API request to create the chat invite link
        async with aiohttp.ClientSession() as session:
            try:
                url = f"https://api.telegram.org/bot{self.token}/createChatInviteLink"
                async with session.post(url, data=params) as response:
                    result = await response.json()
                    
                    if not result.get("ok", False):
                        error_description = result.get('description', 'Unknown error')
                        self.logger.error(f"Error creating chat invite link: {error_description}")
                        
                        # More detailed error logging
                        self.logger.debug(f"Params used: {params}")
                        return None
                    
                    # Parse the response and create a ChatInviteLink object
                    link_data = result.get("result", {})
                    return ChatInviteLink._parse(self, link_data)
                    
            except aiohttp.ClientError as e:
                self.logger.error(f"Network error making request to Telegram API: {e}", exc_info=True)
                return None
            except Exception as e:
                self.logger.error(f"Error making request to Telegram API: {e}", exc_info=True)
                return None 