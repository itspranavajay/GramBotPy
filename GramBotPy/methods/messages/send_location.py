import typing
import json
import aiohttp
from typing import Union, Optional, Dict, Any
from datetime import datetime

from ...types import Message

if typing.TYPE_CHECKING:
    from ...client import GramBotPy
    from ...types import InlineKeyboardMarkup, ReplyKeyboardMarkup
    from ...types import ReplyKeyboardRemove, ForceReply

class SendLocation:
    """Method for sending locations."""
    
    async def send_location(
        self: "GramBotPy",
        chat_id: Union[int, str],
        latitude: float,
        longitude: float,
        horizontal_accuracy: Optional[float] = None,
        live_period: Optional[int] = None,
        heading: Optional[int] = None,
        proximity_alert_radius: Optional[int] = None,
        disable_notification: Optional[bool] = None,
        protect_content: Optional[bool] = None,
        reply_to_message_id: Optional[int] = None,
        allow_sending_without_reply: Optional[bool] = None,
        reply_markup: Optional[Union[
            "InlineKeyboardMarkup",
            "ReplyKeyboardMarkup",
            "ReplyKeyboardRemove",
            "ForceReply"
        ]] = None
    ) -> "Message":
        """Send a location point.
        
        Parameters:
            chat_id (``int`` | ``str``):
                Unique identifier for the target chat or username.
                
            latitude (``float``):
                Latitude of the location.
                
            longitude (``float``):
                Longitude of the location.
                
            horizontal_accuracy (``float``, optional):
                The radius of uncertainty for the location, measured in meters; 0-1500.
                
            live_period (``int``, optional):
                Period in seconds for which the location will be updated, should be 
                between 60 and 86400. For live locations only.
                
            heading (``int``, optional):
                For live locations, a direction in which the user is moving, in degrees.
                
            proximity_alert_radius (``int``, optional):
                For live locations, a maximum distance for proximity alerts, in meters.
                
            disable_notification (``bool``, optional):
                Sends the message silently.
                
            protect_content (``bool``, optional):
                Protects the contents of the sent message from forwarding and saving.
                
            reply_to_message_id (``int``, optional):
                If the message is a reply, ID of the original message.
                
            allow_sending_without_reply (``bool``, optional):
                Pass True if the message should be sent even if the specified replied-to
                message is not found.
                
            reply_markup (:obj:`InlineKeyboardMarkup` | :obj:`ReplyKeyboardMarkup` | :obj:`ReplyKeyboardRemove` | :obj:`ForceReply`, optional):
                Additional interface options.
                
        Returns:
            :obj:`Message`: On success, the sent Message is returned.
            
        Example:
            .. code-block:: python
            
                # Send a location
                await bot.send_location(chat_id, 37.7749, -122.4194)
                
                # Send a live location that updates for 5 minutes
                await bot.send_location(
                    chat_id, 37.7749, -122.4194, 
                    live_period=300
                )
        """
        self.logger.info(f"Sending location to {chat_id}: {latitude}, {longitude}")
        
        # Create params dictionary with required parameters
        params = {
            "chat_id": chat_id,
            "latitude": latitude,
            "longitude": longitude
        }
        
        # Add optional parameters if provided
        if horizontal_accuracy is not None:
            params["horizontal_accuracy"] = horizontal_accuracy
            
        if live_period is not None:
            params["live_period"] = live_period
            
        if heading is not None:
            params["heading"] = heading
            
        if proximity_alert_radius is not None:
            params["proximity_alert_radius"] = proximity_alert_radius
            
        if disable_notification is not None:
            params["disable_notification"] = json.dumps(disable_notification)
            
        if protect_content is not None:
            params["protect_content"] = json.dumps(protect_content)
            
        if reply_to_message_id:
            params["reply_to_message_id"] = reply_to_message_id
            
        if allow_sending_without_reply is not None:
            params["allow_sending_without_reply"] = json.dumps(allow_sending_without_reply)
            
        if reply_markup:
            if hasattr(reply_markup, "to_dict"):
                params["reply_markup"] = json.dumps(reply_markup.to_dict())
            else:
                params["reply_markup"] = json.dumps(reply_markup)
        
        # Make the API request
        return await self._send_location_request(chat_id, params)
    
    async def _send_location_request(
        self,
        chat_id: Union[int, str],
        params: Dict[str, Any]
    ) -> Message:
        """Send the actual request to the Telegram API.
        
        Returns:
            :obj:`Message`: The sent message or a placeholder in case of error.
        """
        async with aiohttp.ClientSession() as session:
            try:
                url = f"https://api.telegram.org/bot{self.token}/sendLocation"
                
                # Following Telethon's pattern for proper HTTP handling
                async with session.post(url, data=params) as response:
                    # Check HTTP status first
                    if response.status != 200:
                        self.logger.error(f"HTTP error {response.status} when sending location: {await response.text()}")
                        return self._get_location_fallback_message(chat_id, params["latitude"], params["longitude"])
                    
                    # Parse the JSON response
                    result = await response.json()
                
                    if not result.get("ok", False):
                        error_description = result.get('description', 'Unknown error')
                        self.logger.error(f"Error sending location: {error_description}")
                        self.logger.debug(f"Params used: {params}")
                        return self._get_location_fallback_message(chat_id, params["latitude"], params["longitude"])
                
                    # Parse the response and create a Message object
                    message_data = result.get("result", {})
                    return Message._parse(self, message_data)
                
            except aiohttp.ClientError as e:
                self.logger.error(f"Network error sending location: {e}", exc_info=True)
                return self._get_location_fallback_message(chat_id, params["latitude"], params["longitude"])
            except Exception as e:
                self.logger.error(f"Error sending location: {e}", exc_info=True)
                return self._get_location_fallback_message(chat_id, params["latitude"], params["longitude"])
    
    def _get_location_fallback_message(
        self, 
        chat_id: Union[int, str], 
        latitude: float, 
        longitude: float
    ) -> Message:
        """Create a fallback message object for error cases.
        
        Returns:
            :obj:`Message`: A placeholder message object.
        """
        return Message(
            message_id=-1,
            date=int(datetime.now().timestamp()),
            chat={"id": int(chat_id) if str(chat_id).lstrip('-').isdigit() else 0, "type": "private"},
            location={"latitude": latitude, "longitude": longitude}
        ) 