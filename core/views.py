# core/views.py

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from .models import Categoria, Pregunta, Respuesta

def home(request):
    # Renderiza la plantilla 'core/home.html'
    return render(request, 'core/home.html')


@login_required
def realizar_informe_visita(request):
    """
    Muestra todas las Categorías y Preguntas de la encuesta “Informe de Visita”.
    Permite subir evidencia y marcar SI/NO/NA. Al hacer POST, crea una Respuesta por cada pregunta respondida.
    """
    categorias = Categoria.objects.prefetch_related('preguntas').order_by('nombre').all()

    if request.method == 'POST':
        for cat in categorias:
            for preg in cat.preguntas.all():
                sel = request.POST.get(f"user_seleccion_{preg.id}")
                comentario = request.POST.get(f"user_comentario_{preg.id}", '').strip()
                evid_file = request.FILES.get(f"user_evidencia_{preg.id}")

                if sel or comentario or evid_file:
                    Respuesta.objects.create(
                        pregunta=preg,
                        seleccion=sel if sel else 'NA',
                        comentario=comentario if comentario else '',
                        evidencia=evid_file if evid_file else None
                    )

        return redirect(reverse('informe_gracias'))

    return render(request, 'core/informe_visita.html', {
        'categorias': categorias
    })


def informe_gracias(request):
    """
    Página sencilla de agradecimiento tras enviar el informe.
    """
    return render(request, 'core/informe_gracias.html')
