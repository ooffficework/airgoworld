from django.contrib import admin
from .models import CustomUser

class CustomUserAdmin(admin.ModelAdmin):
    model = CustomUser
    list_display = ('email', 'firstname', 'lastname', 'phone_number', 'is_active', 'is_staff')
    search_fields = ('email', 'firstname', 'lastname', 'phone_number')
    list_filter = ('is_active', 'is_staff')
    
admin.site.register(CustomUser, CustomUserAdmin)