from django.contrib import admin

from .models import Users, Address, Area, AuthCode


@admin.register(Users)
class UsersAdmin(admin.ModelAdmin):
    list_display = ['username', 'last_name', 'mobile', 'email']


@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ['user', 'phone', 'name', 'province', 'city', 'county', 'address']


@admin.register(Area)
class AreaAdmin(admin.ModelAdmin):
    list_display = ['pid', 'name', 'level']


@admin.register(AuthCode)
class AuthCodeAdmin(admin.ModelAdmin):
    list_display = ['mobile', 'code', 'created_time']