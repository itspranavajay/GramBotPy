import asyncio
import logging
import typing

from .collection import Collection

if typing.TYPE_CHECKING:
    from ...client import GramBotPy

class Database:
    """MongoDB-like database interface using Telegram channels.
    
    Attributes:
        client (:obj:`GramBotPy`):
            The GramBotPy client.
            
        name (``str``):
            The name of the database.
            
        collections (``dict``):
            Dictionary of collections in the database.
    """
    
    def __init__(self, client: "GramBotPy", name: str = "default"):
        self.client = client
        self.name = name
        self.collections = {}
        self.logger = logging.getLogger(f"GramBotPy.Database.{self.name}")
    
    def collection(self, name: str, channel_id: typing.Union[int, str] = None) -> Collection:
        """Get or create a collection.
        
        Parameters:
            name (``str``):
                The name of the collection.
                
            channel_id (``int`` | ``str``, optional):
                The ID or username of the channel to use as the collection.
                If not provided, a channel ID must have been previously specified for this collection.
                
        Returns:
            :obj:`Collection`: The collection.
            
        Raises:
            ValueError: If channel_id is not provided and the collection doesn't exist.
        """
        # Check if the collection already exists
        if name in self.collections:
            # Update channel_id if provided
            if channel_id is not None:
                self.collections[name] = Collection(self.client, channel_id, name)
            return self.collections[name]
        
        # Create a new collection
        if channel_id is None:
            raise ValueError(f"Channel ID must be provided for new collection '{name}'")
            
        collection = Collection(self.client, channel_id, name)
        self.collections[name] = collection
        
        return collection
    
    async def list_collections(self) -> typing.List[str]:
        """List all collections in the database.
        
        Returns:
            List of ``str``: Names of the collections.
        """
        return list(self.collections.keys())
    
    async def drop_collection(self, name: str) -> bool:
        """Drop a collection.
        
        Note: This doesn't actually delete the channel, it just removes it from the database.
        
        Parameters:
            name (``str``):
                The name of the collection to drop.
                
        Returns:
            ``bool``: True if the collection was dropped, False otherwise.
        """
        if name in self.collections:
            del self.collections[name]
            return True
        return False 