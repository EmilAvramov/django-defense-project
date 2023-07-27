from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import UserCreationForm, UserChangeForm
from .models import UserModel, Role


class Admin(UserAdmin):
    add_form = UserCreationForm
    form = UserChangeForm
    model = UserModel
    list_display = (
        "email",
        "is_staff",
        "is_active",
    )
    list_filter = (
        "email",
        "is_staff",
        "is_active",
    )
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        (
            "Permissions",
            {
                "fields": (
                    "is_staff",
                    "is_active",
                    "groups",
                    "user_permissions",
                )
            },
        ),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "email",
                    "password1",
                    "password2",
                    "is_staff",
                    "is_active",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
    )
    search_fields = ("email",)
    ordering = ("email",)


class CustomUserAdmin(UserAdmin):
    add_form = UserCreationForm
    form = UserChangeForm
    model = UserModel
    list_display = ("email", "is_staff", "is_active", "date_joined")
    list_filter = ("is_staff", "is_active", "date_joined")
    filter_horizontal = ("groups", "user_permissions", "roles")
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        ("Personal Info", {"fields": ("first_name", "last_name", "roles")}),
        (
            "Permissions",
            {
                "fields": (
                    "is_staff",
                    "is_active",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        ("Important dates", {"fields": ("last_login", "date_joined")}),
    )

    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "email",
                    "password1",
                    "password2",
                    "is_staff",
                    "is_active",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
    )
    search_fields = ("email", "first_name", "last_name")
    ordering = ("email",)
    date_hierarchy = "date_joined"
    list_per_page = 10
    actions = ["make_active", "make_inactive"]

    def make_active(self, request, queryset):
        queryset.update(is_active=True)

    make_active.short_description = "Mark selected users as active"

    def make_inactive(self, request, queryset):
        queryset.update(is_active=False)

    make_inactive.short_description = "Mark selected users as inactive"

    def has_change_permission(self, request, obj=None):
        has_permission = super().has_change_permission(request, obj)
        if not has_permission:
            restricted_fields = [
                "is_staff",
                "is_active",
                "groups",
                "user_permissions",
            ]
            if obj and request.user.groups.filter(name="staff").exists():
                for field in restricted_fields:
                    if request.POST.get(field) and request.POST[field] != str(
                        getattr(obj, field)
                    ):
                        return False
        return has_permission

    def get_fieldsets(self, request, obj=None):
        fieldsets = super().get_fieldsets(request, obj)
        if not obj:
            fieldsets += ((None, {"fields": ("roles",)}),)
        return fieldsets

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        obj.roles.set(form.cleaned_data["roles"])


admin.site.register(UserModel, CustomUserAdmin)
admin.site.register(Role)
