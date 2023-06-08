from django.contrib import admin

from .models import Users, Address, Area, ClubCard


@admin.register(Users)
class UsersAdmin(admin.ModelAdmin):
    list_display = ['username', 'last_name', 'mobile', 'email']


@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ['user', 'phone', 'name', 'province', 'city', 'county', 'address']


@admin.register(Area)
class AreaAdmin(admin.ModelAdmin):
    list_display = ['pid', 'name', 'level']


@admin.register(ClubCard)
class AreaAdmin(admin.ModelAdmin):
    list_display = ['card_number', 'user', 'money']
