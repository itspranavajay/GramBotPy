from dataclasses import dataclass
from typing import Optional, Dict, Any

@dataclass
class DeleteWebhook:
    """
    Use this method to remove webhook integration if you decide to switch back to getUpdates.
    
    Parameters:
        drop_pending_updates (``bool``, *optional*):
            Pass True to drop all pending updates.
    """
    
    drop_pending_updates: Optional[bool] = None
    
    async def _call(self, client):
        """
        Make the request to the Telegram API.
        
        Returns:
            ``bool``: True on success.
        """
        
        params: Dict[str, Any] = {}
        
        if self.drop_pending_updates is not None:
            params["drop_pending_updates"] = self.drop_pending_updates
        
        result = await client.send_request(
            "deleteWebhook",
            params
        )
        
        return result 