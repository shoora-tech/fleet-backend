"""auth URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions
from vehicle.views import DeviceAutocompleteView
from driver.views import DriverAutocompleteView

from django.contrib import admin
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView

admin.site.site_header = 'Shoora CMS'                    # default: "Django Administration"
admin.site.index_title = 'Shoora CMS'                 # default: "Site administration"
admin.site.site_title = 'Shoora Admin' # default: "Django site admin"

schema_view = get_schema_view(
    openapi.Info(
        title="Snippets API",
        default_version="v1",
        description="Test description",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@snippets.local"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    # path('auth/swagger(?P<format>\.json|\.yaml)/', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('auth/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('auth/swagger/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    # path('api/schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),

    # path(
    #     "swagger/",
    #     schema_view.with_ui("swagger", cache_timeout=0),
    #     name="schema-swagger-ui",
    # ),
    # path(r'^redoc/$', schema_ßview.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path("auth/admin/", admin.site.urls),
    path("auth/api/v1/", include("auth.apiurls.auth_apiurls")),
    path("transport/api/v1/", include("auth.apiurls.transport_apiurls")),
    path("monitor/api/v1/", include("auth.apiurls.monitor_apiurls")),
    path("auth/vehicle_device_autocomplete", DeviceAutocompleteView.as_view(), name='vehicle_device_autocomplete'),
    path("auth/driver_vehicle_autocomplete", DriverAutocompleteView.as_view(), name='driver_vehicle_autocomplete'),
]
