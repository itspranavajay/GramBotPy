from dataclasses import dataclass
from typing import Optional, Dict, Any

@dataclass
class ForceReply:
    """This object represents a request to force a reply from the user.
    
    Parameters:
        force_reply (``bool``):
            Shows reply interface to the user, as if they manually 
            selected the bot's message and tapped 'Reply'.
            Always True.
            
        input_field_placeholder (``str``, optional):
            The placeholder to be shown in the input field when the reply is active.
            
        selective (``bool``, optional):
            Use this parameter if you want to force reply from specific users only.
    """
    
    force_reply: bool = True
    input_field_placeholder: Optional[str] = None
    selective: Optional[bool] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert the object to a dict suitable for JSON serialization."""
        result = {"force_reply": True}
        
        if self.input_field_placeholder is not None:
            result["input_field_placeholder"] = self.input_field_placeholder
        if self.selective is not None:
            result["selective"] = self.selective
            
        return result 