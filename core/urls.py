"""
URL configuration for core project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.urls import include, path, re_path
from django.conf import settings
from django.conf.urls.static import static
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView
from django.contrib import admin
from apps.users import views
from django.views.static import serve

admin.site.site_header = "Administration"

def trigger_error(request):
    division_by_zero = 1 / 0

urlpatterns = [
    path("", include("home.urls")),
    path('admin/password_change/', views.custom_password_change, name='admin_password_change'),
    path('admin/password_change/done/', views.custom_password_change_done, name='password_change_done'),
    path("admin/", admin.site.urls),
    path("users/", include("apps.users.urls")),
    path("charts/", include("apps.charts.urls")),
    path("tables/", include("apps.tables.urls")),
    path('view-builder/', include('apps.view_builder.urls')),
    path('', include('apps.finding.urls')),
    path('', include('apps.file_manager.urls')),

    path('whap/', include('whap.urls')),
    path('loader/', include('loader.urls')),
    path('sso/', include('sso_client.urls')),

    path("tables/", include("apps.tables.tab.tab_urls")),
    path("tables/", include("apps.tables.finding.finding_urls")),
    path("tables/", include("apps.tables.finding_attachment.finding_attachment_urls")),

    path('api/docs/schema', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/'      , SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    # path("__debug__/", include("debug_toolbar.urls")),

    path('sentry-debug/', trigger_error),
    path('i18n/', include('django.conf.urls.i18n')),

    re_path(r'^media/(?P<path>.*)$', serve,{'document_root': settings.MEDIA_ROOT}),
    re_path(r'^static/(?P<path>.*)$', serve,{'document_root': settings.STATIC_ROOT}),

    path('tables/', include('apps.tables.image_loader.image_loader_urls')),

    path('tables/', include('apps.tables.images.images_urls')),

    path('tables/', include('apps.tables.unique_details.unique_details_urls')),
]

urlpatterns += static(settings.MEDIA_URL      , document_root=settings.MEDIA_ROOT     )
