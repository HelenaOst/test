import os.path
from uuid import uuid4


def upload_listing_image(instance, filename):
    """Генерує шлях для збереження фото оголошення: listing_images/<listing_id>/<uuid>.<ext>"""
    ext = filename.split('.')[-1]
    return os.path.join('listing_images', str(instance.listing_id), f'{uuid4()}.{ext}')


def upload_avatar(instance, filename):
    """Генерує шлях для збереження аватара користувача: avatars/<user_id>/<uuid>.<ext>"""
    ext = filename.split('.')[-1]
    return os.path.join('avatars', str(instance.id), f'{uuid4()}.{ext}')


def upload_profile_logo(instance, filename):
    """Генерує шлях для збереження логотипу профілю: profile_logos/<profile_id>/<uuid>.<ext>"""
    ext = filename.split('.')[-1]
    return os.path.join('profile_logos', str(instance.id), f'{uuid4()}.{ext}')