from .bots import BotsMethodsMixin
from .chats import ChatsMethodsMixin
from .messages import MessagesMethodsMixin
from .media import MediaMethodsMixin
from .games import GamesMethodsMixin
from .business import BusinessMethodsMixin
from .gifts import GiftsMethodsMixin
from .database import DatabaseMethodsMixin
from .utility_error_handler import UtilityErrorHandler

class Methods(
    BotsMethodsMixin,
    ChatsMethodsMixin,
    MessagesMethodsMixin,
    MediaMethodsMixin,
    GamesMethodsMixin,
    BusinessMethodsMixin,
    GiftsMethodsMixin,
    DatabaseMethodsMixin,
    UtilityErrorHandler
):
    """Methods class combining all available methods for the GramBotPy client.
    
    This class serves as a mixin container for all methods available in the
    GramBotPy framework, organized into logical categories by functionality.
    """
    pass 