import typing
import aiohttp
from typing import Optional

if typing.TYPE_CHECKING:
    from ...client import GramBotPy

class AnswerCallbackQuery:
    """Method to answer callback queries."""
    
    async def answer_callback_query(
        self: "GramBotPy",
        callback_query_id: str,
        text: Optional[str] = None,
        show_alert: Optional[bool] = None,
        url: Optional[str] = None,
        cache_time: Optional[int] = None
    ) -> bool:
        """Answer a callback query from an inline keyboard button.
        
        Parameters:
            callback_query_id (``str``):
                Unique identifier for the query to be answered.
                
            text (``str``, optional):
                Text of the notification. If not specified, nothing will be shown to the user.
                
            show_alert (``bool``, optional):
                If True, an alert will be shown instead of a notification at the top of the chat screen.
                
            url (``str``, optional):
                URL that will be opened by the user's client.
                
            cache_time (``int``, optional):
                The maximum amount of time in seconds that the result of the callback query
                may be cached client-side.
                
        Returns:
            ``bool``: True on success.
        """
        self.logger.info(f"Answering callback query {callback_query_id}: {text}")
        
        # Create params dictionary with required parameter
        params = {
            "callback_query_id": callback_query_id
        }
        
        # Add optional parameters if provided
        if text is not None:
            params["text"] = text
            
        if show_alert is not None:
            params["show_alert"] = show_alert
            
        if url is not None:
            params["url"] = url
            
        if cache_time is not None:
            params["cache_time"] = cache_time
        
        # Make the API request
        return await self._make_callback_query_request(params)
    
    async def _make_callback_query_request(self, params: dict) -> bool:
        """Make the actual API request for answering callback queries.
        
        Parameters:
            params (``dict``):
                Parameters to send in the request.
                
        Returns:
            ``bool``: True on success.
        """
        async with aiohttp.ClientSession() as session:
            try:
                url = f"https://api.telegram.org/bot{self.token}/answerCallbackQuery"
                
                # Following Telethon's pattern for proper HTTP handling
                async with session.post(url, data=params) as response:
                    # Check HTTP status first
                    if response.status != 200:
                        self.logger.error(f"HTTP error {response.status} when answering callback query: {await response.text()}")
                        return False
                    
                    # Parse the JSON response
                    result = await response.json()
                    
                    if not result.get("ok", False):
                        error_description = result.get('description', 'Unknown error')
                        self.logger.error(f"Error answering callback query: {error_description}")
                        self.logger.debug(f"Params used: {params}")
                        return False
                        
                    return True
                    
            except aiohttp.ClientError as e:
                self.logger.error(f"Network error making request to Telegram API: {e}", exc_info=True)
                return False
            except Exception as e:
                self.logger.error(f"Error making request to Telegram API: {e}", exc_info=True)
                return False 