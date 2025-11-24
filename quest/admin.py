from django.contrib import admin
from .models import Profile, Task, ExchangeRequest

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'role', 'money')
    list_filter = ('role',)

    search_fields = ('user__username',)      # Search box


admin.site.register(Task)
admin.site.register(ExchangeRequest)