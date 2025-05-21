import asyncio
import logging
import typing
import aiohttp
import json

if typing.TYPE_CHECKING:
    from ...client import GramBotPy

class SetMyDescription:
    """Method for setting the bot's description."""
    
    async def set_my_description(
        self: "GramBotPy",
        description: str = None,
        language_code: str = None
    ) -> bool:
        """Change the bot's description, which is shown in the chat with the bot if the chat is empty.
        
        Parameters:
            description (``str``, optional):
                New bot description; 0-512 characters. Pass an empty string to remove
                the dedicated description for the specified language.
                
            language_code (``str``, optional):
                A two-letter ISO 639-1 language code. If empty, the description will be applied
                to all users for whose language there is no dedicated description.
                
        Returns:
            ``bool``: True on success.
            
        Example:
            .. code-block:: python
            
                # Set description for all users
                await bot.set_my_description("This is a bot that helps you organize your tasks.")
                
                # Set description for Spanish language
                await bot.set_my_description(
                    "Este es un bot que te ayuda a organizar tus tareas.",
                    language_code="es"
                )
                
                # Remove description for a specific language
                await bot.set_my_description("", language_code="fr")
        """
        self.logger.info(f"Setting bot description")
        
        # Create the params dictionary
        params = {}
        
        # Add optional parameters if they are provided
        if description is not None:
            params["description"] = description
            
        if language_code is not None:
            params["language_code"] = language_code
        
        # Make the API request to set the bot description
        async with aiohttp.ClientSession() as session:
            try:
                url = f"https://api.telegram.org/bot{self.token}/setMyDescription"
                async with session.post(url, data=params) as response:
                    result = await response.json()
                    
                    if not result.get("ok", False):
                        error_description = result.get('description', 'Unknown error')
                        self.logger.error(f"Error setting bot description: {error_description}")
                        
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