# citation_generator.py
from typing import List, Dict
from generator_utils import generate_textual_citations, insert_citations_into_text

class CitationGenerator:
    def __init__(self, title: str, generated_text: Dict[str, str]):
        self.title = title
        self.generated_text = generated_text
        self.citations_by_block = {}

    def generate_all_citations(self):
        for key, text in self.generated_text.items():
            if not isinstance(text, str):
                print(f"❌ Error: el texto del bloque '{key}' no es string.")
                continue
            self.citations_by_block[key] = generate_textual_citations([text])

    def insert_all_citations(self) -> Dict[str, str]:
        final_text = {}

        for key, text in self.generated_text.items():
            if not isinstance(text, str):
                print(f"❌ Error: el texto del bloque '{key}' no es string.")
                continue

            citations = self.citations_by_block.get(key, [])

            if not citations:
                print(f"⚠️ Advertencia: No hay citas para el bloque '{key}'. Usando cita simulada.")
                citations = ["(Fuente simulada, 2024)"]

            try:
                final_text[key] = insert_citations_into_text(text, citations)
            except Exception as e:
                print(f"❌ Error al insertar citas en '{key}': {e}")
                final_text[key] = text

        return final_text
