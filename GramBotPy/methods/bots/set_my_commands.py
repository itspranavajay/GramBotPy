import asyncio
import logging
import typing
import aiohttp
import json

from ...types import BotCommand, BotCommandScope

if typing.TYPE_CHECKING:
    from ...client import GramBotPy

class SetMyCommands:
    """Method for setting the list of the bot's commands."""
    
    async def set_my_commands(
        self: "GramBotPy",
        commands: typing.List[typing.Union[BotCommand, typing.Dict[str, str]]],
        scope: BotCommandScope = None,
        language_code: str = None
    ) -> bool:
        """Change the list of the bot's commands.
        
        Parameters:
            commands (``list``):
                A list of bot commands to be set as the list of the bot's commands.
                At most 100 commands can be specified.
                
            scope (:obj:`BotCommandScope`, optional):
                A JSON-serialized object, describing scope of users for which the commands are relevant.
                Defaults to BotCommandScopeDefault.
                
            language_code (``str``, optional):
                A two-letter ISO 639-1 language code. If empty, commands will be applied to all users
                from the given scope, for whose language there are no dedicated commands.
                
        Returns:
            ``bool``: True on success.
            
        Example:
            .. code-block:: python
            
                # Set commands for all users
                commands = [
                    BotCommand("start", "Start the bot"),
                    BotCommand("help", "Show help message")
                ]
                await bot.set_my_commands(commands)
                
                # Set commands for a specific language
                commands = [
                    BotCommand("start", "Iniciar el bot"),
                    BotCommand("help", "Mostrar mensaje de ayuda")
                ]
                await bot.set_my_commands(commands, language_code="es")
                
                # Set commands for a specific chat
                from GramBotPy.types import BotCommandScopeChat
                
                commands = [
                    BotCommand("start", "Start the bot"),
                    BotCommand("settings", "Change settings")
                ]
                chat_scope = BotCommandScopeChat(chat_id=123456789)
                await bot.set_my_commands(commands, scope=chat_scope)
        """
        self.logger.info(f"Setting bot commands")
        
        # Create the params dictionary with required parameters
        params = {}
        
        # Format the commands parameter
        formatted_commands = []
        for command in commands:
            if isinstance(command, BotCommand):
                formatted_commands.append(command.to_dict())
            elif isinstance(command, dict):
                formatted_commands.append(command)
            else:
                raise TypeError(f"Expected BotCommand or dict, got {type(command).__name__}")
        
        params["commands"] = json.dumps(formatted_commands)
        
        # Add optional parameters if they are provided
        if scope is not None:
            params["scope"] = json.dumps(scope.to_dict())
            
        if language_code is not None:
            params["language_code"] = language_code
        
        # Make the API request to set the bot commands
        async with aiohttp.ClientSession() as session:
            try:
                url = f"https://api.telegram.org/bot{self.token}/setMyCommands"
                async with session.post(url, data=params) as response:
                    result = await response.json()
                    
                    if not result.get("ok", False):
                        error_description = result.get('description', 'Unknown error')
                        self.logger.error(f"Error setting bot commands: {error_description}")
                        
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