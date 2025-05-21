import typing
from dataclasses import dataclass
from .user import User

@dataclass
class GameHighScore:
    """This object represents one row of the high scores table for a game.
    
    Attributes:
        position (``int``):
            Position in high score table for the game.
            
        user (``User``):
            User.
            
        score (``int``):
            Score.
    """
    
    position: int
    user: User
    score: int
    
    @classmethod
    def _parse(cls, client, high_score_data: dict):
        """Parse a game high score object from the Telegram API response."""
        if not high_score_data:
            return None
            
        user = User._parse(client, high_score_data.get("user"))
        
        return cls(
            position=high_score_data.get("position"),
            user=user,
            score=high_score_data.get("score")
        )
        
    def to_dict(self):
        """Convert the GameHighScore object to a dictionary."""
        return {
            "position": self.position,
            "user": self.user.to_dict(),
            "score": self.score
        } 