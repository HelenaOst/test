import os.path
from uuid import uuid4


def upload_listing_image(instance, filename)->str:
    ext = filename.split('.')[-1]
    return os.path.join('listing_images', str(instance.listing_id), f'{uuid4()}.{ext}')