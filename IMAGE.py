import streamlit as st
import pandas as pd
from datetime import datetime, time
import os
import requests
from filelock import FileLock
import shutil
import socket
import json

# =============================================================================
# 1. CONFIGURATION GLOBALE
# =============================================================================
st.set_page_config(
    page_title="📊 Suivi CQ-2026",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---- STYLE CSS ----
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
    
    * {
        font-family: 'Inter', sans-serif;
        margin: 0;
        padding: 0;
        box-sizing: border-box;
    }
    
    .stApp {
        background: #f0f2f5 !important;
    }
    
    .stApp > header {
        background: rgba(255,255,255,0.8) !important;
        backdrop-filter: blur(10px) !important;
        border-bottom: 1px solid #e8ecf0 !important;
    }
    
    .login-bg {
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        z-index: 0;
        background: linear-gradient(135deg, #e8ecf0 0%, #d5dbe3 50%, #c8d0dc 100%);
        overflow: hidden;
    }
    
    .deco-circle {
        position: absolute;
        border-radius: 50%;
        background: rgba(74, 108, 247, 0.04);
    }
    .deco-circle:nth-child(1) { width: 300px; height: 300px; top: -100px; right: -100px; }
    .deco-circle:nth-child(2) { width: 200px; height: 200px; bottom: -50px; left: -50px; }
    .deco-circle:nth-child(3) { width: 150px; height: 150px; top: 50%; left: 10%; }
    
    .login-wrapper {
        position: relative;
        z-index: 10;
        display: flex;
        justify-content: center;
        align-items: center;
        min-height: 100vh;
        padding: 20px;
    }
    
    .login-box {
        background: rgba(255, 255, 255, 0.95);
        backdrop-filter: blur(20px);
        border-radius: 24px;
        padding: 40px 36px;
        max-width: 420px;
        width: 100%;
        box-shadow: 0 20px 60px rgba(0,0,0,0.08);
        border: 1px solid rgba(255,255,255,0.5);
        animation: slideUp 0.6s ease-out;
    }
    
    @keyframes slideUp {
        from { opacity: 0; transform: translateY(30px) scale(0.97); }
        to { opacity: 1; transform: translateY(0) scale(1); }
    }
    
    .login-logo {
        text-align: center;
        margin-bottom: 28px;
    }
    
    .login-logo .icon {
        font-size: 48px;
        display: block;
        margin-bottom: 6px;
    }
    
    .login-logo h1 {
        font-size: 24px;
        font-weight: 800;
        color: #1a202c;
        margin: 0;
        letter-spacing: -0.5px;
    }
    
    .login-logo h1 span {
        background: linear-gradient(135deg, #4a6cf7 0%, #6a3de8 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    
    .login-logo p {
        color: #718096;
        font-size: 14px;
        margin: 4px 0 0 0;
    }
    
    .login-field {
        margin-bottom: 16px;
    }
    
    .login-field label {
        display: block;
        font-size: 13px;
        font-weight: 600;
        color: #4a5568;
        margin-bottom: 5px;
    }
    
    .login-field .stSelectbox,
    .login-field .stTextInput {
        border-radius: 10px !important;
        border: 2px solid #e2e8f0 !important;
        transition: all 0.3s !important;
        background: white !important;
    }
    
    .login-field .stSelectbox:focus,
    .login-field .stTextInput:focus {
        border-color: #4a6cf7 !important;
        box-shadow: 0 0 0 4px rgba(74, 108, 247, 0.08) !important;
    }
    
    .login-field .stTextInput input {
        padding: 10px 14px !important;
        font-size: 14px !important;
    }
    
    .login-btn {
        background: linear-gradient(135deg, #4a6cf7 0%, #6a3de8 100%) !important;
        color: white !important;
        border: none !important;
        padding: 12px !important;
        border-radius: 10px !important;
        font-weight: 700 !important;
        font-size: 15px !important;
        width: 100% !important;
        letter-spacing: 0.5px !important;
        box-shadow: 0 4px 16px rgba(74, 108, 247, 0.25) !important;
        transition: all 0.3s !important;
        cursor: pointer !important;
        margin-top: 4px !important;
    }
    
    .login-btn:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 28px rgba(74, 108, 247, 0.35) !important;
    }
    
    .login-footer {
        text-align: center;
        margin-top: 20px;
        padding-top: 16px;
        border-top: 1px solid #edf2f7;
        font-size: 13px;
        color: #a0aec0;
    }
    
    .login-footer .name {
        background: linear-gradient(135deg, #4a6cf7 0%, #6a3de8 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 700;
    }
    
    .css-1d391kg {
        background: linear-gradient(180deg, #1a202c 0%, #2d3748 100%) !important;
        border-right: none !important;
    }
    
    .sidebar-user {
        text-align: center;
        padding: 16px 0 12px 0;
        border-bottom: 1px solid rgba(255,255,255,0.06);
    }
    
    .sidebar-user .avatar {
        font-size: 44px;
        margin-bottom: 2px;
    }
    
    .sidebar-user .role {
        font-size: 17px;
        font-weight: 700;
        color: white;
    }
    
    .sidebar-user .sub {
        font-size: 12px;
        color: #a0aec0;
    }
    
    .glass-card {
        background: white;
        border-radius: 16px;
        padding: 24px;
        box-shadow: 0 2px 12px rgba(0,0,0,0.04);
        border: 1px solid #e8ecf0;
        margin-bottom: 20px;
        transition: all 0.2s;
    }
    
    .glass-card:hover {
        box-shadow: 0 4px 24px rgba(0,0,0,0.06);
    }
    
    .card-header {
        display: flex;
        align-items: center;
        gap: 10px;
        margin-bottom: 16px;
        padding-bottom: 12px;
        border-bottom: 2px solid #f0f2f5;
    }
    
    .card-header .icon {
        font-size: 22px;
    }
    
    .card-header h2 {
        font-weight: 700;
        font-size: 18px;
        color: #1a202c;
        margin: 0;
    }
    
    .metrics-grid {
        display: grid;
        grid-template-columns: repeat(6, 1fr);
        gap: 12px;
        margin: 12px 0 8px 0;
    }
    
    .metric-card {
        background: white;
        border-radius: 12px;
        padding: 14px 10px;
        text-align: center;
        border: 1px solid #edf2f7;
        transition: all 0.2s;
        box-shadow: 0 1px 4px rgba(0,0,0,0.02);
    }
    
    .metric-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 8px 24px rgba(0,0,0,0.06);
        border-color: #4a6cf7;
    }
    
    .metric-card .value {
        font-size: 26px;
        font-weight: 800;
        color: #1a202c;
        line-height: 1.2;
    }
    
    .metric-card .label {
        font-size: 10px;
        font-weight: 600;
        color: #a0aec0;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        margin-top: 4px;
    }
    
    .podium-grid {
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: 16px;
        margin: 16px 0;
    }
    
    .podium-card {
        border-radius: 14px;
        padding: 18px 14px;
        text-align: center;
        transition: all 0.3s;
        border: 1px solid #edf2f7;
    }
    
    .podium-card:hover {
        transform: translateY(-4px);
    }
    
    .podium-card .rank {
        font-size: 36px;
        font-weight: 800;
        line-height: 1;
    }
    
    .podium-card .name {
        font-size: 14px;
        font-weight: 700;
        margin: 6px 0 2px 0;
        color: #1a202c;
    }
    
    .podium-card .stats {
        font-size: 11px;
        color: #718096;
        margin-top: 4px;
    }
    
    .podium-1 {
        background: linear-gradient(135deg, #ffd700 0%, #f5a623 100%);
        border-color: #f5a623;
        box-shadow: 0 4px 20px rgba(245, 166, 35, 0.15);
    }
    
    .podium-2 {
        background: linear-gradient(135deg, #e8e8e8 0%, #c0c0c0 100%);
        border-color: #c0c0c0;
        box-shadow: 0 4px 20px rgba(192, 192, 192, 0.12);
    }
    
    .podium-3 {
        background: linear-gradient(135deg, #f5cba7 0%, #cd7f32 100%);
        border-color: #cd7f32;
        box-shadow: 0 4px 20px rgba(205, 127, 50, 0.12);
    }
    
    .podium-other {
        background: white;
        border-color: #edf2f7;
    }
    
    .badge-valid { color: #38a169; font-weight: 600; }
    .badge-pending { color: #d69e2e; font-weight: 600; }
    .badge-rejected { color: #e53e3e; font-weight: 600; }
    
    .footer {
        text-align: center;
        padding: 20px 0 10px 0;
        border-top: 1px solid #edf2f7;
        margin-top: 30px;
    }
    
    .footer .name {
        background: linear-gradient(135deg, #4a6cf7 0%, #6a3de8 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 700;
        font-size: 14px;
    }
    
    @media (max-width: 768px) {
        .metrics-grid { grid-template-columns: repeat(3, 1fr); }
        .podium-grid { grid-template-columns: repeat(2, 1fr); }
        .login-box { padding: 28px 20px; max-width: 380px; }
    }
    
    @media (max-width: 480px) {
        .metrics-grid { grid-template-columns: repeat(2, 1fr); }
        .podium-grid { grid-template-columns: 1fr 1fr; }
        .login-box { padding: 24px 16px; max-width: 340px; }
        .login-logo h1 { font-size: 20px; }
        .login-logo .icon { font-size: 40px; }
    }
</style>
""", unsafe_allow_html=True)

# ---- FOND LOGIN ----
st.markdown("""
<div class="login-bg">
    <div class="deco-circle"></div>
    <div class="deco-circle"></div>
    <div class="deco-circle"></div>
</div>
""", unsafe_allow_html=True)

# =============================================================================
# 2. CONFIGURATION (JSON LOHARANO TOKANA)
# =============================================================================

# ---- FICHIER JSON (SERVER T:) ----
FICHIER_JSON = r"Z:\CQ\BASE\suivi_personnel_backup.json"

# ---- GOOGLE SHEETS (ESORINA, tsy ampiasaina intsony) ----
# GOOGLE_SHEET_BASE_CSV_URL = "https://docs.google.com/..."
# GOOGLE_SHEET_BASE_SCRIPT_URL = "https://script.google.com/..."

# ---- PLANIFICATION CONGE (Google Sheets mbola ilaina) ----
GOOGLE_SHEET_PLANIF_CSV_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vRwU89QIHsgWjpn6EA0NZJK4vonYau_n135EhGsLZpx_-gPvmbV7bigtPRdhFQ-2PObZkvJKYz8E4ya/pub?gid=1905831665&single=true&output=csv"
GOOGLE_SHEET_PLANIF_SCRIPT_URL = "https://script.google.com/macros/s/AKfycby2Pnt1Y0UyciL5fb1lB7639-jfrnmkcDP2y3Fe8Q2e7IHJgwSzSBCr4upJS7ozx_cl/exec"

# ---- PERFORMANCE (Google Sheets mbola ilaina) ----
GOOGLE_SHEET_PERF_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vTit9SdI6ft9WAh9YDVvHGvvvf_mtTxYl4y_lz9fdUSce31s9-wEppif-4UfjUT4Mw5cc46NNRBKZzj/pub?gid=155049620&single=true&output=csv"

# =============================================================================
# 3. GESTION JSON (LOHARANO TOKANA)
# =============================================================================

def initialiser_fichier_json():
    """Mamorona ny dossier sy ny fichier JSON raha tsy mbola misy"""
    global FICHIER_JSON
    
    # 1. Mamorona ny dossier T:\1-APK\BASE raha tsy mbola misy
    dossier = os.path.dirname(FICHIER_JSON)
    if dossier and not os.path.exists(dossier):
        try:
            os.makedirs(dossier, exist_ok=True)
        except Exception:
            # Raha tsy afaka mamorona ao amin'ny T: dia mampiasa local
            FICHIER_JSON = "suivi_personnel_backup.json"
            dossier_local = os.path.dirname(FICHIER_JSON)
            if dossier_local and not os.path.exists(dossier_local):
                os.makedirs(dossier_local, exist_ok=True)
    
    # 2. Mamorona ny fichier JSON raha tsy mbola misy
    if not os.path.exists(FICHIER_JSON):
        try:
            df_vide = pd.DataFrame(columns=["Matricule", "Date", "Type", "Procédure", "Détails", "Statut"])
            df_vide.to_json(FICHIER_JSON, orient="records", force_ascii=False, indent=2)
        except Exception:
            FICHIER_JSON = "suivi_personnel_backup.json"
            df_vide = pd.DataFrame(columns=["Matricule", "Date", "Type", "Procédure", "Détails", "Statut"])
            df_vide.to_json(FICHIER_JSON, orient="records", force_ascii=False, indent=2)

def charger_suivi():
    """Charge depuis JSON (Z:\CQ\BASE)"""
    global SOURCE_UTILISEE
    
    # 🔥 JSON d'abord (serveur T:)
    if os.path.exists(FICHIER_JSON):
        try:
            st.toast("📂 Chargement depuis JSON...", icon="📂")
            df = pd.read_json(FICHIER_JSON, orient="records", dtype={"Matricule": str})
            
            for col in ["Matricule", "Date", "Type", "Procédure", "Détails", "Statut"]:
                if col not in df.columns:
                    df[col] = ""
            if "Statut" not in df.columns or df["Statut"].isna().all():
                df["Statut"] = "Validé"
            
            SOURCE_UTILISEE = "JSON (serveur)"
            st.success(f"✅ {len(df)} lignes chargées depuis JSON")
            return df
        except Exception as e:
            st.warning(f"⚠️ JSON serveur corrompu: {e}")
    
    # 🔥 Raha tsy misy JSON dia mamorona base vide
    st.warning("⚠️ Aucune donnée trouvée, création d'une base vide")
    SOURCE_UTILISEE = "Nouvelle base"
    return pd.DataFrame(columns=["Matricule", "Date", "Type", "Procédure", "Détails", "Statut"])

def sauvegarder_suivi(df):
    """Sauvegarde dans JSON (Z:\CQ\BASE)"""
    try:
        # 🔥 JSON (serveur T:) d'abord
        lock = FileLock(FICHIER_JSON + ".lock")
        with lock:
            df.to_json(FICHIER_JSON, orient="records", force_ascii=False, indent=2)
        st.toast("✅ Sauvegardé dans JSON", icon="📂")
        return True
        
    except Exception as e:
        st.error(f"❌ Erreur sauvegarde JSON: {e}")
        return False

def charger_google_sheets_csv(url):
    try:
        return pd.read_csv(url, dtype=str)
    except Exception:
        return None

def enregistrer_planification_google_sheets(matricule, nom, prenom, date_debut, date_fin, type_evenement):
    """Enregistre dans la planification (Google Sheets)"""
    try:
        payload = {
            "matricule": str(matricule),
            "nom": str(nom),
            "prenom": str(prenom),
            "date_debut": str(date_debut),
            "date_fin": str(date_fin),
            "type": str(type_evenement)
        }
        response = requests.post(GOOGLE_SHEET_PLANIF_SCRIPT_URL, json=payload, timeout=10)
        return response.status_code == 200
    except Exception:
        return False

def charger_planification():
    return charger_google_sheets_csv(GOOGLE_SHEET_PLANIF_CSV_URL)

# ---- INITIALISATION ----
initialiser_fichier_json()
SOURCE_UTILISEE = "Inconnue"

# =============================================================================
# 4. BASE DE DONNEES
# =============================================================================
ANKIZY = pd.DataFrame([
    {"Matricule": "621", "Nom": "RAVAORISOA", "Prénoms": "Célina", "Fonction": "Contrôleur Qualité", "Shift": "MATIN"},
    {"Matricule": "622", "Nom": "JAOLAZA", "Prénoms": "Achiminah", "Fonction": "Contrôleur Qualité", "Shift": "MATIN"},
    {"Matricule": "623", "Nom": "DINARIVELO", "Prénoms": "Heninkajasoa Noellette", "Fonction": "Contrôleur Qualité", "Shift": "MATIN"},
    {"Matricule": "624", "Nom": "RAVAORISOA", "Prénoms": "Aina Fanomezana", "Fonction": "Contrôleur Qualité", "Shift": "MATIN"},
    {"Matricule": "625", "Nom": "HAJAMALALA", "Prénoms": "Zico Georges Jocelyn", "Fonction": "Contrôleur Qualité", "Shift": "MATIN"},
    {"Matricule": "626", "Nom": "SALEKA SOLONIRINA", "Prénoms": "Hantania Bienvenue", "Fonction": "Contrôleur Qualité", "Shift": "MATIN"},
    {"Matricule": "628", "Nom": "RAHERINIRINA", "Prénoms": "Santatriniaina Faniry", "Fonction": "Contrôleur Qualité", "Shift": "MATIN"},
    {"Matricule": "20", "Nom": "RANDRIAMAMONJINIAINA", "Prénoms": "Henintsoa Elisa", "Fonction": "Contrôleur Qualité", "Shift": "MATIN"},
    {"Matricule": "614", "Nom": "RABEMANANTSOA", "Prénoms": "Mamitiana Noëlson", "Fonction": "Contrôleur Qualité", "Shift": "N/A"},
    {"Matricule": "615", "Nom": "RAMIARAMANANA", "Prénoms": "Tolojanahary Luc Donald", "Fonction": "Contrôleur Qualité", "Shift": "N/A"},
    {"Matricule": "619", "Nom": "HANITRINIAINA", "Prénoms": "Fifaliana Arenasoa", "Fonction": "Contrôleur Qualité", "Shift": "N/A"},
    {"Matricule": "620", "Nom": "HERINIAINA", "Prénoms": "Toavina Tinah", "Fonction": "Contrôleur Qualité", "Shift": "N/A"},
    {"Matricule": "634", "Nom": "ROVATINA", "Prénoms": "Rinah Alphonse", "Fonction": "Contrôleur Qualité", "Shift": "N/A"},
    {"Matricule": "704", "Nom": "RANDRIANANTENAINA", "Prénoms": "Andrianarivo Halitiana", "Fonction": "Contrôleur Qualité", "Shift": "N/A"},
    {"Matricule": "856", "Nom": "RAHANITRINIAINA", "Prénoms": "Hortense", "Fonction": "Contrôleur Qualité", "Shift": "N/A"}
])

# ---- CHARGEMENT ----
if "suivi_db" not in st.session_state:
    with st.spinner("📂 Chargement des données..."):
        st.session_state.suivi_db = charger_suivi()

# ---- ETATS ----
if "auth_status" not in st.session_state: st.session_state.auth_status = "Déconnecté"
if "user_role" not in st.session_state: st.session_state.user_role = None
if "user_matricule" not in st.session_state: st.session_state.user_matricule = None
if "message_lu" not in st.session_state: st.session_state.message_lu = False
if "active_msg_view" not in st.session_state: st.session_state.active_msg_view = False
if "active_perf_view" not in st.session_state: st.session_state.active_perf_view = False
if "selected_mat" not in st.session_state: st.session_state.selected_mat = None
if "perf_plateau" not in st.session_state: st.session_state.perf_plateau = "MEN"

# =============================================================================
# 5. LOGIN
# =============================================================================
if st.session_state.auth_status == "Déconnecté":
    st.markdown("""
    <div class="login-wrapper">
        <div class="login-box">
            <div class="login-logo">
                <span class="icon">🔐</span>
                <h1>Portail <span>CQ-2026</span></h1>
                <p>Connectez-vous à votre espace de travail</p>
            </div>
    """, unsafe_allow_html=True)
    
    with st.form(key="login_form", clear_on_submit=False):
        
        st.markdown("""
        <div style="margin-bottom:16px;">
            <label style="display:block; font-size:13px; font-weight:600; color:#4a5568; margin-bottom:5px;">
                📧 Identifiant
            </label>
        """, unsafe_allow_html=True)
        username = st.text_input("", placeholder="Entrez votre matricule", label_visibility="collapsed", key="login_username")
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown("""
        <div style="margin-bottom:16px;">
            <label style="display:block; font-size:13px; font-weight:600; color:#4a5568; margin-bottom:5px;">
                🔑 Mot de passe
            </label>
        """, unsafe_allow_html=True)
        password = st.text_input("", type="password", placeholder="Entrez votre mot de passe", label_visibility="collapsed", key="login_password")
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown("""
        <div style="margin-bottom:16px;">
            <label style="display:block; font-size:13px; font-weight:600; color:#4a5568; margin-bottom:5px;">
                👤 Fonction
            </label>
        """, unsafe_allow_html=True)
        role = st.selectbox("", ["CP", "CE", "CQ"], label_visibility="collapsed", key="login_role")
        st.markdown('</div>', unsafe_allow_html=True)
        
        if st.form_submit_button("🔓 LOGIN", use_container_width=True):
            if role == "CP" and username == "Mahefa" and password == "12345":
                st.session_state.auth_status, st.session_state.user_role = "Connecté", "CP"
                st.session_state.message_lu = True
                st.rerun()
            elif role == "CE" and username == "Tsoa" and password == "12345":
                st.session_state.auth_status, st.session_state.user_role = "Connecté", "CE"
                st.session_state.message_lu = True
                st.rerun()
            elif role == "CQ":
                if username in ANKIZY["Matricule"].tolist() and password == "123456":
                    st.session_state.auth_status = "Connecté"
                    st.session_state.user_role = "CQ"
                    st.session_state.user_matricule = username
                    st.rerun()
                else:
                    st.error("❌ Identifiants incorrects")
            else:
                st.error("❌ Identifiants incorrects")
        
        st.markdown("""
        <div style="display:flex; align-items:center; gap:8px; margin-top:8px; padding-top:4px;">
            <input type="checkbox" id="remember" style="width:16px; height:16px; accent-color:#4a6cf7; cursor:pointer;">
            <label for="remember" style="font-size:13px; color:#4a5568; cursor:pointer;">Se souvenir de moi</label>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("""
            <div class="login-footer">
                © 2026 — <span class="name">Fanomezantsoa Mamy Fitiavana</span>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    st.stop()

# =============================================================================
# 6. SIDEBAR
# =============================================================================
with st.sidebar:
    st.markdown(f"""
    <div class="sidebar-user">
        <div class="avatar">👤</div>
        <div class="role">{st.session_state.user_role}</div>
        <div class="sub">{f"Matricule: {st.session_state.user_matricule}" if st.session_state.user_role == "CQ" else "Administration"}</div>
    </div>
    """, unsafe_allow_html=True)
    
    st.divider()
    
    if st.button("🔄 Actualiser", use_container_width=True):
        st.cache_data.clear()
        st.rerun()
    
    st.divider()
    st.markdown("### 🗂️ Outils")
    st.markdown("""
    <div style="display:flex; flex-direction:column; gap:6px;">
        <a href="http://10.10.10.24:9002/#!/login" target="_blank"><button style="width:100%; background:#4a6cf7; color:white; border:none; padding:9px; border-radius:8px; font-weight:600; cursor:pointer;">🌐 EC-MEN</button></a>
        <a href="http://relecture.studia.local" target="_blank"><button style="width:100%; background:#38a169; color:white; border:none; padding:9px; border-radius:8px; font-weight:600; cursor:pointer;">🌐 EC-MADA</button></a>
        <a href="http://http://10.10.10.62:3002/tri" target="_blank"><button style="width:100%; background:#718096; color:white; border:none; padding:9px; border-radius:8px; font-weight:600; cursor:pointer;">📸 Tri Image</button></a>
    </div>
    """, unsafe_allow_html=True)
    
    st.divider()
    st.markdown("### 📢 Navigation")
    
    msg_label = "🔴 Note d'info" if (st.session_state.user_role == "CQ" and not st.session_state.message_lu) else "📄 Note d'info"
    if st.checkbox(msg_label, value=st.session_state.active_msg_view):
        st.session_state.active_msg_view = True
        st.session_state.message_lu = True
    else:
        st.session_state.active_msg_view = False
    
    if st.checkbox("📊 Performances", value=st.session_state.active_perf_view):
        st.session_state.active_perf_view = True
        st.session_state.perf_plateau = st.radio("Plateau", ["MEN", "EC-MADA"], horizontal=True)
    else:
        st.session_state.active_perf_view = False
    
    st.divider()
    
    # =========================================================================
    # 🔍 DEBUG - SOURCE DE DONNEES
    # =========================================================================
    st.markdown("### 🔍 Debug - Source")
    
    # Jereo raha misy Internet
    try:
        socket.gethostbyname("www.google.com")
        st.success("✅ Internet: OK")
    except:
        st.error("❌ Internet: NON")
    
    # Jereo raha misy JSON
    if os.path.exists(FICHIER_JSON):
        try:
            df_json = pd.read_json(FICHIER_JSON, orient="records", dtype={"Matricule": str})
            st.success(f"✅ JSON: OK ({len(df_json)} lignes)")
            st.caption(f"📁 {FICHIER_JSON}")
        except:
            st.error("❌ JSON: Corrompu")
    else:
        st.warning("⚠️ JSON: Tsy misy")
        st.caption(f"📁 {FICHIER_JSON}")
    
    st.write(f"**Source:** {SOURCE_UTILISEE}")
    st.write(f"**Lignes:** {len(st.session_state.suivi_db)}")
    
    st.divider()
    
    if st.button("🚪 Déconnexion", use_container_width=True):
        for key in ["auth_status", "user_role", "user_matricule", "message_lu", "active_msg_view", "active_perf_view"]:
            if key in st.session_state:
                if key == "auth_status":
                    st.session_state[key] = "Déconnecté"
                elif key in ["message_lu", "active_msg_view", "active_perf_view"]:
                    st.session_state[key] = False
                else:
                    st.session_state[key] = None
        st.rerun()
    
    st.divider()
    st.caption("© 2026 — Fanomezantsoa")

# =============================================================================
# 7. NOTE D'INFORMATION
# =============================================================================
if st.session_state.active_msg_view:
    st.markdown("""
    <div class="glass-card">
        <div class="card-header">
            <span class="icon">📢</span>
            <h2>Communication Interne</h2>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div style="background:#fff9e6; padding:14px; border-radius:10px; border-left:4px solid #f5a623; margin-bottom:16px;">
        <h5 style="margin:0; color:#8a6d1e;">📌 Note d'Information Officielle</h5>
        <p style="margin:4px 0 0 0; color:#6b5a2e; font-size:13px;">Directives de la Direction et captures de validation synchronisées.</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.info("ℹ️ Aucun message disponible pour le moment.")
    st.markdown("</div>", unsafe_allow_html=True)
    st.stop()

# =============================================================================
# 8. PERFORMANCES
# =============================================================================
if st.session_state.active_perf_view:
    st.markdown(f"""
    <div class="glass-card">
        <div class="card-header">
            <span class="icon">📊</span>
            <h2>Tableau des Performances — {st.session_state.perf_plateau}</h2>
        </div>
    """, unsafe_allow_html=True)
    
    df_perf = charger_google_sheets_csv(GOOGLE_SHEET_PERF_URL)
    if df_perf is None:
        st.warning("⚠️ Impossible de charger les données de performance.")
        st.stop()
    
    try:
        df_b1 = df_perf.iloc[:, 0:11].copy()
        df_b2 = df_perf.iloc[:, 12:23].copy()
        df_b3 = df_perf.iloc[:, 24:35].copy()
        df_b4 = df_perf.iloc[:, 36:47].copy()
        
        headers = ["Date", "Étape", "Jour", "Identifiant", "Nom", "Prénom", "Total Actif", "Heures Totale", "Vitesse Moyenne", "Classement Nb", "Faute"]
        for df_b in [df_b1, df_b2, df_b3, df_b4]:
            if len(df_b.columns) >= 11:
                df_b.columns = headers[:len(df_b.columns)]
        
        df_consolide = pd.concat([df_b1, df_b2, df_b3, df_b4], ignore_index=True)
        df_consolide = df_consolide.dropna(subset=["Date"])
        df_consolide = df_consolide[df_consolide["Date"].str.strip() != ""]
        
        if df_consolide.empty:
            st.info("Aucune donnée disponible.")
            st.stop()
        
        col_f1, col_f2 = st.columns(2)
        with col_f1:
            etapes = sorted(df_consolide["Étape"].dropna().unique())
            etape_sel = st.selectbox("🎯 Étape", etapes)
        with col_f2:
            df_temp = df_consolide[df_consolide["Étape"] == etape_sel]
            dates = sorted(df_temp["Date"].dropna().unique(), reverse=True)
            date_sel = st.selectbox("📅 Date", dates)
        
        df_final = df_consolide[(df_consolide["Étape"] == etape_sel) & (df_consolide["Date"] == date_sel)]
        
        if not df_final.empty:
            df_podium = df_final.copy()
            df_podium["Classement Nb"] = pd.to_numeric(df_podium["Classement Nb"], errors="coerce")
            df_podium = df_podium.dropna(subset=["Classement Nb"])
            df_podium = df_podium.sort_values(by="Classement Nb", ascending=True).reset_index(drop=True)
            df_podium["Classement Nb"] = range(1, len(df_podium) + 1)
            
            est_dans_tableau = (st.session_state.user_role == "CQ" and 
                               str(st.session_state.user_matricule) in df_podium["Identifiant"].astype(str).values)
            
            nb_top = 3 if est_dans_tableau else 4
            nb_top = min(nb_top, len(df_podium))
            df_top = df_podium.head(nb_top)
            
            if not df_top.empty:
                st.markdown(f"### 🏆 Tableau d'Honneur (Top {nb_top})")
                cols = st.columns(nb_top)
                
                for i in range(nb_top):
                    row = df_top.iloc[i]
                    rank = i + 1
                    
                    if rank == 1:
                        css_class = "podium-1"
                        emoji = "⭐ Favori"
                    elif rank == 2:
                        css_class = "podium-2"
                        emoji = "🥈 Excellent"
                    elif rank == 3:
                        css_class = "podium-3"
                        emoji = "🥉 Très Bien"
                    else:
                        css_class = "podium-other"
                        emoji = "🏅 Mention"
                    
                    with cols[i]:
                        st.markdown(f"""
                        <div class="podium-card {css_class}">
                            <div class="rank">{rank}</div>
                            <div class="name">{row['Nom']} {row['Prénom']}</div>
                            <div class="stats">⚡ {row['Vitesse Moyenne']} | Total Actes : {row['Total Actif']}</div>
                        </div>
                        """, unsafe_allow_html=True)
                st.write("")
        
        if st.session_state.user_role == "CQ":
            df_final = df_final[df_final["Identifiant"] == str(st.session_state.user_matricule)]
            st.info("💡 Mode individuel — Vos données personnelles")
        
        if df_final.empty:
            st.warning("Aucune donnée pour ces critères.")
        else:
            st.dataframe(df_final, use_container_width=True, hide_index=True)
            
    except Exception as e:
        st.error(f"Erreur: {e}")
    
    st.markdown("</div>", unsafe_allow_html=True)
    st.stop()

# =============================================================================
# 9. CP / CE
# =============================================================================
if st.session_state.user_role in ["CP", "CE"]:
    st.markdown(f"""
    <div class="glass-card">
        <div class="card-header">
            <span class="icon">👑</span>
            <h2>Administration — {st.session_state.user_role}</h2>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div style="background:#f8fafc; padding:14px; border-radius:10px; border-left:4px solid #4a6cf7; margin-bottom:18px; font-size:13px;">
        <b>👤 Hiérarchie :</b> CP : Mahefasoa Andrianarivo | CE : Mamy Fitiavana
    </div>
    """, unsafe_allow_html=True)
    
    with st.expander("📋 Données externes", expanded=False):
        st.markdown("#### 📋 Base principale (JSON)")
        st.dataframe(st.session_state.suivi_db, use_container_width=True, hide_index=True)
        
        st.markdown("#### 📋 Planification Congé / Absence")
        df_planif = charger_planification()
        if df_planif is not None:
            st.dataframe(df_planif, use_container_width=True, hide_index=True)
        else:
            st.info("ℹ️ Aucune donnée dans la planification")
        
        st.markdown("#### 📊 Performances")
        df_perf = charger_google_sheets_csv(GOOGLE_SHEET_PERF_URL)
        if df_perf is not None:
            st.dataframe(df_perf, use_container_width=True, hide_index=True)
        else:
            st.info("ℹ️ Aucune donnée de performance")
    
    st.markdown("<hr style='margin:18px 0; border:0; border-top:1px solid #edf2f7;'>", unsafe_allow_html=True)
    
    # ---- REQUETES EN ATTENTE ----
    df_attente = st.session_state.suivi_db[st.session_state.suivi_db["Statut"] == "En attente"]
    st.markdown(f"### 📬 Requêtes en attente ({len(df_attente)})")
    
    if len(df_attente) > 0:
        for idx, row in df_attente.iterrows():
            mat_demandeur = row["Matricule"]
            info_emp = ANKIZY[ANKIZY["Matricule"] == str(mat_demandeur)]
            
            if not info_emp.empty:
                profil = info_emp.iloc[0]
                nom_complet = f"{profil['Nom']} {profil['Prénoms']}"
                nom, prenom = profil['Nom'], profil['Prénoms']
            else:
                nom_complet = nom = prenom = "Inconnu"
            
            with st.expander(f"📩 {nom_complet} — {row['Type']} ({row['Date']})", expanded=True):
                col1, col2, col3 = st.columns([0.6, 0.2, 0.2])
                with col1:
                    st.write(f"**Détails :** {row['Détails']}")
                with col2:
                    if st.button("✅ Valider", key=f"app_{idx}"):
                        st.session_state.suivi_db.at[idx, "Statut"] = "Validé"
                        sauvegarder_suivi(st.session_state.suivi_db)
                        
                        type_upper = str(row['Type']).upper()
                        if "CONG" in type_upper or "ABSENC" in type_upper:
                            type_sheet = "Congé" if "CONG" in type_upper else "Absence"
                            enregistrer_planification_google_sheets(
                                mat_demandeur, nom, prenom,
                                row['Date'], row['Date'],
                                type_sheet
                            )
                            st.success(f"✅ {type_sheet} enregistré dans la planification!")
                        st.rerun()
                with col3:
                    if st.button("❌ Rejeter", key=f"ref_{idx}"):
                        st.session_state.suivi_db.at[idx, "Statut"] = "Refusé"
                        sauvegarder_suivi(st.session_state.suivi_db)
                        st.rerun()
    else:
        st.success("✅ Aucune requête en attente.")
    
    st.markdown("<hr style='margin:18px 0; border:0; border-top:1px solid #edf2f7;'>", unsafe_allow_html=True)
    
    col_gauche, col_droite = st.columns(2)
    
    with col_gauche:
        st.markdown("### 👥 Répertoire du Personnel")
        recherche = st.text_input("🔍 Rechercher", placeholder="Nom ou matricule", key="search_admin")
        df_filtre = ANKIZY
        if recherche:
            df_filtre = df_filtre[
                df_filtre["Matricule"].str.contains(recherche, case=False) |
                df_filtre["Nom"].str.contains(recherche, case=False) |
                df_filtre["Prénoms"].str.contains(recherche, case=False)
            ]
        
        for _, row in df_filtre.iterrows():
            if st.button(f"🆔 {row['Matricule']} — {row['Nom']} {row['Prénoms']}", key=f"sel_{row['Matricule']}", use_container_width=True):
                st.session_state.selected_mat = row['Matricule']
                st.rerun()
    
    with col_droite:
        if st.session_state.selected_mat:
            mat = st.session_state.selected_mat
            profil = ANKIZY[ANKIZY["Matricule"] == mat]
            
            if not profil.empty:
                p = profil.iloc[0]
                st.markdown(f"### 👤 {p['Nom']} {p['Prénoms']}")
                st.caption(f"Matricule: {p['Matricule']} | Poste: {p['Fonction']} | Shift: {p['Shift']}")
                
                histo = st.session_state.suivi_db[st.session_state.suivi_db["Matricule"] == str(mat)]
                histo_valide = histo[histo["Statut"] == "Validé"]
                
                stats = {
                    "🚨 ESIA": len(histo_valide[histo_valide["Type"] == "ESIA"]),
                    "💼 RH": len(histo_valide[histo_valide["Type"] == "RH"]),
                    "⏱️ RETARD": len(histo_valide[histo_valide["Type"] == "RETARD"]),
                    "❌ ABSENCE": len(histo_valide[histo_valide["Type"] == "ABSENCE"]),
                    "📅 CONGÉ": len(histo_valide[histo_valide["Type"] == "CONGÉ"]),
                    "🍼 MATERN.": len(histo_valide[histo_valide["Type"] == "ASSISTANCE MATERNELLE"])
                }
                
                st.markdown('<div class="metrics-grid">', unsafe_allow_html=True)
                for k, v in stats.items():
                    label = k.split()[1] if len(k.split()) > 1 else k
                    st.markdown(f"""
                    <div class="metric-card">
                        <div class="value">{v}</div>
                        <div class="label">{label}</div>
                    </div>
                    """, unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)
                
                st.markdown("---")
                st.markdown("#### ➕ Ajouter un événement")
                
                with st.form(key="form_admin", clear_on_submit=True):
                    date_evt = st.date_input("Date", datetime.now().date())
                    type_evt = st.selectbox("Nature", ["ESIA", "RH", "RETARD", "ABSENCE", "CONGÉ", "ASSISTANCE MATERNELLE", "AUTRES"])
                    
                    notes_specifiques = ""
                    if type_evt in ["CONGÉ", "ABSENCE"]:
                        d1 = st.date_input("Date de début", datetime.now().date())
                        d2 = st.date_input("Date de fin", datetime.now().date())
                        notes_specifiques = f"[Du {d1.strftime('%d/%m/%Y')} au {d2.strftime('%d/%m/%Y')}] "
                    elif type_evt == "RETARD":
                        d_retard = st.date_input("Date du retard", datetime.now().date())
                        h_retard = st.time_input("Heure du retard", value=time(0, 0, 0))
                        notes_specifiques = f"[{d_retard.strftime('%d/%m/%Y')} à {h_retard.strftime('%H:%M:%S')}] "
                    
                    notes = st.text_area("Observations")
                    
                    if st.form_submit_button("💾 Enregistrer"):
                        if notes.strip() == "":
                            st.error("Veuillez saisir une observation.")
                        else:
                            new_row = {
                                "Matricule": str(mat),
                                "Date": date_evt.strftime("%Y-%m-%d"),
                                "Type": type_evt,
                                "Procédure": f"Par {st.session_state.user_role}",
                                "Détails": f"{notes_specifiques}{notes}",
                                "Statut": "Validé"
                            }
                            st.session_state.suivi_db = pd.concat([st.session_state.suivi_db, pd.DataFrame([new_row])], ignore_index=True)
                            sauvegarder_suivi(st.session_state.suivi_db)
                            
                            if "CONG" in str(type_evt).upper() or "ABSENC" in str(type_evt).upper():
                                type_sheet = "Congé" if "CONG" in str(type_evt).upper() else "Absence"
                                enregistrer_planification_google_sheets(
                                    str(mat), p['Nom'], p['Prénoms'],
                                    date_evt.strftime("%Y-%m-%d"),
                                    date_evt.strftime("%Y-%m-%d"),
                                    type_sheet
                                )
                                st.success(f"✅ {type_sheet} enregistré dans la planification!")
                            st.rerun()
                
                st.markdown("---")
                st.markdown("#### 📜 Historique")
                categories = ["Tout", "ESIA", "RH", "RETARD", "ABSENCE", "CONGÉ", "ASSISTANCE MATERNELLE", "AUTRES"]
                tabs = st.tabs(categories)
                for i, cat in enumerate(categories):
                    with tabs[i]:
                        df_cat = histo if cat == "Tout" else histo[histo["Type"] == cat]
                        if df_cat.empty:
                            st.info(f"Aucune mention pour {cat}")
                        else:
                            for idx_h, row_h in df_cat.iloc[::-1].iterrows():
                                status_class = "badge-valid" if row_h['Statut'] == "Validé" else "badge-pending" if row_h['Statut'] == "En attente" else "badge-rejected"
                                
                                col_info, col_del = st.columns([0.85, 0.15])
                                with col_info:
                                    st.markdown(f"**{row_h['Date']}** — `{row_h['Type']}` <span class='{status_class}'>{row_h['Statut']}</span>", unsafe_allow_html=True)
                                    st.write(row_h['Détails'])
                                with col_del:
                                    if st.button("🗑️", key=f"del_{cat}_{idx_h}", use_container_width=True):
                                        st.session_state.suivi_db = st.session_state.suivi_db.drop(idx_h).reset_index(drop=True)
                                        sauvegarder_suivi(st.session_state.suivi_db)
                                        st.success("✅ Supprimé avec succès!")
                                        st.rerun()
                                st.divider()
            else:
                st.info("👈 Sélectionnez un collaborateur")
        else:
            st.info("👈 Sélectionnez un collaborateur pour voir son dossier")
    
    st.markdown("</div>", unsafe_allow_html=True)

# =============================================================================
# 10. CQ
# =============================================================================
elif st.session_state.user_role == "CQ":
    mat = st.session_state.user_matricule
    profil = ANKIZY[ANKIZY["Matricule"] == mat]
    
    if not profil.empty:
        p = profil.iloc[0]
        
        st.markdown(f"""
        <div class="glass-card">
            <div class="card-header">
                <span class="icon">👋</span>
                <h2>Espace Personnel — {p['Prénoms']} {p['Nom']}</h2>
            </div>
        """, unsafe_allow_html=True)
        
        st.caption(f"Matricule: {p['Matricule']} | Poste: {p['Fonction']} | Shift: {p['Shift']}")
        
        histo = st.session_state.suivi_db[st.session_state.suivi_db["Matricule"] == str(mat)]
        histo_valide = histo[histo["Statut"] == "Validé"]
        
        stats = {
            "🚨 ESIA": len(histo_valide[histo_valide["Type"] == "ESIA"]),
            "💼 RH": len(histo_valide[histo_valide["Type"] == "RH"]),
            "⏱️ RETARD": len(histo_valide[histo_valide["Type"] == "RETARD"]),
            "❌ ABSENCE": len(histo_valide[histo_valide["Type"] == "ABSENCE"]),
            "📅 CONGÉ": len(histo_valide[histo_valide["Type"] == "CONGÉ"]),
            "🍼 MATERN.": len(histo_valide[histo_valide["Type"] == "ASSISTANCE MATERNELLE"])
        }
        
        st.markdown('<div class="metrics-grid">', unsafe_allow_html=True)
        for k, v in stats.items():
            label = k.split()[1] if len(k.split()) > 1 else k
            st.markdown(f"""
            <div class="metric-card">
                <div class="value">{v}</div>
                <div class="label">{label}</div>
            </div>
            """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown("---")
        
        col_form, col_hist = st.columns([0.4, 0.6])
        
        with col_form:
            st.markdown("### 📝 Soumettre une requête")
            type_evt = st.selectbox("Objet", ["RETARD", "ABSENCE", "CONGÉ", "ASSISTANCE MATERNELLE", "AUTRES"], key="cq_type")
            
            with st.form(key="form_cq", clear_on_submit=True):
                notes_specifiques = ""
                date_evt = datetime.now().date()
                
                if type_evt in ["CONGÉ", "ABSENCE"]:
                    d1 = st.date_input("Date de début", datetime.now().date())
                    d2 = st.date_input("Date de fin", datetime.now().date())
                    notes_specifiques = f"[Du {d1.strftime('%d/%m/%Y')} au {d2.strftime('%d/%m/%Y')}] "
                    date_evt = d1
                elif type_evt == "RETARD":
                    d_retard = st.date_input("Date du retard", datetime.now().date())
                    h_retard = st.time_input("Heure du retard", value=time(0, 0, 0))
                    notes_specifiques = f"[{d_retard.strftime('%d/%m/%Y')} à {h_retard.strftime('%H:%M:%S')}] "
                    date_evt = d_retard
                else:
                    date_evt = st.date_input("Date", datetime.now().date())
                
                motif = st.text_area("Motif", placeholder="Décrivez votre demande...")
                
                if st.form_submit_button("📤 Envoyer", use_container_width=True):
                    if motif.strip() == "":
                        st.error("Veuillez saisir un motif.")
                    else:
                        new_row = {
                            "Matricule": str(mat),
                            "Date": date_evt.strftime("%Y-%m-%d"),
                            "Type": type_evt,
                            "Procédure": "[Requête CQ]",
                            "Détails": f"{notes_specifiques}{motif}",
                            "Statut": "En attente"
                        }
                        
                        st.session_state.suivi_db = pd.concat([st.session_state.suivi_db, pd.DataFrame([new_row])], ignore_index=True)
                        sauvegarder_suivi(st.session_state.suivi_db)
                        
                        st.toast("📤 Demande envoyée", icon="📤")
                        st.success("✅ Requête envoyée avec succès!")
                        st.rerun()
        
        with col_hist:
            st.markdown("### 📜 Mes demandes")
            if histo.empty:
                st.info("Aucune demande.")
            else:
                for idx_h, row_h in histo.iloc[::-1].iterrows():
                    status_class = "badge-valid" if row_h['Statut'] == "Validé" else "badge-pending" if row_h['Statut'] == "En attente" else "badge-rejected"
                    st.markdown(f"**{row_h['Date']}** — `{row_h['Type']}` <span class='{status_class}'>{row_h['Statut']}</span>", unsafe_allow_html=True)
                    st.write(row_h['Détails'])
                    st.divider()
        
        st.markdown("</div>", unsafe_allow_html=True)

# =============================================================================
# 11. FOOTER
# =============================================================================
st.divider()
st.markdown("""
<div class="footer">
    © 2026 — <span class="name">Fanomezantsoa Mamy Fitiavana</span> — Tous droits réservés
</div>
""", unsafe_allow_html=True)