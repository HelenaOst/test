from celery import shared_task

from apps.listing.services import ListingPriceService


@shared_task
def update_listings_prices_task():
    ListingPriceService.update_prices()