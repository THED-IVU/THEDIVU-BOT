# guardian_admin_v2.py – Tableau de bord intelligent IA en 3 zones

import streamlit as st
from pathlib import Path
import sys
import os

# === Configuration initiale ===
ROOT_DIR = Path(__file__).resolve().parent
if str(ROOT_DIR) not in sys.path:
    sys.path.append(str(ROOT_DIR))

# === Chargement dynamique des modules de zones ===
from zone_gestion import *  # Zone 1 – Gestion du bot (éditeur IA intelligent)

# === UI globale ===
st.set_page_config(page_title="🛡️ Guardian IA v2 – Interface dynamique", layout="wide")
st.title("🛡️ Interface Guardian IA – Version Dynamique")

# === Navigation latérale ===
zones = {
    "🧠 Zone 1 – Gestion du bot": "zone1",
    "📈 Zone 2 – Fonctions de trading": "zone2",
    "🌐 Zone 3 – Connexions IA & plateformes": "zone3"
}

choix_zone = st.sidebar.radio("📌 Choisir une zone IA à afficher :", list(zones.keys()))
st.sidebar.markdown("---")
st.sidebar.info("Mode intelligent : l’IA propose, vous validez.")

# === Navigation par zone ===
if zones[choix_zone] == "zone1":
    st.header("🧠 Zone 1 – Gestion du bot")
    # Le module zone_gestion.py s'exécute automatiquement à l'import

elif zones[choix_zone] == "zone2":
    st.header("📈 Zone 2 – Fonctions de trading (à venir)")
    st.info("🛠️ Module en cours de développement.")

elif zones[choix_zone] == "zone3":
    st.header("🌐 Zone 3 – Connexions IA & plateformes (à venir)")
    st.info("🛠️ Module en cours de développement.")
