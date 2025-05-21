import logging
import typing
import aiohttp
import json

from ...types import User

if typing.TYPE_CHECKING:
    from ...client import GramBotPy

class GetMe:
    """Get information about the bot."""
    
    async def get_me(self: "GramBotPy") -> User:
        """Get information about the bot.
        
        This method returns basic information about the bot in form of a User object.
        
        Returns:
            :obj:`User`: A User object representing the bot.
            
        Example:
            .. code-block:: python
            
                bot = GramBotPy("BOT_TOKEN")
                async with bot:
                    me = await bot.get_me()
                    print(f"Bot name: {me.first_name}")
                    print(f"Bot username: @{me.username}")
        """
        # Return cached value if available
        if hasattr(self, '_me') and self._me is not None:
            return self._me
            
        self.logger.info("Getting information about the bot")
        
        # Make the API request to get bot information
        async with aiohttp.ClientSession() as session:
            try:
                url = f"https://api.telegram.org/bot{self.token}/getMe"
                
                # Following Telethon's pattern for proper HTTP handling
                async with session.get(url) as response:
                    # Check HTTP status first
                    if response.status != 200:
                        self.logger.error(f"HTTP error {response.status} when getting bot info: {await response.text()}")
                        self._me = self._get_fallback_user()
                        return self._me
                    
                    # Parse the JSON response
                    result = await response.json()
                    
                    if not result.get("ok", False):
                        error_description = result.get('description', 'Unknown error')
                        self.logger.error(f"Error getting bot information: {error_description}")
                        self._me = self._get_fallback_user()
                        return self._me
                        
                    # Parse the response to create a User object
                    user_data = result.get("result", {})
                    self._me = self._parse_user(user_data)
                        
            except aiohttp.ClientError as e:
                self.logger.error(f"Network error making request to Telegram API: {e}", exc_info=True)
                self._me = self._get_fallback_user()
            except Exception as e:
                self.logger.error(f"Error making request to Telegram API: {e}", exc_info=True)
                self._me = self._get_fallback_user()
                
        return self._me
    
    def _parse_user(self, user_data: dict) -> User:
        """Parse Telegram API response into a User object.
        
        Parameters:
            user_data (``dict``):
                User data from Telegram API.
                
        Returns:
            :obj:`User`: A User object.
        """
        return User(
            id=user_data.get("id"),
            is_bot=user_data.get("is_bot", True),
            first_name=user_data.get("first_name", "Bot"),
            last_name=user_data.get("last_name"),
            username=user_data.get("username"),
            language_code=user_data.get("language_code"),
            can_join_groups=user_data.get("can_join_groups", True),
            can_read_all_group_messages=user_data.get("can_read_all_group_messages", False),
            supports_inline_queries=user_data.get("supports_inline_queries", False)
        )
    
    def _get_fallback_user(self) -> User:
        """Create a fallback User object when API requests fail.
        
        Returns:
            :obj:`User`: A fallback User object.
        """
        try:
            # Try to get bot_id from token
            bot_id = int(self.token.split(":")[0])
        except (ValueError, IndexError):
            # Fallback if token parsing fails
            bot_id = 0
            
        return User(
            id=bot_id,
            is_bot=True,
            first_name="Bot",
            username="bot",
            can_join_groups=True,
            can_read_all_group_messages=False,
            supports_inline_queries=False
        ) 