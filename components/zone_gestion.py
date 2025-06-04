# zone_gestion.py – Zone 1 : Gestion du bot (Éditeur IA intelligent)

import streamlit as st
import os
from pathlib import Path
import difflib
import json
import requests

# === CONFIGURATION ===
IA_LOCAL_URL = os.getenv("LOCAL_IA_URL", "http://localhost:5000/analyse")
DOSSIER_BOT = Path(".")  # À adapter si nécessaire

# === UI ===
st.subheader("🧠 Zone 1 – Éditeur IA intelligent")
st.caption("Modifie les fichiers .py, .json, .env avec assistance IA.")

# === 1. Choix du fichier à modifier ===
fichiers = list(DOSSIER_BOT.rglob("*.py")) + list(DOSSIER_BOT.rglob("*.json")) + list(DOSSIER_BOT.rglob("*.env"))
noms_fichiers = [str(f.relative_to(DOSSIER_BOT)) for f in fichiers]

choix_fichier = st.selectbox("📄 Sélectionne un fichier à modifier", noms_fichiers)
chemin_fichier = DOSSIER_BOT / choix_fichier

if chemin_fichier.exists():
    contenu_original = chemin_fichier.read_text(encoding="utf-8")
    contenu_modifie = st.text_area("✏️ Code actuel (modifiable)", value=contenu_original, height=300)

    # === 2. Demande IA de modification ===
    prompt_ia = st.text_area("🧠 Que veux-tu que l’IA modifie ? (ex: Ajoute un print au début)")
    if st.button("🤖 Proposer une modification IA"):
        try:
            r = requests.post(IA_LOCAL_URL, json={
                "prompt": prompt_ia,
                "fichier": choix_fichier,
                "contenu": contenu_original
            })
            if r.ok:
                data = r.json()
                nouvelle_version = data.get("resultat", contenu_original)
                diff = difflib.HtmlDiff().make_table(
                    contenu_original.splitlines(),
                    nouvelle_version.splitlines(),
                    fromdesc="Original",
                    todesc="Modifié par IA"
                )
                st.markdown("✅ Modification proposée :")
                st.components.v1.html(diff, height=400, scrolling=True)

                if st.button("💾 Appliquer la modification IA", key="appliquer_ia"):
                    chemin_fichier.write_text(nouvelle_version, encoding="utf-8")
                    st.success("Fichier mis à jour avec la proposition IA.")
            else:
                st.error(f"Erreur IA : {r.text}")
        except Exception as e:
            st.error(f"❌ Erreur de requête IA : {e}")

# === 3. Boutons de maintenance ===
st.markdown("---")
st.caption("🛠️ Outils de maintenance du bot")
col1, col2, col3 = st.columns(3)

with col1:
    if st.button("🧹 Nettoyer les fichiers __pycache__"):
        for root, dirs, files in os.walk(DOSSIER_BOT):
            for d in dirs:
                if d == "__pycache__":
                    pyc_path = Path(root) / d
                    for file in pyc_path.glob("*.*"):
                        file.unlink()
                    pyc_path.rmdir()
        st.success("Caches Python supprimés.")

with col2:
    if st.button("🔁 Recharger l’IA"):
        st.info("Rechargement simulé. Implémenter si nécessaire.")

with col3:
    if st.button("🔍 Scanner fichiers manquants"):
        st.warning("Fonction à implémenter : lister les fichiers attendus mais absents.")
