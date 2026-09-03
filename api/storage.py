from urllib.parse import quote

from storages.backends.s3boto3 import S3Boto3Storage
from django.conf import settings


def local_media_url(name):
    """URL for a file kept under MEDIA_ROOT, used when S3 isn't configured."""
    return f"{settings.MEDIA_URL}{quote(str(name).lstrip('/'))}"


class PublicMediaStorage(S3Boto3Storage):
    """
    Custom storage class for public media files (like gallery images)
    that should be accessible without pre-signed URLs
    """
    bucket_name = settings.AWS_STORAGE_BUCKET_NAME
    endpoint_url = settings.AWS_S3_ENDPOINT_URL
    access_key = settings.AWS_ACCESS_KEY_ID
    secret_key = settings.AWS_SECRET_ACCESS_KEY
    region_name = settings.AWS_S3_REGION_NAME
    file_overwrite = settings.AWS_S3_FILE_OVERWRITE
    default_acl = 'public-read'  # Make files publicly accessible
    object_parameters = settings.AWS_S3_OBJECT_PARAMETERS
    verify = settings.AWS_S3_VERIFY
    location = "media"
    addressing_style = settings.AWS_S3_ADDRESSING_STYLE
    signature_version = settings.AWS_S3_SIGNATURE_VERSION
    querystring_auth = False  # Disable signed URLs for public access
    
    def url(self, name):
        """
        Return a public URL without signature for the file
        """
        # No object storage configured (local development): the file lives
        # under MEDIA_ROOT and Django serves it from MEDIA_URL.
        if not settings.USE_S3_MEDIA:
            return local_media_url(name)

        # Construct direct public URL without pre-signed parameters
        if self.endpoint_url and self.bucket_name:
            # Remove trailing slash from endpoint_url if present
            endpoint = self.endpoint_url.rstrip('/')
            # Construct the public URL
            return f"{endpoint}/{self.bucket_name}/{self.location}/{name}"
        
        # Fallback to default behavior if something goes wrong
        return super().url(name)


class PrivateMediaStorage(S3Boto3Storage):
    """
    Custom storage class for private media files 
    that require pre-signed URLs for access
    """
    bucket_name = settings.AWS_STORAGE_BUCKET_NAME
    endpoint_url = settings.AWS_S3_ENDPOINT_URL
    access_key = settings.AWS_ACCESS_KEY_ID
    secret_key = settings.AWS_SECRET_ACCESS_KEY
    region_name = settings.AWS_S3_REGION_NAME
    file_overwrite = settings.AWS_S3_FILE_OVERWRITE
    default_acl = None  # Keep files private
    object_parameters = settings.AWS_S3_OBJECT_PARAMETERS
    verify = settings.AWS_S3_VERIFY
    location = "media/private"
    addressing_style = settings.AWS_S3_ADDRESSING_STYLE
    signature_version = settings.AWS_S3_SIGNATURE_VERSION
    querystring_auth = True  # Enable signed URLs for private access

    def url(self, name, *args, **kwargs):
        # Same local-development fallback as PublicMediaStorage: without
        # credentials there is nothing to sign, so serve from MEDIA_URL.
        if not settings.USE_S3_MEDIA:
            return local_media_url(name)
        return super().url(name, *args, **kwargs)