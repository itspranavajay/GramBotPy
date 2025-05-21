from dataclasses import dataclass
import typing
import json
from datetime import datetime

@dataclass
class Document:
    """Represents a document stored in a Telegram database.
    
    Attributes:
        _id (``int``):
            Unique identifier of the document (message_id).
            
        data (``dict``):
            The actual data stored in the document.
            
        created_at (``datetime``):
            When the document was created.
            
        updated_at (``datetime``):
            When the document was last updated.
    """
    
    _id: int
    data: dict
    created_at: datetime
    updated_at: datetime = None
    
    @classmethod
    def _parse(cls, client, message_data: dict):
        """Parse a Document object from a Telegram message."""
        if not message_data:
            return None
            
        message_id = message_data.get("message_id")
        text = message_data.get("text", "{}")
        
        # Try to parse the text as JSON
        try:
            data = json.loads(text)
        except json.JSONDecodeError:
            # If not valid JSON, use the text as a single field
            data = {"text": text}
        
        # Get the date from the message
        date = message_data.get("date")
        if date:
            created_at = datetime.fromtimestamp(date)
        else:
            created_at = datetime.now()
        
        # Get the edit date if available
        edit_date = message_data.get("edit_date")
        updated_at = datetime.fromtimestamp(edit_date) if edit_date else None
        
        return cls(
            _id=message_id,
            data=data,
            created_at=created_at,
            updated_at=updated_at
        )
    
    def to_dict(self):
        """Convert the Document object to a dictionary."""
        return {
            "_id": self._id,
            "data": self.data,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None
        }
    
    def to_json(self):
        """Convert the data of the document to a JSON string."""
        return json.dumps(self.data, ensure_ascii=False)


@dataclass
class QueryFilter:
    """Represents a query filter for database operations.
    
    Attributes:
        filter_dict (``dict``):
            Dictionary containing the filter conditions.
    """
    
    filter_dict: dict
    
    def match(self, document: Document) -> bool:
        """Check if a document matches the filter.
        
        Parameters:
            document (:obj:`Document`):
                The document to check.
                
        Returns:
            ``bool``: True if the document matches the filter, False otherwise.
        """
        for key, value in self.filter_dict.items():
            # Handle nested keys with dot notation
            if "." in key:
                parts = key.split(".")
                current = document.data
                for part in parts[:-1]:
                    if part not in current:
                        return False
                    current = current[part]
                    
                if parts[-1] not in current or current[parts[-1]] != value:
                    return False
            else:
                # Handle top-level keys
                if key not in document.data or document.data[key] != value:
                    return False
                    
        return True 