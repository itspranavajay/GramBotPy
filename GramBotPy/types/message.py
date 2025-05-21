from dataclasses import dataclass, field
from typing import Dict, List, Optional, Union, Any, Type, TypeVar
from datetime import datetime

T = TypeVar('T', bound='Message')

@dataclass
class Message:
    """This object represents a message.
    
    Parameters:
        message_id (``int``):
            Unique message identifier inside this chat.
            
        date (``int``):
            Date the message was sent in Unix time.
            
        chat (``dict``):
            Conversation the message belongs to.
            
        from_user (``dict``, optional):
            Sender of the message; empty for messages sent to channels.
            
        text (``str``, optional):
            For text messages, the actual UTF-8 text of the message.
            
        entities (``list``, optional):
            For text messages, special entities like usernames, URLs, etc. that appear in the text.
            
        reply_to_message (``Message``, optional):
            For replies, the original message.
            
        reply_markup (``object``, optional):
            Inline keyboard attached to the message.
            
        caption (``str``, optional):
            Caption for media messages.
            
        photo (``list``, optional):
            Available sizes of the photo (for photo messages).
            
        video (``dict``, optional):
            Video data (for video messages).
            
        audio (``dict``, optional):
            Audio data (for audio messages).
            
        document (``dict``, optional):
            Document data (for document messages).
            
        sticker (``dict``, optional):
            Sticker data (for sticker messages).
        
        new_chat_members (``list``, optional):
            New chat members added to the group.
        
        contact (``dict``, optional):
            Contact information for the message.
        
        location (``dict``, optional):
            Location information for the message.
    """
    
    message_id: int
    date: int
    chat: Dict[str, Any]
    from_user: Optional[Dict[str, Any]] = None
    text: Optional[str] = None
    entities: Optional[List[Dict[str, Any]]] = None
    reply_to_message: Optional['Message'] = None
    reply_markup: Optional[Any] = None
    caption: Optional[str] = None
    photo: Optional[List[Dict[str, Any]]] = None
    video: Optional[Dict[str, Any]] = None
    audio: Optional[Dict[str, Any]] = None
    document: Optional[Dict[str, Any]] = None
    sticker: Optional[Dict[str, Any]] = None
    new_chat_members: Optional[List[Dict[str, Any]]] = None
    contact: Optional[Dict[str, Any]] = None
    location: Optional[Dict[str, Any]] = None
    _client: Any = field(default=None, repr=False)
    
    def __post_init__(self):
        # Convert Unix timestamp to datetime if needed
        if isinstance(self.date, int):
            self._date_dt = datetime.fromtimestamp(self.date)
    
    @classmethod
    def _parse(cls: Type[T], client: Any, data: Dict[str, Any]) -> T:
        """Parse a message from Telegram API response.
        
        Parameters:
            client: The client instance.
            data: The message data from Telegram API.
            
        Returns:
            A Message instance.
        """
        if not data:
            return cls(
                message_id=-1,
                date=int(datetime.now().timestamp()),
                chat={"id": 0, "type": "private"},
                _client=client
            )
        
        # Handle reply_to_message recursively if it exists
        reply_to_message = None
        if data.get('reply_to_message'):
            reply_to_message = cls._parse(client, data['reply_to_message'])
        
        # Create dictionary with required parameters
        params = {
            "message_id": data.get('message_id', -1),
            "date": data.get('date', int(datetime.now().timestamp())),
            "chat": data.get('chat', {"id": 0, "type": "private"}),
            "_client": client
        }
        
        # Add optional parameters if they exist
        optional_fields = [
            'from', 'text', 'entities', 'caption', 'photo', 
            'video', 'audio', 'document', 'sticker', 'reply_markup', 
            'new_chat_members', 'contact', 'location'
        ]
        
        for field in optional_fields:
            if field in data:
                # Map 'from' to 'from_user' in our class
                if field == 'from':
                    params['from_user'] = data['from']
                else:
                    params[field] = data[field]
        
        # Add reply_to_message if we parsed it
        if reply_to_message:
            params['reply_to_message'] = reply_to_message
            
        # Create a new Message instance
        return cls(**params)
    
    @property
    def id(self) -> int:
        """Alias for message_id."""
        return self.message_id
    
    @property
    def chat_id(self) -> int:
        """Get the chat ID."""
        return self.chat.get("id")
    
    @property
    def sender_id(self) -> Optional[int]:
        """Get the sender ID."""
        if self.from_user:
            return self.from_user.get("id")
        return None
    
    @property
    def date_dt(self) -> datetime:
        """Get the message date as a datetime object."""
        return self._date_dt
    
    @property
    def content(self) -> Optional[str]:
        """Get the message content (text or caption)."""
        return self.text or self.caption
    
    @property
    def media(self) -> bool:
        """Check if the message contains media."""
        return any([self.photo, self.video, self.audio, self.document, self.sticker])
    
    async def reply(
        self,
        text: str,
        parse_mode: str = None,
        entities: list = None,
        disable_web_page_preview: bool = None,
        disable_notification: bool = None,
        reply_markup: Any = None
    ) -> 'Message':
        """Reply to this message.
        
        Parameters:
            text (``str``):
                Text of the message to be sent.
                
            parse_mode (``str``, optional):
                Mode for parsing entities in the message text.
                
            entities (``list``, optional):
                List of special entities that appear in message text.
                
            disable_web_page_preview (``bool``, optional):
                Disables link previews for links in this message.
                
            disable_notification (``bool``, optional):
                Sends the message silently.
                
            reply_markup (``object``, optional):
                Additional interface options.
                
        Returns:
            :obj:`Message`: On success, the sent message is returned.
        """
        if not self._client:
            raise ValueError("Message is not associated with a client")
        
        return await self._client.send_message(
            chat_id=self.chat_id,
            text=text,
            parse_mode=parse_mode,
            entities=entities,
            disable_web_page_preview=disable_web_page_preview,
            disable_notification=disable_notification,
            reply_to_message_id=self.message_id,
            reply_markup=reply_markup
        )
    
    async def edit_text(
        self,
        text: str,
        parse_mode: str = None,
        entities: list = None,
        disable_web_page_preview: bool = None,
        reply_markup: Any = None
    ) -> 'Message':
        """Edit this message's text.
        
        Parameters:
            text (``str``):
                New text of the message.
                
            parse_mode (``str``, optional):
                Mode for parsing entities in the message text.
                
            entities (``list``, optional):
                List of special entities that appear in message text.
                
            disable_web_page_preview (``bool``, optional):
                Disables link previews for links in this message.
                
            reply_markup (``object``, optional):
                Additional interface options.
                
        Returns:
            :obj:`Message`: On success, the edited message is returned.
        """
        if not self._client:
            raise ValueError("Message is not associated with a client")
        
        return await self._client.edit_message_text(
            chat_id=self.chat_id,
            message_id=self.message_id,
            text=text,
            parse_mode=parse_mode,
            entities=entities,
            disable_web_page_preview=disable_web_page_preview,
            reply_markup=reply_markup
        )
    
    async def delete(self) -> bool:
        """Delete this message.
        
        Returns:
            ``bool``: True on success.
        """
        if not self._client:
            raise ValueError("Message is not associated with a client")
        
        return await self._client.delete_messages(
            chat_id=self.chat_id,
            message_ids=self.message_id
        )
        
    async def forward_to(self, chat_id: Union[int, str]) -> 'Message':
        """Forward this message to another chat.
        
        Parameters:
            chat_id (``int`` | ``str``):
                Unique identifier for the target chat or username.
                
        Returns:
            :obj:`Message`: The forwarded message.
        """
        if not self._client:
            raise ValueError("Message is not associated with a client")
            
        return await self._client.forward_messages(
            chat_id=chat_id,
            from_chat_id=self.chat_id,
            message_ids=self.message_id
        )
    
    async def reply_photo(
        self,
        photo: Union[str, bytes],
        caption: str = None,
        parse_mode: str = None,
        caption_entities: list = None,
        disable_notification: bool = None,
        reply_markup: Any = None
    ) -> 'Message':
        """Reply to this message with a photo.
        
        Parameters:
            photo (``str`` | ``bytes``):
                Photo to send. Pass a file_id as string to send a photo that exists on the 
                Telegram servers, pass an HTTP URL as a string for Telegram to get a photo 
                from the Internet, or pass bytes for uploading a new photo.
                
            caption (``str``, optional):
                Photo caption, 0-1024 characters after entities parsing.
                
            parse_mode (``str``, optional):
                Mode for parsing entities in the photo caption.
                
            caption_entities (``list``, optional):
                List of special entities that appear in the caption.
                
            disable_notification (``bool``, optional):
                Sends the message silently.
                
            reply_markup (``object``, optional):
                Additional interface options.
                
        Returns:
            :obj:`Message`: On success, the sent photo message is returned.
        """
        if not self._client:
            raise ValueError("Message is not associated with a client")
        
        return await self._client.send_photo(
            chat_id=self.chat_id,
            photo=photo,
            caption=caption,
            parse_mode=parse_mode,
            caption_entities=caption_entities,
            disable_notification=disable_notification,
            reply_to_message_id=self.message_id,
            reply_markup=reply_markup
        )
        
    async def reply_contact(
        self,
        phone_number: str,
        first_name: str,
        last_name: str = None,
        vcard: str = None,
        disable_notification: bool = None,
        reply_markup: Any = None
    ) -> 'Message':
        """Reply to this message with a contact.
        
        Parameters:
            phone_number (``str``):
                Contact's phone number.
                
            first_name (``str``):
                Contact's first name.
                
            last_name (``str``, optional):
                Contact's last name.
                
            vcard (``str``, optional):
                Additional data about the contact in the form of a vCard, 0-2048 bytes.
                
            disable_notification (``bool``, optional):
                Sends the message silently.
                
            reply_markup (``object``, optional):
                Additional interface options.
                
        Returns:
            :obj:`Message`: On success, the sent contact message is returned.
        """
        if not self._client:
            raise ValueError("Message is not associated with a client")
        
        return await self._client.send_contact(
            chat_id=self.chat_id,
            phone_number=phone_number,
            first_name=first_name,
            last_name=last_name,
            vcard=vcard,
            disable_notification=disable_notification,
            reply_to_message_id=self.message_id,
            reply_markup=reply_markup
        )
        
    async def reply_location(
        self,
        latitude: float,
        longitude: float,
        horizontal_accuracy: float = None,
        live_period: int = None,
        heading: int = None,
        proximity_alert_radius: int = None,
        disable_notification: bool = None,
        reply_markup: Any = None
    ) -> 'Message':
        """Reply to this message with a location.
        
        Parameters:
            latitude (``float``):
                Latitude of the location.
                
            longitude (``float``):
                Longitude of the location.
                
            horizontal_accuracy (``float``, optional):
                The radius of uncertainty for the location, measured in meters (0-1500).
                
            live_period (``int``, optional):
                Period in seconds for which the location will be updated, should be 60-86400.
                
            heading (``int``, optional):
                For live locations, a direction in which the user is moving, in degrees (1-360).
                
            proximity_alert_radius (``int``, optional):
                For live locations, maximum distance for proximity alerts, in meters (1-100000).
                
            disable_notification (``bool``, optional):
                Sends the message silently.
                
            reply_markup (``object``, optional):
                Additional interface options.
                
        Returns:
            :obj:`Message`: On success, the sent location message is returned.
        """
        if not self._client:
            raise ValueError("Message is not associated with a client")
        
        return await self._client.send_location(
            chat_id=self.chat_id,
            latitude=latitude,
            longitude=longitude,
            horizontal_accuracy=horizontal_accuracy,
            live_period=live_period,
            heading=heading,
            proximity_alert_radius=proximity_alert_radius,
            disable_notification=disable_notification,
            reply_to_message_id=self.message_id,
            reply_markup=reply_markup
        ) 