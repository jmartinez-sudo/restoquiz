from django.db import models
from django.contrib.auth.models import User

class Categoria(models.Model):
    nombre = models.CharField(max_length=100)
    peso = models.FloatField(default=1.0)
    def __str__(self): return self.nombre

class Pregunta(models.Model):
    categoria = models.ForeignKey(Categoria, related_name='preguntas', on_delete=models.CASCADE)
    texto = models.TextField()
    archivo = models.FileField(upload_to='preguntas/', blank=True, null=True)
    def __str__(self): return self.texto

class Respuesta(models.Model):
    pregunta = models.ForeignKey(Pregunta, related_name='respuestas', on_delete=models.CASCADE)
    texto = models.CharField(max_length=255)
    es_correcta = models.BooleanField(default=False)
    puntaje = models.IntegerField(default=1)
    def __str__(self): return self.texto

class QuizAttempt(models.Model):
    usuario = models.ForeignKey(User, related_name='intentos', on_delete=models.CASCADE)
    fecha = models.DateTimeField(auto_now_add=True)
    puntaje_total = models.FloatField()
    def __str__(self): return f"{self.usuario.username} @ {self.fecha:%Y-%m-%d %H:%M}"

class AttemptAnswer(models.Model):
    intento = models.ForeignKey(QuizAttempt, related_name='answers', on_delete=models.CASCADE)
    pregunta = models.ForeignKey(Pregunta, on_delete=models.CASCADE)
    respuesta = models.ForeignKey(Respuesta, on_delete=models.CASCADE)
    adjunto = models.FileField(upload_to='attempts/', blank=True, null=True)
