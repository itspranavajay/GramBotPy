from dataclasses import dataclass
from typing import Optional

@dataclass
class Location:
    """This object represents a point on the map.
    
    Parameters:
        longitude (``float``):
            Longitude as defined by sender.
            
        latitude (``float``):
            Latitude as defined by sender.
            
        horizontal_accuracy (``float``, optional):
            The radius of uncertainty for the location, measured in meters; 0-1500.
            
        live_period (``int``, optional):
            Time relative to the message sending date, during which the location can be updated.
            
        heading (``int``, optional):
            The direction in which user is moving, in degrees; 1-360.
            
        proximity_alert_radius (``int``, optional):
            Maximum distance for proximity alerts about approaching another chat member, in meters.
    """
    
    longitude: float
    latitude: float
    horizontal_accuracy: Optional[float] = None
    live_period: Optional[int] = None
    heading: Optional[int] = None
    proximity_alert_radius: Optional[int] = None 