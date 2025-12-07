# 1) Importer les librairies nécessaires
from groq import Groq
from dotenv import load_dotenv
import os
from pypdf import PdfReader

# 2) Charger la clé API depuis .env
load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

client = Groq(api_key=GROQ_API_KEY)

# 3) Lire le PDF
pdf_path = input("Chemin du PDF : ")
reader = PdfReader(pdf_path)

text = ""
for page in reader.pages:
    text += page.extract_text()

# 4) Préparer le prompt
prompt = f"""
Tu es un générateur de QCM.
A partir de ce texte extrait du PDF, génère 3 questions QCM différentes.
Chaque question doit comporter :
- 4 choix (A, B, C, D)
- La réponse correcte clairement indiquée à la fin

Texte du PDF :
{text}
"""

# 5) Appel à Groq
response = client.chat.completions.create(
    model="llama-3.1-8b-instant",
    messages=[
        {"role": "user", "content": prompt}
    ],
    temperature=0.2
)

# 6) Afficher la réponse
print("\n=== QCM GENERÉ ===\n")
print(response.choices[0].message.content)

# **Question 2**