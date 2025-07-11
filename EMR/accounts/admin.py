from django.contrib import admin
from accounts.models import User, Plans, Coverage
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from accounts.forms import CustomUserCreationForm, CustomUserChangeForm
# Register your models here.
admin.site.register(Plans)
admin.site.register(Coverage)

class UserAdmin(BaseUserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = User
    list_display = (
        "email", "full_name", "display_picture", "is_staff", "is_active", "is_superuser")
    list_filter = (
        "is_staff", "is_superuser", "is_active", "groups")
    fieldsets = (
        (None, {"fields": ("email", "password",)}),
        ("Personal info", {"fields": (
            "full_name", "display_picture", )}),
        ("Permissions", {"fields": (
            "is_active", "is_staff", "is_superuser", "groups", "user_permissions")}),
        # ("Important Dates", {"fields": (
        #     "last_login", "date_joined")})
    )
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": (
                "email", "full_name", "password1", "password2"
            )}),
    )
    search_fields = ("email", )
    ordering = ("email", )


admin.site.register(User, UserAdmin)