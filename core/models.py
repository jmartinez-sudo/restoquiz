# core/models.py

from django.db import models
from django.contrib.auth.models import User, Group

class Categoria(models.Model):
    # Cada bloque de tu “Informe de Visita” (ej: “1. CONTROL DOCUMENTAL”, “2. SEÑALÉTICAS / BOTIQUÍN”, etc.)
    nombre = models.CharField(max_length=100, unique=True)
    peso = models.FloatField(default=1.0)  # Si en algún momento quieres ponderar categorías

    def __str__(self):
        return self.nombre


class Pregunta(models.Model):
    # Relación con la categoría (bloque). Cuando importemos, creamos tantas Pregunta como filas en tu CSV.
    categoria = models.ForeignKey(
        Categoria,
        related_name='preguntas',
        on_delete=models.CASCADE
    )
    # Texto completo de la pregunta (ej: “EXISTENCIA DE CONTRATO DE TRABAJO POR LA TOTALIDAD…”)
    texto = models.TextField()

    # Ayuda visual: foto o video explicativo de qué debe revisarse en esa pregunta.
    # Queda opcional (blank=True, null=True); desde el CSV inicial no lo llenamos, pero
    # al crear manualmente en el Admin sí podrías subir el PDF o imagen.
    ayuda_visual = models.FileField(
        upload_to='ayudas_preguntas/',
        blank=True,
        null=True,
        help_text="Opcional: sube aquí una foto o video que explique cómo evaluar esta pregunta"
    )

    # Para identificar el orden (“1.1”, “1.2”, “2.3”…), y facilitar el CSV importador.
    orden = models.CharField(
        max_length=10,
        blank=True,
        null=True,
        help_text="Ej: 1.1, 1.2, 2.1…"
    )

    def __str__(self):
        display = f"{self.orden + ' - ' if self.orden else ''}{self.texto}"
        return display[:50] + ("..." if len(display) > 50 else "")


class Respuesta(models.Model):
    # Cada vez que un usuario completo la encuesta, se crea una Respuesta
    pregunta = models.ForeignKey(
        Pregunta,
        related_name='respuestas',
        on_delete=models.CASCADE
    )

    # Selección: SI / NO / NA
    OPCIONES = [
        ('SI', 'SI'),
        ('NO', 'NO'),
        ('NA', 'NA'),
    ]
    seleccion = models.CharField(
        max_length=2,
        choices=OPCIONES,
        default='NA'
    )

    # Observaciones adicionales (el texto que el usuario escribe junto a la pregunta)
    comentario = models.TextField(
        blank=True,
        null=True,
        help_text="Puedes dejar una observación o detalle extra aquí"
    )

    # Evidencia: foto o video que sube el usuario al responder (ej: foto de la inspección)
    evidencia = models.FileField(
        upload_to='evidencias_respuestas/',
        blank=True,
        null=True,
        help_text="Sube aquí la foto o video como evidencia de tu respuesta"
    )

    fecha_respuesta = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.pregunta.orden} → {self.seleccion}"


# (En tu proyecto original tal vez tengas otros modelos – aquí sólo aparecen
#  los que conciernen a las encuestas y checklist. Deja el resto de tu código intacto.)
