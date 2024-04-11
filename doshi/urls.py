from django.contrib import admin
from django.urls import path, include, re_path  # Import re_path
from django.conf import settings
from django.conf.urls.static import static
from django.views.static import serve

urlpatterns = [
    path('doshi-admin/', admin.site.urls),
    path('', include('app.urls')),
    path('__debug__/', include('debug_toolbar.urls')),
]

urlpatterns += [
    re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
    re_path(r'^static/(?P<path>.*)$', serve, {'document_root': settings.STATIC_ROOT}),
]
