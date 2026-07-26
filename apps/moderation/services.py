
from apps.listing.models import Listing
from apps.moderation.bad_words import BAD_WORDS
from apps.moderation.models import ListingModeration


class ModerationBadWords:
    @staticmethod
    def moderation_bad_words(listing_id):
        listing = Listing.objects.get(id=listing_id)

        text = f'{listing.description} {listing.color}'
        if any(word in text.lower() for word in BAD_WORDS):
            listing.status = 'rejected'
            listing.save(
                update_fields=['status']
            )
            ListingModeration.objects.create(
                listing=listing,
                moderation_action='auto_rejected',
                moderator=None
            )
        else:
            listing.status = 'active'
            listing.save(
                update_fields=['status']
            )
            ListingModeration.objects.create(
                listing=listing,
                moderation_action='auto_approved',
                moderator=None
            )




