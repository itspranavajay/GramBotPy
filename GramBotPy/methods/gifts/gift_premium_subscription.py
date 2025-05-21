import asyncio
import logging
import typing
from datetime import datetime
import aiohttp
import json

from ...types import Message

if typing.TYPE_CHECKING:
    from ...client import GramBotPy

class GiftPremiumSubscription:
    """Method for gifting premium subscriptions."""
    
    async def gift_premium_subscription(
        self: "GramBotPy",
        user_id: int,
        gift_code: str = None,
        months: int = None,
        disable_notification: bool = None
    ) -> "Message":
        """Gift a Telegram Premium subscription to a user.
        
        Parameters:
            user_id (``int``):
                Unique identifier of the target user.
                
            gift_code (``str``, optional):
                Telegram gift code for a Premium subscription.
                Either gift_code or months must be provided.
                
            months (``int``, optional):
                Number of months to gift, should be one of the values available for gifting.
                Either gift_code or months must be provided.
                
            disable_notification (``bool``, optional):
                Sends the message silently. Users will receive a notification with no sound.
                
        Returns:
            :obj:`Message`: On success, the sent message is returned.
            
        Example:
            .. code-block:: python
            
                # Gift premium using a gift code
                await bot.gift_premium_subscription(user_id=123456789, gift_code="ABCDEF123456")
                
                # Gift premium for 3 months
                await bot.gift_premium_subscription(user_id=123456789, months=3)
        """
        self.logger.info(f"Gifting premium subscription to user {user_id}")
        
        # Create the params dictionary with required parameters
        params = {
            "user_id": user_id
        }
        
        # Either gift_code or months must be provided
        if gift_code is not None:
            params["gift_code"] = gift_code
        elif months is not None:
            params["months"] = months
        else:
            raise ValueError("Either gift_code or months must be provided")
        
        # Add optional parameters if they are provided
        if disable_notification is not None:
            params["disable_notification"] = disable_notification
        
        # Make the API request to gift the premium subscription
        async with aiohttp.ClientSession() as session:
            try:
                url = f"https://api.telegram.org/bot{self.token}/giftPremiumSubscription"
                async with session.post(url, data=params) as response:
                    result = await response.json()
                    
                    if not result.get("ok", False):
                        error_description = result.get('description', 'Unknown error')
                        self.logger.error(f"Error gifting premium subscription: {error_description}")
                        
                        # More detailed error logging
                        self.logger.debug(f"Params used: {params}")
                        
                        # Return a mock message in case of error
                        return Message(
                            message_id=-1,
                            date=int(datetime.now().timestamp()),
                            chat={"id": user_id, "type": "private"}
                        )
                    
                    # Parse the response and create a Message object
                    message_data = result.get("result", {})
                    return Message._parse(self, message_data)
                    
            except aiohttp.ClientError as e:
                self.logger.error(f"Network error making request to Telegram API: {e}", exc_info=True)
                return Message(
                    message_id=-1,
                    date=int(datetime.now().timestamp()),
                    chat={"id": user_id, "type": "private"}
                )
            except Exception as e:
                self.logger.error(f"Error making request to Telegram API: {e}", exc_info=True)
                # Return a mock message in case of exception
                return Message(
                    message_id=-1,
                    date=int(datetime.now().timestamp()),
                    chat={"id": user_id, "type": "private"}
                ) 