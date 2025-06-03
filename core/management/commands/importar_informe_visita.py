# core/management/commands/importar_informe_visita.py

import csv
import os
from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from core.models import Categoria, Pregunta

class Command(BaseCommand):
    help = (
        "Importa la encuesta 'Informe de Visita' desde un CSV "
        "y crea Categorías y Preguntas en la BD."
    )

    def add_arguments(self, parser):
        parser.add_argument(
            '--csv',
            dest='csv_path',
            help='Ruta al archivo CSV, relativo a la base del proyecto. '
                 'Ejemplo: data/encuesta_informe_visita.csv'
        )

    def handle(self, *args, **options):
        csv_path = options.get('csv_path')
        if not csv_path:
            raise CommandError("Debes indicar la ruta al CSV usando --csv <ruta>")

        # Construimos la ruta absoluta
        full_path = os.path.join(settings.BASE_DIR, csv_path)
        if not os.path.exists(full_path):
            raise CommandError(f"El archivo no existe en {full_path}")

        created_cats = 0
        created_qs = 0

        with open(full_path, newline='', encoding='utf-8') as csvfile:
            lector = csv.DictReader(csvfile)
            for fila in lector:
                orden = fila.get('orden', '').strip()
                nombre_cat = fila.get('categoria', '').strip()
                texto_pregunta = fila.get('pregunta', '').strip()

                if not nombre_cat or not texto_pregunta:
                    self.stdout.write(self.style.WARNING(
                        f"  • Fila incompleta, se salta: {fila}"
                    ))
                    continue

                # 1. Obtener o crear la categoría
                cat_obj, cat_created = Categoria.objects.get_or_create(
                    nombre=nombre_cat
                )
                if cat_created:
                    created_cats += 1
                    self.stdout.write(self.style.SUCCESS(
                        f"  ➤ Creada categoría: '{nombre_cat}'"
                    ))

                # 2. Si ya existe esa pregunta con el mismo orden, no duplicar
                existe_preg = Pregunta.objects.filter(
                    categoria=cat_obj,
                    orden=orden
                ).exists()
                if existe_preg:
                    self.stdout.write(self.style.NOTICE(
                        f"  • Pregunta con orden {orden} ya existe en '{nombre_cat}'"
                    ))
                    continue

                # 3. Crear la pregunta nueva
                nueva_preg = Pregunta.objects.create(
                    categoria=cat_obj,
                    texto=texto_pregunta,
                    orden=orden
                )
                created_qs += 1
                self.stdout.write(self.style.SUCCESS(
                    f"  ➤ Creada pregunta [{orden}] en '{nombre_cat}': {texto_pregunta[:50]}..."
                ))

        self.stdout.write(self.style.SUCCESS(
            f"\n✅ Import terminado: {created_cats} categoría(s) creadas, "
            f"{created_qs} pregunta(s) creadas."
        ))
