from dataclasses import dataclass

@dataclass
class StarAmount:
    """This object represents an amount of Telegram Stars.
    
    Attributes:
        star_count (``int``):
            Amount of Telegram Stars.
            
        nanostar_amount (``int``):
            Amount of nano stars (1 star = 1'000'000'000 nanostars).
    """
    
    star_count: int
    nanostar_amount: int
    
    @classmethod
    def _parse(cls, client, amount_data: dict):
        """Parse a StarAmount object from the Telegram API response."""
        if not amount_data:
            return None
            
        return cls(
            star_count=amount_data.get("star_count", 0),
            nanostar_amount=amount_data.get("nanostar_amount", 0)
        )
        
    def to_dict(self):
        """Convert the StarAmount object to a dictionary."""
        return {
            "star_count": self.star_count,
            "nanostar_amount": self.nanostar_amount
        } 