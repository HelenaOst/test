from apps.listing.models import Listing
from apps.payment.models import CurrencyRate


class ListingPriceService:
    """Сервіс для перерахунку цін оголошень в різних валютах."""

    @staticmethod
    def _calculate_prices(listing, usd_to_uah, eur_to_uah):
        """
        Перераховує ціни оголошення на основі поточної валюти.
        Підтримує: UAH, USD, EUR.
        """
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

    @staticmethod
    def update_prices():
        """
        Оновлює ціни для ВСІХ активних оголошень.
        Використовується при щоденному оновленні курсів валют.
        """
        rate = CurrencyRate.objects.order_by('-created_at').first()
        if rate is None:
            raise Exception('No currency rate')

        usd_to_uah = rate.usd_to_uah
        eur_to_uah = rate.eur_to_uah

        listings = list(Listing.objects.filter(status='active'))

        for listing in listings:
            listing.exchange_rate = rate
            ListingPriceService._calculate_prices(listing, usd_to_uah, eur_to_uah)

        # Масове оновлення одним запитом
        Listing.objects.bulk_update(listings, ['price_eur', 'price_uah', 'price_usd', 'exchange_rate'])

    @staticmethod
    def update_one_price(listing_id):
        """
        Оновлює ціни для ОДНОГО оголошення.
        Використовується при створенні або редагуванні оголошення.
        """
        rate = CurrencyRate.objects.order_by('-created_at').first()
        if rate is None:
            raise Exception('No currency rate')

        listing = Listing.objects.get(id=listing_id)
        usd_to_uah = rate.usd_to_uah
        eur_to_uah = rate.eur_to_uah

        ListingPriceService._calculate_prices(listing, usd_to_uah, eur_to_uah)
        listing.exchange_rate = rate
        listing.save(update_fields=['price_eur', 'price_uah', 'price_usd', 'exchange_rate'])