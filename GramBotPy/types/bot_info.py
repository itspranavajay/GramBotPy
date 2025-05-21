from dataclasses import dataclass
import typing
from .bot_command import BotCommand

@dataclass
class BotInfo:
    """This object represents comprehensive information about a bot.
    
    Attributes:
        user_id (``int``):
            Unique identifier of the bot.
            
        description (``str``):
            Bot's description.
            
        commands (``list``):
            List of the bot's commands.
            
        bot_pic_url (``str``, optional):
            URL of the bot's profile photo.
            
        menu_button (``str``, optional):
            Type of the bot's menu button.
            
        commands_list_url (``str``, optional):
            URL of the list of all bot's commands.
    """
    
    user_id: int
    description: str
    commands: typing.List[BotCommand]
    bot_pic_url: str = None
    menu_button: str = None
    commands_list_url: str = None
    
    @classmethod
    def _parse(cls, client, info_data: dict):
        """Parse a BotInfo object from the Telegram API response."""
        if not info_data:
            return None
            
        commands = [BotCommand._parse(client, command) for command in info_data.get("commands", [])]
        
        return cls(
            user_id=info_data.get("user_id"),
            description=info_data.get("description"),
            commands=commands,
            bot_pic_url=info_data.get("bot_pic_url"),
            menu_button=info_data.get("menu_button"),
            commands_list_url=info_data.get("commands_list_url")
        )
        
    def to_dict(self):
        """Convert the BotInfo object to a dictionary."""
        result = {
            "user_id": self.user_id,
            "description": self.description,
            "commands": [command.to_dict() for command in self.commands]
        }
        
        if self.bot_pic_url:
            result["bot_pic_url"] = self.bot_pic_url
            
        if self.menu_button:
            result["menu_button"] = self.menu_button
            
        if self.commands_list_url:
            result["commands_list_url"] = self.commands_list_url
            
        return result 