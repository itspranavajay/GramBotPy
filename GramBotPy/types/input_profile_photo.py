import typing
from dataclasses import dataclass

@dataclass
class InputProfilePhoto:
    """This object describes a profile photo to be set.
    
    Attributes:
        photo_id (``str``, optional):
            File identifier of the photo to set as profile picture.
            Only the specific photo from a message will be set as profile photo.
            
        video_id (``str``, optional):
            File identifier of the video to set as profile picture.
            Only the specific video from a message can be set.
            
        thumbnail_position (``float``, optional):
            Timestamp in seconds defining the moment in the video that will be shown as static preview.
            If not specified, the video will be used as an animation.
    """
    
    photo_id: str = None
    video_id: str = None
    thumbnail_position: float = None
    
    @classmethod
    def _parse(cls, client, photo_data: dict):
        """Parse an InputProfilePhoto object from the Telegram API response."""
        if not photo_data:
            return None
            
        return cls(
            photo_id=photo_data.get("photo_id"),
            video_id=photo_data.get("video_id"),
            thumbnail_position=photo_data.get("thumbnail_position")
        )
        
    def to_dict(self):
        """Convert the InputProfilePhoto object to a dictionary."""
        result = {}
        
        if self.photo_id:
            result["photo_id"] = self.photo_id
            
        if self.video_id:
            result["video_id"] = self.video_id
            
        if self.thumbnail_position is not None:
            result["thumbnail_position"] = self.thumbnail_position
            
        return result 