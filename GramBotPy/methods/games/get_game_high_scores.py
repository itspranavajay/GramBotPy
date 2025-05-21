import asyncio
import logging
import typing
from datetime import datetime
import aiohttp
import json

from ...types import GameHighScore

if typing.TYPE_CHECKING:
    from ...client import GramBotPy

class GetGameHighScores:
    """Method for getting game high scores."""
    
    async def get_game_high_scores(
        self: "GramBotPy",
        user_id: int,
        chat_id: int = None,
        message_id: int = None,
        inline_message_id: str = None
    ) -> typing.List["GameHighScore"]:
        """Get data for high score tables.
        
        This method will currently return scores for the target user, plus two of their
        closest neighbors on each side. Will also return the top three users if the user
        and their neighbors are not among them.
        
        Parameters:
            user_id (``int``):
                Target user id.
                
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
            List of :obj:`GameHighScore`: Array of GameHighScore objects.
            
        Example:
            .. code-block:: python
            
                # Get high scores for a message in a chat
                high_scores = await bot.get_game_high_scores(user_id, chat_id=chat_id, message_id=message_id)
                for score in high_scores:
                    print(f"{score.position}. {score.user.first_name}: {score.score} points")
                
                # Get high scores for an inline message
                high_scores = await bot.get_game_high_scores(user_id, inline_message_id=inline_message_id)
        """
        self.logger.info(f"Getting game high scores for user {user_id}")
        
        # Create the params dictionary with required parameters
        params = {
            "user_id": user_id
        }
        
        # Add optional parameters if they are provided
        if chat_id is not None:
            params["chat_id"] = chat_id
            
        if message_id is not None:
            params["message_id"] = message_id
            
        if inline_message_id is not None:
            params["inline_message_id"] = inline_message_id
            
        if not inline_message_id and not (chat_id and message_id):
            self.logger.error("Both inline_message_id and chat_id/message_id are missing")
            raise ValueError("Either inline_message_id or both chat_id and message_id must be provided")
        
        # Make the API request to get the game high scores
        async with aiohttp.ClientSession() as session:
            try:
                url = f"https://api.telegram.org/bot{self.token}/getGameHighScores"
                async with session.post(url, data=params) as response:
                    result = await response.json()
                    
                    if not result.get("ok", False):
                        error_description = result.get('description', 'Unknown error')
                        self.logger.error(f"Error getting game high scores: {error_description}")
                        
                        # More detailed error logging
                        self.logger.debug(f"Params used: {params}")
                        return []
                    
                    # Parse the response and create GameHighScore objects
                    high_scores_data = result.get("result", [])
                    return [GameHighScore._parse(self, high_score_data) for high_score_data in high_scores_data]
                    
            except aiohttp.ClientError as e:
                self.logger.error(f"Network error making request to Telegram API: {e}", exc_info=True)
                return []
            except Exception as e:
                self.logger.error(f"Error making request to Telegram API: {e}", exc_info=True)
                return [] 