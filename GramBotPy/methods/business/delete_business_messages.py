from dataclasses import dataclass
from typing import List, Union, Dict, Any, Optional

@dataclass
class DeleteBusinessMessages:
    """
    Use this method to delete all messages sent on behalf of a connected business connected to the bot.
    
    Args:
        business_connection_id (``str``):
            Unique identifier of the business connection on behalf of which the messages were sent.
        
        chat_id (``int`` | ``str``):
            Unique identifier for the target chat or username of the target channel 
            (in the format @channelusername).
        
        message_ids (``List[int]``):
            Identifiers of messages to delete.
    """
    
    business_connection_id: str
    chat_id: Union[int, str]
    message_ids: List[int]
    
    async def _call(self, client):
        """Make the request to the Telegram API."""
        
        result = await client.send_request(
            "deleteBusinessMessages",
            {
                "business_connection_id": self.business_connection_id,
                "chat_id": self.chat_id,
                "message_ids": self.message_ids
            }
        )
        
        return result 