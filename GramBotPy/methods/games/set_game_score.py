import asyncio
import logging
import typing
from datetime import datetime
import aiohttp
import json

from ...types import Message

if typing.TYPE_CHECKING:
    from ...client import GramBotPy

class SetGameScore:
    """Method for setting game scores."""
    
    async def set_game_score(
        self: "GramBotPy",
        user_id: int,
        score: int,
        force: bool = None,
        disable_edit_message: bool = None,
        chat_id: int = None,
        message_id: int = None,
        inline_message_id: str = None
    ) -> typing.Union["Message", bool]:
        """Set the score of the specified user in a game.
        
        Parameters:
            user_id (``int``):
                User identifier.
                
            score (``int``):
                New score, must be non-negative.
                
            force (``bool``, optional):
                Pass True if the high score is allowed to decrease.
                This can be useful when fixing mistakes or banning cheaters.
                
            disable_edit_message (``bool``, optional):
                Pass True if the game message should not be automatically edited to include
                the current scoreboard.
                
            chat_id (``int``, optional):
                Required if inline_message_id is not specified.
                Unique identifier for the target chat.
                
            message_id (``int``, optional):
                Required if inline_message_id is not specified.
                Identifier of the sent message.
                
            inline_message_id (``str``, optional):
                Required if chat_id and message_id are not specified.
                Identifier of the inline message.
                
        Returns:
            :obj:`Message` | ``bool``: On success, if the message is not an inline message, the edited
            Message is returned, otherwise True is returned.
            
        Example:
            .. code-block:: python
            
                # Set score for a message in a chat
                await bot.set_game_score(user_id, 100, chat_id=chat_id, message_id=message_id)
                
                # Set score for an inline message
                await bot.set_game_score(user_id, 100, inline_message_id=inline_message_id)
        """
        self.logger.info(f"Setting game score for user {user_id} to {score}")
        
        # Create the params dictionary with required parameters
        params = {
            "user_id": user_id,
            "score": score
        }
        
        # Add optional parameters if they are provided
        if force is not None:
            params["force"] = force
            
        if disable_edit_message is not None:
            params["disable_edit_message"] = disable_edit_message
            
        if chat_id is not None:
            params["chat_id"] = chat_id
            
        if message_id is not None:
            params["message_id"] = message_id
            
        if inline_message_id is not None:
            params["inline_message_id"] = inline_message_id
            
        if not inline_message_id and not (chat_id and message_id):
            self.logger.error("Both inline_message_id and chat_id/message_id are missing")
            raise ValueError("Either inline_message_id or both chat_id and message_id must be provided")
        
        # Make the API request to set the game score
        async with aiohttp.ClientSession() as session:
            try:
                url = f"https://api.telegram.org/bot{self.token}/setGameScore"
                async with session.post(url, data=params) as response:
                    result = await response.json()
                    
                    if not result.get("ok", False):
                        error_description = result.get('description', 'Unknown error')
                        self.logger.error(f"Error setting game score: {error_description}")
                        
                        # More detailed error logging
                        self.logger.debug(f"Params used: {params}")
                        return False
                    
                    # If it's an inline message, return True
                    if inline_message_id:
                        return True
                    
                    # For regular messages, parse the response and create a Message object
                    message_data = result.get("result", {})
                    return Message._parse(self, message_data)
                    
            except aiohttp.ClientError as e:
                self.logger.error(f"Network error making request to Telegram API: {e}", exc_info=True)
                return False
            except Exception as e:
                self.logger.error(f"Error making request to Telegram API: {e}", exc_info=True)
                return False 