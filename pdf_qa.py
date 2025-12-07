# pdf_qa.py
from groq import Groq
from dotenv import load_dotenv
import os
from pypdf import PdfReader

# Charger la clé API
load_dotenv()
GROQ_API_KEY = "votre cle api ici"  # Remplacez par votre clé API réelle ou utilisez os.getenv("GROQ_API_KEY")
client = Groq(api_key=GROQ_API_KEY)

def generate_qcm_from_pdf(pdf_path):
    """Lit un PDF et génère un QCM via l'API Groq."""

    # Lire le PDF
    reader = PdfReader(pdf_path)
    text = ""
    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            text += page_text + "\n"

    # Prompt correctement indenté
    prompt = f"""
Tu es un générateur de QCM.
Ta réponse doit être EXCLUSIVEMENT un JSON VALIDE. 
PAS de texte avant. PAS après. PAS de markdown. PAS de commentaires.

Répond EXACTEMENT sous cette forme :

{{
  "questions": [
    {{
      "question": "Texte de la question",
      "choices": ["A", "B", "C", "D"],
      "answer": "A"
    }}
  ]
}}

Génère EXACTEMENT 10 questions.
Utilise UNIQUEMENT le texte suivant :

{text}
"""


    # Appel à Groq
    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2,
        max_tokens=2000
    )

    # Retourner la réponse texte (JSON)
    return response.choices[0].message.content


# Test manuel
if __name__ == "__main__":
    pdf_path = input("Chemin du PDF : ")
    qcm = generate_qcm_from_pdf(pdf_path)
    print("\n=== QCM GÉNÉRÉ ===\n")
    print(qcm)
