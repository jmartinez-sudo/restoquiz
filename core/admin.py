# core/admin.py

from django.contrib import admin
from .models import Categoria, Pregunta, Respuesta

@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'peso')
    search_fields = ('nombre',)


@admin.register(Pregunta)
class PreguntaAdmin(admin.ModelAdmin):
    list_display = ('orden', 'texto', 'categoria')
    list_filter = ('categoria',)
    search_fields = ('texto', 'orden')
    raw_id_fields = ('categoria',)
    readonly_fields = ('orden',)  # O quítalo si quieres editar el orden desde el admin


@admin.register(Respuesta)
class RespuestaAdmin(admin.ModelAdmin):
    list_display = ('pregunta', 'seleccion', 'fecha_respuesta')
    list_filter = ('seleccion', 'pregunta__categoria', 'fecha_respuesta')
    search_fields = ('pregunta__texto',)
    raw_id_fields = ('pregunta',)
    readonly_fields = ('fecha_respuesta',)
