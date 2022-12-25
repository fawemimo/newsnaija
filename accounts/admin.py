from django.contrib import admin
from django.contrib.admin import SimpleListFilter
from django.contrib.auth.admin import UserAdmin

from accounts.models import User


class EmailFilter(SimpleListFilter):
    title = "Email Filter"
    parameter_name = "user_email"

    def lookups(self, request, model_admin):
        return (("has_email", "has_email"), ("no_email", "no_email"))

    def queryset(self, request, queryset):
        if not self.value():
            return queryset

        # has  email
        if self.value().lower() == "has_email":
            return queryset.exclude(email="")

        # has no email
        if self.value().lower() == "no_email":
            return queryset.filter(email="")


@admin.register(User)
class UserAdmin(UserAdmin):
    list_display = (
        "email",
        "full_name",
        "username",
        "last_login",
        "date_joined",
        "is_active",
    )

    # custom name
    @admin.display(description="Full Name")
    def full_name(self, obj):
        return ("%s %s" % (obj.first_name, obj.last_name)).upper()

    list_per_page = 25
    list_display_links = ("email",)
    readonly_fields = ("last_login", "date_joined")
    search_fields = ("email",)
    ordering = ("-date_joined",)

    filter_horizontal = ()
    list_per_page = 25
    list_filter = (EmailFilter, "date_joined", "last_login", "is_active")
    fieldsets = ()
