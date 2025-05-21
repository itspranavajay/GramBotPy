from dataclasses import dataclass, field
import typing


class BotCommandScope:
    """This object represents the scope to which bot commands are applied.
    
    Currently, the following 7 scopes are supported:
    - BotCommandScopeDefault
    - BotCommandScopeAllPrivateChats
    - BotCommandScopeAllGroupChats
    - BotCommandScopeAllChatAdministrators
    - BotCommandScopeChat
    - BotCommandScopeChatAdministrators
    - BotCommandScopeChatMember
    """
    
    def __init__(self, type):
        self.type = type
    
    @classmethod
    def _parse(cls, client, scope_data: dict):
        """Parse a BotCommandScope object from the Telegram API response."""
        if not scope_data:
            return None
            
        scope_type = scope_data.get("type")
        
        if scope_type == "default":
            return BotCommandScopeDefault._parse(client, scope_data)
        elif scope_type == "all_private_chats":
            return BotCommandScopeAllPrivateChats._parse(client, scope_data)
        elif scope_type == "all_group_chats":
            return BotCommandScopeAllGroupChats._parse(client, scope_data)
        elif scope_type == "all_chat_administrators":
            return BotCommandScopeAllChatAdministrators._parse(client, scope_data)
        elif scope_type == "chat":
            return BotCommandScopeChat._parse(client, scope_data)
        elif scope_type == "chat_administrators":
            return BotCommandScopeChatAdministrators._parse(client, scope_data)
        elif scope_type == "chat_member":
            return BotCommandScopeChatMember._parse(client, scope_data)
        
        return cls(type=scope_type)
    
    def to_dict(self):
        """Convert the BotCommandScope object to a dictionary."""
        return {
            "type": self.type
        }


class BotCommandScopeDefault(BotCommandScope):
    """Represents the default scope of bot commands.
    
    Default commands are used if no commands with a narrower scope are specified for the user.
    """
    
    def __init__(self):
        super().__init__(type="default")
    
    @classmethod
    def _parse(cls, client, scope_data: dict):
        """Parse a BotCommandScopeDefault object from the Telegram API response."""
        return cls()


class BotCommandScopeAllPrivateChats(BotCommandScope):
    """Represents the scope of bot commands, covering all private chats."""
    
    def __init__(self):
        super().__init__(type="all_private_chats")
    
    @classmethod
    def _parse(cls, client, scope_data: dict):
        """Parse a BotCommandScopeAllPrivateChats object from the Telegram API response."""
        return cls()


class BotCommandScopeAllGroupChats(BotCommandScope):
    """Represents the scope of bot commands, covering all group and supergroup chats."""
    
    def __init__(self):
        super().__init__(type="all_group_chats")
    
    @classmethod
    def _parse(cls, client, scope_data: dict):
        """Parse a BotCommandScopeAllGroupChats object from the Telegram API response."""
        return cls()


class BotCommandScopeAllChatAdministrators(BotCommandScope):
    """Represents the scope of bot commands, covering all group and supergroup chat administrators."""
    
    def __init__(self):
        super().__init__(type="all_chat_administrators")
    
    @classmethod
    def _parse(cls, client, scope_data: dict):
        """Parse a BotCommandScopeAllChatAdministrators object from the Telegram API response."""
        return cls()


class BotCommandScopeChat(BotCommandScope):
    """Represents the scope of bot commands, covering a specific chat.
    
    Attributes:
        chat_id (``int`` | ``str``):
            Unique identifier for the target chat or username of the target supergroup
            (in the format @supergroupusername)
    """
    
    def __init__(self, chat_id: typing.Union[int, str]):
        super().__init__(type="chat")
        self.chat_id = chat_id
    
    @classmethod
    def _parse(cls, client, scope_data: dict):
        """Parse a BotCommandScopeChat object from the Telegram API response."""
        return cls(
            chat_id=scope_data.get("chat_id")
        )
    
    def to_dict(self):
        """Convert the BotCommandScopeChat object to a dictionary."""
        return {
            "type": self.type,
            "chat_id": self.chat_id
        }


class BotCommandScopeChatAdministrators(BotCommandScope):
    """Represents the scope of bot commands, covering all administrators of a specific chat.
    
    Attributes:
        chat_id (``int`` | ``str``):
            Unique identifier for the target chat or username of the target supergroup
            (in the format @supergroupusername)
    """
    
    def __init__(self, chat_id: typing.Union[int, str]):
        super().__init__(type="chat_administrators")
        self.chat_id = chat_id
    
    @classmethod
    def _parse(cls, client, scope_data: dict):
        """Parse a BotCommandScopeChatAdministrators object from the Telegram API response."""
        return cls(
            chat_id=scope_data.get("chat_id")
        )
    
    def to_dict(self):
        """Convert the BotCommandScopeChatAdministrators object to a dictionary."""
        return {
            "type": self.type,
            "chat_id": self.chat_id
        }


class BotCommandScopeChatMember(BotCommandScope):
    """Represents the scope of bot commands, covering a specific member of a group or supergroup chat.
    
    Attributes:
        chat_id (``int`` | ``str``):
            Unique identifier for the target chat or username of the target supergroup
            (in the format @supergroupusername)
            
        user_id (``int``):
            Unique identifier of the target user
    """
    
    def __init__(self, chat_id: typing.Union[int, str], user_id: int):
        super().__init__(type="chat_member")
        self.chat_id = chat_id
        self.user_id = user_id
    
    @classmethod
    def _parse(cls, client, scope_data: dict):
        """Parse a BotCommandScopeChatMember object from the Telegram API response."""
        return cls(
            chat_id=scope_data.get("chat_id"),
            user_id=scope_data.get("user_id")
        )
    
    def to_dict(self):
        """Convert the BotCommandScopeChatMember object to a dictionary."""
        return {
            "type": self.type,
            "chat_id": self.chat_id,
            "user_id": self.user_id
        } 