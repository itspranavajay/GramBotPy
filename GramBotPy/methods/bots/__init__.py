from .get_me import GetMe
from .get_updates import GetUpdates
from .answer_callback_query import AnswerCallbackQuery
from .set_my_commands import SetMyCommands
from .delete_my_commands import DeleteMyCommands
from .get_my_commands import GetMyCommands
from .set_my_description import SetMyDescription
from .get_my_description import GetMyDescription
from .set_my_short_description import SetMyShortDescription
from .get_my_short_description import GetMyShortDescription
from .answer_web_app_query import AnswerWebAppQuery
from .delete_webhook import DeleteWebhook
from .helpers import delete_webhook

class BotsMethodsMixin(
    GetMe,
    GetUpdates,
    AnswerCallbackQuery,
    SetMyCommands,
    DeleteMyCommands,
    GetMyCommands,
    SetMyDescription,
    GetMyDescription,
    SetMyShortDescription,
    GetMyShortDescription,
    AnswerWebAppQuery,
    DeleteWebhook
):
    """Bot-specific methods.
    
    This mixin includes all bot-specific methods, such as getting bot information,
    retrieving updates, handling callback queries, and managing bot commands and descriptions.
    """
    delete_webhook = delete_webhook
    pass 