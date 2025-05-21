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
from .create_chat_invite_link import CreateChatInviteLink
from .get_channel_messages import GetChannelMessages
from .helpers import (
    get_chat,
    get_chat_member,
    get_chat_members,
    get_chat_member_count,
    get_chat_administrators,
    get_me,
    set_chat_title,
    set_chat_description,
    set_chat_photo
)

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
    GetChatInformation,
    CreateChatInviteLink,
    GetChannelMessages
):
    """Chat management methods.
    
    This mixin includes all methods related to managing chats and their members,
    such as getting chat information, banning members, etc.
    """
    # Helper methods
    get_chat = get_chat
    get_chat_member = get_chat_member
    get_chat_members = get_chat_members
    get_chat_member_count = get_chat_member_count
    get_chat_administrators = get_chat_administrators
    get_me = get_me
    set_chat_title = set_chat_title
    set_chat_description = set_chat_description
    set_chat_photo = set_chat_photo 