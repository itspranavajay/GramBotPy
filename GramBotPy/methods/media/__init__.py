from .download_media import DownloadMedia
from .upload_media import UploadMedia

class MediaMethodsMixin(
    DownloadMedia,
    UploadMedia
):
    """Media handling methods.
    
    This mixin includes methods related to downloading and uploading media files.
    """
    pass 