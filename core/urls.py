from django.urls import path
from . import views

urlpatterns = [
    path('',                          views.lista_encuestas,   name='lista_encuestas'),
    path('crear/',                    views.crear_encuesta,    name='crear_encuesta'),
    path('editar/<int:encuesta_id>/', views.editar_encuesta,   name='editar_encuesta'),
    path('asignar/<int:encuesta_id>/',views.asignar_encuesta,  name='asignar_encuesta'),
    path('eliminar/<int:encuesta_id>/', views.eliminar_encuesta, name='eliminar_encuesta'),
    path('mis/',                      views.mis_asignaciones,  name='mis_asignaciones'),
]
