from dataclasses import dataclass
import typing

@dataclass
class WebAppInfo:
    """Contains information about a Web App.
    
    Attributes:
        url (``str``):
            An HTTPS URL of a Web App to be opened with additional data as specified in 
            Initializing Web Apps
    """
    
    url: str
    
    @classmethod
    def _parse(cls, client, app_data: dict):
        """Parse a WebAppInfo object from the Telegram API response."""
        if not app_data:
            return None
            
        return cls(
            url=app_data.get("url")
        )
    
    def to_dict(self):
        """Convert the WebAppInfo object to a dictionary."""
        return {
            "url": self.url
        }


@dataclass
class WebAppData:
    """Contains data sent from a Web App to the bot.
    
    Attributes:
        data (``str``):
            The data. Be aware that a bad client can send arbitrary data in this field.
            
        button_text (``str``):
            Text of the web_app keyboard button from which the Web App was opened. 
            Be aware that a bad client can send arbitrary data in this field.
    """
    
    data: str
    button_text: str
    
    @classmethod
    def _parse(cls, client, app_data: dict):
        """Parse a WebAppData object from the Telegram API response."""
        if not app_data:
            return None
            
        return cls(
            data=app_data.get("data"),
            button_text=app_data.get("button_text")
        )
    
    def to_dict(self):
        """Convert the WebAppData object to a dictionary."""
        return {
            "data": self.data,
            "button_text": self.button_text
        }


@dataclass
class SentWebAppMessage:
    """Contains information about an inline message sent by a Web App on behalf of a user.
    
    Attributes:
        inline_message_id (``str``, optional):
            Identifier of the sent inline message. Available only if there is an inline keyboard 
            attached to the message.
    """
    
    inline_message_id: str = None
    
    @classmethod
    def _parse(cls, client, message_data: dict):
        """Parse a SentWebAppMessage object from the Telegram API response."""
        if not message_data:
            return None
            
        return cls(
            inline_message_id=message_data.get("inline_message_id")
        )
    
    def to_dict(self):
        """Convert the SentWebAppMessage object to a dictionary."""
        result = {}
        
        if self.inline_message_id:
            result["inline_message_id"] = self.inline_message_id
            
        return result 