from django import forms
from .models import Categoria, Pregunta, Respuesta

class CategoriaForm(forms.ModelForm):
    class Meta:
        model = Categoria
        fields = ['nombre', 'peso']

class PreguntaForm(forms.ModelForm):
    class Meta:
        model = Pregunta
        fields = ['categoria', 'texto', 'archivo']

class RespuestaForm(forms.ModelForm):
    class Meta:
        model = Respuesta
        fields = ['texto', 'es_correcta', 'puntaje']
