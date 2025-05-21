from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional

@dataclass
class ReplyKeyboardMarkup:
    """This object represents a custom keyboard with reply options.
    
    Parameters:
        keyboard (``list``):
            Array of button rows, each represented by an array of strings.
            
        resize_keyboard (``bool``, optional):
            Requests clients to resize the keyboard vertically for optimal fit.
            
        one_time_keyboard (``bool``, optional):
            Requests clients to hide the keyboard as soon as it's been used.
            
        input_field_placeholder (``str``, optional):
            The placeholder to be shown in the input field when the keyboard is active.
            
        selective (``bool``, optional):
            Use this parameter if you want to show the keyboard to specific users only.
    """
    
    keyboard: List[List[str]] = field(default_factory=list)
    resize_keyboard: Optional[bool] = None
    one_time_keyboard: Optional[bool] = None
    input_field_placeholder: Optional[str] = None
    selective: Optional[bool] = None
    
    def add(self, *buttons: str) -> "ReplyKeyboardMarkup":
        """Add a row of buttons to the keyboard.
        
        Parameters:
            buttons (``str``):
                The buttons to add to the row.
                
        Returns:
            :obj:`ReplyKeyboardMarkup`: The reply keyboard with the new row.
        """
        self.keyboard.append(list(buttons))
        return self
    
    def row(self, *buttons: str) -> "ReplyKeyboardMarkup":
        """Add a row of buttons to the keyboard.
        
        Parameters:
            buttons (``str``):
                The buttons to add to the row.
                
        Returns:
            :obj:`ReplyKeyboardMarkup`: The reply keyboard with the new row.
        """
        return self.add(*buttons)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert the object to a dict suitable for JSON serialization."""
        result = {"keyboard": self.keyboard}
        
        if self.resize_keyboard is not None:
            result["resize_keyboard"] = self.resize_keyboard
        if self.one_time_keyboard is not None:
            result["one_time_keyboard"] = self.one_time_keyboard
        if self.input_field_placeholder is not None:
            result["input_field_placeholder"] = self.input_field_placeholder
        if self.selective is not None:
            result["selective"] = self.selective
            
        return result 