from dataclasses import dataclass, field
from typing import Optional, Dict, Any, ClassVar, Type, TypeVar

T = TypeVar('T', bound='Update')

@dataclass
class Update:
    """This object represents an incoming update.
    
    Parameters:
        update_id (``int``):
            The update's unique identifier.
            
        message (``dict``, optional):
            New incoming message.
            
        edited_message (``dict``, optional):
            New version of a message that is known to the bot and was edited.
            
        channel_post (``dict``, optional):
            New incoming channel post.
            
        edited_channel_post (``dict``, optional):
            New version of a channel post that is known to the bot and was edited.
            
        inline_query (``dict``, optional):
            New incoming inline query.
            
        chosen_inline_result (``dict``, optional):
            The result of an inline query that was chosen by a user.
            
        callback_query (``dict``, optional):
            New incoming callback query.
            
        shipping_query (``dict``, optional):
            New incoming shipping query.
            
        pre_checkout_query (``dict``, optional):
            New incoming pre-checkout query.
            
        poll (``dict``, optional):
            New poll state.
            
        poll_answer (``dict``, optional):
            A user changed their answer in a non-anonymous poll.
            
        my_chat_member (``dict``, optional):
            The bot's chat member status was updated in a chat.
            
        chat_member (``dict``, optional):
            A chat member's status was updated in a chat.
            
        chat_join_request (``dict``, optional):
            A request to join the chat has been sent.
    """
    
    update_id: int
    message: Optional[Dict[str, Any]] = None
    edited_message: Optional[Dict[str, Any]] = None
    channel_post: Optional[Dict[str, Any]] = None
    edited_channel_post: Optional[Dict[str, Any]] = None
    inline_query: Optional[Dict[str, Any]] = None
    chosen_inline_result: Optional[Dict[str, Any]] = None
    callback_query: Optional[Dict[str, Any]] = None
    shipping_query: Optional[Dict[str, Any]] = None
    pre_checkout_query: Optional[Dict[str, Any]] = None
    poll: Optional[Dict[str, Any]] = None
    poll_answer: Optional[Dict[str, Any]] = None
    my_chat_member: Optional[Dict[str, Any]] = None
    chat_member: Optional[Dict[str, Any]] = None
    chat_join_request: Optional[Dict[str, Any]] = None
    _client: Any = field(default=None, repr=False)
    
    def __post_init__(self):
        # Convert dictionaries to appropriate types if needed
        if self.message:
            if isinstance(self.message, dict):
                from .message import Message
                self.message = Message._parse(self._client, self.message)
            
        if self.callback_query:
            if isinstance(self.callback_query, dict):
                from .callback_query import CallbackQuery
                self.callback_query = CallbackQuery._parse(self._client, self.callback_query)
    
    @classmethod
    def _parse(cls: Type[T], client: Any, data: Dict[str, Any]) -> T:
        """Parse an update from Telegram API response.
        
        Parameters:
            client: The client instance.
            data: The update data from Telegram API.
            
        Returns:
            An Update instance.
        """
        update = cls(
            update_id=data["update_id"],
            message=data.get("message"),
            edited_message=data.get("edited_message"),
            channel_post=data.get("channel_post"),
            edited_channel_post=data.get("edited_channel_post"),
            inline_query=data.get("inline_query"),
            chosen_inline_result=data.get("chosen_inline_result"),
            callback_query=data.get("callback_query"),
            shipping_query=data.get("shipping_query"),
            pre_checkout_query=data.get("pre_checkout_query"),
            poll=data.get("poll"),
            poll_answer=data.get("poll_answer"),
            my_chat_member=data.get("my_chat_member"),
            chat_member=data.get("chat_member"),
            chat_join_request=data.get("chat_join_request"),
            _client=client
        )
        
        return update 