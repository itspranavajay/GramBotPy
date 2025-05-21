from .get_me import GetMe
from .get_updates import GetUpdates
from .answer_callback_query import AnswerCallbackQuery

class BotsMethodsMixin(
    GetMe,
    GetUpdates,
    AnswerCallbackQuery
):
    """Bot-specific methods.
    
    This mixin includes all bot-specific methods, such as getting bot information,
    retrieving updates, and handling callback queries.
    """
    pass 