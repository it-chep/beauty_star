from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include, re_path
from django.views.static import serve

handler404 = 'main_site.views.page_400'
handler500 = 'main_site.views.page_500'

urlpatterns = [
    path('admin/', admin.site.urls),
    re_path(r'^grappelli/', include('grappelli.urls')),

    path('', include('main_site.urls'))
]

if not settings.DEBUG:
    urlpatterns += [
        re_path(r'^static/(?P<path>.*)$', serve, {'document_root': settings.STATIC_ROOT}),
        re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
    ]
else:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


