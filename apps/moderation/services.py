from apps.listing.models import Listing
from apps.moderation.bad_words import BAD_WORDS
from apps.moderation.models import ListingModeration


class ModerationBadWords:
    """Сервіс для автоматичної модерації оголошень за списком заборонених слів."""

    @staticmethod
    def moderation_bad_words(listing_id):
        """
        Перевіряє оголошення на наявність заборонених слів.

        Якщо знайдено заборонені слова - статус REJECTED.
        Якщо не знайдено - статус ACTIVE.
        Створює запис в логу модерації з відповідною дією.
        """
        listing = Listing.objects.get(id=listing_id)

        # Перевірка опису та кольору на заборонені слова
        text = f'{listing.description} {listing.color}'
        has_bad_words = any(word in text.lower() for word in BAD_WORDS)

        if has_bad_words:
            listing.status = Listing.ListingStatus.REJECTED
            moderation_action = ListingModeration.ModerationAction.AUTO_REJECTED
        else:
            listing.status = Listing.ListingStatus.ACTIVE
            moderation_action = ListingModeration.ModerationAction.AUTO_APPROVED

        listing.save(update_fields=['status'])

        # Логування дії модерації
        ListingModeration.objects.create(
            listing=listing,
            moderation_action=moderation_action
        )