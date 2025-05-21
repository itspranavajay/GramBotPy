import asyncio
import logging
import typing
from datetime import datetime
import aiohttp
import json

from ...types import Message

if typing.TYPE_CHECKING:
    from ...client import GramBotPy

class SendGift:
    """Method for sending gifts."""
    
    async def send_gift(
        self: "GramBotPy",
        user_id: int = None,
        chat_id: typing.Union[int, str] = None,
        message_thread_id: int = None,
        gift_star_count: int = None,
        pay_for_upgrade: bool = None,
        disable_notification: bool = None,
        protect_content: bool = None
    ) -> "Message":
        """Send a gift to a user or chat.
        
        Parameters:
            user_id (``int``, optional):
                Unique identifier of the target user. Required if chat_id is not specified.
                
            chat_id (``int`` | ``str``, optional):
                Unique identifier for the target chat or username of the target channel.
                Required if user_id is not specified.
                
            message_thread_id (``int``, optional):
                Unique identifier for the target message thread (topic) of the forum; for forum supergroups only.
                
            gift_star_count (``int``, optional):
                Amount of stars to send with the gift, should be one of the amounts allowed by Telegram.
                
            pay_for_upgrade (``bool``, optional):
                Pass True to pay for upgrading the gift from regular to unique, instead of just paying for a regular gift.
                
            disable_notification (``bool``, optional):
                Sends the message silently. Users will receive a notification with no sound.
                
            protect_content (``bool``, optional):
                Protects the contents of the sent message from forwarding and saving.
                
        Returns:
            :obj:`Message`: On success, the sent message is returned.
            
        Example:
            .. code-block:: python
            
                # Send a gift to a user
                await bot.send_gift(user_id=123456789, gift_star_count=10)
                
                # Send a gift to a channel
                await bot.send_gift(chat_id="@channel_username", gift_star_count=50)
        """
        self.logger.info(f"Sending gift to user_id={user_id}, chat_id={chat_id}")
        
        # Create the params dictionary
        params = {}
        
        # Add required parameters based on target (user or chat)
        if user_id is not None:
            params["user_id"] = user_id
        elif chat_id is not None:
            params["chat_id"] = chat_id
        else:
            raise ValueError("Either user_id or chat_id must be provided")
        
        # Add optional parameters if they are provided
        if message_thread_id is not None:
            params["message_thread_id"] = message_thread_id
            
        if gift_star_count is not None:
            params["gift_star_count"] = gift_star_count
            
        if pay_for_upgrade is not None:
            params["pay_for_upgrade"] = pay_for_upgrade
            
        if disable_notification is not None:
            params["disable_notification"] = disable_notification
            
        if protect_content is not None:
            params["protect_content"] = protect_content
        
        # Make the API request to send the gift
        async with aiohttp.ClientSession() as session:
            try:
                url = f"https://api.telegram.org/bot{self.token}/sendGift"
                async with session.post(url, data=params) as response:
                    result = await response.json()
                    
                    if not result.get("ok", False):
                        error_description = result.get('description', 'Unknown error')
                        self.logger.error(f"Error sending gift: {error_description}")
                        
                        # More detailed error logging
                        self.logger.debug(f"Params used: {params}")
                        
                        # Return a mock message in case of error
                        return Message(
                            message_id=-1,
                            date=int(datetime.now().timestamp()),
                            chat={"id": chat_id if chat_id else user_id, "type": "private"}
                        )
                    
                    # Parse the response and create a Message object
                    message_data = result.get("result", {})
                    return Message._parse(self, message_data)
                    
            except aiohttp.ClientError as e:
                self.logger.error(f"Network error making request to Telegram API: {e}", exc_info=True)
                return Message(
                    message_id=-1,
                    date=int(datetime.now().timestamp()),
                    chat={"id": chat_id if chat_id else user_id, "type": "private"}
                )
            except Exception as e:
                self.logger.error(f"Error making request to Telegram API: {e}", exc_info=True)
                # Return a mock message in case of exception
                return Message(
                    message_id=-1,
                    date=int(datetime.now().timestamp()),
                    chat={"id": chat_id if chat_id else user_id, "type": "private"}
                ) 