from django.contrib import admin

from inpage.models import Advertisement


class AdvAdmin(admin.ModelAdmin):
    list_display = ['name', 'active']


admin.site.register(Advertisement, AdvAdmin)
