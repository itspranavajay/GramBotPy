import asyncio
import logging
import typing
import aiohttp
import json

if typing.TYPE_CHECKING:
    from ...client import GramBotPy

class SetBusinessAccountName:
    """Method for changing business account name."""
    
    async def set_business_account_name(
        self: "GramBotPy",
        business_connection_id: str,
        first_name: str,
        last_name: str = None
    ) -> bool:
        """Change the first and last name of a managed business account.
        
        Parameters:
            business_connection_id (``str``):
                Unique identifier of the business connection on behalf of which the name will be changed.
                
            first_name (``str``):
                New first name for the business account; 1-64 characters.
                
            last_name (``str``, optional):
                New last name for the business account; 0-64 characters.
                
        Returns:
            ``bool``: True on success.
            
        Example:
            .. code-block:: python
            
                # Set the business account name
                await bot.set_business_account_name(
                    business_connection_id, 
                    "Coffee Shop", 
                    "Downtown"
                )
        """
        self.logger.info(f"Setting business account name: {first_name} {last_name}")
        
        # Create the params dictionary with required parameters
        params = {
            "business_connection_id": business_connection_id,
            "first_name": first_name
        }
        
        # Add optional parameters if they are provided
        if last_name is not None:
            params["last_name"] = last_name
        
        # Make the API request to change the business account name
        async with aiohttp.ClientSession() as session:
            try:
                url = f"https://api.telegram.org/bot{self.token}/setBusinessAccountName"
                async with session.post(url, data=params) as response:
                    result = await response.json()
                    
                    if not result.get("ok", False):
                        error_description = result.get('description', 'Unknown error')
                        self.logger.error(f"Error setting business account name: {error_description}")
                        
                        # More detailed error logging
                        self.logger.debug(f"Params used: {params}")
                        return False
                    
                    return True
                    
            except aiohttp.ClientError as e:
                self.logger.error(f"Network error making request to Telegram API: {e}", exc_info=True)
                return False
            except Exception as e:
                self.logger.error(f"Error making request to Telegram API: {e}", exc_info=True)
                return False 