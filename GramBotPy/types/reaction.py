from dataclasses import dataclass
import typing

class ReactionType:
    """Base class for reaction types in Telegram."""
    
    def __init__(self, type: str):
        self.type = type
    
    @classmethod
    def _parse(cls, client, reaction_data: dict):
        """Parse a ReactionType object from the Telegram API response."""
        if not reaction_data:
            return None
            
        reaction_type = reaction_data.get("type")
        
        if reaction_type == "emoji":
            return ReactionTypeEmoji._parse(client, reaction_data)
        elif reaction_type == "custom_emoji":
            return ReactionTypeCustomEmoji._parse(client, reaction_data)
        
        return cls(type=reaction_type)
    
    def to_dict(self):
        """Convert the ReactionType object to a dictionary."""
        return {
            "type": self.type
        }


class ReactionTypeEmoji(ReactionType):
    """Represents a reaction with a basic emoji."""
    
    def __init__(self, emoji: str):
        super().__init__(type="emoji")
        self.emoji = emoji
    
    @classmethod
    def _parse(cls, client, reaction_data: dict):
        """Parse a ReactionTypeEmoji object from the Telegram API response."""
        return cls(
            emoji=reaction_data.get("emoji")
        )
    
    def to_dict(self):
        """Convert the ReactionTypeEmoji object to a dictionary."""
        return {
            "type": self.type,
            "emoji": self.emoji
        }


class ReactionTypeCustomEmoji(ReactionType):
    """Represents a reaction with a custom emoji."""
    
    def __init__(self, custom_emoji_id: str):
        super().__init__(type="custom_emoji")
        self.custom_emoji_id = custom_emoji_id
    
    @classmethod
    def _parse(cls, client, reaction_data: dict):
        """Parse a ReactionTypeCustomEmoji object from the Telegram API response."""
        return cls(
            custom_emoji_id=reaction_data.get("custom_emoji_id")
        )
    
    def to_dict(self):
        """Convert the ReactionTypeCustomEmoji object to a dictionary."""
        return {
            "type": self.type,
            "custom_emoji_id": self.custom_emoji_id
        }


@dataclass
class MessageReaction:
    """This object represents a reaction to a message along with the number of times it was added.
    
    Attributes:
        type (:obj:`ReactionType`):
            Type of the reaction
            
        total_count (``int``):
            Number of times the reaction was added
            
        is_me (``bool``):
            True, if the reaction was added by the current user; otherwise - false
            
        is_big (``bool``, optional):
            True, if the reaction was added with a large animation
    """
    
    type: ReactionType
    total_count: int
    is_me: bool
    is_big: bool = None
    
    @classmethod
    def _parse(cls, client, reaction_data: dict):
        """Parse a MessageReaction object from the Telegram API response."""
        if not reaction_data:
            return None
            
        return cls(
            type=ReactionType._parse(client, reaction_data.get("type", {})),
            total_count=reaction_data.get("total_count"),
            is_me=reaction_data.get("is_me"),
            is_big=reaction_data.get("is_big")
        )
    
    def to_dict(self):
        """Convert the MessageReaction object to a dictionary."""
        result = {
            "type": self.type.to_dict(),
            "total_count": self.total_count,
            "is_me": self.is_me
        }
        
        if self.is_big is not None:
            result["is_big"] = self.is_big
            
        return result


@dataclass
class ReactionCount:
    """This object represents a reaction added to a message along with its count.
    
    Attributes:
        type (:obj:`ReactionType`):
            Type of the reaction
            
        total_count (``int``):
            Number of times the reaction was added
    """
    
    type: ReactionType
    total_count: int
    
    @classmethod
    def _parse(cls, client, count_data: dict):
        """Parse a ReactionCount object from the Telegram API response."""
        if not count_data:
            return None
            
        return cls(
            type=ReactionType._parse(client, count_data.get("type", {})),
            total_count=count_data.get("total_count")
        )
    
    def to_dict(self):
        """Convert the ReactionCount object to a dictionary."""
        return {
            "type": self.type.to_dict(),
            "total_count": self.total_count
        } 