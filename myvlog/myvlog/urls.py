from django.urls import path, include
from django.contrib import admin
from debug_toolbar.toolbar import debug_toolbar_urls


urlpatterns = [
    path("admin/", admin.site.urls),
    path('', include('vlog.urls')),
    path('users/', include('users.urls', namespace='users')),
] + debug_toolbar_urls()
