from django.contrib import admin
from django.utils.html import mark_safe
from users.models import User


@admin.register(User)
class User(admin.ModelAdmin):
    list_display = ('id', 'email', 'first_name', 'last_name', 'phone', 'avatar_tag', 'city', 'is_active')

    def avatar_tag(self, obj):
        if obj.avatar:
            return mark_safe(
                f'<img src="{obj.avatar.url}" width="50" height="50" style="object-fit: cover; border-radius: 50%;" />'
            )
        return "-"

    avatar_tag.short_description = 'Аватар'
