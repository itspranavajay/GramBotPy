import typing
from dataclasses import dataclass

@dataclass
class UniqueGiftSymbol:
    """This object represents a symbol for a unique gift.
    
    Attributes:
        symbol (``str``):
            Emoji symbol.
            
        position (``list``):
            Position of the symbol inside the gift [x, y].
            
        rotation (``float``):
            Rotation angle of the symbol in degrees.
    """
    
    symbol: str
    position: typing.List[float]
    rotation: float
    
    @classmethod
    def _parse(cls, client, symbol_data: dict):
        """Parse a UniqueGiftSymbol object from the Telegram API response."""
        if not symbol_data:
            return None
            
        return cls(
            symbol=symbol_data.get("symbol"),
            position=symbol_data.get("position"),
            rotation=symbol_data.get("rotation")
        )
        
    def to_dict(self):
        """Convert the UniqueGiftSymbol object to a dictionary."""
        return {
            "symbol": self.symbol,
            "position": self.position,
            "rotation": self.rotation
        }

@dataclass
class UniqueGiftBackdropColors:
    """This object represents backdrop colors for a unique gift.
    
    Attributes:
        top_color (``str``):
            Top color in HEX.
            
        bottom_color (``str``):
            Bottom color in HEX.
    """
    
    top_color: str
    bottom_color: str
    
    @classmethod
    def _parse(cls, client, colors_data: dict):
        """Parse a UniqueGiftBackdropColors object from the Telegram API response."""
        if not colors_data:
            return None
            
        return cls(
            top_color=colors_data.get("top_color"),
            bottom_color=colors_data.get("bottom_color")
        )
        
    def to_dict(self):
        """Convert the UniqueGiftBackdropColors object to a dictionary."""
        return {
            "top_color": self.top_color,
            "bottom_color": self.bottom_color
        }

@dataclass
class UniqueGiftBackdrop:
    """This object represents a backdrop for a unique gift.
    
    Attributes:
        type (``str``):
            Type of the backdrop.
            
        colors (``UniqueGiftBackdropColors``, optional):
            Backdrop colors.
    """
    
    type: str
    colors: UniqueGiftBackdropColors = None
    
    @classmethod
    def _parse(cls, client, backdrop_data: dict):
        """Parse a UniqueGiftBackdrop object from the Telegram API response."""
        if not backdrop_data:
            return None
            
        colors = None
        if backdrop_data.get("colors"):
            colors = UniqueGiftBackdropColors._parse(client, backdrop_data.get("colors"))
            
        return cls(
            type=backdrop_data.get("type"),
            colors=colors
        )
        
    def to_dict(self):
        """Convert the UniqueGiftBackdrop object to a dictionary."""
        result = {
            "type": self.type
        }
        
        if self.colors:
            result["colors"] = self.colors.to_dict()
            
        return result

@dataclass
class UniqueGiftModel:
    """This object represents a model for a unique gift.
    
    Attributes:
        symbols (``list``):
            List of symbols inside the gift.
            
        backdrop (``UniqueGiftBackdrop``):
            Backdrop of the gift.
    """
    
    symbols: typing.List[UniqueGiftSymbol]
    backdrop: UniqueGiftBackdrop
    
    @classmethod
    def _parse(cls, client, model_data: dict):
        """Parse a UniqueGiftModel object from the Telegram API response."""
        if not model_data:
            return None
            
        symbols = [UniqueGiftSymbol._parse(client, symbol) for symbol in model_data.get("symbols", [])]
        backdrop = UniqueGiftBackdrop._parse(client, model_data.get("backdrop"))
            
        return cls(
            symbols=symbols,
            backdrop=backdrop
        )
        
    def to_dict(self):
        """Convert the UniqueGiftModel object to a dictionary."""
        return {
            "symbols": [symbol.to_dict() for symbol in self.symbols],
            "backdrop": self.backdrop.to_dict()
        }

@dataclass
class UniqueGiftInfo:
    """This object represents information about a unique gift.
    
    Attributes:
        telegram_payment_charge_id (``str``):
            Unique identifier of the successful payment in Telegram.
            
        provider_payment_charge_id (``str``):
            Unique identifier of the successful payment in the provider system.
            
        gift_star_count (``int``):
            Number of stars that was paid for the gift.
            
        model (``UniqueGiftModel``):
            Unique gift model.
    """
    
    telegram_payment_charge_id: str
    provider_payment_charge_id: str
    gift_star_count: int
    model: UniqueGiftModel
    
    @classmethod
    def _parse(cls, client, gift_data: dict):
        """Parse a UniqueGiftInfo object from the Telegram API response."""
        if not gift_data:
            return None
            
        model = UniqueGiftModel._parse(client, gift_data.get("model"))
            
        return cls(
            telegram_payment_charge_id=gift_data.get("telegram_payment_charge_id"),
            provider_payment_charge_id=gift_data.get("provider_payment_charge_id"),
            gift_star_count=gift_data.get("gift_star_count"),
            model=model
        )
        
    def to_dict(self):
        """Convert the UniqueGiftInfo object to a dictionary."""
        return {
            "telegram_payment_charge_id": self.telegram_payment_charge_id,
            "provider_payment_charge_id": self.provider_payment_charge_id,
            "gift_star_count": self.gift_star_count,
            "model": self.model.to_dict()
        } 