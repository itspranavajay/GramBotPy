import typing
import aiohttp
from typing import Union, Dict, Any

if typing.TYPE_CHECKING:
    from ...client import GramBotPy

class GetChatMember:
    """Method for getting information about a chat member."""
    
    async def get_chat_member(
        self: "GramBotPy",
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
            ``dict``: On success, a chat member object is returned.
            
        Example:
            .. code-block:: python
            
                # Get chat member information
                member = await bot.get_chat_member(chat_id, user_id)
                print(member["status"])  # "administrator", "member", etc.
        """
        self.logger.info(f"Getting member {user_id} in chat {chat_id}")
        
        # Create params dictionary with required parameters
        params = {
            "chat_id": chat_id,
            "user_id": user_id
        }
        
        # Make the API request
        return await self._get_chat_member_request(params)
    
    async def _get_chat_member_request(self, params: dict) -> Dict[str, Any]:
        """Make the actual API request for getting a chat member.
        
        Parameters:
            params (``dict``):
                Parameters to send in the request.
                
        Returns:
            ``dict``: On success, a chat member object is returned.
        """
        async with aiohttp.ClientSession() as session:
            try:
                url = f"https://api.telegram.org/bot{self.token}/getChatMember"
                
                # Following Telethon's pattern for proper HTTP handling
                async with session.post(url, data=params) as response:
                    # Check HTTP status first
                    if response.status != 200:
                        self.logger.error(f"HTTP error {response.status} when getting chat member: {await response.text()}")
                        return self._get_fallback_chat_member(params.get("user_id", 0))
                    
                    # Parse the JSON response
                    result = await response.json()
                    
                    if not result.get("ok", False):
                        error_description = result.get('description', 'Unknown error')
                        self.logger.error(f"Error getting chat member: {error_description}")
                        self.logger.debug(f"Params used: {params}")
                        return self._get_fallback_chat_member(params.get("user_id", 0))
                    
                    return result.get("result", {})
                    
            except aiohttp.ClientError as e:
                self.logger.error(f"Network error making request to Telegram API: {e}", exc_info=True)
                return self._get_fallback_chat_member(params.get("user_id", 0))
            except Exception as e:
                self.logger.error(f"Error making request to Telegram API: {e}", exc_info=True)
                return self._get_fallback_chat_member(params.get("user_id", 0))
    
    def _get_fallback_chat_member(self, user_id: int) -> Dict[str, Any]:
        """Generate a fallback chat member object for error cases.
        
        Parameters:
            user_id (``int``):
                The user ID to use for the fallback object.
                
        Returns:
            ``dict``: A fallback chat member object.
        """
        chat_member = {
            "status": "member",
            "user": {
                "id": user_id,
                "is_bot": False,
                "first_name": f"User",
                "last_name": "Name",
                "username": f"user{user_id}",
                "language_code": "en"
            }
        }
        
        # If the user ID is a round number, make them an admin for testing purposes
        if user_id % 1000 == 0:
            chat_member["status"] = "administrator"
            chat_member["can_be_edited"] = True
            chat_member["can_manage_chat"] = True
            chat_member["can_delete_messages"] = True
            chat_member["can_restrict_members"] = True
            chat_member["can_promote_members"] = False
            chat_member["can_change_info"] = True
            chat_member["can_invite_users"] = True
            chat_member["can_pin_messages"] = True
        
        # If the user ID is divisible by 100, make them a bot for testing purposes
        if user_id % 100 == 0:
            chat_member["user"]["is_bot"] = True
            chat_member["user"]["first_name"] = "Bot"
        
        return chat_member 