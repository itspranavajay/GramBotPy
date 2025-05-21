from .collection import Collection
from .database import Database

class DatabaseMethodsMixin:
    """Database methods.
    
    This mixin includes methods for interacting with the Telegram database.
    """
    
    def get_database(self, name: str = "default") -> Database:
        """Get a database.
        
        Parameters:
            name (``str``, optional):
                The name of the database. Defaults to "default".
                
        Returns:
            :obj:`Database`: The database object.
        """
        return Database(self, name) 