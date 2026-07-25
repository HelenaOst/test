import os

from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template

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

class EmailForModeration:
    @staticmethod
    def _send_email(to:str, template_name:str, context:dict, subject:str):
        template = get_template(template_name)
        html_message = template.render(context)
        msg = EmailMultiAlternatives(
            to=[to],
            from_email=os.environ.get('EMAIL_HOST_USER'),
            subject=subject
        )
        msg.attach_alternative(html_message, "text/html")
        msg.send()

    @staticmethod
    def send_blocked_listing_email(listing):
        EmailForModeration._send_email(
            to=os.environ.get('MANAGERS_EMAIL', 'moderation@automarket.com'),
            template_name='moderation/blocked_listing.html',
            context={
                'owner_name': listing.owner.username,
                'listing_id': listing.id,
                'car': str(listing.car_model),
            },
            subject='Оголошення заблоковано'
        )


