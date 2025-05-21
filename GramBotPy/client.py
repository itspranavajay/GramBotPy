import asyncio
import logging
import platform
import typing
import signal
import sys
from datetime import datetime

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