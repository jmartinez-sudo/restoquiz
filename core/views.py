from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from .decorators import group_required
from .models import (
    Categoria, Pregunta, Respuesta,
    QuizAttempt, AttemptAnswer, Encuesta
)
from .forms import (
    CategoriaForm, PreguntaForm, RespuestaForm,
    EncuestaForm, AsignarEncuestaForm
)

@login_required
def home(request):
    return render(request, 'core/home.html')

@login_required
def lista_encuestas(request):
    encuestas = Encuesta.objects.order_by('-fecha_creacion')
    return render(request, 'core/encuesta_list.html', {'encuestas': encuestas})

@login_required
@group_required('Casa Matriz')
def crear_encuesta(request):
    if request.method == 'POST':
        form = EncuestaForm(request.POST)
        if form.is_valid():
            encuesta = form.save(commit=False)
            encuesta.creador = request.user
            encuesta.save()
            form.save_m2m()
            return redirect('lista_encuestas')
    else:
        form = EncuestaForm()
    return render(request, 'core/crear_encuesta.html', {'form': form})

@login_required
@group_required('Casa Matriz')
def editar_encuesta(request, encuesta_id):
    encuesta = get_object_or_404(Encuesta, pk=encuesta_id)
    if not (request.user.is_superuser or request.user.groups.filter(name='Casa Matriz').exists()):
        return HttpResponseForbidden()
    if request.method == 'POST':
        form = EncuestaForm(request.POST, instance=encuesta)
        if form.is_valid():
            form.save()
            return redirect('lista_encuestas')
    else:
        form = EncuestaForm(instance=encuesta)
    return render(request, 'core/editar_encuesta.html', {
        'form': form,
        'encuesta': encuesta
    })

@login_required
@group_required('Casa Matriz')
def asignar_encuesta(request, encuesta_id):
    encuesta = get_object_or_404(Encuesta, pk=encuesta_id)
    if request.method == 'POST':
        form = AsignarEncuestaForm(request.POST, instance=encuesta)
        if form.is_valid():
            form.save()
            return redirect('lista_encuestas')
    else:
        form = AsignarEncuestaForm(instance=encuesta)
    return render(request, 'core/asignar_encuesta.html', {
        'form': form,
        'encuesta': encuesta
    })

@login_required
@group_required('Casa Matriz')
def eliminar_encuesta(request, encuesta_id):
    encuesta = get_object_or_404(Encuesta, pk=encuesta_id)
    # Solo superuser o Casa Matriz pueden eliminar
    if not (request.user.is_superuser or request.user.groups.filter(name='Casa Matriz').exists()):
        return HttpResponseForbidden()
    if request.method == 'POST':
        encuesta.delete()
        return redirect('lista_encuestas')
    return render(request, 'core/eliminar_encuesta.html', {
        'encuesta': encuesta
    })

@login_required
@group_required('Auditor')
def mis_asignaciones(request):
    from django.db.models import Q
    grupos = request.user.groups.values_list('pk', flat=True)
    encuestas = Encuesta.objects.filter(
        Q(assigned_users=request.user) |
        Q(assigned_groups__in=grupos)
    ).distinct()
    return render(request, 'core/mis_asignaciones.html', {
        'encuestas': encuestas
    })

# …tus vistas de Quiz y Resultado siguen igual…
