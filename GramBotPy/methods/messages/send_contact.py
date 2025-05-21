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

class SendContact:
    """Method for sending contact information."""
    
    async def send_contact(
        self: "GramBotPy",
        chat_id: Union[int, str],
        phone_number: str,
        first_name: str,
        last_name: Optional[str] = None,
        vcard: Optional[str] = None,
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
        """Send a phone contact.
        
        Parameters:
            chat_id (``int`` | ``str``):
                Unique identifier for the target chat or username.
                
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
            
                # Send a basic contact
                await bot.send_contact(
                    chat_id,
                    phone_number="+1234567890",
                    first_name="John",
                    last_name="Doe"
                )
                
                # Send a contact with vCard
                vcard = (
                    "BEGIN:VCARD\n"
                    "VERSION:3.0\n"
                    "N:Doe;John;;;\n"
                    "FN:John Doe\n"
                    "TEL;TYPE=CELL:+1234567890\n"
                    "EMAIL:john.doe@example.com\n"
                    "END:VCARD"
                )
                await bot.send_contact(
                    chat_id,
                    phone_number="+1234567890",
                    first_name="John",
                    last_name="Doe",
                    vcard=vcard
                )
        """
        self.logger.info(f"Sending contact to {chat_id}: {first_name} {last_name or ''} ({phone_number})")
        
        # Create params dictionary with required parameters
        params = {
            "chat_id": chat_id,
            "phone_number": phone_number,
            "first_name": first_name
        }
        
        # Add optional parameters if provided
        if last_name:
            params["last_name"] = last_name
            
        if vcard:
            params["vcard"] = vcard
            
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
        return await self._send_contact_request(chat_id, params)
    
    async def _send_contact_request(
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
                url = f"https://api.telegram.org/bot{self.token}/sendContact"
                
                # Following Telethon's pattern for proper HTTP handling
                async with session.post(url, data=params) as response:
                    # Check HTTP status first
                    if response.status != 200:
                        self.logger.error(f"HTTP error {response.status} when sending contact: {await response.text()}")
                        return self._get_fallback_message(
                            chat_id, 
                            params["phone_number"], 
                            params["first_name"], 
                            params.get("last_name")
                        )
                    
                    # Parse the JSON response
                    result = await response.json()
                
                    if not result.get("ok", False):
                        error_description = result.get('description', 'Unknown error')
                        self.logger.error(f"Error sending contact: {error_description}")
                        self.logger.debug(f"Params used: {params}")
                        return self._get_fallback_message(
                            chat_id, 
                            params["phone_number"], 
                            params["first_name"], 
                            params.get("last_name")
                        )
                
                    # Parse the response and create a Message object
                    message_data = result.get("result", {})
                    return Message._parse(self, message_data)
                
            except aiohttp.ClientError as e:
                self.logger.error(f"Network error sending contact: {e}", exc_info=True)
                return self._get_fallback_message(
                    chat_id, 
                    params["phone_number"], 
                    params["first_name"], 
                    params.get("last_name")
                )
            except Exception as e:
                self.logger.error(f"Error sending contact: {e}", exc_info=True)
                return self._get_fallback_message(
                    chat_id, 
                    params["phone_number"], 
                    params["first_name"], 
                    params.get("last_name")
                )
    
    def _get_fallback_message(
        self, 
        chat_id: Union[int, str], 
        phone_number: str,
        first_name: str,
        last_name: Optional[str] = None
    ) -> Message:
        """Create a fallback message object for error cases.
        
        Returns:
            :obj:`Message`: A placeholder message object.
        """
        contact = {
            "phone_number": phone_number,
            "first_name": first_name
        }
        
        if last_name:
            contact["last_name"] = last_name
            
        return Message(
            message_id=-1,
            date=int(datetime.now().timestamp()),
            chat={"id": int(chat_id) if str(chat_id).lstrip('-').isdigit() else 0, "type": "private"},
            contact=contact
        ) 