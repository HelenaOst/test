from apps.listing.models import Listing
from apps.payment.models import CurrencyRate


class ListingPriceService:
    @staticmethod
    def update_prices():
        rate = CurrencyRate.objects.order_by('-created_at').first()

        if rate is None:
            raise Exception('No currency rate')

        usd_to_uah = rate.usd_to_uah
        eur_to_uah = rate.eur_to_uah

        listings = list(Listing.objects.filter(status='active'))

        for listing in listings:
            if listing.currency == 'UAH':
                listing.price_uah = listing.original_price
                listing.price_usd = listing.original_price / usd_to_uah
                listing.price_eur = listing.original_price / eur_to_uah

            elif listing.currency == 'USD':
                listing.price_usd = listing.original_price
                listing.price_uah = listing.original_price * usd_to_uah
                listing.price_eur = listing.price_uah / eur_to_uah

            elif listing.currency == 'EUR':
                listing.price_eur = listing.original_price
                listing.price_uah = listing.original_price * eur_to_uah
                listing.price_usd = listing.price_uah / usd_to_uah

        Listing.objects.bulk_update(listings, ['price_eur', 'price_uah', 'price_usd'])








