from typing import Optional, Union

from .delete_webhook import DeleteWebhook

async def delete_webhook(
    self,
    drop_pending_updates: Optional[bool] = None
) -> bool:
    """
    Use this method to remove webhook integration if you decide to switch back to getUpdates.
    
    Parameters:
        drop_pending_updates (``bool``, *optional*):
            Pass True to drop all pending updates.
            
    Returns:
        ``bool``: True on success.
    """
    delete_webhook_obj = DeleteWebhook(
        drop_pending_updates=drop_pending_updates
    )
    
    return await delete_webhook_obj._call(self) 