from celery import shared_task

from apps.listing.tasks import update_listings_prices_task
from apps.payment.services import ExchangeRateService


@shared_task
def fetch_currency_rates_task():
    """
    Оновлює курси валют і перераховує ціни оголошень.
    Виконується за розкладом (щодня о 9:00).
    """
    ExchangeRateService.fetch_currency_rates()
    # Після оновлення курсів - перерахунок цін всіх активних оголошень
    update_listings_prices_task.delay()
