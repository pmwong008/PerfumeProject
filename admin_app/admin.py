from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin ):

    list_display = ('id','username', 'email', 'is_staff', 'is_active')

    search_fields = ('username', 'email')

    list_filter = ('is_staff', 'is_active')

    fieldsets = (
        (None, {'fields': ('username', 'password', 'avatar')}),
        ('Personal info', {'fields': ('email',)}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser',
                                   'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2', 'avatar'),
        }),
    )
