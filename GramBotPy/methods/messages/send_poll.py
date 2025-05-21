import typing
import json
import aiohttp
from typing import Union, Optional, List
from datetime import datetime

from ...types import Message

if typing.TYPE_CHECKING:
    from ...client import GramBotPy
    from ...types import InlineKeyboardMarkup, ReplyKeyboardMarkup
    from ...types import ReplyKeyboardRemove, ForceReply

class SendPoll:
    """Method for sending polls."""
    
    async def send_poll(
        self: "GramBotPy",
        chat_id: Union[int, str],
        question: str,
        options: List[str],
        is_anonymous: Optional[bool] = None,
        type: Optional[str] = None,
        allows_multiple_answers: Optional[bool] = None,
        correct_option_id: Optional[int] = None,
        explanation: Optional[str] = None,
        explanation_parse_mode: Optional[str] = None,
        explanation_entities: Optional[List[dict]] = None,
        open_period: Optional[int] = None,
        close_date: Optional[int] = None,
        is_closed: Optional[bool] = None,
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
        """Send a poll.
        
        Parameters:
            chat_id (``int`` | ``str``):
                Unique identifier for the target chat or username.
                
            question (``str``):
                Poll question, 1-300 characters.
                
            options (``list``):
                List of answer options, 2-10 strings 1-100 characters each.
                
            is_anonymous (``bool``, optional):
                True if the poll needs to be anonymous, defaults to True.
                
            type (``str``, optional):
                Poll type, "quiz" or "regular", defaults to "regular".
                
            allows_multiple_answers (``bool``, optional):
                True if the poll allows multiple answers, defaults to False.
                
            correct_option_id (``int``, optional):
                0-based identifier of the correct answer for quiz polls.
                
            explanation (``str``, optional):
                Text that is shown when a user chooses an incorrect answer.
                
            explanation_parse_mode (``str``, optional):
                Mode for parsing entities in the explanation.
                
            explanation_entities (``list``, optional):
                List of special entities that appear in the explanation.
                
            open_period (``int``, optional):
                Amount of time in seconds the poll will be active after creation.
                
            close_date (``int``, optional):
                Point in time when the poll will be automatically closed.
                
            is_closed (``bool``, optional):
                Pass True if the poll needs to be immediately closed.
                
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
            
                # Send a regular poll
                await bot.send_poll(
                    chat_id,
                    "Do you like Python?",
                    ["Yes, I do!", "No, I don't!"]
                )
                
                # Send a quiz poll with explanation
                await bot.send_poll(
                    chat_id,
                    "Which programming language was created by Guido van Rossum?",
                    ["JavaScript", "Python", "Ruby", "Java"],
                    type="quiz",
                    correct_option_id=1,
                    explanation="Python was created by Guido van Rossum in 1991."
                )
        """
        self.logger.info(f"Sending poll to {chat_id}")
        
        # Create params dictionary with required parameters
        params = {
            "chat_id": chat_id,
            "question": question,
            "options": json.dumps(options)
        }
        
        # Add optional parameters if provided
        if is_anonymous is not None:
            params["is_anonymous"] = json.dumps(is_anonymous)
            
        if type:
            params["type"] = type
            
        if allows_multiple_answers is not None:
            params["allows_multiple_answers"] = json.dumps(allows_multiple_answers)
            
        if correct_option_id is not None:
            params["correct_option_id"] = correct_option_id
            
        if explanation:
            params["explanation"] = explanation
            
        if explanation_parse_mode:
            params["explanation_parse_mode"] = explanation_parse_mode
            
        if explanation_entities:
            params["explanation_entities"] = json.dumps(explanation_entities)
            
        if open_period:
            params["open_period"] = open_period
            
        if close_date:
            params["close_date"] = close_date
            
        if is_closed is not None:
            params["is_closed"] = json.dumps(is_closed)
            
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
        return await self._send_poll_request(chat_id, params)
    
    async def _send_poll_request(
        self,
        chat_id: Union[int, str],
        params: dict
    ) -> Message:
        """Send the actual request to the Telegram API.
        
        Returns:
            :obj:`Message`: The sent message or a placeholder in case of error.
        """
        async with aiohttp.ClientSession() as session:
            try:
                url = f"https://api.telegram.org/bot{self.token}/sendPoll"
                
                # Following Telethon's pattern for proper HTTP handling
                async with session.post(url, data=params) as response:
                    # Check HTTP status first
                    if response.status != 200:
                        self.logger.error(f"HTTP error {response.status} when sending poll: {await response.text()}")
                        return self._get_poll_fallback_message(chat_id, params.get("question", ""))
                    
                    # Parse the JSON response
                    result = await response.json()
                
                    if not result.get("ok", False):
                        error_description = result.get('description', 'Unknown error')
                        self.logger.error(f"Error sending poll: {error_description}")
                        self.logger.debug(f"Params used: {params}")
                        return self._get_poll_fallback_message(chat_id, params.get("question", ""))
                
                    # Parse the response and create a Message object
                    message_data = result.get("result", {})
                    return Message._parse(self, message_data)
                
            except aiohttp.ClientError as e:
                self.logger.error(f"Network error sending poll: {e}", exc_info=True)
                return self._get_poll_fallback_message(chat_id, params.get("question", ""))
            except Exception as e:
                self.logger.error(f"Error sending poll: {e}", exc_info=True)
                return self._get_poll_fallback_message(chat_id, params.get("question", ""))
    
    def _get_poll_fallback_message(self, chat_id: Union[int, str], question: str) -> Message:
        """Create a fallback message object for error cases.
        
        Returns:
            :obj:`Message`: A placeholder message object.
        """
        return Message(
            message_id=-1,
            date=int(datetime.now().timestamp()),
            chat={"id": int(chat_id) if str(chat_id).lstrip('-').isdigit() else 0, "type": "private"},
            poll={
                "id": "error_poll_id",
                "question": question,
                "options": [{"text": "Error", "voter_count": 0}],
                "total_voter_count": 0,
                "is_closed": True,
                "is_anonymous": True,
                "type": "regular",
                "allows_multiple_answers": False
            }
        ) 