from django.contrib import admin
from django.urls import path, include,re_path
from django.conf.urls.static import static
from django.conf import settings
from django.views.static import serve
from django.contrib.auth import views as auth_views
from recipes.views import handler404

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('recipes.urls')),
    re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    re_path(r'^static/(?P<path>.*)$', serve, {'document_root': settings.STATIC_ROOT}), 
]
handler404 = handler404