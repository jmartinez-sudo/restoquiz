# core/urls.py

from django.urls import path
from . import views

urlpatterns = [
    # Página de inicio
    path('', views.home, name='home'),

    # Rutas para el Informe de Visita
    path('informe-visita/', views.realizar_informe_visita, name='informe_visita'),
    path('informe-visita/gracias/', views.informe_gracias, name='informe_gracias'),

    # (No definimos rutas relacionadas a 'Encuesta' porque por ahora no existe ese modelo)
]
