import json
import logging
import os
import typing
from pathlib import Path

class Session:
    """Session handler for the GramBotPy framework.
    
    This class handles the storage and retrieval of session data for
    connecting to Telegram.
    
    Parameters:
        name (``str``):
            The name of the session.
    """
    
    SESSION_DATA_KEYS = [
        "dc_id",
        "auth_key",
        "user_id",
        "is_bot"
    ]
    
    def __init__(self, name: str):
        self.name = name
        self.logger = logging.getLogger(__name__)
        
        # Session data
        self._dc_id = None
        self._auth_key = None
        self._user_id = None
        self._is_bot = True  # Always True for GramBotPy
        
        # Load session if it exists
        self._load()
        
    def _load(self):
        """Load the session from disk."""
        session_file = self._get_session_file()
        
        if not session_file.exists():
            return
            
        try:
            with open(session_file, 'r') as f:
                data = json.load(f)
                
            for key in self.SESSION_DATA_KEYS:
                if key in data:
                    setattr(self, f"_{key}", data[key])
                    
            self.logger.info(f"Session loaded: {self.name}")
        except Exception as e:
            self.logger.error(f"Failed to load session: {e}")
            
    def save(self):
        """Save the session to disk."""
        session_file = self._get_session_file()
        
        # Create directory if it doesn't exist
        session_file.parent.mkdir(parents=True, exist_ok=True)
        
        data = {}
        for key in self.SESSION_DATA_KEYS:
            value = getattr(self, f"_{key}")
            if value is not None:
                data[key] = value
                
        try:
            with open(session_file, 'w') as f:
                json.dump(data, f)
                
            self.logger.info(f"Session saved: {self.name}")
        except Exception as e:
            self.logger.error(f"Failed to save session: {e}")
            
    def delete(self):
        """Delete the session from disk."""
        session_file = self._get_session_file()
        
        if session_file.exists():
            try:
                os.remove(session_file)
                self.logger.info(f"Session deleted: {self.name}")
            except Exception as e:
                self.logger.error(f"Failed to delete session: {e}")
                
    def _get_session_file(self) -> Path:
        """Get the session file path.
        
        Returns:
            Path: The session file path.
        """
        home = Path.home()
        directory = home / ".GramBotPy" / "sessions"
        return directory / f"{self.name}.json"
        
    @property
    def dc_id(self) -> int:
        """Get the DC ID for this session.
        
        Returns:
            int: The DC ID.
        """
        return self._dc_id
        
    @dc_id.setter
    def dc_id(self, value: int):
        """Set the DC ID for this session.
        
        Parameters:
            value (``int``):
                The DC ID to set.
        """
        self._dc_id = value
        self.save()
        
    @property
    def auth_key(self) -> bytes:
        """Get the auth key for this session.
        
        Returns:
            bytes: The auth key.
        """
        return self._auth_key
        
    @auth_key.setter
    def auth_key(self, value: bytes):
        """Set the auth key for this session.
        
        Parameters:
            value (``bytes``):
                The auth key to set.
        """
        self._auth_key = value
        self.save()
        
    @property
    def user_id(self) -> int:
        """Get the user ID for this session.
        
        Returns:
            int: The user ID.
        """
        return self._user_id
        
    @user_id.setter
    def user_id(self, value: int):
        """Set the user ID for this session.
        
        Parameters:
            value (``int``):
                The user ID to set.
        """
        self._user_id = value
        self.save()
        
    @property
    def is_bot(self) -> bool:
        """Check if this session is for a bot.
        
        Returns:
            bool: True if this session is for a bot, else False.
        """
        return self._is_bot
        
    def set_bot(self, value: bool = True):
        """Set whether this session is for a bot.
        
        Parameters:
            value (``bool``):
                True if this session is for a bot, else False.
        """
        self._is_bot = value
        self.save() 