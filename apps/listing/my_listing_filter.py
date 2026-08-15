import django_filters

from apps.listing.models import Listing


class MyListingFilter(django_filters.FilterSet):
    """Фільтр для списку власних оголошень продавця."""

    status = django_filters.ChoiceFilter(
        choices=Listing.ListingStatus.choices
    )

    class Meta:
        model = Listing
        fields = ["status"]