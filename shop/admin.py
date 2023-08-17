from django.contrib import admin

from shop.models import (
    Category, Product,
    AccountGroup, HistoryByAccountGroup,
    Game, GameOnSteam, BoolParamsForProducts,
    PIFParamsForProducts, PSIFParamsForProducts,
    SexParam, EmailDomainParam, PhoneCountryParam,
    EmailAccessModel
)


class BoolInline(admin.TabularInline):
    model = BoolParamsForProducts
    extra = 1
    min_num = 0


class EmailAccessInline(admin.TabularInline):
    model = EmailAccessModel
    extra = 1
    min_num = 0


class SexInline(admin.TabularInline):
    model = SexParam
    extra = 1
    min_num = 0


class EmailDomainInline(admin.TabularInline):
    model = EmailDomainParam
    extra = 1
    min_num = 0


class PhoneCountryInline(admin.TabularInline):
    model = PhoneCountryParam
    extra = 1
    min_num = 0


class GameInline(admin.TabularInline):
    model = GameOnSteam
    min_num = 0
    extra = 1


class PIFInline(admin.TabularInline):
    model = PIFParamsForProducts
    min_num = 0
    extra = 1


class PSIFInline(admin.TabularInline):
    model = PSIFParamsForProducts
    min_num = 0
    extra = 1


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}


class ProductAdmin(admin.ModelAdmin):
    list_display = [
        'name',
        'slug',
        'price',
        'available',
        'created',
        'updated'
    ]
    list_filter = ['available', 'created', 'updated']
    list_editable = ['price', 'available']
    prepopulated_fields = {'slug': ('name',)}
    inlines = (
        EmailDomainInline, SexInline,
        BoolInline, PIFInline,
        PSIFInline, GameInline,
        PhoneCountryInline,
        EmailAccessInline
    )


class AccountGroupAdmin(admin.ModelAdmin):
    list_display = ['product', 'account_name', 'torrent_file']


class HistoryByAccountGroupAdmin(admin.ModelAdmin):
    list_display = ['user', 'account_name', 'torrent_file']


admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Game, CategoryAdmin)
admin.site.register(AccountGroup, AccountGroupAdmin)
admin.site.register(HistoryByAccountGroup, HistoryByAccountGroupAdmin)
