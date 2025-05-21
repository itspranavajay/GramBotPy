import typing
import asyncio
import functools
import inspect
import logging
import time
import traceback
from typing import Any, Callable, Dict, List, Optional, TypeVar, Union, Awaitable

if typing.TYPE_CHECKING:
    from ..client import GramBotPy

T = TypeVar('T')

class APIError(Exception):
    """Base class for API errors"""
    def __init__(self, description: str, error_code: int = None, parameters: Dict = None):
        self.description = description
        self.error_code = error_code
        self.parameters = parameters or {}
        super().__init__(f"[{error_code}] {description}")

class RateLimitError(APIError):
    """Raised when hitting rate limits"""
    def __init__(self, description: str, retry_after: float, error_code: int = 429):
        super().__init__(description, error_code)
        self.retry_after = retry_after

class NetworkError(Exception):
    """Base class for network-related errors"""
    pass

class ConnectionError(NetworkError):
    """Raised when connection to Telegram fails"""
    pass

class TimeoutError(NetworkError):
    """Raised when a request times out"""
    pass

class UtilityErrorHandler:
    """Utility methods for error handling and retries."""
    
    def safe_api_call(
        self: "GramBotPy",
        retries: int = 3,
        delay: float = 1.0,
        backoff: float = 2.0,
        exceptions: List[Exception] = None
    ) -> Callable:
        """Decorator for safely making API calls with retries.
        
        Parameters:
            retries (``int``, optional):
                Maximum number of retries. Defaults to 3.
                
            delay (``float``, optional):
                Initial delay between retries in seconds. Defaults to 1.0.
                
            backoff (``float``, optional):
                Backoff multiplier. Defaults to 2.0.
                
            exceptions (``list``, optional):
                List of exceptions to catch. Defaults to [NetworkError, RateLimitError].
                
        Returns:
            ``Callable``: Decorated function.
            
        Example:
            .. code-block:: python
            
                @bot.safe_api_call(retries=5, delay=2.0)
                async def my_api_method(chat_id, message):
                    # Method implementation
                    pass
        """
        exceptions = exceptions or [NetworkError, RateLimitError, ConnectionError]
        
        def decorator(func):
            @functools.wraps(func)
            async def wrapper(*args, **kwargs):
                attempt = 0
                current_delay = delay
                last_exception = None
                
                while attempt < retries:
                    try:
                        return await func(*args, **kwargs)
                    except RateLimitError as e:
                        last_exception = e
                        wait_time = e.retry_after if e.retry_after > 0 else current_delay
                        self.logger.warning(f"Rate limited. Waiting {wait_time} seconds before retry.")
                        await asyncio.sleep(wait_time)
                    except tuple(exceptions) as e:
                        last_exception = e
                        self.logger.warning(f"API call failed: {e}. Retrying in {current_delay} seconds...")
                        await asyncio.sleep(current_delay)
                        current_delay *= backoff
                    except Exception as e:
                        # For non-retryable exceptions, log and re-raise
                        self.logger.error(f"Unhandled error in API call: {e}", exc_info=True)
                        raise
                        
                    attempt += 1
                
                # If we've exhausted all retries
                if last_exception:
                    self.logger.error(f"Maximum retries ({retries}) exceeded. Last error: {last_exception}")
                    raise last_exception
                
            return wrapper
        return decorator
    
    async def with_error_handling(
        self: "GramBotPy",
        func: Callable[..., Awaitable[T]],
        *args,
        **kwargs
    ) -> Union[T, Dict[str, Any]]:
        """Execute a function with comprehensive error handling.
        
        Parameters:
            func (``Callable``):
                Async function to execute.
                
            *args, **kwargs:
                Arguments to pass to the function.
                
        Returns:
            Result of the function or error information.
            
        Example:
            .. code-block:: python
            
                result = await bot.with_error_handling(
                    bot.send_message, 
                    chat_id=chat_id, 
                    text="Hello"
                )
                
                if "error" in result:
                    # Handle error
                    pass
        """
        try:
            return await func(*args, **kwargs)
        except APIError as e:
            self.logger.error(f"API Error: {e.description} (Code: {e.error_code})")
            return {
                "error": "api_error",
                "description": e.description,
                "error_code": e.error_code,
                "parameters": e.parameters,
                "timestamp": time.time()
            }
        except NetworkError as e:
            self.logger.error(f"Network Error: {str(e)}")
            return {
                "error": "network_error",
                "description": str(e),
                "timestamp": time.time()
            }
        except Exception as e:
            self.logger.error(f"Unexpected Error: {str(e)}", exc_info=True)
            return {
                "error": "unexpected_error",
                "description": str(e),
                "traceback": traceback.format_exc(),
                "timestamp": time.time()
            }
    
    def log_errors(
        self: "GramBotPy",
        level: int = logging.ERROR
    ) -> Callable:
        """Decorator to log errors from a function.
        
        Parameters:
            level (``int``, optional):
                Logging level. Defaults to logging.ERROR.
                
        Returns:
            ``Callable``: Decorated function.
            
        Example:
            .. code-block:: python
            
                @bot.log_errors(level=logging.WARNING)
                async def risky_operation(chat_id):
                    # Implementation
                    pass
        """
        def decorator(func):
            @functools.wraps(func)
            async def wrapper(*args, **kwargs):
                try:
                    return await func(*args, **kwargs)
                except Exception as e:
                    self.logger.log(
                        level,
                        f"Error in {func.__name__}: {str(e)}",
                        exc_info=True
                    )
                    raise
            return wrapper
        return decorator
    
    def handle_telegram_errors(
        self: "GramBotPy"
    ) -> Callable:
        """Decorator to handle Telegram API errors.
        
        Returns:
            ``Callable``: Decorated function.
            
        Example:
            .. code-block:: python
            
                @bot.handle_telegram_errors()
                async def send_special_message(chat_id, text):
                    # Implementation
                    pass
        """
        def decorator(func):
            @functools.wraps(func)
            async def wrapper(*args, **kwargs):
                try:
                    return await func(*args, **kwargs)
                except Exception as e:
                    error_str = str(e).lower()
                    
                    # Handle different types of Telegram errors
                    if "bot was blocked by the user" in error_str:
                        self.logger.warning(f"User blocked the bot: {error_str}")
                        return {"error": "user_blocked_bot", "description": str(e)}
                    
                    elif "chat not found" in error_str:
                        self.logger.warning(f"Chat not found: {error_str}")
                        return {"error": "chat_not_found", "description": str(e)}
                    
                    elif "message to delete not found" in error_str:
                        self.logger.warning(f"Message not found: {error_str}")
                        return {"error": "message_not_found", "description": str(e)}
                    
                    elif "bot is not a member" in error_str:
                        self.logger.warning(f"Bot not in chat: {error_str}")
                        return {"error": "bot_not_in_chat", "description": str(e)}
                    
                    elif "have no rights to send" in error_str:
                        self.logger.warning(f"No permission to send: {error_str}")
                        return {"error": "no_send_permission", "description": str(e)}
                    
                    elif "too many requests" in error_str or "flood" in error_str:
                        self.logger.warning(f"Rate limited: {error_str}")
                        return {"error": "rate_limited", "description": str(e)}
                    
                    # If no specific error is caught, re-raise
                    raise
                    
            return wrapper
        return decorator 