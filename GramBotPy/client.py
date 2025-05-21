import asyncio
import logging
import platform
import typing
import signal
import sys
from datetime import datetime
import aiohttp
import json

from .dispatcher import Dispatcher
from .methods import Methods
from .session import Session
from .types import User

class GramBotPy(Methods):
    """GramBotPy Client - A Telegram Bot API framework
    
    This is the main class for interacting with Telegram Bot API, 
    designed to combine Telethon features with Pyrogram organization.
    
    Parameters:
        token (``str``):
            The Bot API token obtained from @BotFather.
            
        api_id (``int``, optional):
            Your Telegram API ID from my.telegram.org.
            
        api_hash (``str``, optional):
            Your Telegram API hash from my.telegram.org.
            
        session (``str``, optional):
            The session name to be used. Defaults to token's first part.
            
        use_ipv6 (``bool``, optional):
            Whether to connect to Telegram using IPv6. Defaults to False.
            
        proxy (``dict``, optional):
            Proxy configuration as dictionary with keys: scheme, hostname, port, 
            and optionally username and password.
            
        timeout (``int``, optional):
            Connection timeout. Defaults to 10 seconds.
            
        max_retries (``int``, optional):
            Number of connection retries. Defaults to 5.
            
        workers (``int``, optional):
            Number of workers for handling updates. Defaults to 4.
            
    """

    APP_VERSION = f"GramBotPy 0.1.0"
    DEVICE_MODEL = f"{platform.python_implementation()} {platform.python_version()}"
    SYSTEM_VERSION = f"{platform.system()} {platform.release()}"
    
    def __init__(
        self,
        token: str,
        api_id: int = None,
        api_hash: str = None,
        session: str = None,
        use_ipv6: bool = False,
        proxy: dict = None,
        timeout: int = 10,
        max_retries: int = 5,
        workers: int = 4
    ):
        super().__init__()
        
        if not token:
            raise ValueError("Bot token is required")
        
        # Validate bot token format
        if not len(token.split(":")) == 2:
            raise ValueError("Invalid bot token format. It should contain a ':' character.")
        
        # Set instance attributes
        self.token = token
        self.api_id = api_id or 12345  # Default API ID
        self.api_hash = api_hash or "0123456789abcdef0123456789abcdef"  # Default API hash
        self.session = session or token.split(":")[0]  # Use first part of token as session name
        self.use_ipv6 = use_ipv6
        self.proxy = proxy
        self.timeout = timeout
        self.max_retries = max_retries
        self.workers = workers
        
        # Setup logging
        self.logger = logging.getLogger(__name__)
        
        # Initialize session
        self._session = Session(self.session)
        
        # Initialize dispatcher for handling updates
        self._dispatcher = Dispatcher(self, workers)
        
        # Initialized flag
        self._is_initialized = False
        self._is_connected = False
        self._me = None
        
    async def start(self) -> "GramBotPy":
        """Start the bot.
        
        This method connects to Telegram and logs in with the provided bot token.
        
        Returns:
            :obj:`GramBotPy`: The instance itself.
        """
        if self._is_connected:
            return self
        
        # Connect to Telegram
        await self.connect()
        
        # Log in with the bot token
        self._me = await self.sign_in_bot(self.token)
        
        # Start the update loop
        await self._dispatcher.start()
        
        self._is_connected = True
        return self
    
    async def connect(self) -> bool:
        """Connect to Telegram servers.
        
        Returns:
            ``bool``: True on success.
        """
        if self._is_connected:
            return True
        
        # Initialize connection
        # Here would be the actual connection logic
        
        self._is_initialized = True
        return True
    
    async def disconnect(self) -> bool:
        """Disconnect from Telegram servers.
        
        Returns:
            ``bool``: True on success.
        """
        if not self._is_connected:
            return True
        
        # Stop the dispatcher
        await self._dispatcher.stop()
        
        # Close the connection
        # Here would be the actual disconnection logic
        
        self._is_connected = False
        return True
    
    async def sign_in_bot(self, bot_token: str) -> User:
        """Sign in as a bot with the given token.
        
        Parameters:
            bot_token (``str``):
                The bot token to sign in with.
                
        Returns:
            :obj:`User`: The bot user.
        """
        # Here would be the actual sign in logic
        # Simplified for example
        return User(
            id=int(bot_token.split(":")[0]),
            is_bot=True,
            first_name="Bot",
            username="bot"
        )
    
    def command(self, command_name):
        """Decorator for handling bot commands.
        
        Parameters:
            command_name (``str``):
                The command name without the leading slash (e.g. "start" for /start).
                
        Returns:
            Callable: The decorator.
        """
        def command_filter(message):
            if not message.text:
                return False
            parts = message.text.split()
            if not parts:
                return False
            # Check if the first part of the message is the command
            return parts[0] == f"/{command_name}" or parts[0] == f"/{command_name}@{self._me.username}"
        
        return self.on_message(command_filter)
    
    def on_message(self, filters=None):
        """Decorator for handling messages.
        
        Parameters:
            filters: Optional filters to apply.
            
        Returns:
            Callable: The decorator.
        """
        return self._dispatcher.on_message(filters)
    
    def on_callback_query(self, filters=None):
        """Decorator for handling callback queries.
        
        Parameters:
            filters: Optional filters to apply.
            
        Returns:
            Callable: The decorator.
        """
        return self._dispatcher.on_callback_query(filters)
    
    def callback_query(self, data):
        """Decorator for handling callback queries with specific data.
        
        Parameters:
            data (``str``):
                The callback data to filter for.
                
        Returns:
            Callable: The decorator.
        """
        def callback_filter(callback_query):
            return callback_query.data == data
        
        return self.on_callback_query(callback_filter)
    
    def message_handler(self, message_type):
        """Decorator for handling specific message types.
        
        Parameters:
            message_type (``str``):
                The type of message to handle.
                
        Returns:
            Callable: The decorator.
        """
        def message_filter(message):
            if message_type == "text" and message.text:
                return True
            elif message_type == "photo" and message.photo:
                return True
            elif message_type == "video" and message.video:
                return True
            elif message_type == "audio" and message.audio:
                return True
            elif message_type == "sticker" and message.sticker:
                return True
            elif message_type == "document" and message.document:
                return True
            elif message_type == "contact" and message.contact:
                return True
            elif message_type == "location" and message.location:
                return True
            elif message_type == "new_chat_members" and message.new_chat_members:
                return True
            return False
        
        return self.on_message(message_filter)
    
    def chat_join_request_handler(self):
        """Decorator for handling chat join requests.
        
        Returns:
            Callable: The decorator.
        """
        def decorator(func):
            # This would be implemented in a real scenario
            return func
        return decorator
    
    def inline_query_handler(self):
        """Decorator for handling inline queries.
        
        Returns:
            Callable: The decorator.
        """
        def decorator(func):
            # Register handler with the dispatcher
            self._dispatcher.inline_query_handlers.append((func, None))
            return func
        return decorator
    
    def chosen_inline_result_handler(self):
        """Decorator for handling chosen inline results.
        
        Returns:
            Callable: The decorator.
        """
        def decorator(func):
            # Register handler with the dispatcher
            self._dispatcher.chosen_inline_result_handlers.append((func, None))
            return func
        return decorator
    
    def game_query_handler(self):
        """Decorator for handling game queries.
        
        Returns:
            Callable: The decorator.
        """
        def decorator(func):
            # Register handler with the dispatcher
            self._dispatcher.game_query_handlers.append((func, None))
            return func
        return decorator
    
    def callback_query_handler(self):
        """Decorator for handling all callback queries.
        
        Returns:
            Callable: The decorator.
        """
        return self.on_callback_query()
    
    def error_handler(self):
        """Decorator for handling errors.
        
        Returns:
            Callable: The decorator.
        """
        def decorator(func):
            # This would be implemented in a real scenario
            return func
        return decorator
    
    async def idle(self):
        """Idle the bot.
        
        This method keeps the bot running until stop() is called.
        """
        try:
            while self._is_connected:
                await asyncio.sleep(1)
        except (KeyboardInterrupt, SystemExit):
            await self.stop()
    
    def run(self):
        """Run the bot synchronously.
        
        This is a convenience method that calls `asyncio.run(bot.start())` 
        and sets up appropriate signal handlers for graceful shutdown.
        """
        loop = asyncio.get_event_loop()
        
        # Set up signal handlers for graceful shutdown
        try:
            for sig in (signal.SIGINT, signal.SIGTERM):
                loop.add_signal_handler(sig, lambda: asyncio.create_task(self.stop()))
        except NotImplementedError:
            # Windows doesn't support add_signal_handler
            pass
        
        try:
            print("Starting bot...")
            loop.run_until_complete(self.start())
            print(f"Bot started as @{self._me.username}")
            # Keep the event loop running until stop() is called
            loop.run_forever()
        except KeyboardInterrupt:
            pass
        finally:
            print("Shutting down...")
            loop.run_until_complete(self.stop())
            loop.close()
            print("Bot stopped")
    
    async def stop(self):
        """Stop the bot.
        
        This method disconnects from Telegram.
        """
        await self.disconnect()
    
    async def __aenter__(self) -> "GramBotPy":
        """Enter the context manager.
        
        Returns:
            :obj:`GramBotPy`: The instance itself.
        """
        await self.start()
        return self
    
    async def __aexit__(self, *args) -> None:
        """Exit the context manager."""
        await self.stop()
    
    async def send_request(self, method_name: str, params: dict = None) -> typing.Any:
        """Send a request to the Telegram Bot API.
        
        Parameters:
            method_name (``str``):
                The name of the method to call.
                
            params (``dict``, optional):
                The parameters to send with the request.
                
        Returns:
            ``typing.Any``: The response from the API.
        """
        base_url = f"https://api.telegram.org/bot{self.token}"
        url = f"{base_url}/{method_name}"
        
        if params is None:
            params = {}
        
        async with aiohttp.ClientSession() as session:
            try:
                async with session.post(url, json=params) as response:
                    result = await response.json()
                    
                    if result.get("ok"):
                        return result.get("result")
                    else:
                        error_message = result.get("description", "Unknown error")
                        error_code = result.get("error_code", 0)
                        self.logger.error(f"API Error {error_code}: {error_message}")
                        return False
            except Exception as e:
                self.logger.error(f"Request error: {e}")
                return False 