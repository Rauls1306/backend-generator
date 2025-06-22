# generator_utils.py

import random

def generate_apa_references(label: str, source_type: str = "cientifico") -> list:
    """
    Simula la búsqueda de referencias reales según el tema (label) y tipo de fuente.
    En producción esto se conectaría con una API real como Semantic Scholar o Google Scholar.
    """
    if source_type == "institucional":
        return [
            f"World Health Organization. (2023). {label.capitalize()}. Geneva: WHO.",
            f"UNESCO. (2022). {label.capitalize()} in Latin America. Paris: UNESCO.",
            f"OECD. (2024). Global Report on {label.capitalize()}. OECD Publishing.",
            f"UNICEF. (2023). Challenges of {label.lower()} in vulnerable populations."
        ]
    else:
        return [
            f"Smith, J. (2023). Advances in {label.lower()} research. Journal of Applied Sciences, 45(3), 120–134.",
            f"Lopez, M. & Wang, Y. (2022). Perspectives on {label.lower()} in modern education. Educational Review, 39(2), 88–101.",
            f"Kumar, R. (2021). Conceptual analysis of {label.lower()}. International Journal of Research, 12(4), 55–70."
        ]

def generate_textual_citations(apa_list: list) -> list:
    """
    Alterna entre citas narrativas y parentéticas a partir de una lista APA.
    """
    citations = []
    for i, ref in enumerate(apa_list):
        author = ref.split(".")[0]
        year = ref.split("(")[1].split(")")[0]
        if i % 2 == 0:
            citations.append(f"Además, {author} ({year})")
        else:
            citations.append(f"({author}, {year})")
    return citations

def insert_citations_into_text(text: str, citations: list) -> str:
    """
    Inserta una cita por oración, alternando entre narrativa y parentética,
    dividiendo el párrafo si se repite una cita.
    """
    sentences = text.split(". ")
    result = []
    used = set()
    current_para = []

    for i, sentence in enumerate(sentences):
        if not sentence.strip():
            continue

        citation = citations[i % len(citations)]

        if citation in used:
            result.append(". ".join(current_para) + ".")
            current_para = [f"{sentence.strip()} {citation}"]
            used = {citation}
        else:
            current_para.append(f"{sentence.strip()} {citation}")
            used.add(citation)

    if current_para:
        result.append(". ".join(current_para) + ".")

    return "\n\n".join(result)
