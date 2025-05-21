from dataclasses import dataclass
from typing import Optional, Dict, Any

@dataclass
class Venue:
    """This object represents a venue.
    
    Parameters:
        location (``dict``):
            Venue location. Can't be a live location.
            
        title (``str``):
            Name of the venue.
            
        address (``str``):
            Address of the venue.
            
        foursquare_id (``str``, optional):
            Foursquare identifier of the venue.
            
        foursquare_type (``str``, optional):
            Foursquare type of the venue.
            
        google_place_id (``str``, optional):
            Google Places identifier of the venue.
            
        google_place_type (``str``, optional):
            Google Places type of the venue.
    """
    
    location: Dict[str, Any]
    title: str
    address: str
    foursquare_id: Optional[str] = None
    foursquare_type: Optional[str] = None
    google_place_id: Optional[str] = None
    google_place_type: Optional[str] = None 