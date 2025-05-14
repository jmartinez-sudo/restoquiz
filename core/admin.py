from django.contrib import admin
from .models import Categoria, Pregunta, Respuesta, QuizAttempt, AttemptAnswer

@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'peso')

@admin.register(Pregunta)
class PreguntaAdmin(admin.ModelAdmin):
    list_display = ('texto', 'categoria')

@admin.register(Respuesta)
class RespuestaAdmin(admin.ModelAdmin):
    list_display = ('texto', 'pregunta', 'es_correcta', 'puntaje')
    list_filter  = ('pregunta__categoria',)

@admin.register(QuizAttempt)
class QuizAttemptAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'fecha', 'puntaje_total')

@admin.register(AttemptAnswer)
class AttemptAnswerAdmin(admin.ModelAdmin):
    list_display = ('intento', 'pregunta', 'respuesta')
