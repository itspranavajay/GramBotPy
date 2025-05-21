from dataclasses import dataclass

@dataclass
class GiftInfo:
    """This object represents information about a gift.
    
    Attributes:
        telegram_payment_charge_id (``str``):
            Unique identifier of the successful payment in Telegram.
            
        provider_payment_charge_id (``str``):
            Unique identifier of the successful payment in the provider system.
            
        gift_star_count (``int``):
            Number of stars that was paid for the gift.
            
        upgrade_star_count (``int``, optional):
            Number of stars needed to upgrade the gift to a unique gift.
    """
    
    telegram_payment_charge_id: str
    provider_payment_charge_id: str
    gift_star_count: int
    upgrade_star_count: int = None
    
    @classmethod
    def _parse(cls, client, gift_data: dict):
        """Parse a GiftInfo object from the Telegram API response."""
        if not gift_data:
            return None
            
        return cls(
            telegram_payment_charge_id=gift_data.get("telegram_payment_charge_id"),
            provider_payment_charge_id=gift_data.get("provider_payment_charge_id"),
            gift_star_count=gift_data.get("gift_star_count"),
            upgrade_star_count=gift_data.get("upgrade_star_count")
        )
        
    def to_dict(self):
        """Convert the GiftInfo object to a dictionary."""
        result = {
            "telegram_payment_charge_id": self.telegram_payment_charge_id,
            "provider_payment_charge_id": self.provider_payment_charge_id,
            "gift_star_count": self.gift_star_count
        }
        
        if self.upgrade_star_count is not None:
            result["upgrade_star_count"] = self.upgrade_star_count
            
        return result 