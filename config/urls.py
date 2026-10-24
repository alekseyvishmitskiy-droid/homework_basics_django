"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://djangoproject.com
"""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns  # Импортируем авто-раздатчик статики Django

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('catalog.urls', namespace='catalog')),
    path('blog/', include('blog.urls', namespace='blog')),
    path('users/', include('users.urls', namespace='users')),
]

# Жестко прописываем раздачу медиафайлов (картинок)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# Автоматически склеиваем и принудительно раздаем все CSS/JS файлы из STATICFILES_DIRS
urlpatterns += staticfiles_urlpatterns()
