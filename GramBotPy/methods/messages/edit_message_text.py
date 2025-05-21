import typing
import json
import aiohttp
from typing import Optional, Union, Dict, Any
from datetime import datetime

from ...types import Message

if typing.TYPE_CHECKING:
    from ...client import GramBotPy
    from ...types import InlineKeyboardMarkup

class EditMessageText:
    """Method for editing text of messages."""
    
    async def edit_message_text(
        self: "GramBotPy",
        chat_id: Optional[Union[int, str]] = None,
        message_id: Optional[int] = None,
        inline_message_id: Optional[str] = None,
        text: str = "",
        parse_mode: Optional[str] = None,
        entities: Optional[list] = None,
        disable_web_page_preview: Optional[bool] = None,
        reply_markup: Optional["InlineKeyboardMarkup"] = None
    ) -> Union[Message, bool]:
        """Edit text and entities of messages.
        
        Parameters:
            chat_id (``int`` | ``str``, optional):
                Required if inline_message_id is not provided. ID of the chat or username.
                
            message_id (``int``, optional):
                Required if inline_message_id is not provided. ID of the message to edit.
                
            inline_message_id (``str``, optional):
                Required if chat_id and message_id are not provided. ID of the inline message.
                
            text (``str``):
                New text of the message, 1-4096 characters.
                
            parse_mode (``str``, optional):
                Mode for parsing entities in the message text.
                
            entities (``list``, optional):
                List of special entities that appear in message text, which can be specified
                instead of parse_mode.
                
            disable_web_page_preview (``bool``, optional):
                Disables link previews for links in this message.
                
            reply_markup (:obj:`InlineKeyboardMarkup`, optional):
                A JSON-serialized object for an inline keyboard.
                
        Returns:
            :obj:`Message` | ``bool``: On success, if edited message is sent by the bot, 
            the edited Message is returned, otherwise True is returned.
        """
        self.logger.info(f"Editing message text in chat {chat_id}, message {message_id}")
        
        # Validate required parameters
        if inline_message_id is None and (chat_id is None or message_id is None):
            self.logger.error("Either inline_message_id or both chat_id and message_id must be provided")
            if chat_id:
                return self._get_fallback_message(chat_id, message_id or 0, text)
            return False
            
        # Create params dictionary
        params = await self._prepare_edit_params(
            chat_id, message_id, inline_message_id, text, parse_mode,
            entities, disable_web_page_preview, reply_markup
        )
        
        # Make the API request
        return await self._send_edit_request(chat_id, message_id, inline_message_id, params)
    
    async def _prepare_edit_params(
        self,
        chat_id: Optional[Union[int, str]],
        message_id: Optional[int],
        inline_message_id: Optional[str],
        text: str,
        parse_mode: Optional[str],
        entities: Optional[list],
        disable_web_page_preview: Optional[bool],
        reply_markup: Optional["InlineKeyboardMarkup"]
    ) -> Dict[str, Any]:
        """Prepare parameters for editing a message.
        
        Returns:
            Dict[str, Any]: The parameters for the API request.
        """
        params = {"text": text}
        
        # Add appropriate ID parameters
        if inline_message_id:
            params["inline_message_id"] = inline_message_id
        else:
            params["chat_id"] = chat_id
            params["message_id"] = message_id
            
        # Add optional parameters if provided
        if parse_mode:
            params["parse_mode"] = parse_mode
            
        if entities:
            params["entities"] = json.dumps(entities)
            
        if disable_web_page_preview is not None:
            params["disable_web_page_preview"] = json.dumps(disable_web_page_preview)
            
        if reply_markup:
            if hasattr(reply_markup, "to_dict"):
                params["reply_markup"] = json.dumps(reply_markup.to_dict())
            else:
                params["reply_markup"] = json.dumps(reply_markup)
                
        return params
    
    async def _send_edit_request(
        self,
        chat_id: Optional[Union[int, str]],
        message_id: Optional[int],
        inline_message_id: Optional[str],
        params: Dict[str, Any]
    ) -> Union[Message, bool]:
        """Send the actual request to the Telegram API.
        
        Returns:
            :obj:`Message` | ``bool``: The edited message or True for inline messages.
        """
        async with aiohttp.ClientSession() as session:
            try:
                url = f"https://api.telegram.org/bot{self.token}/editMessageText"
                
                # Following Telethon's pattern for proper HTTP handling
                async with session.post(url, data=params) as response:
                    # Check HTTP status first
                    if response.status != 200:
                        self.logger.error(f"HTTP error {response.status} when editing message: {await response.text()}")
                        if chat_id and message_id:
                            return self._get_fallback_message(chat_id, message_id, params["text"])
                        return False
                    
                    # Parse the JSON response
                    result = await response.json()
                
                    if not result.get("ok", False):
                        error_description = result.get('description', 'Unknown error')
                        self.logger.error(f"Error editing message: {error_description}")
                        self.logger.debug(f"Params used: {params}")
                        if chat_id and message_id:
                            return self._get_fallback_message(chat_id, message_id, params["text"])
                        return False
                
                    # If this was an inline message, return True on success
                    if inline_message_id:
                        return True
                        
                    # Parse the response and create a Message object
                    message_data = result.get("result", {})
                    return Message._parse(self, message_data)
                
            except aiohttp.ClientError as e:
                self.logger.error(f"Network error editing message: {e}", exc_info=True)
                if chat_id and message_id:
                    return self._get_fallback_message(chat_id, message_id, params["text"])
                return False
            except Exception as e:
                self.logger.error(f"Error editing message: {e}", exc_info=True)
                if chat_id and message_id:
                    return self._get_fallback_message(chat_id, message_id, params["text"])
                return False
    
    def _get_fallback_message(
        self, 
        chat_id: Union[int, str],
        message_id: int,
        text: str
    ) -> Message:
        """Create a fallback message object for error cases.
        
        Returns:
            :obj:`Message`: A placeholder message object.
        """
        return Message(
            message_id=message_id,
            date=int(datetime.now().timestamp()),
            chat={"id": int(chat_id) if str(chat_id).lstrip('-').isdigit() else 0, "type": "private"},
            from_user={
                "id": self._me.id if self._me else 0,
                "is_bot": True,
                "first_name": self._me.first_name if self._me else "Bot"
            },
            text=text
        ) 