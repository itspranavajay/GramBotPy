from .send_message import SendMessage
from .edit_message_text import EditMessageText
from .delete_messages import DeleteMessages
from .forward_messages import ForwardMessages
from .send_photo import SendPhoto
from .send_video import SendVideo
from .send_document import SendDocument
from .send_audio import SendAudio
from .send_voice import SendVoice
from .send_sticker import SendSticker
from .send_location import SendLocation
from .send_contact import SendContact
from .send_animation import SendAnimation
from .send_poll import SendPoll
from .send_dice import SendDice
from .message_scheduler import MessageScheduler

class MessagesMethodsMixin(
    SendMessage,
    EditMessageText,
    DeleteMessages,
    ForwardMessages,
    SendPhoto,
    SendVideo,
    SendDocument,
    SendAudio,
    SendVoice,
    SendSticker,
    SendLocation,
    SendContact,
    SendAnimation,
    SendPoll,
    SendDice,
    MessageScheduler
):
    """Message handling methods.
    
    This mixin includes all methods related to sending, editing, and deleting 
    messages, as well as sending different types of media.
    """
    pass