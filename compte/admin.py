from django.contrib import admin

from .forms import UserChangeForm, UserCreationForm
from .models import ImageUser, User
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _
from django.utils.html import format_html
class ImageUserInline(admin.TabularInline):
    model = ImageUser
    readonly_fields = ('image_tag',)

    def image_tag(self, obj):
        if obj.profil:
            return format_html('<img src="{}" style="max-width: 200px; max-height: 200px;" />'.format(obj.profil.url))
        return "-"
    image_tag.short_description = 'Profil'

@admin.register(User)
class UserAdmin(UserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm
    fieldsets = (
        (None, {"fields": ("username", "password")}),
        (_("Personal info"), {"fields": ("first_name", "last_name", "email" ,"post")}),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "is_members",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("username", "email", "first_name", "last_name","post" ,"password1", "password2"),
            },
        ),
    )
    inlines = [ImageUserInline]
    list_display = ("username", "email", "first_name", "last_name","post", "is_staff",'photo_de_profil')
    list_filter = ("is_staff", "is_superuser", "is_active", "is_members","post"
                   ,"groups")
    search_fields = ("username", "first_name", "last_name", "email","post")
    ordering = ("username",)
    filter_horizontal = (
        "groups",
        "user_permissions",
    )

    def photo_de_profil(self, obj):
        if hasattr(obj, 'imageuser') and obj.imageuser.profil:
            return format_html('<img src="{}" style="max-width: 100px; max-height: 100px;" />'.format(obj.imageuser.profil.url))
        return "photo de profil non disponible"
    photo_de_profil.short_description = 'photo de profil'

# Register your models here.
