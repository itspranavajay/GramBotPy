import asyncio
import logging
import typing
from datetime import datetime
import aiohttp
import json

from ...types import Message

if typing.TYPE_CHECKING:
    from ...client import GramBotPy
    from ...types import InlineKeyboardMarkup, ReplyKeyboardMarkup
    from ...types import ReplyKeyboardRemove, ForceReply

class SendMessage:
    """Method for sending messages."""
    
    async def send_message(
        self: "GramBotPy",
        chat_id: typing.Union[int, str],
        text: str,
        parse_mode: str = None,
        entities: list = None,
        disable_web_page_preview: bool = None,
        disable_notification: bool = None,
        protect_content: bool = None,
        reply_to_message_id: int = None,
        allow_sending_without_reply: bool = None,
        reply_markup: typing.Union[
            "InlineKeyboardMarkup",
            "ReplyKeyboardMarkup",
            "ReplyKeyboardRemove",
            "ForceReply"
        ] = None
    ) -> "Message":
        """Send text messages.
        
        Parameters:
            chat_id (``int`` | ``str``):
                Unique identifier for the target chat or username of the target channel
                (in the format @channelusername).
                
            text (``str``):
                Text of the message to be sent, 1-4096 characters.
                
            parse_mode (``str``, optional):
                Mode for parsing entities in the message text.
                See Telegram Bot API for available options.
                
            entities (``list``, optional):
                List of special entities that appear in message text, which can be specified
                instead of parse_mode.
                
            disable_web_page_preview (``bool``, optional):
                Disables link previews for links in this message.
                
            disable_notification (``bool``, optional):
                Sends the message silently. Users will receive a notification with no sound.
                
            protect_content (``bool``, optional):
                Protects the contents of the sent message from forwarding and saving.
                
            reply_to_message_id (``int``, optional):
                If the message is a reply, ID of the original message.
                
            allow_sending_without_reply (``bool``, optional):
                Pass True if the message should be sent even if the specified replied-to
                message is not found.
                
            reply_markup (:obj:`InlineKeyboardMarkup` | :obj:`ReplyKeyboardMarkup` | :obj:`ReplyKeyboardRemove` | :obj:`ForceReply`, optional):
                Additional interface options. An object for an inline keyboard,
                custom reply keyboard, instructions to remove reply keyboard
                or to force a reply from the user.
                
        Returns:
            :obj:`Message`: On success, the sent message is returned.
            
        Example:
            .. code-block:: python
            
                # Simple example
                await bot.send_message(chat_id, "Hello, world!")
                
                # With markdown
                await bot.send_message(chat_id, "*Bold* text", parse_mode="Markdown")
                
                # With inline keyboard
                from GramBotPy.types import InlineKeyboardMarkup, InlineKeyboardButton
                
                markup = InlineKeyboardMarkup([
                    [InlineKeyboardButton("Button 1", callback_data="btn1")],
                    [InlineKeyboardButton("Button 2", callback_data="btn2")]
                ])
                
                await bot.send_message(chat_id, "Message with buttons", reply_markup=markup)
        """
        self.logger.info(f"Sending message to {chat_id}: {text}")
        
        # Create the params dictionary with required parameters
        params = {
            "chat_id": chat_id,
            "text": text
        }
        
        # Add optional parameters if they are provided
        if parse_mode:
            params["parse_mode"] = parse_mode
            
        if entities:
            params["entities"] = json.dumps(entities)
            
        if disable_web_page_preview is not None:
            params["disable_web_page_preview"] = disable_web_page_preview
            
        if disable_notification is not None:
            params["disable_notification"] = disable_notification
            
        if protect_content is not None:
            params["protect_content"] = protect_content
            
        if reply_to_message_id:
            params["reply_to_message_id"] = reply_to_message_id
            
        if allow_sending_without_reply is not None:
            params["allow_sending_without_reply"] = allow_sending_without_reply
            
        if reply_markup:
            if hasattr(reply_markup, "to_dict"):
                params["reply_markup"] = json.dumps(reply_markup.to_dict())
            else:
                params["reply_markup"] = json.dumps(reply_markup)
        
        # Make the API request to send the message
        async with aiohttp.ClientSession() as session:
            try:
                url = f"https://api.telegram.org/bot{self.token}/sendMessage"
                async with session.post(url, data=params) as response:
                    result = await response.json()
                    
                    if not result.get("ok", False):
                        error_description = result.get('description', 'Unknown error')
                        self.logger.error(f"Error sending message: {error_description}")
                        
                        # More detailed error logging like Telethon does
                        self.logger.debug(f"Params used: {params}")
                        
                        # Return a mock message in case of error
                        return Message(
                            message_id=-1,
                            date=int(datetime.now().timestamp()),
                            chat={"id": int(chat_id) if str(chat_id).lstrip('-').isdigit() else 0, "type": "private"},
                            text=text
                        )
                    
                    # Parse the response and create a Message object
                    message_data = result.get("result", {})
                    return Message._parse(self, message_data)
                    
            except aiohttp.ClientError as e:
                self.logger.error(f"Network error making request to Telegram API: {e}", exc_info=True)
                return Message(
                    message_id=-1,
                    date=int(datetime.now().timestamp()),
                    chat={"id": int(chat_id) if str(chat_id).lstrip('-').isdigit() else 0, "type": "private"},
                    text=text
                )
            except Exception as e:
                self.logger.error(f"Error making request to Telegram API: {e}", exc_info=True)
                # Return a mock message in case of exception
                return Message(
                    message_id=-1,
                    date=int(datetime.now().timestamp()),
                    chat={"id": int(chat_id) if str(chat_id).lstrip('-').isdigit() else 0, "type": "private"},
                    text=text
                ) 