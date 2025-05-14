# Restoquiz/urls.py
from django.contrib import admin
from django.urls import path, include
from core import views as core_views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),

    # Página de inicio (home) — para que {% url 'home' %} funcione
    path('', core_views.home, name='home'),

    # Autenticación de Django
    path('accounts/', include('django.contrib.auth.urls')),

    # Encuestas (todas las rutas: lista, crear, asignar)
    path('encuestas/', include('core.urls')),
]

# En dev, servir media y static
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
