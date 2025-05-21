from .get_chat import GetChat
from .leave_chat import LeaveChat
from .get_chat_members import GetChatMembers
from .get_chat_member import GetChatMember
from .ban_chat_member import BanChatMember
from .unban_chat_member import UnbanChatMember
from .restrict_chat_member import RestrictChatMember
from .promote_chat_member import PromoteChatMember
from .pin_chat_message import PinChatMessage
from .unpin_chat_message import UnpinChatMessage
from .mute_chat_member import MuteChatMember
from .unmute_chat_member import UnmuteChatMember
from .get_user_info import GetUserInfo
from .get_chat_information import GetChatInformation

class ChatsMethodsMixin(
    GetChat,
    LeaveChat,
    GetChatMembers,
    GetChatMember,
    BanChatMember,
    UnbanChatMember,
    RestrictChatMember,
    PromoteChatMember,
    PinChatMessage,
    UnpinChatMessage,
    MuteChatMember,
    UnmuteChatMember,
    GetUserInfo,
    GetChatInformation
):
    """Chat management methods.
    
    This mixin includes all methods related to managing chats and their members,
    such as getting chat information, banning members, etc.
    """
    pass 