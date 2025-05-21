import logging
import typing
import aiohttp
import json

from ...types import ReactionType

if typing.TYPE_CHECKING:
    from ...client import GramBotPy

class SetMessageReaction:
    """Method for setting reaction to a message."""
    
    async def set_message_reaction(
        self: "GramBotPy",
        chat_id: typing.Union[int, str],
        message_id: int,
        reaction: typing.List[ReactionType] = None,
        is_big: bool = None
    ) -> bool:
        """Change the chosen reactions on a message.
        
        Parameters:
            chat_id (``int`` | ``str``):
                Unique identifier for the target chat or username of the
                target channel (in the format @channelusername).
                
            message_id (``int``):
                Identifier of the target message.
                
            reaction (List of :obj:`ReactionType`, optional):
                New list of reaction types to set on the message.
                Pass an empty list to remove all reactions.
                
            is_big (``bool``, optional):
                Pass True to set the reaction with a big animation.
                
        Returns:
            ``bool``: True on success.
            
        Example:
            .. code-block:: python
            
                # Set a simple emoji reaction
                from GramBotPy.types import ReactionTypeEmoji
                
                emoji_reaction = ReactionTypeEmoji(emoji="👍")
                await bot.set_message_reaction(
                    chat_id=123456789,
                    message_id=42,
                    reaction=[emoji_reaction]
                )
                
                # Set a custom emoji reaction
                from GramBotPy.types import ReactionTypeCustomEmoji
                
                custom_reaction = ReactionTypeCustomEmoji(custom_emoji_id="5368324170671202286")
                await bot.set_message_reaction(
                    chat_id=123456789,
                    message_id=42,
                    reaction=[custom_reaction],
                    is_big=True
                )
                
                # Remove all reactions
                await bot.set_message_reaction(
                    chat_id=123456789,
                    message_id=42,
                    reaction=[]
                )
        """
        self.logger.info(f"Setting message reaction in {chat_id} for message {message_id}")
        
        # Create the params dictionary with required parameters
        params = {
            "chat_id": chat_id,
            "message_id": message_id
        }
        
        # Add optional parameters if they are provided
        if reaction is not None:
            params["reaction"] = json.dumps([r.to_dict() for r in reaction])
            
        if is_big is not None:
            params["is_big"] = is_big
        
        # Make the API request to set the message reaction
        async with aiohttp.ClientSession() as session:
            try:
                url = f"https://api.telegram.org/bot{self.token}/setMessageReaction"
                async with session.post(url, data=params) as response:
                    result = await response.json()
                    
                    if not result.get("ok", False):
                        error_description = result.get('description', 'Unknown error')
                        self.logger.error(f"Error setting message reaction: {error_description}")
                        
                        # More detailed error logging
                        self.logger.debug(f"Params used: {params}")
                        return False
                    
                    return True
                    
            except aiohttp.ClientError as e:
                self.logger.error(f"Network error making request to Telegram API: {e}", exc_info=True)
                return False
            except Exception as e:
                self.logger.error(f"Error making request to Telegram API: {e}", exc_info=True)
                return False 