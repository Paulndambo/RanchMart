from django.contrib import admin
from .models import User

# Register your models here.
@admin.register(User)
class UsersAdmin(admin.ModelAdmin):
    list_display = ["username", "email", "first_name", "last_name", "phone_number", "gender", "is_active", "is_staff"]
   
    search_fields = ["username", "email", "first_name", "last_name", "phone_number"]
    list_per_page = 10

