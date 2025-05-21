import asyncio
import logging
import typing
import aiohttp
import json

from ...types import SentWebAppMessage

if typing.TYPE_CHECKING:
    from ...client import GramBotPy

class AnswerWebAppQuery:
    """Method for answering web app queries."""
    
    async def answer_web_app_query(
        self: "GramBotPy",
        web_app_query_id: str,
        result: dict
    ) -> SentWebAppMessage:
        """Sets the result of interaction with a Web App and sends a corresponding message on behalf of the user to the chat from which the query originated.
        
        Parameters:
            web_app_query_id (``str``):
                Unique identifier for the query to be answered.
                
            result (``dict``):
                A JSON-serialized object describing the message to be sent.
                
        Returns:
            :obj:`SentWebAppMessage`: On success, a SentWebAppMessage object is returned.
            
        Example:
            .. code-block:: python
            
                # Answer with a text message
                result = {
                    "type": "article",
                    "id": "unique_id",
                    "title": "Result Title",
                    "input_message_content": {
                        "message_text": "Message from the web app",
                        "parse_mode": "HTML"
                    }
                }
                await bot.answer_web_app_query(web_app_query_id="query123", result=result)
        """
        self.logger.info(f"Answering web app query: {web_app_query_id}")
        
        # Create the params dictionary with required parameters
        params = {
            "web_app_query_id": web_app_query_id,
            "result": json.dumps(result)
        }
        
        # Make the API request to answer the web app query
        async with aiohttp.ClientSession() as session:
            try:
                url = f"https://api.telegram.org/bot{self.token}/answerWebAppQuery"
                async with session.post(url, data=params) as response:
                    result_json = await response.json()
                    
                    if not result_json.get("ok", False):
                        error_description = result_json.get('description', 'Unknown error')
                        self.logger.error(f"Error answering web app query: {error_description}")
                        
                        # More detailed error logging
                        self.logger.debug(f"Params used: {params}")
                        return None
                    
                    # Parse the response and create a SentWebAppMessage object
                    message_data = result_json.get("result", {})
                    return SentWebAppMessage._parse(self, message_data)
                    
            except aiohttp.ClientError as e:
                self.logger.error(f"Network error making request to Telegram API: {e}", exc_info=True)
                return None
            except Exception as e:
                self.logger.error(f"Error making request to Telegram API: {e}", exc_info=True)
                return None 