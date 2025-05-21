import asyncio
import logging
import typing
import aiohttp
import json

from ...types import BotCommand, BotCommandScope

if typing.TYPE_CHECKING:
    from ...client import GramBotPy

class GetMyCommands:
    """Method for getting the list of the bot's commands."""
    
    async def get_my_commands(
        self: "GramBotPy",
        scope: BotCommandScope = None,
        language_code: str = None
    ) -> typing.List[BotCommand]:
        """Get the current list of the bot's commands for the given scope and user language.
        
        Parameters:
            scope (:obj:`BotCommandScope`, optional):
                A JSON-serialized object, describing scope of users. Defaults to BotCommandScopeDefault.
                
            language_code (``str``, optional):
                A two-letter ISO 639-1 language code or an empty string.
                
        Returns:
            List of :obj:`BotCommand`: List of bot commands.
            
        Example:
            .. code-block:: python
            
                # Get all commands
                commands = await bot.get_my_commands()
                for cmd in commands:
                    print(f"/{cmd.command} - {cmd.description}")
                
                # Get commands for Spanish language
                commands = await bot.get_my_commands(language_code="es")
                
                # Get commands for a specific chat
                from GramBotPy.types import BotCommandScopeChat
                
                chat_scope = BotCommandScopeChat(chat_id=123456789)
                commands = await bot.get_my_commands(scope=chat_scope)
        """
        self.logger.info(f"Getting bot commands")
        
        # Create the params dictionary
        params = {}
        
        # Add optional parameters if they are provided
        if scope is not None:
            params["scope"] = json.dumps(scope.to_dict())
            
        if language_code is not None:
            params["language_code"] = language_code
        
        # Make the API request to get the bot commands
        async with aiohttp.ClientSession() as session:
            try:
                url = f"https://api.telegram.org/bot{self.token}/getMyCommands"
                async with session.post(url, data=params) as response:
                    result = await response.json()
                    
                    if not result.get("ok", False):
                        error_description = result.get('description', 'Unknown error')
                        self.logger.error(f"Error getting bot commands: {error_description}")
                        
                        # More detailed error logging
                        self.logger.debug(f"Params used: {params}")
                        return []
                    
                    # Parse the response and create BotCommand objects
                    commands_data = result.get("result", [])
                    return [BotCommand._parse(self, command_data) for command_data in commands_data]
                    
            except aiohttp.ClientError as e:
                self.logger.error(f"Network error making request to Telegram API: {e}", exc_info=True)
                return []
            except Exception as e:
                self.logger.error(f"Error making request to Telegram API: {e}", exc_info=True)
                return [] 