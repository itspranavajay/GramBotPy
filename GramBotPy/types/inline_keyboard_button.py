from dataclasses import dataclass
from typing import Optional, Union, Dict, Any

@dataclass
class InlineKeyboardButton:
    """This object represents one button of an inline keyboard.
    
    Parameters:
        text (``str``):
            Label text on the button.
            
        url (``str``, optional):
            HTTP or tg:// url to be opened when the button is pressed.
            
        callback_data (``str``, optional):
            Data to be sent in a callback query when the button is pressed.
            
        web_app (``dict``, optional):
            Description of the Web App that will be launched when the button is pressed.
            
        login_url (``dict``, optional):
            An HTTPS URL used to automatically authorize the user.
            
        switch_inline_query (``str``, optional):
            Switch to inline mode with the specified query.
            
        switch_inline_query_current_chat (``str``, optional):
            Switch to inline mode in the current chat with the specified query.
            
        callback_game (``dict``, optional):
            Description of the game that will be launched when the button is pressed.
            
        pay (``bool``, optional):
            Specify True to send a Pay button.
    """
    
    text: str
    url: Optional[str] = None
    callback_data: Optional[str] = None
    web_app: Optional[Dict[str, Any]] = None
    login_url: Optional[Dict[str, Any]] = None
    switch_inline_query: Optional[str] = None
    switch_inline_query_current_chat: Optional[str] = None
    callback_game: Optional[Dict[str, Any]] = None
    pay: Optional[bool] = None
    
    def __post_init__(self):
        # Validate that at least one of the optional parameters is set
        if not any([
            self.url, 
            self.callback_data, 
            self.web_app, 
            self.login_url, 
            self.switch_inline_query is not None, 
            self.switch_inline_query_current_chat is not None, 
            self.callback_game, 
            self.pay
        ]):
            raise ValueError(
                "One and only one of url, callback_data, web_app, login_url, "
                "switch_inline_query, switch_inline_query_current_chat, "
                "callback_game, or pay must be specified"
            )
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert the object to a dict suitable for JSON serialization."""
        result = {"text": self.text}
        
        if self.url:
            result["url"] = self.url
        if self.callback_data:
            result["callback_data"] = self.callback_data
        if self.web_app:
            result["web_app"] = self.web_app
        if self.login_url:
            result["login_url"] = self.login_url
        if self.switch_inline_query is not None:
            result["switch_inline_query"] = self.switch_inline_query
        if self.switch_inline_query_current_chat is not None:
            result["switch_inline_query_current_chat"] = self.switch_inline_query_current_chat
        if self.callback_game:
            result["callback_game"] = self.callback_game
        if self.pay:
            result["pay"] = self.pay
            
        return result 