import asyncio
import logging
import inspect
import typing
from concurrent.futures import ThreadPoolExecutor

if typing.TYPE_CHECKING:
    from .client import GramBotPy
    from .types import Update, Message, CallbackQuery

class Dispatcher:
    """Dispatcher for handling updates.
    
    This class is responsible for handling incoming updates from Telegram
    and dispatching them to the appropriate handlers.
    
    Parameters:
        client (:obj:`GramBotPy`):
            The GramBotPy client instance.
            
        workers (``int``):
            Number of workers to use for handling updates.
    """
    
    def __init__(self, client: "GramBotPy", workers: int = 4):
        self.client = client
        self.workers = workers
        self.logger = logging.getLogger(__name__)
        
        self.message_handlers = []
        self.callback_query_handlers = []
        
        self._loop = None
        self._executor = None
        self._running = False
        self._update_handler_task = None
        
    async def start(self):
        """Start the dispatcher."""
        if self._running:
            return
            
        self._loop = asyncio.get_event_loop()
        self._executor = ThreadPoolExecutor(max_workers=self.workers)
        self._running = True
        
        # Start update handler
        self._update_handler_task = asyncio.create_task(self._update_handler())
        
    async def stop(self):
        """Stop the dispatcher."""
        if not self._running:
            return
            
        self._running = False
        
        if self._update_handler_task:
            self._update_handler_task.cancel()
            
        if self._executor:
            self._executor.shutdown()
            
    async def _update_handler(self):
        """Handle updates in the background."""
        last_update_id = 0
        
        while self._running:
            try:
                # Get updates from the client with the last_update_id + 1 as offset
                updates = await self.client.get_updates(offset=last_update_id + 1 if last_update_id else None)
                
                # Process each update
                for update in updates:
                    asyncio.create_task(self.process_update(update))
                    # Update the last_update_id
                    if update.update_id > last_update_id:
                        last_update_id = update.update_id
                    
                # Sleep to avoid high CPU usage
                await asyncio.sleep(0.1)
                
            except asyncio.CancelledError:
                break
            except Exception as e:
                self.logger.error(f"Error while handling updates: {e}", exc_info=True)
                await asyncio.sleep(1)
                
    async def process_update(self, update: "Update"):
        """Process a single update.
        
        Parameters:
            update (:obj:`Update`):
                The update to process.
        """
        try:
            if update.message:
                await self.process_message(update.message)
            elif update.callback_query:
                await self.process_callback_query(update.callback_query)
        except Exception as e:
            self.logger.error(f"Error while processing update: {e}")
            
    async def process_message(self, message: "Message"):
        """Process a message.
        
        Parameters:
            message (:obj:`Message`):
                The message to process.
        """
        for handler, filters in self.message_handlers:
            if await self._check_filters(filters, message):
                try:
                    if inspect.iscoroutinefunction(handler):
                        await handler(self.client, message)
                    else:
                        await self._loop.run_in_executor(
                            self._executor,
                            handler,
                            self.client,
                            message
                        )
                except Exception as e:
                    self.logger.error(f"Error in message handler: {e}")
                    
    async def process_callback_query(self, callback_query: "CallbackQuery"):
        """Process a callback query.
        
        Parameters:
            callback_query (:obj:`CallbackQuery`):
                The callback query to process.
        """
        for handler, filters in self.callback_query_handlers:
            if await self._check_filters(filters, callback_query):
                try:
                    if inspect.iscoroutinefunction(handler):
                        await handler(self.client, callback_query)
                    else:
                        await self._loop.run_in_executor(
                            self._executor,
                            handler,
                            self.client,
                            callback_query
                        )
                except Exception as e:
                    self.logger.error(f"Error in callback query handler: {e}")
                    
    async def _check_filters(self, filters, update):
        """Check if an update passes the filters.
        
        Parameters:
            filters:
                The filters to apply.
                
            update:
                The update to check.
                
        Returns:
            ``bool``: True if the update passes the filters.
        """
        if not filters:
            return True
            
        if callable(filters):
            result = filters(update)
            if inspect.isawaitable(result):
                return await result
            return result
            
        return True
        
    def on_message(self, filters=None):
        """Decorator for handling messages.
        
        Parameters:
            filters: Optional filters to apply.
            
        Returns:
            Callable: The decorator.
        """
        def decorator(func):
            self.message_handlers.append((func, filters))
            return func
        return decorator
        
    def on_callback_query(self, filters=None):
        """Decorator for handling callback queries.
        
        Parameters:
            filters: Optional filters to apply.
            
        Returns:
            Callable: The decorator.
        """
        def decorator(func):
            self.callback_query_handlers.append((func, filters))
            return func
        return decorator 