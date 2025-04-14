from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _
from .models import User

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    """Best Practice: Comprehensive admin interface"""
    
    list_display = (
        'username', 'email', 'phone_number', 
        'is_active', 'is_staff', 'is_verified',
        'date_joined'
    )
    list_filter = (
        'is_active', 'is_staff', 'is_superuser', 
        'is_verified', 'date_joined'
    )
    search_fields = ('username', 'email', 'phone_number')
    ordering = ('-date_joined',)
    filter_horizontal = ('groups', 'user_permissions',)
    readonly_fields = ('date_joined', 'last_login')
    
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Contact Info'), {
            'fields': ('email', 'phone_number', 'language')
        }),
        (_('Permissions'), {
            'fields': (
                'is_active', 'is_staff', 'is_superuser',
                'is_verified', 'groups', 'user_permissions'
            ),
        }),
        (_('Important dates'), {
            'fields': ('last_login', 'date_joined')
        }),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'username', 'email', 'phone_number',
                'password1', 'password2', 'language'
            ),
        }),
    )
    
    actions = ['activate_users', 'deactivate_users']
    
    def activate_users(self, request, queryset):
        """Best Practice: Custom admin action"""
        updated = queryset.update(is_active=True)
        self.message_user(
            request,
            f'Activated {updated} users'
        )
    activate_users.short_description = "Activate selected users"
    
    def deactivate_users(self, request, queryset):
        """Best Practice: Custom admin action"""
        updated = queryset.update(is_active=False)
        self.message_user(
            request,
            f'Deactivated {updated} users'
        )
    deactivate_users.short_description = "Deactivate selected users"
