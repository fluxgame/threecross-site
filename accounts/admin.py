from django.contrib import admin

# Register your models here.

from .models import Account


class AccountAdmin(admin.ModelAdmin):
    list_display = ('name', 'address', 'show_on_web')


admin.site.register(Account, AccountAdmin)
