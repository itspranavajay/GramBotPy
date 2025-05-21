import asyncio
import logging
import typing
from datetime import datetime
import aiohttp
import json

from ...types import Message

if typing.TYPE_CHECKING:
    from ...client import GramBotPy
    from ...types import InlineKeyboardMarkup

class SendGame:
    """Method for sending games."""
    
    async def send_game(
        self: "GramBotPy",
        chat_id: int,
        game_short_name: str,
        business_connection_id: str = None,
        message_thread_id: int = None,
        disable_notification: bool = None,
        protect_content: bool = None,
        allow_paid_broadcast: bool = None,
        message_effect_id: str = None,
        reply_to_message_id: int = None,
        allow_sending_without_reply: bool = None,
        reply_markup: "InlineKeyboardMarkup" = None
    ) -> "Message":
        """Send a game.
        
        Parameters:
            chat_id (``int``):
                Unique identifier for the target chat.
                
            game_short_name (``str``):
                Short name of the game, serves as the unique identifier for the game.
                Set up your games via @BotFather.
                
            business_connection_id (``str``, optional):
                Unique identifier of the business connection on behalf of which the message will be sent.
                
            message_thread_id (``int``, optional):
                Unique identifier for the target message thread (topic) of the forum; for forum supergroups only.
                
            disable_notification (``bool``, optional):
                Sends the message silently. Users will receive a notification with no sound.
                
            protect_content (``bool``, optional):
                Protects the contents of the sent message from forwarding and saving.
                
            allow_paid_broadcast (``bool``, optional):
                Pass True to allow up to 1000 messages per second, ignoring broadcasting limits for a fee.
                
            message_effect_id (``str``, optional):
                Unique identifier of the message effect to be added to the message; for private chats only.
                
            reply_to_message_id (``int``, optional):
                If the message is a reply, ID of the original message.
                
            allow_sending_without_reply (``bool``, optional):
                Pass True if the message should be sent even if the specified replied-to message is not found.
                
            reply_markup (:obj:`InlineKeyboardMarkup`, optional):
                A JSON-serialized object for an inline keyboard. If empty, one 'Play game_title' button will be shown.
                If not empty, the first button must launch the game.
                
        Returns:
            :obj:`Message`: On success, the sent message is returned.
            
        Example:
            .. code-block:: python
            
                # Send a game with default 'Play' button
                await bot.send_game(chat_id, "my_game")
                
                # Send a game with custom buttons
                from GramBotPy.types import InlineKeyboardMarkup, InlineKeyboardButton
                
                markup = InlineKeyboardMarkup([
                    [InlineKeyboardButton("Play Now!", callback_game=CallbackGame())]
                ])
                
                await bot.send_game(chat_id, "my_game", reply_markup=markup)
        """
        self.logger.info(f"Sending game to {chat_id}: {game_short_name}")
        
        # Create the params dictionary with required parameters
        params = {
            "chat_id": chat_id,
            "game_short_name": game_short_name
        }
        
        # Add optional parameters if they are provided
        if business_connection_id:
            params["business_connection_id"] = business_connection_id
            
        if message_thread_id:
            params["message_thread_id"] = message_thread_id
            
        if disable_notification is not None:
            params["disable_notification"] = disable_notification
            
        if protect_content is not None:
            params["protect_content"] = protect_content
            
        if allow_paid_broadcast is not None:
            params["allow_paid_broadcast"] = allow_paid_broadcast
            
        if message_effect_id:
            params["message_effect_id"] = message_effect_id
            
        if reply_to_message_id:
            params["reply_to_message_id"] = reply_to_message_id
            
        if allow_sending_without_reply is not None:
            params["allow_sending_without_reply"] = allow_sending_without_reply
            
        if reply_markup:
            if hasattr(reply_markup, "to_dict"):
                params["reply_markup"] = json.dumps(reply_markup.to_dict())
            else:
                params["reply_markup"] = json.dumps(reply_markup)
        
        # Make the API request to send the game
        async with aiohttp.ClientSession() as session:
            try:
                url = f"https://api.telegram.org/bot{self.token}/sendGame"
                async with session.post(url, data=params) as response:
                    result = await response.json()
                    
                    if not result.get("ok", False):
                        error_description = result.get('description', 'Unknown error')
                        self.logger.error(f"Error sending game: {error_description}")
                        
                        # More detailed error logging
                        self.logger.debug(f"Params used: {params}")
                        
                        # Return a mock message in case of error
                        return Message(
                            message_id=-1,
                            date=int(datetime.now().timestamp()),
                            chat={"id": int(chat_id), "type": "private"}
                        )
                    
                    # Parse the response and create a Message object
                    message_data = result.get("result", {})
                    return Message._parse(self, message_data)
                    
            except aiohttp.ClientError as e:
                self.logger.error(f"Network error making request to Telegram API: {e}", exc_info=True)
                return Message(
                    message_id=-1,
                    date=int(datetime.now().timestamp()),
                    chat={"id": int(chat_id), "type": "private"}
                )
            except Exception as e:
                self.logger.error(f"Error making request to Telegram API: {e}", exc_info=True)
                # Return a mock message in case of exception
                return Message(
                    message_id=-1,
                    date=int(datetime.now().timestamp()),
                    chat={"id": int(chat_id), "type": "private"}
                ) 