from django.contrib import admin
from .models import Profile, Payment


class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'date_of_birth', 'photo']


class PaymentAdimin(admin.ModelAdmin):
    list_display = ['user', 'amount']


admin.site.register(Profile, ProfileAdmin)

admin.site.register(Payment, PaymentAdimin)
