from django import forms
from django.contrib.auth.models import Group
from .models import (
    Categoria, Pregunta, Respuesta,
    QuizAttempt, AttemptAnswer, Encuesta
)

class CategoriaForm(forms.ModelForm):
    class Meta:
        model = Categoria
        fields = '__all__'

class PreguntaForm(forms.ModelForm):
    class Meta:
        model = Pregunta
        fields = '__all__'

class RespuestaForm(forms.ModelForm):
    class Meta:
        model = Respuesta
        fields = '__all__'

class EncuestaForm(forms.ModelForm):
    class Meta:
        model = Encuesta
        fields = ['nombre', 'descripcion', 'supervisores', 'auditores', 'tiendas']

class AsignarEncuestaForm(forms.ModelForm):
    # Personaliza etiquetas si quieres:
    assigned_users = forms.ModelMultipleChoiceField(
        queryset=Encuesta._meta.get_field('assigned_users').remote_field.model.objects.all(),
        required=False,
        label="Usuarios asignados"
    )
    assigned_groups = forms.ModelMultipleChoiceField(
        queryset=Group.objects.all(),
        required=False,
        label="Grupos asignados"
    )

    class Meta:
        model = Encuesta
        fields = ['assigned_users', 'assigned_groups']
