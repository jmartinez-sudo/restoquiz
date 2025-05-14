from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Categoria, Pregunta, Respuesta, QuizAttempt, AttemptAnswer

@login_required
def home(request):
    return render(request, 'core/home.html', {'categorias': Categoria.objects.all()})

@login_required
def lista_categorias(request):
    return render(request, 'core/categoria_list.html', {'categorias': Categoria.objects.all()})

@login_required
def tomar_quiz(request):
    preguntas = Pregunta.objects.prefetch_related('respuestas').all()
    if request.method == 'POST':
        intento = QuizAttempt.objects.create(usuario=request.user, puntaje_total=0)
        total = 0
        for p in preguntas:
            rid = request.POST.get(f"pregunta_{p.id}")
            if rid:
                r = get_object_or_404(Respuesta, id=rid)
                total += r.puntaje * p.categoria.peso
                AttemptAnswer.objects.create(intento=intento, pregunta=p, respuesta=r)
        intento.puntaje_total = total
        intento.save()
        return redirect('resultado_quiz', intento.id)
    return render(request, 'core/quiz.html', {'preguntas': preguntas})

@login_required
def resultado_quiz(request, intento_id):
    intento = get_object_or_404(QuizAttempt, id=intento_id, usuario=request.user)
    breakdown = {}
    for ans in intento.answers.select_related('respuesta__pregunta__categoria'):
        cat = ans.pregunta.categoria.nombre
        breakdown[cat] = breakdown.get(cat, 0) + ans.respuesta.puntaje * ans.pregunta.categoria.peso
    return render(request, 'core/resultado_quiz.html', {'intento': intento, 'breakdown': breakdown.items()})
