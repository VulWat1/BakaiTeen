from django.contrib import admin
from .models import Profile

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'account_type', 'coin')  # Columns shown in admin list view
    list_filter = ('account_type',)          # Filter sidebar
    search_fields = ('user__username',)      # Search box
