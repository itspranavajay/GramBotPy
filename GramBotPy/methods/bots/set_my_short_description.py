import asyncio
import logging
import typing
import aiohttp
import json

if typing.TYPE_CHECKING:
    from ...client import GramBotPy

class SetMyShortDescription:
    """Method for setting the bot's short description."""
    
    async def set_my_short_description(
        self: "GramBotPy",
        short_description: str = None,
        language_code: str = None
    ) -> bool:
        """Change the bot's short description, which is shown on the bot's profile page.
        
        Parameters:
            short_description (``str``, optional):
                New short description for the bot; 0-120 characters. Pass an empty string to remove
                the dedicated short description for the specified language.
                
            language_code (``str``, optional):
                A two-letter ISO 639-1 language code. If empty, the short description will be applied
                to all users for whose language there is no dedicated short description.
                
        Returns:
            ``bool``: True on success.
            
        Example:
            .. code-block:: python
            
                # Set short description for all users
                await bot.set_my_short_description("Task organization bot")
                
                # Set short description for Spanish language
                await bot.set_my_short_description(
                    "Bot de organización de tareas",
                    language_code="es"
                )
                
                # Remove short description for a specific language
                await bot.set_my_short_description("", language_code="fr")
        """
        self.logger.info(f"Setting bot short description")
        
        # Create the params dictionary
        params = {}
        
        # Add optional parameters if they are provided
        if short_description is not None:
            params["short_description"] = short_description
            
        if language_code is not None:
            params["language_code"] = language_code
        
        # Make the API request to set the bot short description
        async with aiohttp.ClientSession() as session:
            try:
                url = f"https://api.telegram.org/bot{self.token}/setMyShortDescription"
                async with session.post(url, data=params) as response:
                    result = await response.json()
                    
                    if not result.get("ok", False):
                        error_description = result.get('description', 'Unknown error')
                        self.logger.error(f"Error setting bot short description: {error_description}")
                        
                        # More detailed error logging
                        self.logger.debug(f"Params used: {params}")
                        return False
                    
                    return True
                    
            except aiohttp.ClientError as e:
                self.logger.error(f"Network error making request to Telegram API: {e}", exc_info=True)
                return False
            except Exception as e:
                self.logger.error(f"Error making request to Telegram API: {e}", exc_info=True)
                return False 