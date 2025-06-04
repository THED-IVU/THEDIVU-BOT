# ai_router.py – Redirection IA locale > fallback OpenAI / Gemini

import os
import requests
import openai
from google.generativeai import GenerativeModel
import google.generativeai as genai

# Chargement des clés depuis .env
LOCAL_IA_URL = os.getenv("LOCAL_IA_URL", "http://localhost:5000/analyse")
FALLBACK = os.getenv("PREFERED_AI_FALLBACK", "openai")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")

# Setup OpenAI
if OPENAI_API_KEY:
    openai.api_key = OPENAI_API_KEY

# Setup Gemini
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)

def appel_ia(prompt: str, context: str = ""):
    """ Appelle l'IA locale, puis fallback si erreur """
    # 1. Essai IA locale
    try:
        r = requests.post(LOCAL_IA_URL, json={"prompt": prompt, "contexte": context}, timeout=10)
        if r.ok:
            data = r.json()
            return data.get("resultat", ""), "ia_locale"
    except Exception as e:
        pass  # Passer au fallback

    # 2. Fallback IA
    if FALLBACK == "openai" and OPENAI_API_KEY:
        try:
            completion = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}]
            )
            return completion.choices[0].message.content.strip(), "openai"
        except Exception as e:
            return f"Erreur OpenAI : {e}", "openai"

    elif FALLBACK == "gemini" and GEMINI_API_KEY:
        try:
            model = GenerativeModel("gemini-pro")
            response = model.generate_content(prompt)
            return response.text.strip(), "gemini"
        except Exception as e:
            return f"Erreur Gemini : {e}", "gemini"

    return "Aucune IA n'est disponible ou valide.", "aucune"

# Exemple d'appel (pour tests manuels uniquement)
if __name__ == "__main__":
    result, source = appel_ia("Quelle est la tendance du marché EURUSD ?")
    print(f"[{source}] {result}")