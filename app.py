"""
🌿 Herbario Digital Comunitario
Versión 1.0 — Aplicación moderna para comunidades educativas rurales
"""

import streamlit as st
import pandas as pd
import os
import uuid
import base64
from datetime import datetime
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path

# ─────────────────────────────────────────────
#  CONFIGURACIÓN GENERAL
# ─────────────────────────────────────────────

st.set_page_config(
    page_title="Herbario Digital Comunitario",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────
#  ESTILOS GLOBALES
# ─────────────────────────────────────────────

st.markdown("""
<link href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700;900&family=DM+Sans:wght@300;400;500;600&display=swap" rel="stylesheet">

<style>
/* ── Variables de tema ── */
:root {
    --verde-oscuro:   #1a3d2b;
    --verde-medio:    #2d6a4f;
    --verde-claro:    #52b788;
    --verde-suave:    #b7e4c7;
    --tierra:         #a0522d;
    --crema:          #f5f0e8;
    --texto-oscuro:   #1c2b1e;
    --texto-suave:    #4a6153;
    --sombra:         rgba(26,61,43,0.12);
    --radio:          16px;
    --transicion:     0.3s ease;
}

/* ── Tipografía global ── */
html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif !important;
    font-size: 15px;
}

h1, h2, h3 {
    font-family: 'Playfair Display', serif !important;
    letter-spacing: 0.5px;
}

/* ── Fondo principal ── */
.stApp {
    background-color: var(--crema);
}

/* ── Sidebar ── */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, var(--verde-oscuro) 0%, var(--verde-medio) 100%) !important;
    border-right: none !important;
}

[data-testid="stSidebar"] * {
    color: #e8f5e9 !important;
}

[data-testid="stSidebar"] .stRadio label {
    font-size: 15px;
    font-weight: 500;
    padding: 8px 0;
}

/* ── Métricas ── */
[data-testid="metric-container"] {
    background: white;
    border: 1px solid #d8ead0;
    border-radius: var(--radio);
    padding: 16px !important;
    box-shadow: 0 2px 8px var(--sombra);
    transition: transform var(--transicion);
}

[data-testid="metric-container"]:hover {
    transform: translateY(-3px);
    box-shadow: 0 6px 20px var(--sombra);
}

/* ── Botones ── */
.stButton > button {
    background: var(--verde-medio) !important;
    color: white !important;
    border: none !important;
    border-radius: 10px !important;
    font-family: 'DM Sans', sans-serif !important;
    font-weight: 600 !important;
    padding: 10px 24px !important;
    transition: all var(--transicion) !important;
    box-shadow: 0 2px 8px var(--sombra) !important;
}

.stButton > button:hover {
    background: var(--verde-oscuro) !important;
    transform: translateY(-2px) !important;
    box-shadow: 0 6px 16px var(--sombra) !important;
}

/* ── Inputs ── */
.stTextInput input, .stTextArea textarea, .stSelectbox select {
    border-radius: 10px !important;
    border: 1.5px solid #c8dfc0 !important;
    font-family: 'DM Sans', sans-serif !important;
    transition: border-color var(--transicion) !important;
}

.stTextInput input:focus, .stTextArea textarea:focus {
    border-color: var(--verde-claro) !important;
    box-shadow: 0 0 0 3px rgba(82,183,136,0.15) !important;
}

/* ── Tarjetas de plantas ── */
.planta-card {
    background: white;
    border-radius: var(--radio);
    overflow: hidden;
    box-shadow: 0 3px 12px var(--sombra);
    transition: all var(--transicion);
    border: 1px solid #e0eedf;
    margin-bottom: 8px;
    animation: fadeInUp 0.5s ease both;
}

.planta-card:hover {
    transform: translateY(-5px);
    box-shadow: 0 10px 30px rgba(26,61,43,0.18);
    border-color: var(--verde-claro);
}

.planta-card-img {
    width: 100%;
    height: 200px;
    object-fit: cover;
}

.planta-card-body {
    padding: 16px;
}

.planta-card-title {
    font-family: 'Playfair Display', serif;
    font-size: 18px;
    font-weight: 700;
    color: var(--verde-oscuro);
    margin: 0 0 4px 0;
}

.planta-card-subtitle {
    font-style: italic;
    font-size: 13px;
    color: var(--texto-suave);
    margin: 0 0 10px 0;
}

.planta-card-familia {
    display: inline-block;
    background: var(--verde-suave);
    color: var(--verde-oscuro);
    font-size: 11px;
    font-weight: 600;
    padding: 3px 10px;
    border-radius: 20px;
    margin-bottom: 8px;
    letter-spacing: 0.5px;
    text-transform: uppercase;
}

.planta-card-desc {
    font-size: 13px;
    color: #555;
    line-height: 1.5;
    display: -webkit-box;
    -webkit-line-clamp: 3;
    -webkit-box-orient: vertical;
    overflow: hidden;
}

.planta-card-footer {
    padding: 10px 16px;
    background: #f8fdf8;
    border-top: 1px solid #eaf3e8;
    font-size: 12px;
    color: var(--texto-suave);
}

.planta-no-img {
    width: 100%;
    height: 200px;
    background: linear-gradient(135deg, var(--verde-suave), #d8f3dc);
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 48px;
}

/* ── Banner header ── */
.hero-banner {
    background: linear-gradient(135deg, var(--verde-oscuro) 0%, var(--verde-medio) 60%, var(--verde-claro) 100%);
    border-radius: 20px;
    padding: 48px 40px;
    color: white;
    margin-bottom: 32px;
    position: relative;
    overflow: hidden;
}

.hero-banner::before {
    content: '🌿';
    position: absolute;
    font-size: 200px;
    right: -30px;
    top: -40px;
    opacity: 0.08;
    transform: rotate(-15deg);
}

.hero-title {
    font-family: 'Playfair Display', serif;
    font-size: 38px;
    font-weight: 900;
    margin: 0 0 8px 0;
    line-height: 1.2;
}

.hero-subtitle {
    font-size: 17px;
    font-weight: 300;
    opacity: 0.9;
    margin: 0;
}

/* ── Sección de estadísticas ── */
.stats-card {
    background: white;
    border-radius: var(--radio);
    padding: 24px;
    box-shadow: 0 3px 12px var(--sombra);
    border: 1px solid #e0eedf;
    margin-bottom: 16px;
}

.stats-card h3 {
    color: var(--verde-oscuro);
    font-size: 18px;
    margin-bottom: 16px;
}

/* ── Form card ── */
.form-card {
    background: white;
    border-radius: 20px;
    padding: 32px;
    box-shadow: 0 4px 20px var(--sombra);
    border: 1px solid #d8ead0;
}

/* ── Badges de categoría ── */
.badge {
    display: inline-block;
    padding: 4px 12px;
    border-radius: 20px;
    font-size: 12px;
    font-weight: 600;
    letter-spacing: 0.5px;
}

.badge-medicinal  { background: #fff3e0; color: #e65100; }
.badge-ornamental { background: #fce4ec; color: #880e4f; }
.badge-alimentaria { background: #e8f5e9; color: #1b5e20; }
.badge-aromatica  { background: #f3e5f5; color: #4a148c; }
.badge-otro       { background: #e3f2fd; color: #0d47a1; }

/* ── Info box ── */
.info-box {
    background: linear-gradient(135deg, #e8f5e9, #f1f8e9);
    border-left: 4px solid var(--verde-claro);
    border-radius: 0 12px 12px 0;
    padding: 16px 20px;
    margin: 16px 0;
    font-size: 14px;
    color: var(--texto-oscuro);
}

/* ── Animaciones ── */
@keyframes fadeInUp {
    from { opacity: 0; transform: translateY(20px); }
    to   { opacity: 1; transform: translateY(0); }
}

@keyframes fadeIn {
    from { opacity: 0; }
    to   { opacity: 1; }
}

.animate-fadein {
    animation: fadeIn 0.6s ease both;
}

/* ── Divisor decorativo ── */
.divider {
    border: none;
    border-top: 2px solid var(--verde-suave);
    margin: 24px 0;
}

/* ── Chip de búsqueda ── */
.search-chip {
    background: var(--verde-suave);
    color: var(--verde-oscuro);
    padding: 6px 16px;
    border-radius: 20px;
    font-size: 13px;
    font-weight: 600;
    display: inline-block;
    margin: 4px;
}

/* ── Empty state ── */
.empty-state {
    text-align: center;
    padding: 60px 20px;
    color: var(--texto-suave);
}

.empty-state .icon { font-size: 64px; margin-bottom: 16px; }
.empty-state h3 { font-family: 'Playfair Display', serif; color: var(--verde-oscuro); }

/* ── Modo oscuro automático ── */
@media (prefers-color-scheme: dark) {
    :root {
        --crema: #121d17;
        --texto-oscuro: #e0f2e9;
        --sombra: rgba(0,0,0,0.35);
    }
    .stApp { background-color: #121d17; }
    .planta-card, .stats-card, .form-card,
    [data-testid="metric-container"] {
        background: #1c2e24 !important;
        border-color: #2d4a38 !important;
        color: #dceee3 !important;
    }
    .planta-card-title { color: #a8d5b5 !important; }
    .planta-card-footer { background: #182719; border-color: #2a3e2e; }
}
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
#  RUTAS Y CONSTANTES
# ─────────────────────────────────────────────

IMG_DIR = Path("imagenes")
IMG_DIR.mkdir(exist_ok=True)

CSV_PATH = Path("plantas.csv")

COLUMNAS = [
    "ID", "Nombre común", "Nombre científico",
    "Familia botánica", "Categoría", "Hábitat",
    "Descripción", "Usos", "Registrado por",
    "Fecha de registro", "Imagen"
]

CATEGORIAS = ["Medicinal", "Alimentaria", "Ornamental", "Aromática", "Otro"]

FAMILIAS = [
    "Asteraceae", "Fabaceae", "Poaceae", "Rosaceae",
    "Solanaceae", "Lamiaceae", "Euphorbiaceae", "Orchidaceae",
    "Bromeliaceae", "Araceae", "Otra",
]

HABITATS = [
    "Bosque húmedo", "Páramo", "Sabana", "Selva tropical",
    "Ribereño", "Humedal", "Jardín doméstico", "Rastrojo", "Otro",
]

# ─────────────────────────────────────────────
#  FUNCIONES DE DATOS
# ─────────────────────────────────────────────

def cargar_datos() -> pd.DataFrame:
    """Carga el CSV o crea uno vacío si no existe."""
    if not CSV_PATH.exists():
        pd.DataFrame(columns=COLUMNAS).to_csv(CSV_PATH, index=False)
    df = pd.read_csv(CSV_PATH)
    # Garantizar que todas las columnas existan (retrocompatibilidad)
    for col in COLUMNAS:
        if col not in df.columns:
            df[col] = ""
    return df


def guardar_datos(df: pd.DataFrame) -> None:
    """Guarda el DataFrame en CSV."""
    df.to_csv(CSV_PATH, index=False)


def imagen_a_base64(ruta: str) -> str | None:
    """Convierte una imagen a base64 para incrustar en HTML."""
    try:
        with open(ruta, "rb") as f:
            data = base64.b64encode(f.read()).decode()
        ext = Path(ruta).suffix.lower().replace(".", "")
        if ext == "jpg":
            ext = "jpeg"
        return f"data:image/{ext};base64,{data}"
    except Exception:
        return None


def guardar_imagen(archivo) -> str:
    """Guarda un archivo subido y devuelve la ruta."""
    nombre = f"{uuid.uuid4().hex}{Path(archivo.name).suffix}"
    ruta = IMG_DIR / nombre
    with open(ruta, "wb") as f:
        f.write(archivo.getbuffer())
    return str(ruta)


def badge_categoria(cat: str) -> str:
    mapa = {
        "Medicinal":  "badge-medicinal",
        "Ornamental": "badge-ornamental",
        "Alimentaria": "badge-alimentaria",
        "Aromática":  "badge-aromatica",
    }
    clase = mapa.get(cat, "badge-otro")
    return f'<span class="badge {clase}">{cat}</span>'

# ─────────────────────────────────────────────
#  SIDEBAR / NAVEGACIÓN
# ─────────────────────────────────────────────

with st.sidebar:
    st.markdown("""
    <div style="text-align:center; padding: 24px 0 16px;">
        <div style="font-size:56px;">🌿</div>
        <div style="font-family:'Playfair Display',serif; font-size:22px;
                    font-weight:900; color:#b7e4c7; margin-top:8px;">
            Herbario Digital
        </div>
        <div style="font-size:12px; color:#81c995; margin-top:4px;">
            Comunidad Educativa Rural
        </div>
    </div>
    <hr style="border-color:#2d6a4f; margin:8px 0 24px;">
    """, unsafe_allow_html=True)

    pagina = st.radio(
        "Navegación",
        ["🏡  Inicio", "🖼️  Galería", "➕  Registrar planta", "✏️  Editar / Eliminar", "📊  Estadísticas"],
        label_visibility="collapsed",
    )

    st.markdown("<hr style='border-color:#2d6a4f; margin:24px 0 16px;'>", unsafe_allow_html=True)
    st.markdown("""
    <div style="font-size:12px; color:#81c995; padding: 0 4px; line-height:1.8;">
        <strong style="color:#b7e4c7;">📌 Acerca de</strong><br>
        Esta herramienta permite documentar, preservar y compartir el conocimiento
        botánico de tu territorio.
        <br><br>
        <em>Versión 1.0 — 2026-- Creado por: Jorge Alfredo Martínez Ramírez</em>
    </div>
    """, unsafe_allow_html=True)

# ─────────────────────────────────────────────
#  CARGA INICIAL DE DATOS
# ─────────────────────────────────────────────

df = cargar_datos()

# ══════════════════════════════════════════════
#  PÁGINA: INICIO
# ══════════════════════════════════════════════

if pagina == "🏡  Inicio":
    st.markdown("""
    <div class="hero-banner animate-fadein">
        <p class="hero-title">Herbario Digital<br>Comunitario 🌿</p>
        <p class="hero-subtitle">
            Preservando el conocimiento botánico de nuestro territorio,<br>
            una planta a la vez.
        </p>
    </div>
    """, unsafe_allow_html=True)

    # Métricas rápidas
    total = len(df)
    familias_unicas = df["Familia botánica"].nunique() if total else 0
    registradores = df["Registrado por"].nunique() if total else 0
    categorias_unicas = df["Categoría"].nunique() if total else 0

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("🌱 Plantas registradas", total)
    col2.metric("🔬 Familias botánicas", familias_unicas)
    col3.metric("👩‍🌾 Colaboradores", registradores)
    col4.metric("🏷️ Categorías", categorias_unicas)

    st.markdown("<hr class='divider'>", unsafe_allow_html=True)

    # Vista previa: últimas 3 plantas
    if not df.empty:
        st.markdown("### ✨ Plantas añadidas recientemente")
        ultimas = df.tail(3).iloc[::-1]
        cols = st.columns(min(len(ultimas), 3))
        for i, (_, row) in enumerate(ultimas.iterrows()):
            with cols[i]:
                img_html = ""
                b64 = imagen_a_base64(str(row.get("Imagen", "")))
                if b64:
                    img_html = f'<img class="planta-card-img" src="{b64}" alt="{row["Nombre común"]}">'
                else:
                    img_html = '<div class="planta-no-img">🌿</div>'

                cat = str(row.get("Categoría", "Otro"))
                st.markdown(f"""
                <div class="planta-card">
                    {img_html}
                    <div class="planta-card-body">
                        <div class="planta-card-familia">{row.get("Familia botánica","—")}</div>
                        <p class="planta-card-title">{row["Nombre común"]}</p>
                        <p class="planta-card-subtitle">{row["Nombre científico"]}</p>
                        {badge_categoria(cat)}
                        <p class="planta-card-desc">{str(row.get("Descripción",""))[:120]}…</p>
                    </div>
                    <div class="planta-card-footer">
                        👤 {row.get("Registrado por","—")} &nbsp;|&nbsp;
                        📅 {str(row.get("Fecha de registro","—"))[:10]}
                    </div>
                </div>
                """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class="info-box">
            🌱 ¡Aún no hay plantas registradas! Ve a <strong>Registrar planta</strong> para comenzar el herbario.
        </div>
        """, unsafe_allow_html=True)

    # ¿Cómo funciona?
    st.markdown("### 📖 ¿Cómo funciona?")
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown("""
        <div class="stats-card" style="text-align:center;">
            <div style="font-size:36px;">📷</div>
            <strong>1. Fotografía</strong>
            <p style="font-size:13px;color:#555;margin-top:8px;">
                Toma una foto de la planta en su hábitat natural.
            </p>
        </div>
        """, unsafe_allow_html=True)
    with c2:
        st.markdown("""
        <div class="stats-card" style="text-align:center;">
            <div style="font-size:36px;">✍️</div>
            <strong>2. Documenta</strong>
            <p style="font-size:13px;color:#555;margin-top:8px;">
                Registra su nombre, familia, usos y descripción.
            </p>
        </div>
        """, unsafe_allow_html=True)
    with c3:
        st.markdown("""
        <div class="stats-card" style="text-align:center;">
            <div style="font-size:36px;">🌍</div>
            <strong>3. Comparte</strong>
            <p style="font-size:13px;color:#555;margin-top:8px;">
                Construye memoria ecológica con tu comunidad.
            </p>
        </div>
        """, unsafe_allow_html=True)

# ══════════════════════════════════════════════
#  PÁGINA: GALERÍA
# ══════════════════════════════════════════════

elif pagina == "🖼️  Galería":
    st.markdown("## 🖼️ Galería del Herbario")

    if df.empty:
        st.markdown("""
        <div class="empty-state">
            <div class="icon">🌾</div>
            <h3>El herbario está vacío</h3>
            <p>Registra la primera planta para verla aquí.</p>
        </div>
        """, unsafe_allow_html=True)
    else:
        # ── Filtros ──
        with st.expander("🔍 Buscar y filtrar", expanded=True):
            col_b, col_c, col_f, col_h = st.columns([3, 2, 2, 2])
            with col_b:
                busqueda = st.text_input("🔍 Buscar por nombre", placeholder="Ej: Orquídea, Helecho…")
            with col_c:
                cats_disp = ["Todas"] + sorted(df["Categoría"].dropna().unique().tolist())
                filtro_cat = st.selectbox("Categoría", cats_disp)
            with col_f:
                fams_disp = ["Todas"] + sorted(df["Familia botánica"].dropna().unique().tolist())
                filtro_fam = st.selectbox("Familia botánica", fams_disp)
            with col_h:
                hab_disp = ["Todos"] + sorted(df["Hábitat"].dropna().unique().tolist())
                filtro_hab = st.selectbox("Hábitat", hab_disp)

        # ── Aplicar filtros ──
        df_filtrado = df.copy()

        if busqueda:
            mask = (
                df_filtrado["Nombre común"].str.contains(busqueda, case=False, na=False)
                | df_filtrado["Nombre científico"].str.contains(busqueda, case=False, na=False)
            )
            df_filtrado = df_filtrado[mask]

        if filtro_cat != "Todas":
            df_filtrado = df_filtrado[df_filtrado["Categoría"] == filtro_cat]

        if filtro_fam != "Todas":
            df_filtrado = df_filtrado[df_filtrado["Familia botánica"] == filtro_fam]

        if filtro_hab != "Todos":
            df_filtrado = df_filtrado[df_filtrado["Hábitat"] == filtro_hab]

        st.markdown(
            f"<p style='color:var(--texto-suave); font-size:14px;'>"
            f"Mostrando <strong>{len(df_filtrado)}</strong> de <strong>{len(df)}</strong> plantas</p>",
            unsafe_allow_html=True
        )

        if df_filtrado.empty:
            st.markdown("""
            <div class="empty-state">
                <div class="icon">🔍</div>
                <h3>Sin resultados</h3>
                <p>Intenta con otros filtros o términos de búsqueda.</p>
            </div>
            """, unsafe_allow_html=True)
        else:
            # ── Grilla de tarjetas ──
            NUM_COLS = 3
            filas = [
                df_filtrado.iloc[i:i + NUM_COLS]
                for i in range(0, len(df_filtrado), NUM_COLS)
            ]

            for fila in filas:
                cols = st.columns(NUM_COLS)
                for j, (_, row) in enumerate(fila.iterrows()):
                    with cols[j]:
                        cat = str(row.get("Categoría", "Otro"))
                        b64 = imagen_a_base64(str(row.get("Imagen", "")))

                        # ── Cabecera de la tarjeta (siempre visible) ──
                        img_html = (
                            f'<img class="planta-card-img" src="{b64}" alt="{row["Nombre común"]}">'
                            if b64
                            else '<div class="planta-no-img">🌿</div>'
                        )
                        st.markdown(f"""
                        <div class="planta-card" style="margin-bottom:0; border-radius:16px 16px 0 0;">
                            {img_html}
                            <div class="planta-card-body">
                                <div class="planta-card-familia">{row.get("Familia botánica","—")}</div>
                                <p class="planta-card-title">{row["Nombre común"]}</p>
                                <p class="planta-card-subtitle"><em>{row["Nombre científico"]}</em></p>
                                {badge_categoria(cat)}
                            </div>
                        </div>
                        """, unsafe_allow_html=True)

                        # ── Detalle completo con expander ──
                        with st.expander("📋 Ver información completa"):
                            if b64:
                                st.image(b64, use_container_width=True)

                            st.markdown(f"""
                            <div style="padding: 4px 0 8px;">
                                <p style="font-family:'Playfair Display',serif; font-size:20px;
                                          font-weight:700; color:#1a3d2b; margin:0 0 2px;">
                                    {row["Nombre común"]}
                                </p>
                                <p style="font-style:italic; font-size:13px;
                                          color:#4a6153; margin:0 0 10px;">
                                    {row["Nombre científico"]}
                                </p>
                            </div>
                            """, unsafe_allow_html=True)

                            col_a, col_b_ = st.columns(2)
                            with col_a:
                                st.markdown(f"🌿 **Familia:** {row.get('Familia botánica','—')}")
                                st.markdown(f"🏷️ **Categoría:** {cat}")
                            with col_b_:
                                st.markdown(f"🌍 **Hábitat:** {row.get('Hábitat','—')}")
                                st.markdown(f"👤 **Registrado por:** {row.get('Registrado por','—')}")

                            st.markdown(f"📅 **Fecha:** {str(row.get('Fecha de registro','—'))[:10]}")
                            st.markdown("---")
                            st.markdown("**📝 Descripción:**")
                            st.markdown(str(row.get("Descripción", "Sin descripción.")))

                            usos = str(row.get("Usos", "")).strip()
                            if usos:
                                st.markdown("**🌱 Usos conocidos:**")
                                st.markdown(usos)

# ══════════════════════════════════════════════
#  PÁGINA: REGISTRAR
# ══════════════════════════════════════════════

elif pagina == "➕  Registrar planta":
    st.markdown("## ➕ Registrar nueva planta")
    st.markdown("""
    <div style="
        background: linear-gradient(135deg, #e8f5e9, #f1f8e9);
        border-left: 4px solid #52b788;
        border-radius: 0 12px 12px 0;
        padding: 16px 20px;
        margin: 16px 0;
        font-size: 14px;
        color: #1a3d2b !important;
        font-family: 'DM Sans', sans-serif;
        font-weight: 500;
    ">
        📌 Completa todos los campos obligatorios (*) para añadir una planta al herbario.
        Cuanta más información incluyas, más valioso será el registro para la comunidad.
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="form-card">', unsafe_allow_html=True)

    with st.form("form_registro", clear_on_submit=True):
        st.markdown("### 🌱 Información taxonómica")
        col1, col2 = st.columns(2)
        with col1:
            nombre_comun = st.text_input("Nombre común *", placeholder="Ej: Árnica")
            familia = st.selectbox("Familia botánica *", FAMILIAS)
            habitat = st.selectbox("Hábitat *", HABITATS)
        with col2:
            nombre_cientifico = st.text_input("Nombre científico *", placeholder="Ej: Arnica montana")
            categoria = st.selectbox("Categoría *", CATEGORIAS)
            registrado_por = st.text_input("Registrado por *", placeholder="Tu nombre o comunidad")

        st.markdown("<hr class='divider'>", unsafe_allow_html=True)
        st.markdown("### 📝 Descripción y usos")

        descripcion = st.text_area(
            "Descripción *",
            placeholder="Describe la planta: características físicas, tamaño, flores, hojas…",
            height=120,
        )
        usos = st.text_area(
            "Usos conocidos",
            placeholder="Ej: Se usa para infusiones contra la fiebre, en cataplasmas…",
            height=100,
        )

        st.markdown("<hr class='divider'>", unsafe_allow_html=True)
        st.markdown("### 📷 Imagen de la planta")
        imagen = st.file_uploader(
            "Sube una fotografía (JPG, JPEG o PNG)",
            type=["jpg", "jpeg", "png"],
        )
        if imagen:
            st.image(imagen, width=300, caption="Vista previa")

        submitted = st.form_submit_button("💾 Guardar planta en el herbario", use_container_width=True)

        if submitted:
            campos_ok = all([nombre_comun, nombre_cientifico, descripcion, registrado_por, imagen])
            if campos_ok:
                ruta_img = guardar_imagen(imagen)
                nueva = pd.DataFrame([[
                    str(uuid.uuid4()),
                    nombre_comun.strip(),
                    nombre_cientifico.strip(),
                    familia,
                    categoria,
                    habitat,
                    descripcion.strip(),
                    usos.strip(),
                    registrado_por.strip(),
                    datetime.now().strftime("%Y-%m-%d"),
                    ruta_img,
                ]], columns=COLUMNAS)

                df = pd.concat([df, nueva], ignore_index=True)
                guardar_datos(df)
                st.success(f"✅ **{nombre_comun}** ha sido registrada correctamente en el herbario.")
                st.balloons()
                st.rerun()
            else:
                st.error("⚠️ Por favor completa todos los campos obligatorios (*) e incluye una imagen.")

    st.markdown('</div>', unsafe_allow_html=True)

# ══════════════════════════════════════════════
#  PÁGINA: EDITAR / ELIMINAR
# ══════════════════════════════════════════════

elif pagina == "✏️  Editar / Eliminar":
    st.markdown("## ✏️ Editar o eliminar planta")

    df = cargar_datos()

    if df.empty:
        st.markdown("""
        <div class="empty-state">
            <div class="icon">🌾</div>
            <h3>Sin plantas para gestionar</h3>
            <p>Primero registra algunas plantas.</p>
        </div>
        """, unsafe_allow_html=True)
    else:
        planta_id = st.selectbox(
            "Selecciona una planta",
            df["ID"].tolist(),
            format_func=lambda x: (
                f"{df[df['ID']==x]['Nombre común'].values[0]}"
                f" — {df[df['ID']==x]['Nombre científico'].values[0]}"
            ),
        )

        planta = df[df["ID"] == planta_id].iloc[0]

        # Vista previa de la imagen
        col_img, col_info = st.columns([1, 2])
        with col_img:
            b64 = imagen_a_base64(str(planta.get("Imagen", "")))
            if b64:
                st.image(b64, use_container_width=True)
            else:
                st.markdown('<div class="planta-no-img" style="border-radius:12px;">🌿</div>', unsafe_allow_html=True)

        with col_info:
            st.markdown(f"""
            <div style="padding:16px 0;">
                <p class="planta-card-title" style="font-size:22px;">{planta["Nombre común"]}</p>
                <p class="planta-card-subtitle"><em>{planta["Nombre científico"]}</em></p>
                {badge_categoria(str(planta.get("Categoría","Otro")))}
                <br><br>
                <span style="font-size:13px;color:var(--texto-suave);">
                    🌿 {planta.get("Familia botánica","—")} &nbsp;|&nbsp;
                    🌍 {planta.get("Hábitat","—")} &nbsp;|&nbsp;
                    👤 {planta.get("Registrado por","—")}
                </span>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("<hr class='divider'>", unsafe_allow_html=True)
        st.markdown("### ✏️ Modificar información")

        with st.form("form_edicion"):
            col1, col2 = st.columns(2)
            with col1:
                n_comun = st.text_input("Nombre común", planta["Nombre común"])
                n_familia = st.selectbox(
                    "Familia botánica",
                    FAMILIAS,
                    index=FAMILIAS.index(planta.get("Familia botánica", FAMILIAS[0]))
                    if planta.get("Familia botánica") in FAMILIAS else 0,
                )
                n_habitat = st.selectbox(
                    "Hábitat",
                    HABITATS,
                    index=HABITATS.index(planta.get("Hábitat", HABITATS[0]))
                    if planta.get("Hábitat") in HABITATS else 0,
                )
            with col2:
                n_cientifico = st.text_input("Nombre científico", planta["Nombre científico"])
                n_categoria = st.selectbox(
                    "Categoría",
                    CATEGORIAS,
                    index=CATEGORIAS.index(planta.get("Categoría", CATEGORIAS[0]))
                    if planta.get("Categoría") in CATEGORIAS else 0,
                )
                n_registrado = st.text_input("Registrado por", planta.get("Registrado por", ""))

            n_descripcion = st.text_area("Descripción", planta.get("Descripción", ""), height=120)
            n_usos = st.text_area("Usos conocidos", planta.get("Usos", ""), height=100)

            nueva_img = st.file_uploader("Reemplazar imagen (opcional)", type=["jpg", "jpeg", "png"])
            if nueva_img:
                st.image(nueva_img, width=250, caption="Nueva imagen")

            col_save, col_del = st.columns([2, 1])
            with col_save:
                guardar = st.form_submit_button("💾 Guardar cambios", use_container_width=True)
            with col_del:
                eliminar = st.form_submit_button("🗑️ Eliminar planta", use_container_width=True)

            if guardar:
                df.loc[df["ID"] == planta_id, "Nombre común"] = n_comun
                df.loc[df["ID"] == planta_id, "Nombre científico"] = n_cientifico
                df.loc[df["ID"] == planta_id, "Familia botánica"] = n_familia
                df.loc[df["ID"] == planta_id, "Categoría"] = n_categoria
                df.loc[df["ID"] == planta_id, "Hábitat"] = n_habitat
                df.loc[df["ID"] == planta_id, "Descripción"] = n_descripcion
                df.loc[df["ID"] == planta_id, "Usos"] = n_usos
                df.loc[df["ID"] == planta_id, "Registrado por"] = n_registrado

                if nueva_img:
                    ruta = guardar_imagen(nueva_img)
                    df.loc[df["ID"] == planta_id, "Imagen"] = ruta

                guardar_datos(df)
                st.success("✅ Cambios guardados correctamente.")
                st.rerun()

            if eliminar:
                nombre_eliminado = planta["Nombre común"]
                df = df[df["ID"] != planta_id]
                guardar_datos(df)
                st.warning(f"🗑️ **{nombre_eliminado}** ha sido eliminada del herbario.")
                st.rerun()

# ══════════════════════════════════════════════
#  PÁGINA: ESTADÍSTICAS
# ══════════════════════════════════════════════

elif pagina == "📊  Estadísticas":
    st.markdown("## 📊 Estadísticas del Herbario")

    df = cargar_datos()

    if df.empty:
        st.markdown("""
        <div class="empty-state">
            <div class="icon">📊</div>
            <h3>Sin datos para mostrar</h3>
            <p>Registra plantas para ver las estadísticas del herbario.</p>
        </div>
        """, unsafe_allow_html=True)
    else:
        # ── KPIs ──
        total = len(df)
        familias = df["Familia botánica"].nunique()
        colaboradores = df["Registrado por"].nunique()
        cat_mas = df["Categoría"].value_counts().idxmax() if not df["Categoría"].isnull().all() else "—"

        c1, c2, c3, c4 = st.columns(4)
        c1.metric("🌱 Total plantas", total)
        c2.metric("🔬 Familias botánicas", familias)
        c3.metric("👩‍🌾 Colaboradores", colaboradores)
        c4.metric("🏆 Categoría más común", cat_mas)

        st.markdown("<hr class='divider'>", unsafe_allow_html=True)

        # ── Gráficas ──
        col_g1, col_g2 = st.columns(2)

        with col_g1:
            st.markdown('<div class="stats-card">', unsafe_allow_html=True)
            st.markdown("### Distribución por categoría")
            cat_counts = df["Categoría"].value_counts().reset_index()
            cat_counts.columns = ["Categoría", "Cantidad"]
            colores = ["#2d6a4f", "#52b788", "#95d5b2", "#b7e4c7", "#d8f3dc"]
            fig_cat = px.pie(
                cat_counts,
                values="Cantidad",
                names="Categoría",
                color_discrete_sequence=colores,
                hole=0.4,
            )
            fig_cat.update_layout(
                margin=dict(t=20, b=20, l=20, r=20),
                showlegend=True,
                font_family="DM Sans",
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
            )
            st.plotly_chart(fig_cat, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)

        with col_g2:
            st.markdown('<div class="stats-card">', unsafe_allow_html=True)
            st.markdown("### Plantas por familia botánica")
            fam_counts = df["Familia botánica"].value_counts().reset_index().head(10)
            fam_counts.columns = ["Familia", "Cantidad"]
            fig_fam = px.bar(
                fam_counts,
                x="Cantidad",
                y="Familia",
                orientation="h",
                color="Cantidad",
                color_continuous_scale=["#b7e4c7", "#2d6a4f"],
            )
            fig_fam.update_layout(
                margin=dict(t=20, b=20, l=20, r=20),
                yaxis=dict(autorange="reversed"),
                font_family="DM Sans",
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                coloraxis_showscale=False,
            )
            st.plotly_chart(fig_fam, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)

        # ── Segunda fila ──
        col_g3, col_g4 = st.columns(2)

        with col_g3:
            st.markdown('<div class="stats-card">', unsafe_allow_html=True)
            st.markdown("### Hábitats representados")
            hab_counts = df["Hábitat"].value_counts().reset_index()
            hab_counts.columns = ["Hábitat", "Cantidad"]
            fig_hab = px.bar(
                hab_counts,
                x="Hábitat",
                y="Cantidad",
                color="Cantidad",
                color_continuous_scale=["#d8f3dc", "#1a3d2b"],
            )
            fig_hab.update_layout(
                margin=dict(t=20, b=60, l=20, r=20),
                font_family="DM Sans",
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                coloraxis_showscale=False,
                xaxis_tickangle=-35,
            )
            st.plotly_chart(fig_hab, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)

        with col_g4:
            st.markdown('<div class="stats-card">', unsafe_allow_html=True)
            st.markdown("### Aportes por colaborador")
            col_counts = df["Registrado por"].value_counts().reset_index().head(10)
            col_counts.columns = ["Colaborador", "Plantas"]
            fig_col = px.bar(
                col_counts,
                x="Colaborador",
                y="Plantas",
                color="Plantas",
                color_continuous_scale=["#95d5b2", "#1a3d2b"],
            )
            fig_col.update_layout(
                margin=dict(t=20, b=60, l=20, r=20),
                font_family="DM Sans",
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                coloraxis_showscale=False,
                xaxis_tickangle=-30,
            )
            st.plotly_chart(fig_col, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)

        # ── Tabla completa ──
        st.markdown("<hr class='divider'>", unsafe_allow_html=True)
        st.markdown("### 📋 Listado completo")
        columnas_tabla = ["Nombre común", "Nombre científico", "Familia botánica", "Categoría", "Hábitat", "Registrado por", "Fecha de registro"]
        cols_mostrar = [c for c in columnas_tabla if c in df.columns]
        st.dataframe(
            df[cols_mostrar].sort_values("Nombre común"),
            use_container_width=True,
            hide_index=True,
        )

        # Descarga CSV
        csv_bytes = df.to_csv(index=False).encode("utf-8")
        st.download_button(
            label="⬇️ Descargar datos completos (CSV)",
            data=csv_bytes,
            file_name="herbario_digital.csv",
            mime="text/csv",
        )