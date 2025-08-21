from django.conf.urls.static import static
from django.contrib import admin
from clothes.views import *
from django.urls import path, include

from yanki import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include("clothes.urls")),
    path("accounts/", include("allauth.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_ROOT, document_root=settings.MEDIA_ROOT)

handler404 = pageNotFound

if settings.DEBUG:
    import debug_toolbar

    urlpatterns = [
                      path('__debug__/', include(debug_toolbar.urls)),
                  ] + urlpatterns
