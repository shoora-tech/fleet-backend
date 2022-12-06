from django.contrib import admin
from django.db.models import Q
from .models import *
from django.contrib.auth.admin import UserAdmin

# Register your models here.
@admin.register(User)
class UserAdmin(UserAdmin):
    list_display = ("email", "name", "organization", "uuid")
    exclude = ["is_installer", "installer_organizations", "groups", "user_permissions"]
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('name', 'address', 'contact_code', 'contact_number', 'organization',)}),
        ('Django Permissions', {'fields': ('is_admin', 'is_active', 'is_staff', 'is_superuser')}),
        ('Shoora Permissions', {'fields': ('roles',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'name', 'address', 'contact_code', 'contact_number', 'organization', 'roles'),
        }),
    )
    list_per_page = 20
    ordering = ('email',)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.filter(Q(is_installer=None) | Q(is_installer=False))


@admin.register(Installer)
class InstallerAdmin(UserAdmin):
    list_display = ("email", "name", "organization", "uuid")
    exclude = ("organization", "is_admin", "is_superuser", "roles")
    filter_horizontal = ("installer_organizations",)
    list_per_page = 20
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('name', 'address', 'contact_code', 'contact_number', 'installer_organizations','is_installer', 'is_staff')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'name', 'address', 'contact_code', 'contact_number', 'installer_organizations',),
        }),
    )
    ordering = ('email',)

    def get_queryset(self, request):
        return Installer.objects.all()


@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ("name", "uuid")


@admin.register(AccessControl)
class AccessControlAdmin(admin.ModelAdmin):
    list_display = ("role", "feature", "get_methods")

    def get_methods(self, obj):
        return " | ".join([p.name for p in obj.method.all()])


admin.site.register(Method)
