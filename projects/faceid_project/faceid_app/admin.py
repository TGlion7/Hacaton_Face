from django.contrib import admin
from .models import User

class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'first_name', 'last_name', 'level', 'club', 'coach', 'profile_picture')
    search_fields = ('username', 'first_name', 'last_name')
    list_filter = ('level',)

admin.site.register(User, UserAdmin)
