from celery import shared_task

from apps.listing.services import ListingPriceService


@shared_task
def update_listings_prices_task():
    ListingPriceService.update_prices()

@shared_task
def update_one_listing_prices_task(listing_id):
    ListingPriceService.update_one_price(listing_id)