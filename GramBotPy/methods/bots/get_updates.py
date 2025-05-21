import asyncio
import logging
import typing
from typing import List, Optional, Dict, Any
import aiohttp
import json
import time

if typing.TYPE_CHECKING:
    from ...client import GramBotPy
    from ...types import Update

class GetUpdates:
    """Method to get updates from Telegram."""
    
    async def get_updates(
        self: "GramBotPy",
        offset: Optional[int] = None,
        limit: Optional[int] = 100,
        timeout: Optional[int] = 0,
        allowed_updates: Optional[List[str]] = None
    ) -> List["Update"]:
        """Get new updates from Telegram.
        
        Parameters:
            offset (``int``, optional):
                Identifier of the first update to be returned.
                
            limit (``int``, optional):
                Limits the number of updates to be retrieved.
                Values between 1-100 are accepted. Default: 100.
                
            timeout (``int``, optional):
                Timeout in seconds for long polling. Default: 0 (short polling).
                
            allowed_updates (``list``, optional):
                List of update types to receive.
                
        Returns:
            ``list``: List of Update objects.
        """
        from ...types import Update
        
        # Use the last_update_id if offset is not provided
        if offset is None and hasattr(self, '_last_update_id'):
            offset = self._last_update_id + 1
        
        self.logger.debug(f"Getting updates with offset={offset}, limit={limit}")
        
        # Create params dictionary and filter out None values
        params = {}
        if offset is not None:
            params["offset"] = offset
        if limit is not None:
            params["limit"] = limit
        if timeout is not None:
            params["timeout"] = timeout
        
        if allowed_updates:
            params["allowed_updates"] = json.dumps(allowed_updates)
            
        # Make the request to Telegram Bot API
        try:
            updates = await self._make_get_updates_request(params)
            
            # Update the last_update_id if we received updates
            if updates and len(updates) > 0:
                self._last_update_id = max(update.update_id for update in updates)
                self.logger.debug(f"Updated last_update_id to {self._last_update_id}")
                
            return updates
        except Exception as e:
            self.logger.error(f"Error in get_updates: {e}", exc_info=True)
            return []
    
    async def _make_get_updates_request(self, params: Dict[str, Any]) -> List["Update"]:
        """Make the actual API request to get updates.
        
        Returns:
            List of Update objects.
        """
        from ...types import Update
        
        start_time = time.time()
        async with aiohttp.ClientSession() as session:
            try:
                url = f"https://api.telegram.org/bot{self.token}/getUpdates"
                
                # Following Telethon's pattern for proper HTTP handling
                async with session.get(url, params=params) as response:
                    # Check HTTP status first
                    if response.status != 200:
                        self.logger.error(f"HTTP error {response.status} when getting updates: {await response.text()}")
                        return []
                    
                    # Parse the JSON response
                    result = await response.json()
                    
                    if not result.get("ok", False):
                        error_description = result.get('description', 'Unknown error')
                        self.logger.error(f"Error getting updates: {error_description}")
                        return []
                        
                    # Parse the response and return Update objects
                    updates = []
                    for update_data in result.get("result", []):
                        try:
                            updates.append(Update._parse(self, update_data))
                        except Exception as e:
                            self.logger.error(f"Error parsing update {update_data.get('update_id', 'unknown')}: {e}", exc_info=True)
                    
                    # Log performance metrics
                    elapsed = time.time() - start_time
                    if updates:
                        self.logger.debug(f"Received {len(updates)} updates in {elapsed:.3f}s")
                    elif "timeout" in params and params["timeout"] > 0 and elapsed >= params["timeout"] - 1:
                        # This is normal for long polling timeouts
                        self.logger.debug(f"Long polling timeout after {elapsed:.3f}s")
                    else:
                        self.logger.debug(f"No updates received in {elapsed:.3f}s")
                            
                    return updates
                    
            except aiohttp.ClientError as e:
                self.logger.error(f"Network error making request to Telegram API: {e}", exc_info=True)
                return []
            except asyncio.CancelledError:
                # This is a normal way to stop the updates loop
                self.logger.debug("Update request cancelled")
                raise
            except Exception as e:
                self.logger.error(f"Error making request to Telegram API: {e}", exc_info=True)
                return []
    
    async def start_polling(
        self,
        poll_interval: float = 0.5,
        timeout: int = 10,
        limit: int = 100,
        allowed_updates: Optional[List[str]] = None,
        drop_pending_updates: bool = False
    ) -> None:
        """Start polling for updates.
        
        This method starts polling for updates in the background.
        It keeps track of the last received update ID and uses it as offset.
        
        Parameters:
            poll_interval (``float``, optional):
                Time to wait between polling requests in seconds. Default: 0.5.
                
            timeout (``int``, optional):
                Timeout for long polling in seconds. Default: 10.
                
            limit (``int``, optional):
                Limits the number of updates to be retrieved per request.
                Values between 1-100 are accepted. Default: 100.
                
            allowed_updates (``list``, optional):
                List of update types to receive.
                
            drop_pending_updates (``bool``, optional):
                Whether to drop pending updates. Default: False.
        """
        self.logger.info("Starting updates polling")
        
        # Initialize the last update ID
        if not hasattr(self, '_last_update_id'):
            self._last_update_id = 0
            
        # Drop pending updates if requested
        if drop_pending_updates:
            await self.get_updates(offset=-1)
            
        # Start the polling loop
        self._is_polling = True
        
        while self._is_polling:
            try:
                updates = await self.get_updates(
                    limit=limit,
                    timeout=timeout,
                    allowed_updates=allowed_updates
                )
                
                # Process updates
                for update in updates:
                    await self._dispatcher.process_update(update)
                    
                # Small pause between polling iterations
                if not updates and poll_interval > 0:
                    await asyncio.sleep(poll_interval)
                    
            except asyncio.CancelledError:
                self.logger.info("Updates polling cancelled")
                self._is_polling = False
                break
            except Exception as e:
                self.logger.error(f"Error in updates polling loop: {e}", exc_info=True)
                await asyncio.sleep(3)  # Pause on error to avoid rapid retries
                
        self.logger.info("Updates polling stopped")
    
    async def stop_polling(self) -> None:
        """Stop the updates polling."""
        self.logger.info("Stopping updates polling")
        self._is_polling = False 