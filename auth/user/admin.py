from django.contrib import admin
from django.db.models import Q
from .models import *

# Register your models here.


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("email", "name", "organization", "uuid")
    exclude = ["is_installer", "installer_organizations", "groups", "user_permissions"]
    list_per_page = 20

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.filter(Q(is_installer=None) | Q(is_installer=False))


@admin.register(Installer)
class InstallerAdmin(admin.ModelAdmin):
    list_display = ("email", "name", "organization", "uuid")
    exclude = ("organization", "is_admin", "is_superuser", "roles")
    filter_horizontal = ("installer_organizations",)
    list_per_page = 20

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.filter(is_installer=True)


@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ("name", "uuid")


@admin.register(AccessControl)
class AccessControlAdmin(admin.ModelAdmin):
    list_display = ("role", "feature", "get_methods")

    def get_methods(self, obj):
        return " | ".join([p.name for p in obj.method.all()])


admin.site.register(Method)
