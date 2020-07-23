from django.contrib import admin
from addresses.models import Address
from businesses.models import Business
from members.models import Member
from .models import User, Group
from cuser.forms import UserChangeForm, UserCreationForm
from django.contrib.auth.admin import GroupAdmin as BaseGroupAdmin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import Group as StockGroup


class AddressAdmin(admin.StackedInline):
    model = Address


class MemberAdmin(admin.StackedInline):
    model = Member


class BusinessAdmin(admin.StackedInline):
    model = Business


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    inlines = [AddressAdmin, BusinessAdmin, MemberAdmin]
    add_form_template = 'admin/cuser/cuser/add_form.html'
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser',
                                       'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2'),
        }),
    )
    form = UserChangeForm
    add_form = UserCreationForm
    list_display = ('full_name', 'street_address', 'city_state', 'is_active')
    search_fields = ('email',)
    ordering = ('email',)


admin.site.unregister(StockGroup)


@admin.register(Group)
class GroupAdmin(BaseGroupAdmin):
    pass

# class UserAdmin(ReverseModelAdmin):
#    inline_type = 'stacked'
#    inline_reverse = ['address']
#    list_display = ('business_name', 'street_address', 'show_on_web')
