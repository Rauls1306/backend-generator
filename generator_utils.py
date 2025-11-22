# generator_utils.py
import openai
from typing import List, Dict, Optional


def generate_apa_references(label: str, source_type: str = "cientifico") -> list:
    """
    Simula la generación de referencias APA a partir de un tema (label).
    En producción, esto se conectaría con una API real como Semantic Scholar.
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

def generate_textual_citations(texts: List[str]) -> List[str]:
    citations = []

    for text in texts:
        try:
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[
                    {
                        "role": "system",
                        "content": "Eres un experto en redacción académica. Tu tarea es insertar citas textuales apropiadas en formato APA 7."
                    },
                    {
                        "role": "user",
                        "content": f"Inserta 2 citas en formato APA 7 en el siguiente texto:\n\n{text}"
                    }
                ]
            )
            content = response.choices[0].message.content.strip()
            citations.append(content)
        except Exception as e:
            print("❌ Error generando citas:", e)
            citations.append("(Fuente simulada, 2024)")

    return citations

def insert_citations_into_text(text: str, citations: list) -> str:
    """
    Inserta citas en cada oración del texto, alternando entre narrativa y parentética.
    Si se repite una cita, divide en párrafos.
    """
    if not citations:
        print("⚠️ Advertencia: No hay citas para insertar en el texto.")
        return text

    sentences = text.split(". ")
    result = []
    used = set()
    current_para = []

    for i, sentence in enumerate(sentences):
        sentence = sentence.strip()
        if not sentence:
            continue

        citation = citations[i % len(citations)]

        if citation in used:
            result.append(". ".join(current_para) + ".")
            current_para = [f"{sentence} {citation}"]
            used = {citation}
        else:
            current_para.append(f"{sentence} {citation}")
            used.add(citation)

    if current_para:
        result.append(". ".join(current_para) + ".")

    return "\n\n".join(result)
def generate_references_from_citations(citations: List[str]) -> List[str]:
    try:
        joined = "\n".join(citations)
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {
                    "role": "system",
                    "content": "Eres un generador de referencias en formato APA 7. Devuelve solo la lista de referencias en formato correcto."
                },
                {
                    "role": "user",
                    "content": f"Genera las referencias bibliográficas en APA 7 a partir de estas citas:\n\n{joined}"
                }
            ]
        )
        return response.choices[0].message.content.strip().split("\n")
    except Exception as e:
        print("❌ Error generando referencias:", e)
        return ["Referencia simulada, 2024."]
