from django.contrib import admin
from django.conf.urls import url, include
from . import views
from JazzBluesApp import views as JazzBluesAppViews
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^accounts/', include('accounts.urls')),
    url(r'^JazzBlues/', include('JazzBluesApp.urls')),
    url(r'^$', JazzBluesAppViews.albums, name="home"), #homepage & logout
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
