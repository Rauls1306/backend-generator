# citation_generator.py

import re
from typing import List, Dict
from generator_utils import generate_apa_references, generate_textual_citations, insert_citations_into_text

class CitationGenerator:
    def __init__(self, title: str, generated_text: Dict[str, str]):
        self.title = title
        self.generated_text = generated_text  # Diccionario con claves como 'contexto', 'mundial', 'latam', 'peru', 'teoria1', etc.
        self.index = self._create_index()
        self.references_by_block = {}
        self.citations_by_block = {}

    def _create_index(self) -> Dict[str, str]:
        # Genera el índice auxiliar en base al título y al texto ya generado
        theme = self.title.lower()
        return {
            "problematica mundial": f"problematica {theme} mundial",
            "problematica latam": f"problematica {theme} latam",
            "problematica peru": f"problematica {theme} peru",
            "1 teoria": self.generated_text.get("teoria1_title", "1 teoria"),
            "2 teoria": self.generated_text.get("teoria2_title", "2 teoria"),
            "1 variable": self.generated_text.get("variable1_title", "1 variable"),
            "2 variable": self.generated_text.get("variable2_title", "2 variable"),
        }

    def generate_all_references(self):
        # Búsqueda automática de fuentes y generación de referencias APA
        for key, label in self.index.items():
            if "problematica" in key:
                self.references_by_block[key] = generate_apa_references(label, source_type="institucional")
            else:
                self.references_by_block[key] = generate_apa_references(label, source_type="cientifico")

    def generate_all_citations(self):
        # Genera las citas en formato textual (narrativas y parentéticas)
        for key, refs in self.references_by_block.items():
            self.citations_by_block[key] = generate_textual_citations(refs)

    def insert_all_citations(self) -> Dict[str, str]:
        # Inserta las citas en el texto generado, cumpliendo reglas de alternancia y estructura
        final_text = {}
        for block, text in self.generated_text.items():
            if block == "contexto":
                citations = self.citations_by_block.get("problematica mundial", [])
            elif block in ["mundial", "latam", "peru"]:
                key = f"problematica {block}"
                citations = self.citations_by_block.get(key, [])
            elif block.startswith("teoria"):
                key = f"{block[-1]} teoria"
                citations = self.citations_by_block.get(key, [])
            elif block.startswith("concepto1"):
                citations = self.citations_by_block.get("1 variable", [])
            elif block.startswith("concepto2"):
                citations = self.citations_by_block.get("2 variable", [])
            else:
                citations = []

            final_text[block] = insert_citations_into_text(text, citations)

        return final_text

    def get_references_list(self) -> List[str]:
        # Devuelve todas las referencias en formato APA ordenadas
        all_refs = []
        for block in self.references_by_block.values():
            all_refs.extend(block)
        return sorted(list(set(all_refs)))
