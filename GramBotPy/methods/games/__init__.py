from .send_game import SendGame
from .set_game_score import SetGameScore
from .get_game_high_scores import GetGameHighScores

class GamesMethodsMixin(
    SendGame,
    SetGameScore,
    GetGameHighScores
):
    """Game handling methods.
    
    This mixin includes all methods related to Telegram games,
    such as sending games, setting scores, and getting high scores.
    """
    pass 