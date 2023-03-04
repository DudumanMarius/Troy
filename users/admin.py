from django.contrib import admin
from users.models import User


class UserAdmin(admin.ModelAdmin):
    list_display = ("pk", "email", "is_active", "date_joined")


admin.site.register(User, UserAdmin)
