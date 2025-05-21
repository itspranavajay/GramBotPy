from dataclasses import dataclass
from typing import Optional, Dict, Any

@dataclass
class ReplyKeyboardRemove:
    """This object represents a request to remove the custom keyboard.
    
    Parameters:
        remove_keyboard (``bool``):
            Requests clients to remove the custom keyboard.
            Always True.
            
        selective (``bool``, optional):
            Use this parameter if you want to remove the keyboard for specific users only.
    """
    
    remove_keyboard: bool = True
    selective: Optional[bool] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert the object to a dict suitable for JSON serialization."""
        result = {"remove_keyboard": True}
        
        if self.selective is not None:
            result["selective"] = self.selective
            
        return result 