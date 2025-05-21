from dataclasses import dataclass, field
from typing import Optional, Dict, Any, Type, TypeVar

T = TypeVar('T', bound='CallbackQuery')

@dataclass
class CallbackQuery:
    """This object represents an incoming callback query from a callback button.
    
    Parameters:
        id (``str``):
            Unique identifier for this query.
            
        from_user (``dict``):
            Sender.
            
        chat_instance (``str``):
            Global identifier, uniquely corresponding to the chat.
            
        message (``dict``, optional):
            Message with the callback button that originated the query.
            
        inline_message_id (``str``, optional):
            Identifier of the message sent via the bot in inline mode.
            
        data (``str``, optional):
            Data associated with the callback button.
            
        game_short_name (``str``, optional):
            Short name of a Game to be returned.
    """
    
    id: str
    from_user: Dict[str, Any]
    chat_instance: str
    message: Optional[Dict[str, Any]] = None
    inline_message_id: Optional[str] = None
    data: Optional[str] = None
    game_short_name: Optional[str] = None
    _client: Any = field(default=None, repr=False)
    
    @classmethod
    def _parse(cls: Type[T], client: Any, data: Dict[str, Any]) -> T:
        """Parse a callback query from Telegram API response.
        
        Parameters:
            client: The client instance.
            data: The callback query data from Telegram API.
            
        Returns:
            A CallbackQuery instance.
        """
        # Create a new CallbackQuery instance
        return cls(
            id=data['id'],
            from_user=data['from'],
            chat_instance=data['chat_instance'],
            message=data.get('message'),
            inline_message_id=data.get('inline_message_id'),
            data=data.get('data'),
            game_short_name=data.get('game_short_name'),
            _client=client
        )
    
    async def answer(
        self,
        text: Optional[str] = None,
        show_alert: Optional[bool] = None,
        url: Optional[str] = None,
        cache_time: Optional[int] = None
    ) -> bool:
        """Answer this callback query.
        
        Parameters:
            text (``str``, optional):
                Text of the notification. If not specified, nothing will be shown to the user.
                
            show_alert (``bool``, optional):
                If True, an alert will be shown instead of a notification at the top of the chat screen.
                
            url (``str``, optional):
                URL that will be opened by the user's client.
                
            cache_time (``int``, optional):
                The maximum amount of time in seconds that the result of the callback query
                may be cached client-side.
                
        Returns:
            ``bool``: True on success.
        """
        if not self._client:
            raise ValueError("Callback query is not associated with a client")
        
        return await self._client.answer_callback_query(
            callback_query_id=self.id,
            text=text,
            show_alert=show_alert,
            url=url,
            cache_time=cache_time
        )
    
    async def edit_message_text(
        self,
        text: str,
        parse_mode: Optional[str] = None,
        entities: Optional[list] = None,
        disable_web_page_preview: Optional[bool] = None,
        reply_markup: Optional[Any] = None
    ) -> Any:
        """Edit the text of the message that triggered this callback query.
        
        Parameters:
            text (``str``):
                New text of the message.
                
            parse_mode (``str``, optional):
                Mode for parsing entities in the message text.
                
            entities (``list``, optional):
                List of special entities that appear in message text.
                
            disable_web_page_preview (``bool``, optional):
                Disables link previews for links in this message.
                
            reply_markup (:obj:`InlineKeyboardMarkup`, optional):
                A JSON-serialized object for an inline keyboard.
                
        Returns:
            :obj:`Message` | ``bool``: On success, if edited message is sent by the bot, 
            the edited Message is returned, otherwise True is returned.
        """
        if not self._client:
            raise ValueError("Callback query is not associated with a client")
        
        if self.inline_message_id:
            return await self._client.edit_message_text(
                inline_message_id=self.inline_message_id,
                text=text,
                parse_mode=parse_mode,
                entities=entities,
                disable_web_page_preview=disable_web_page_preview,
                reply_markup=reply_markup
            )
        
        if not self.message:
            raise ValueError("Message is not available in the callback query")
            
        return await self._client.edit_message_text(
            chat_id=self.message.get("chat", {}).get("id"),
            message_id=self.message.get("message_id"),
            text=text,
            parse_mode=parse_mode,
            entities=entities,
            disable_web_page_preview=disable_web_page_preview,
            reply_markup=reply_markup
        ) 