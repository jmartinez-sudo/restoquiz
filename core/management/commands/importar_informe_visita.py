# core/management/commands/importar_visita.py

import re
import pandas as pd
from django.core.management.base import BaseCommand
from core.models import Categoria, Pregunta  # Ajusta a tus modelos reales

class Command(BaseCommand):
    help = "Importa categorías y preguntas desde el Excel de Informe de Visita"

    def add_arguments(self, parser):
        parser.add_argument(
            "--ruta",
            type=str,
            help="Ruta al archivo Excel (con el nombre y extensión)",
            default="INFORME DE VISITA  MODIFICADO (002).xlsx"
        )
        parser.add_argument(
            "--hoja",
            type=str,
            help="Nombre de la hoja en el Excel",
            default="Informe de visita"
        )

    def handle(self, *args, **options):
        ruta_excel = options["ruta"]
        hoja = options["hoja"]

        # 1) Leemos TODO el contenido sin asumir encabezados en pandas:
        df = pd.read_excel(ruta_excel, sheet_name=hoja, header=None)

        categoria_actual = None
        total_categ = 0
        total_preg = 0

        # 2) Iteramos cada fila para detectar categorías y preguntas
        for idx, fila in df.iterrows():
            celda_col1 = str(fila[1]) if not pd.isna(fila[1]) else ""
            celda_col2 = str(fila[2]) if not pd.isna(fila[2]) else ""

            # 2.1) Si coincide con patrón de categoría (ej: "1.- CONTROL DOCUMENTAL")
            if re.match(r"^\d+\.\-\s*", celda_col1):
                # Extraemos solo el nombre de la categoría
                nombre_cat = re.sub(r"^\d+\.\-\s*", "", celda_col1).strip()
                if nombre_cat:
                    categoria_actual, creado = Categoria.objects.get_or_create(
                        nombre=nombre_cat
                    )
                    total_categ += 1

            # 2.2) Si coincide con patrón de pregunta (ej: "1.1", "2.3", "4.10", etc.)
            elif re.match(r"^\d+\.\d+", celda_col1):
                texto_preg = celda_col2.strip()
                # Nos aseguramos de tener una categoría padre ya creada
                if categoria_actual and texto_preg:
                    Pregunta.objects.create(
                        categoria=categoria_actual,
                        texto=texto_preg
                        # Si tu modelo de Pregunta tiene más campos (peso, tipo, etc.), agrégalos acá.
                    )
                    total_preg += 1

            # 2.3) Si no coincide con ninguno, lo ignoramos (otros bloques como "TOTAL", "OBSERVACIONES", etc.)

        self.stdout.write(
            self.style.SUCCESS(
                f"Fin de importación: {total_categ} categorías y {total_preg} preguntas agregadas."
            )
        )
