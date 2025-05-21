import asyncio
import logging
import typing
import aiohttp
import json

from ...types import BotCommandScope

if typing.TYPE_CHECKING:
    from ...client import GramBotPy

class DeleteMyCommands:
    """Method for deleting the list of the bot's commands."""
    
    async def delete_my_commands(
        self: "GramBotPy",
        scope: BotCommandScope = None,
        language_code: str = None
    ) -> bool:
        """Delete the list of the bot's commands for the given scope and user language.
        
        After deletion, older users will still be able to use the deleted commands, 
        but new users won't see them in the interface.
        
        Parameters:
            scope (:obj:`BotCommandScope`, optional):
                A JSON-serialized object, describing scope of users for which the commands are relevant.
                Defaults to BotCommandScopeDefault.
                
            language_code (``str``, optional):
                A two-letter ISO 639-1 language code. If empty, commands will be deleted for all users
                from the given scope, for whose language there are no dedicated commands.
                
        Returns:
            ``bool``: True on success.
            
        Example:
            .. code-block:: python
            
                # Delete commands for all users
                await bot.delete_my_commands()
                
                # Delete commands for Spanish language
                await bot.delete_my_commands(language_code="es")
                
                # Delete commands for a specific chat
                from GramBotPy.types import BotCommandScopeChat
                
                chat_scope = BotCommandScopeChat(chat_id=123456789)
                await bot.delete_my_commands(scope=chat_scope)
        """
        self.logger.info(f"Deleting bot commands")
        
        # Create the params dictionary
        params = {}
        
        # Add optional parameters if they are provided
        if scope is not None:
            params["scope"] = json.dumps(scope.to_dict())
            
        if language_code is not None:
            params["language_code"] = language_code
        
        # Make the API request to delete the bot commands
        async with aiohttp.ClientSession() as session:
            try:
                url = f"https://api.telegram.org/bot{self.token}/deleteMyCommands"
                async with session.post(url, data=params) as response:
                    result = await response.json()
                    
                    if not result.get("ok", False):
                        error_description = result.get('description', 'Unknown error')
                        self.logger.error(f"Error deleting bot commands: {error_description}")
                        
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