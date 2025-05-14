from django.urls import path
from .views import home, tomar_quiz, resultado_quiz, lista_categorias

urlpatterns = [
    path('', home, name='home'),
    path('categorias/', lista_categorias, name='lista_categorias'),
    path('quiz/', tomar_quiz, name='tomar_quiz'),
    path('quiz/<int:intento_id>/resultado/', resultado_quiz, name='resultado_quiz'),
]
