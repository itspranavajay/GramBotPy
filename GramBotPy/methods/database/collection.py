import asyncio
import logging
import typing
import aiohttp
import json
from datetime import datetime

from ...types import Document, QueryFilter

if typing.TYPE_CHECKING:
    from ...client import GramBotPy

class Collection:
    """Represents a collection in the Telegram database (a channel).
    
    Attributes:
        client (:obj:`GramBotPy`):
            The GramBotPy client.
            
        channel_id (``int`` | ``str``):
            The ID or username of the channel serving as the collection.
            
        name (``str``):
            The name of the collection.
    """
    
    def __init__(self, client: "GramBotPy", channel_id: typing.Union[int, str], name: str = None):
        self.client = client
        self.channel_id = channel_id
        self.name = name or str(channel_id)
        self.logger = logging.getLogger(f"GramBotPy.Collection.{self.name}")
    
    async def insert_one(self, data: dict) -> Document:
        """Insert a document into the collection.
        
        Parameters:
            data (``dict``):
                The data to insert.
                
        Returns:
            :obj:`Document`: The inserted document.
        """
        self.logger.info(f"Inserting document into {self.name}")
        
        # Convert data to JSON
        json_data = json.dumps(data, ensure_ascii=False)
        
        # Send a message to the channel with the JSON data
        message = await self.client.send_message(
            chat_id=self.channel_id,
            text=json_data
        )
        
        if not message:
            self.logger.error("Failed to insert document")
            return None
            
        # Create a Document object
        return Document(
            _id=message.message_id,
            data=data,
            created_at=datetime.now()
        )
    
    async def find_one(self, filter_query: dict = None) -> Document:
        """Find a document in the collection.
        
        Parameters:
            filter_query (``dict``, optional):
                The filter criteria. If not provided, returns the most recent document.
                
        Returns:
            :obj:`Document`: The found document or None.
        """
        self.logger.info(f"Finding document in {self.name}")
        
        # If no filter, get the most recent message
        if not filter_query:
            messages = await self.client.get_channel_messages(
                chat_id=self.channel_id,
                limit=1
            )
            if not messages or len(messages) == 0:
                return None
                
            return Document._parse(self.client, messages[0])
        
        # If there's a filter, we need to search through messages
        query_filter = QueryFilter(filter_query)
        
        # Start with a reasonable limit
        limit = 100
        messages = await self.client.get_channel_messages(
            chat_id=self.channel_id,
            limit=limit
        )
        
        if not messages:
            return None
        
        # Check each message against the filter
        for message in messages:
            document = Document._parse(self.client, message)
            if document and query_filter.match(document):
                return document
                
        # Not found with initial limit
        return None
    
    async def find(self, filter_query: dict = None, limit: int = 50) -> typing.List[Document]:
        """Find documents in the collection.
        
        Parameters:
            filter_query (``dict``, optional):
                The filter criteria. If not provided, returns all documents up to the limit.
                
            limit (``int``, optional):
                Maximum number of documents to return. Defaults to 50.
                
        Returns:
            List of :obj:`Document`: The found documents.
        """
        self.logger.info(f"Finding documents in {self.name}")
        
        # Get messages from the channel
        messages = await self.client.get_channel_messages(
            chat_id=self.channel_id,
            limit=limit
        )
        
        if not messages:
            return []
        
        # Convert messages to documents
        documents = []
        query_filter = QueryFilter(filter_query) if filter_query else None
        
        for message in messages:
            document = Document._parse(self.client, message)
            if document:
                # Apply filter if provided
                if not query_filter or query_filter.match(document):
                    documents.append(document)
                    
                # Stop if we reached the limit
                if len(documents) >= limit:
                    break
                    
        return documents
    
    async def update_one(self, filter_query: dict, update: dict) -> bool:
        """Update a document in the collection.
        
        Parameters:
            filter_query (``dict``):
                The filter criteria to find the document to update.
                
            update (``dict``):
                The updates to apply to the document.
                
        Returns:
            ``bool``: True if the update was successful, False otherwise.
        """
        self.logger.info(f"Updating document in {self.name}")
        
        # Find the document to update
        document = await self.find_one(filter_query)
        if not document:
            self.logger.warning("Document not found for update")
            return False
        
        # Apply the updates to the document's data
        for key, value in update.items():
            # Support dot notation for nested fields
            if "." in key:
                parts = key.split(".")
                current = document.data
                for part in parts[:-1]:
                    if part not in current:
                        current[part] = {}
                    current = current[part]
                current[parts[-1]] = value
            else:
                document.data[key] = value
        
        # Convert updated data to JSON
        json_data = document.to_json()
        
        # Edit the message
        success = await self.client.edit_message_text(
            chat_id=self.channel_id,
            message_id=document._id,
            text=json_data
        )
        
        return success
    
    async def delete_one(self, filter_query: dict) -> bool:
        """Delete a document from the collection.
        
        Parameters:
            filter_query (``dict``):
                The filter criteria to find the document to delete.
                
        Returns:
            ``bool``: True if the deletion was successful, False otherwise.
        """
        self.logger.info(f"Deleting document from {self.name}")
        
        # Find the document to delete
        document = await self.find_one(filter_query)
        if not document:
            self.logger.warning("Document not found for deletion")
            return False
        
        # Delete the message
        success = await self.client.delete_messages(
            chat_id=self.channel_id,
            message_ids=[document._id]
        )
        
        return success
    
    async def delete_many(self, filter_query: dict) -> int:
        """Delete multiple documents from the collection.
        
        Parameters:
            filter_query (``dict``):
                The filter criteria to find the documents to delete.
                
        Returns:
            ``int``: Number of documents deleted.
        """
        self.logger.info(f"Deleting multiple documents from {self.name}")
        
        # Find the documents to delete
        documents = await self.find(filter_query, limit=100)
        if not documents:
            self.logger.warning("No documents found for deletion")
            return 0
        
        # Get message IDs
        message_ids = [doc._id for doc in documents]
        
        # Delete the messages
        success = await self.client.delete_messages(
            chat_id=self.channel_id,
            message_ids=message_ids
        )
        
        return len(message_ids) if success else 0
    
    async def count_documents(self, filter_query: dict = None) -> int:
        """Count documents in the collection.
        
        Parameters:
            filter_query (``dict``, optional):
                The filter criteria. If not provided, counts all documents.
                
        Returns:
            ``int``: Number of documents matching the filter.
        """
        self.logger.info(f"Counting documents in {self.name}")
        
        # If there's a filter, we need to actually load and check each document
        if filter_query:
            # We'll try with a high limit to get an accurate count
            documents = await self.find(filter_query, limit=1000)
            return len(documents)
        else:
            # If no filter, we can just get the total count of messages
            # This is an approximation as it might include non-document messages
            chat = await self.client.get_chat(chat_id=self.channel_id)
            if not chat:
                return 0
                
            return getattr(chat, 'message_count', 0) 