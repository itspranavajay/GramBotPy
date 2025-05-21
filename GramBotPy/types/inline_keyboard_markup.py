from dataclasses import dataclass, field
from typing import List, Dict, Any, Union, Optional
from .inline_keyboard_button import InlineKeyboardButton

@dataclass
class InlineKeyboardMarkup:
    """This object represents an inline keyboard attached to a message.
    
    Parameters:
        inline_keyboard (``list``):
            Array of button rows, each represented by an array of InlineKeyboardButton objects.
    """
    
    inline_keyboard: List[List[Union[InlineKeyboardButton, Dict[str, Any]]]] = field(default_factory=list)
    
    def __post_init__(self):
        # Convert dict buttons to InlineKeyboardButton objects
        for i, row in enumerate(self.inline_keyboard):
            for j, button in enumerate(row):
                if isinstance(button, dict):
                    self.inline_keyboard[i][j] = InlineKeyboardButton(**button)
    
    @classmethod
    def from_button(cls, button: Union[InlineKeyboardButton, Dict[str, Any]]) -> "InlineKeyboardMarkup":
        """Create an inline keyboard with a single button.
        
        Parameters:
            button (:obj:`InlineKeyboardButton` | ``dict``):
                The button to include in the keyboard.
                
        Returns:
            :obj:`InlineKeyboardMarkup`: The inline keyboard.
        """
        if isinstance(button, dict):
            button = InlineKeyboardButton(**button)
        return cls(inline_keyboard=[[button]])
    
    @classmethod
    def from_row(cls, row: List[Union[InlineKeyboardButton, Dict[str, Any]]]) -> "InlineKeyboardMarkup":
        """Create an inline keyboard with a single row of buttons.
        
        Parameters:
            row (``list``):
                The row of buttons to include in the keyboard.
                
        Returns:
            :obj:`InlineKeyboardMarkup`: The inline keyboard.
        """
        return cls(inline_keyboard=[row])
    
    def row(self, *buttons: Union[InlineKeyboardButton, Dict[str, Any]]) -> "InlineKeyboardMarkup":
        """Add a row of buttons to the keyboard.
        
        Parameters:
            buttons (:obj:`InlineKeyboardButton` | ``dict``):
                The buttons to add to the row.
                
        Returns:
            :obj:`InlineKeyboardMarkup`: The inline keyboard with the new row.
        """
        button_row = []
        for button in buttons:
            if isinstance(button, dict):
                button = InlineKeyboardButton(**button)
            button_row.append(button)
        self.inline_keyboard.append(button_row)
        return self
    
    def add(self, *buttons: Union[InlineKeyboardButton, Dict[str, Any]]) -> "InlineKeyboardMarkup":
        """Add buttons to the keyboard as separate rows.
        
        Parameters:
            buttons (:obj:`InlineKeyboardButton` | ``dict``):
                The buttons to add as separate rows.
                
        Returns:
            :obj:`InlineKeyboardMarkup`: The inline keyboard with the new rows.
        """
        for button in buttons:
            if isinstance(button, dict):
                button = InlineKeyboardButton(**button)
            self.inline_keyboard.append([button])
        return self
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert the object to a dict suitable for JSON serialization."""
        return {
            "inline_keyboard": [
                [button.to_dict() for button in row]
                for row in self.inline_keyboard
            ]
        } 