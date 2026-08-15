from celery import shared_task

from apps.listing.services import ListingPriceService


@shared_task
def update_listings_prices_task():
    """
    Оновлює ціни для всіх активних оголошень.
    Запускається після оновлення курсів валют.
    """
    ListingPriceService.update_prices()


@shared_task
def update_one_listing_prices_task(listing_id):
    """
    Оновлює ціни для одного оголошення.
    Запускається при створенні або редагуванні оголошення.
    """
    ListingPriceService.update_one_price(listing_id)


@shared_task
def send_report_email_task(listing_id, user_id, message):
    """Надсилає email менеджеру зі скаргою на оголошення."""
    from apps.core.services.email_service import EmailService
    from apps.listing.models import Listing
    from apps.users.models import User

    listing = Listing.objects.get(id=listing_id)
    user = User.objects.get(id=user_id)
    EmailService.send_listing_report_email(listing, user, message)


@shared_task
def send_blocked_listing_email_task(listing_id):
    """Надсилає email продавцю про блокування оголошення."""
    from apps.core.services.email_service import EmailService
    from apps.listing.models import Listing

    listing = Listing.objects.get(id=listing_id)
    EmailService.send_blocked_listing_email(listing)