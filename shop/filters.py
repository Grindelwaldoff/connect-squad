from datetime import datetime, timedelta

from django.contrib.auth import get_user_model
import django_filters as filter

from shop.models import Product

User = get_user_model()


class GeneralFilter(filter.FilterSet):
    premium = filter.BooleanFilter(
        method='bool_method',
    )
    spam_block = filter.BooleanFilter(
        method='bool_method',
    )
    password = filter.BooleanFilter(
        method='bool_method',
    )
    cookies = filter.BooleanFilter(
        method='bool_method',
    )
    binding_phone = filter.BooleanFilter(
        method='bool_method',
    )
    country = filter.CharFilter()
    country_phone_code = filter.CharFilter(
        field_name='phone_country__value'
    )
    sex = filter.CharFilter(
        field_name='sex__value'
    )
    seller = filter.NumberFilter(
        field_name='seller',
    )
    price = filter.RangeFilter(
        field_name='price'
    )
    date_range = filter.NumberFilter(
        method='filter_by_date_range'
    )
    chats = filter.RangeFilter(
        method='psif_method'
    )
    groups = filter.RangeFilter(
        method='psif_method'
    )
    admin_chats = filter.RangeFilter(
        method='psif_method'
    )
    channels = filter.RangeFilter(
        method='psif_method'
    )
    age = filter.RangeFilter(
        method='psif_method'
    )
    friends = filter.RangeFilter(
        method='psif_method'
    )
    guaranty = filter.RangeFilter(
        method='psif_method'
    )
    votes = filter.RangeFilter(
        method='pif_method'
    )
    chat_subs = filter.RangeFilter(
        method='pif_method'
    )
    general_balance = filter.RangeFilter(
        method='pif_method'
    )

    class Meta:
        model = Product
        fields = (
            'premium', 'spam_block',
            'password',
            'seller',
            'price',
            'country',
            'chats',
            'admin_chats',
            'groups', 'channels',
            'age', 'friends', 'votes',
            'guaranty', 'general_balance',
            'chat_subs', 'country_phone_code',
            'sex',
        )

    def filter_by_date_range(self, queryset, name, value):
        today = datetime.today()
        return queryset.filter(
            product__created__gte=today - timedelta(days=int(value)),
            product__created__lte=today
        )

    def bool_method(self, queryset, name, value):
        return queryset.filter(bools__name=name, bools__value=value)

    def psif_method(self, queryset, name, value):
        if value:
            if value.start is not None and value.stop is not None:
                return queryset.filter(
                    psif_params__name=name,
                    psif_params__value__gte=value.start,
                    psif_params__value__lte=value.stop)
            elif value.start is not None:
                return queryset.filter(
                    psif_params__name=name,
                    psif_params__value__gte=value.start)
            elif value.stop is not None:
                return queryset.filter(
                    psif_params__name=name,
                    psif_params__value__lte=value.stop)
        return queryset

    def pif_method(self, queryset, name, value):
        if value:
            if value.start is not None and value.stop is not None:
                return queryset.filter(
                    pif_params__name=name,
                    pif_params__value__gte=value.start,
                    pif_params__value__lte=value.stop)
            elif value.start is not None:
                return queryset.filter(
                    pif_params__name=name,
                    pif_params__value__gte=value.start)
            elif value.stop is not None:
                return queryset.filter(
                    pif_params__name=name,
                    pif_params__value__lte=value.stop)
        return queryset


# class SteamFilter(filter.FilterSet):
#     """Фильтр для аккаунтов Стим."""

#     price = filter.RangeFilter(
#         field_name='product__price',
#     )
#     date_range = filter.NumberFilter(
#         method='filter_by_date_range'
#     )
#     seller = filter.NumberFilter(
#         field_name='product__seller',
#     )
#     general_balance = filter.RangeFilter(
#         field_name='general_balance',
#     )
#     inventory_price = filter.RangeFilter(
#         field_name='games__balance',
#     )
#     guaranty = filter.NumberFilter(
#         field_name='guaranty',
#         lookup_expr='gte'
#     )
#     email_ac = filter.BooleanFilter(
#         field_name='email_available'
#     )
#     games = filter.CharFilter(
#         field_name='products__name'
#     )

#     class Meta:
#         model = ProductSteam
#         fields = [
#             'price', 'date_range',
#             'seller',
#             'general_balance',
#             'inventory_price',
#             'guaranty', 'email_ac', 'games'
#         ]

#     def filter_by_date_range(self, queryset, name, value):
#         today = datetime.today()
#         return queryset.filter(
#             product__created__gte=today - timedelta(days=int(value)),
#             product__created__lte=today
#         )
