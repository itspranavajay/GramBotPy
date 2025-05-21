import asyncio
import logging
import typing
import aiohttp
import json

from ...types import BotDescription

if typing.TYPE_CHECKING:
    from ...client import GramBotPy

class GetMyDescription:
    """Method for getting the bot's description."""
    
    async def get_my_description(
        self: "GramBotPy",
        language_code: str = None
    ) -> "BotDescription":
        """Get the bot's description.
        
        Parameters:
            language_code (``str``, optional):
                A two-letter ISO 639-1 language code or an empty string.
                
        Returns:
            :obj:`BotDescription`: The bot's description.
            
        Example:
            .. code-block:: python
            
                # Get description for all users
                desc = await bot.get_my_description()
                print(f"Bot description: {desc.description}")
                
                # Get description for Spanish language
                desc = await bot.get_my_description(language_code="es")
                print(f"Bot description (ES): {desc.description}")
        """
        self.logger.info(f"Getting bot description")
        
        # Create the params dictionary
        params = {}
        
        # Add optional parameters if they are provided
        if language_code is not None:
            params["language_code"] = language_code
        
        # Make the API request to get the bot description
        async with aiohttp.ClientSession() as session:
            try:
                url = f"https://api.telegram.org/bot{self.token}/getMyDescription"
                async with session.post(url, data=params) as response:
                    result = await response.json()
                    
                    if not result.get("ok", False):
                        error_description = result.get('description', 'Unknown error')
                        self.logger.error(f"Error getting bot description: {error_description}")
                        
                        # More detailed error logging
                        self.logger.debug(f"Params used: {params}")
                        return BotDescription(description="")
                    
                    # Parse the response and create a BotDescription object
                    description_data = result.get("result", {})
                    return BotDescription._parse(self, description_data)
                    
            except aiohttp.ClientError as e:
                self.logger.error(f"Network error making request to Telegram API: {e}", exc_info=True)
                return BotDescription(description="")
            except Exception as e:
                self.logger.error(f"Error making request to Telegram API: {e}", exc_info=True)
                return BotDescription(description="") 