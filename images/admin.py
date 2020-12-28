from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import Upload, User

admin.site.register(User, UserAdmin)
admin.site.register(Upload)

UserAdmin.fieldsets += (
    (
        "User fields",
        {"fields": ("description", "following", "avatar", "liked", "saved", "private")},
    ),
)
