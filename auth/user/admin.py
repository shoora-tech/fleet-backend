from django.contrib import admin
from .models import *
# Register your models here.

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("email", "name", "organization")

@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ("name", "uuid")

@admin.register(AccessControl)
class AccessControlAdmin(admin.ModelAdmin):
    list_display = ("role", "feature", "get_methods")

    def get_methods(self, obj):
        return "\n".join([p.name for p in obj.method.all()])

admin.site.register(Method)
