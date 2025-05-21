import asyncio
import logging
import typing
import aiohttp
import json

from ...types import BotShortDescription

if typing.TYPE_CHECKING:
    from ...client import GramBotPy

class GetMyShortDescription:
    """Method for getting the bot's short description."""
    
    async def get_my_short_description(
        self: "GramBotPy",
        language_code: str = None
    ) -> "BotShortDescription":
        """Get the bot's short description.
        
        Parameters:
            language_code (``str``, optional):
                A two-letter ISO 639-1 language code or an empty string.
                
        Returns:
            :obj:`BotShortDescription`: The bot's short description.
            
        Example:
            .. code-block:: python
            
                # Get short description for all users
                desc = await bot.get_my_short_description()
                print(f"Bot short description: {desc.short_description}")
                
                # Get short description for Spanish language
                desc = await bot.get_my_short_description(language_code="es")
                print(f"Bot short description (ES): {desc.short_description}")
        """
        self.logger.info(f"Getting bot short description")
        
        # Create the params dictionary
        params = {}
        
        # Add optional parameters if they are provided
        if language_code is not None:
            params["language_code"] = language_code
        
        # Make the API request to get the bot short description
        async with aiohttp.ClientSession() as session:
            try:
                url = f"https://api.telegram.org/bot{self.token}/getMyShortDescription"
                async with session.post(url, data=params) as response:
                    result = await response.json()
                    
                    if not result.get("ok", False):
                        error_description = result.get('description', 'Unknown error')
                        self.logger.error(f"Error getting bot short description: {error_description}")
                        
                        # More detailed error logging
                        self.logger.debug(f"Params used: {params}")
                        return BotShortDescription(short_description="")
                    
                    # Parse the response and create a BotShortDescription object
                    description_data = result.get("result", {})
                    return BotShortDescription._parse(self, description_data)
                    
            except aiohttp.ClientError as e:
                self.logger.error(f"Network error making request to Telegram API: {e}", exc_info=True)
                return BotShortDescription(short_description="")
            except Exception as e:
                self.logger.error(f"Error making request to Telegram API: {e}", exc_info=True)
                return BotShortDescription(short_description="") 