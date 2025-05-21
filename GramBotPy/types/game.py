import json
import typing
from dataclasses import dataclass
from .photo_size import PhotoSize
from .message_entity import MessageEntity
from .animation import Animation

@dataclass
class Game:
    """This object represents a game.
    
    Use BotFather to create and edit games, their short names will act as unique identifiers.
    
    Attributes:
        title (``str``):
            Title of the game.
            
        description (``str``):
            Description of the game.
            
        photo (``list``):
            Photo that will be displayed in the game message in chats.
            
        text (``str``, optional):
            Brief description of the game or high scores included in the game message.
            Can be automatically edited to include current high scores for the game when
            the bot calls setGameScore, or manually edited using editMessageText.
            0-4096 characters.
            
        text_entities (``list``, optional):
            Special entities that appear in text, such as usernames, URLs, bot commands, etc.
            
        animation (``Animation``, optional):
            Animation that will be displayed in the game message in chats.
            Upload via BotFather.
    """
    
    title: str
    description: str
    photo: typing.List[PhotoSize]
    text: str = None
    text_entities: typing.List[MessageEntity] = None
    animation: Animation = None
    
    @classmethod
    def _parse(cls, client, game_data: dict):
        """Parse a game object from the Telegram API response."""
        if not game_data:
            return None
            
        photo = [PhotoSize._parse(client, photo_size) for photo_size in game_data.get("photo", [])]
        text_entities = [MessageEntity._parse(client, entity) for entity in game_data.get("text_entities", [])]
        animation = Animation._parse(client, game_data.get("animation"))
        
        return cls(
            title=game_data.get("title"),
            description=game_data.get("description"),
            photo=photo,
            text=game_data.get("text"),
            text_entities=text_entities,
            animation=animation
        )
        
    def to_dict(self):
        """Convert the Game object to a dictionary."""
        result = {
            "title": self.title,
            "description": self.description,
            "photo": [photo.to_dict() for photo in self.photo]
        }
        
        if self.text is not None:
            result["text"] = self.text
            
        if self.text_entities is not None:
            result["text_entities"] = [entity.to_dict() for entity in self.text_entities]
            
        if self.animation is not None:
            result["animation"] = self.animation.to_dict()
            
        return result 