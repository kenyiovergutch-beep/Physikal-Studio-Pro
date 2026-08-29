import streamlit as st
import math
import plotly.graph_objects as go
import numpy as np
import io

# Intento de importación de ReportLab para exportar reportes en PDF profesional
try:
    from reportlab.lib.pagesizes import letter
    from reportlab.pdfgen import canvas
    REPORTLAB_AVAILABLE = True
except ImportError:
    REPORTLAB_AVAILABLE = False

# ------------------------------------------------------------------------------
# 1. CONFIGURACIÓN DE PÁGINA Y ESTILOS CSS PERSONALIZADOS
# ------------------------------------------------------------------------------
st.set_page_config(
    page_title="Physikal Studio Pro", 
    layout="wide"
)

import streamlit as st
import urllib.parse
import requests

# 2. AQUÍ INSERTA EL CÓDIGO DE AUTENTICACIÓN (Punto 1)
try:
    oauth_config = st.secrets["google_oauth"]
except Exception:
    st.error("Faltan las credenciales en Secrets.")
    st.stop()

def get_google_auth_url():
    params = {
        "client_id": oauth_config["client_id"],
        "redirect_uri": oauth_config["redirect_uri"],
        "response_type": "code",
        "scope": "openid email profile",
        "access_type": "online",
        "prompt": "select_account"
    }
    return f"https://accounts.google.com/o/oauth2/v2/auth?{urllib.parse.urlencode(params)}"

if "user_info" not in st.session_state:
    st.session_state["user_info"] = None

query_params = st.query_params
if "code" in query_params and st.session_state["user_info"] is None:
    code = query_params["code"]
    token_url = "https://oauth2.googleapis.com/token"
    data = {
        "code": code,
        "client_id": oauth_config["client_id"],
        "client_secret": oauth_config["client_secret"],
        "redirect_uri": oauth_config["redirect_uri"],
        "grant_type": "authorization_code",
    }
    response = requests.post(token_url, data=data)
    if response.status_code == 200:
        tokens = response.json()
        access_token = tokens.get("access_token")
        user_info_resp = requests.get(
            "https://www.googleapis.com/oauth2/v2/userinfo",
            headers={"Authorization": f"Bearer {access_token}"}
        )
        if user_info_resp.status_code == 200:
            st.session_state["user_info"] = user_info_resp.json()
            st.query_params.clear()
            st.rerun()

user = st.session_state["user_info"]

user = st.session_state["user_info"]

# --- BLOQUE FALTANTE: Si NO hay usuario, muestra el botón y detiene la ejecución ---
if not user:
    # Estilos CSS para el fondo y la tarjeta centrada
    st.markdown("""
        <style>
        /* Fondo con degradado moderno */
        .stApp {
            background: linear-gradient(135deg, #0f172a 0%, #1e1b4b 50%, #311042 100%);
        }
        
        /* Ocultar la barra lateral cuando no hay sesión */
        [data-testid="stSidebar"] {
            display: none;
        }

        /* Estilo del botón de Google */
        .google-btn {
            display: inline-flex;
            align-items: center;
            justify-content: center;
            background-color: #ffffff;
            color: #1f2937;
            font-weight: 600;
            font-size: 16px;
            padding: 12px 24px;
            border-radius: 8px;
            text-decoration: none;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
            transition: all 0.2s ease;
            margin-top: 15px;
        }
        .google-btn:hover {
            background-color: #f3f4f6;
            transform: translateY(-2px);
            box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.2);
            color: #111827;
        }
        </style>
    """, unsafe_allow_html=True)

    # Estructura en columnas para centrar horizontalmente
    col1, col2, col3 = st.columns([1, 2, 1])

    with col2:
        st.write("##")  # Espaciado vertical
        st.write("##")
        
        # Tarjeta contenedora centrada
        with st.container(border=True):
            st.markdown("<h1 style='text-align: center; color: #ffffff;'>⚡ PhysiKal Studio Pro</h1>", unsafe_allow_html=True)
            st.markdown("<p style='text-align: center; color: #94a3b8; font-size: 16px;'>Inicia sesión con tu cuenta de Google para ingresar a la plataforma.</p>", unsafe_allow_html=True)
            st.markdown("---")
            
            auth_url = get_google_auth_url()
            
            # Botón centrado con icono de Google
            st.markdown(f'''
                <div style="text-align: center;">
                    <a href="{auth_url}" target="_self" class="google-btn">
                        <img src="https://www.svgrepo.com/show/475656/google-color.svg" width="20" style="margin-right: 10px; vertical-align: middle;">
                        Iniciar sesión con Google
                    </a>
                </div>
            ''', unsafe_allow_html=True)
            
            st.write("##")

    st.stop()

# Si SI hay usuario, muestra su foto/email en la barra lateral
with st.sidebar:
    if "picture" in user:
        st.image(user["picture"], width=60)
    st.write(f"**{user.get('name', 'Usuario')}**")
    st.write(f"*{user.get('email', '')}*")
    
    if st.button("Cerrar Sesión"):
        st.session_state["user_info"] = None
        st.rerun()
        
# 3. AHORA TUS ESTILOS PERSONALIZADOS (CSS, colores, etc.)
# st.markdown("<style>...</style>", unsafe_allow_html=True)
# Inicializar sesión de tema si no existe
if "tema" not in st.session_state:
    st.session_state.tema = "Oscuro"

# Menú de configuración en la barra lateral
st.sidebar.markdown("### Estilo Visual")
modo = st.sidebar.radio("Selecciona el Tema:", ["Oscuro", "Claro"], key="selector_tema")

if modo == "Oscuro":
    bg_app = "#0F172A"
    text_color = "#F8FAFC"
    card_bg = "#1E293B"
    card_border = "#334155"
    subtext_color = "#94A3B8"
else:
    bg_app = "#F8FAFC"
    text_color = "#0F172A"
    card_bg = "#FFFFFF"
    card_border = "#E2E8F0"
    subtext_color = "#64748B"

custom_css = f"""
<style>
    .stApp {{
        background-color: {bg_app};
        color: {text_color};
    }}
    
    .main-header {{
        font-size: 2.6rem;
        font-weight: 800;
        background: linear-gradient(90deg, #38BDF8 0%, #818CF8 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.2rem;
    }}
    
    .sub-header {{
        font-size: 1.05rem;
        color: {subtext_color};
        margin-bottom: 1.5rem;
    }}

    .metric-card {{
        background-color: {card_bg};
        border: 1px solid {card_border};
        border-radius: 12px;
        padding: 1.5rem;
        margin-bottom: 1rem;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
    }}
    
    .result-box {{
        background: linear-gradient(135deg, #064E3B 0%, #047857 100%);
        border: 1px solid #10B981;
        border-radius: 10px;
        padding: 1.2rem;
        color: #ECFDF5;
        font-size: 1.25rem;
        font-weight: 700;
        text-align: center;
        margin-top: 1rem;
    }}

    section[data-testid="stSidebar"] {{
        background-color: {card_bg};
        border-right: 1px solid {card_border};
    }}

    .stButton>button {{
        background: linear-gradient(90deg, #2563EB 0%, #3B82F6 100%);
        color: white;
        font-weight: 600;
        border: none;
        border-radius: 8px;
        padding: 0.5rem 1.2rem;
        transition: all 0.3s ease;
    }}
    
    .stButton>button:hover {{
        background: linear-gradient(90deg, #1D4ED8 0%, #2563EB 100%);
        box-shadow: 0 4px 12px rgba(37, 99, 235, 0.4);
    }}
</style>
"""

st.markdown(custom_css, unsafe_allow_html=True)

# ------------------------------------------------------------------------------
# 2. HISTORIAL DE CÁLCULOS Y GENERADOR PDF
# ------------------------------------------------------------------------------
if "historial" not in st.session_state:
    st.session_state.historial = []

def guardar_historial(cat, form, res):
    st.session_state.historial.append({"categoria": cat, "formula": form, "resultado": res})

def generar_pdf_historial(historial):
    buffer = io.BytesIO()
    p = canvas.Canvas(buffer, pagesize=letter)
    p.setFont("Helvetica-Bold", 16)
    p.drawString(50, 750, "Reporte de Cálculos - Studio Pro")
    p.setFont("Helvetica", 10)
    p.drawString(50, 735, "Generado automáticamente por Studio Pro")
    p.line(50, 725, 550, 725)
    
    y = 700
    p.setFont("Helvetica", 11)
    for idx, item in enumerate(reversed(historial), 1):
        if y < 60:
            p.showPage()
            y = 750
            p.setFont("Helvetica", 11)
        p.setFont("Helvetica-Bold", 11)
        p.drawString(50, y, f"{idx}. [{item['categoria']}] - {item['formula']}")
        y -= 15
        p.setFont("Helvetica", 10)
        p.drawString(65, y, f"Resultado: {item['resultado']}")
        y -= 25
        
    p.save()
    buffer.seek(0)
    return buffer

# --- SELECCIÓN DE ROL / PORTADA DE BIENVENIDA ---
if "user_role" not in st.session_state:
    st.session_state.user_role = None

if st.session_state.user_role is None:
    # Encabezado principal estilo neón
    st.markdown("""
        <div style="background: rgba(15, 23, 42, 0.75); border: 1px solid #38bdf8; box-shadow: 0 0 20px rgba(56, 189, 248, 0.25); border-radius: 16px; padding: 30px; text-align: center; margin-bottom: 25px;">
            <h1 style="color: #38bdf8; font-family: 'Courier New', monospace; font-size: 2.5rem; font-weight: bold; margin-bottom: 5px;"> PHYSIKAL STUDIO PRO</h1>
            <p style="color: #94a3b8; font-size: 1.1rem; margin: 0;">Plataforma Interactiva para el Cálculo Científico, Física Avanzada y Simulaciones</p>
        </div>
    """, unsafe_allow_html=True)

    col_img1, col_img2, col_img3 = st.columns([1, 2, 1])
    with col_img2:
        try:
            st.image("logo.png", use_container_width=True)
        except Exception:
            pass

    st.markdown("<h3 style='text-align: center; color: #e2e8f0; margin-top: 20px;'> Para comenzar, selecciona tu perfil:</h3>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        st.info("###  Modo Estudiante\nAccede a calculadoras paso a paso, solucionarios interactivos y herramientas de práctica.")
        if st.button("Ingresar como Estudiante", use_container_width=True, type="primary"):
            st.session_state.user_role = "Estudiante"
            st.rerun()

    with col2:
        st.success("###  Modo Profesor\nDiseña problemas personalizados, genera reportes en PDF y recursos para laboratorio.")
        if st.button("Ingresar como Profesor", use_container_width=True):
            st.session_state.user_role = "Profesor"
            st.rerun()

    st.stop()  # Detiene la carga hasta que elijan rol

# Mostrar el perfil en la barra lateral
st.sidebar.markdown(f" Perfil activo: **{st.session_state.user_role}**")
if st.sidebar.button(" Cambiar Perfil"):
    st.session_state.user_role = None
    st.rerun()

# ==========================================
# SECCIÓN MODOS DE USUARIO: ESTUDIANTE / PROFESOR
# ==========================================

# ------------------------------------------
#  MODO ESTUDIANTE: Práctica Paso a Paso
# ------------------------------------------

if st.session_state.user_role == "Estudiante":
    st.markdown("##  Área de Práctica y Solucionarios Paso a Paso")
    st.info("Selecciona un tema para poner a prueba tus conocimientos y ver soluciones explicadas a detalle.")
    
    tema_estudiante = st.selectbox(
        " Selecciona la materia o módulo de práctica:",
        ["Cinemática: MRU y MRUA", "Dinámica: Leyes de Newton", "Trabajo y Energía"]
    )
    
    if tema_estudiante == "Cinemática: MRU y MRUA":
        st.markdown("###  Problema de Práctica")
        st.write("**Enunciado:** Un automóvil parte del reposo y acelera a razón constante de $2.5 \\text{ m/s}^2$ durante $8 \\text{ s}$. ¿Cuál es la distancia total recorrida?")
        
        respuesta = st.radio("Elige tu respuesta:", ["80 metros", "100 metros", "160 metros", "64 metros"])
        
        col_btn1, col_btn2 = st.columns([1, 4])
        with col_btn1:
            if st.button("Verificar Respuesta", type="primary"):
                if respuesta == "100 metros":
                    st.success(" ¡Correcto! La distancia recorrida es $100 \\text{ m}$.")
                else:
                    st.error(" Respuesta incorrecta. Inténtalo de nuevo o revisa el solucionario.")
        
        with st.expander(" Ver Solucionario Paso a Paso"):
            st.markdown("""
            **Paso 1: Identificar datos e incógnitas**
            * Velocidad inicial ($v_0$) = $0 \\text{ m/s}$ (parte del reposo)
            * Aceleración ($a$) = $2.5 \\text{ m/s}^2$
            * Tiempo ($t$) = $8 \\text{ s}$
            * Distancia ($d$) = $?$

            **Paso 2: Seleccionar la fórmula adecuada**
            $$d = v_0 t + \\frac{1}{2} a t^2$$

            **Paso 3: Sustituir valores**
            $$d = (0)(8) + \\frac{1}{2} (2.5) (8)^2$$
            $$d = 0 + 1.25 \\times 64 = 100 \\text{ m}$$
            """)

elif st.session_state.user_role == "Profesor":
    st.markdown("##  Panel de Control de Docente")
    st.info("Diseña exámenes personalizados y genera guías de trabajo para tus clases.")
    
    tab1, tab2 = st.tabs([" Generador de Exámenes", " Registro de Asistencia y Calificaciones"])
    
    with tab1:
        st.markdown("### Configuración de la Evaluación")
        col_prof1, col_prof2 = st.columns(2)
        with col_prof1:
            titulo_examen = st.text_input("Título de la prueba/guía:", "Examen Parcial de Física I")
            nivel = st.selectbox("Nivel educativo:", ["Secundaria", "Universidad - Física General", "Universidad - Avanzado"])
        with col_prof2:
            num_preguntas = st.number_input("Número de ejercicios a incluir:", min_value=1, max_value=20, value=5)
            incluir_solucionario = st.checkbox("Incluir clave de respuestas al final", value=True)
            
        st.markdown("---")
        st.markdown("### Vista Previa del Material")
        st.markdown(f"#### 📄 {titulo_examen}")
        st.caption(f"Nivel: {nivel} | Total de ítems: {num_preguntas}")
        
        for i in range(1, num_preguntas + 1):
            m_val = i * 2
            f_val = i * 10
            st.markdown(f"**{i}.** *[Ejercicio de {nivel}]* Un cuerpo de masa $m = {m_val} \\text{{ kg}}$ experimenta una fuerza constante de ${f_val} \\text{{ N}}$. Calcule la aceleración del sistema.")
        
        st.button(" Exportar Guía a PDF / Imprimir", help="Próximamente exportación directa a PDF")

    with tab2:
        st.markdown("### Registro de Asistencia y Evaluaciones")
        st.write("Módulo para seguimiento del grupo y control de entregas de laboratorio.")
        
# ------------------------------------------------------------------------------
# 3. ENCABEZADO Y BUSCADOR RÁPIDO
# ------------------------------------------------------------------------------
st.markdown('<div class="main-header">Studio Pro</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Plataforma interactiva de resolución, conversión, análisis vectorial y simulación gráfica</div>', unsafe_allow_html=True)

diccionario_search = {
    "MRU: Distancia": ("Mecánica", "d = v * t"),
    "MRU: Tiempo": ("Mecánica", "t = d / v"),
    "MRUV: Velocidad Final": ("Mecánica", "vf = v0 + a * t"),
    "MRUV: Distancia": ("Mecánica", "d = v0 * t + 0.5 * a * t²"),
    "1ª Ley de Newton (Inercia)": ("Mecánica", "ΣF = 0"),
    "2ª Ley de Newton (Fuerza)": ("Mecánica", "F = m * a"),
    "Peso": ("Mecánica", "P = m * g"),
    "3ª Ley de Newton (Reacción)": ("Mecánica", "FAB = -FBA"),
    "Trabajo Mecánico": ("Mecánica", "W = F * d"),
    "Alcance Proyectil": ("Mecánica", "R = v0² * sin(2θ) / g"),
    "Energía Cinética": ("Energía y Potencia", "Ec = 0.5 * m * v²"),
    "Energía Potencial": ("Energía y Potencia", "Ep = m * g * h"),
    "Energía Mecánica": ("Energía y Potencia", "Em = Ec + Ep"),
    "Potencia Mecánica": ("Energía y Potencia", "P = W / t"),
    "Rendimiento": ("Energía y Potencia", "% = (Pu / Pt) * 100"),
    "Presión General": ("Presión y Fluidos", "P = F / A"),
    "Densidad": ("Presión y Fluidos", "ρ = m / V"),
    "Presión Hidrostática": ("Presión y Fluidos", "P = P0 + ρ * g * h"),
    "Caudal": ("Presión y Fluidos", "Q = V / t"),
    "Ecuación de Bernoulli": ("Hidrodinámica", "P1 + ½ρv1² + ρgh1 = P2 + ½ρv2² + ρgh2"),
    "Ecuación de Continuidad": ("Hidrodinámica", "A1 * v1 = A2 * v2"),
    "Péndulo Simple": ("Movimiento Armónico Simple", "T = 2π √(L / g)"),
    "Masa-Resorte": ("Movimiento Armónico Simple", "T = 2π √(m / k)"),
    "Ley de Ohm (Voltaje)": ("Electricidad", "V = I * R"),
    "Resistencia Paralelo": ("Electricidad", "1/R_eq = 1/R1 + 1/R2"),
    "Gases Ideales": ("Termodinámica", "P * V = n * R * T"),
    "Celsius a Kelvin": ("Termodinámica", "K = C + 273.15"),
    "Celsius a Fahrenheit": ("Termodinámica", "F = (C * 9/5) + 32"),
    "Calor Sensible": ("Termodinámica", "Q = m * c * ΔT"),
    "Dilatación Lineal": ("Termodinámica", "ΔL = L0 * α * ΔT"),
    "Velocidad de Onda": ("Óptica y Ondas", "v = λ * f"),
    "Frecuencia (Periodo)": ("Óptica y Ondas", "f = 1 / T"),
    "Ley de Snell": ("Óptica y Ondas", "n2 = (n1 * sin θ1) / sin θ2"),
    "Focal Lentes": ("Óptica y Ondas", "f = (do * di) / (do + di)"),
    "Energía Fotón": ("Óptica y Ondas", "E = h * f"),
    "Ley de Coulomb": ("Electromagnetismo", "F = k * |q1 * q2| / r²"),
    "Campo Eléctrico": ("Electromagnetismo", "E = F / q"),
    "Fuerza de Lorentz": ("Electromagnetismo", "F = |q| * v * B * sin(θ)"),
    "Gravitación Universal": ("Mecánica Celeste", "F = G * m1 * m2 / r²"),
    "Velocidad Orbital": ("Mecánica Celeste", "v = √(G * M / r)"),
    "Gravedad Superficial": ("Mecánica Celeste", "g = G * M / R²"),
    "Masa-Energía": ("Física Moderna", "E = m * c²"),
    "Onda De Broglie": ("Física Moderna", "λ = h / p"),
    "Factor Lorentz": ("Física Moderna", "γ = 1 / √(1 - v²/c²)")
}

with st.expander("Buscador Dinámico de Fórmulas"):
    busqueda = st.text_input("Escribe el nombre de la fórmula (Ej: Bernoulli, Péndulo, Ohm):")
    if busqueda:
        res = [k for k in diccionario_search.keys() if busqueda.lower() in k.lower()]
        if res:
            for item in res:
                cat, form = diccionario_search[item]
                st.write(f"- **{item}** | Categoría: `{cat}` | Fórmula: `{form}`")
        else:
            st.warning("No se encontraron coincidencias.")

st.markdown("---")

# ------------------------------------------------------------------------------
# 4. MENÚ LATERAL Y SELECCIÓN DE CATEGORÍA
# ------------------------------------------------------------------------------
st.sidebar.markdown("### Navegación")
categoria = st.sidebar.selectbox(
    "Selecciona un Módulo / Categoría:", 
    [
        "Conversor de Unidades",
        "Álgebra Vectorial 2D/3D",
        "Tabla de Constantes Físicas",
        "Mecánica", 
        "Movimiento Armónico Simple",
        "Energía y Potencia", 
        "Presión y Fluidos", 
        "Hidrodinámica",
        "Electricidad", 
        "Termodinámica", 
        "Óptica y Ondas", 
        "Electromagnetismo", 
        "Mecánica Celeste",
        "Física Moderna",
        "creador de gráficas"
    ]
)

# ------------------------------------------------------------------------------
# 5. HERRAMIENTAS GLOBALES (CONVERSOR, VECTORES, CONSTANTES)
# ------------------------------------------------------------------------------

if categoria == "Conversor de Unidades":
    st.subheader("Conversor Universal de Unidades Físicas")
    st.markdown('<div class="metric-card">', unsafe_allow_html=True)
    
    t_conv1, t_conv2, t_conv3, t_conv4, t_conv5 = st.tabs(["Longitud", "Masa", "Velocidad", "Energía", "Presión"])
    
    with t_conv1:
        c1, c2, c3 = st.columns(3)
        val = c1.number_input("Valor a convertir:", value=1.0, key="conv_l_val")
        u_in = c2.selectbox("De:", ["Metros (m)", "Kilómetros (km)", "Millas (mi)", "Pies (ft)", "Pulgadas (in)"], key="conv_l_in")
        u_out = c3.selectbox("A:", ["Metros (m)", "Kilómetros (km)", "Millas (mi)", "Pies (ft)", "Pulgadas (in)"], key="conv_l_out")
        
        factors_l = {"Metros (m)": 1.0, "Kilómetros (km)": 1000.0, "Millas (mi)": 1609.34, "Pies (ft)": 0.3048, "Pulgadas (in)": 0.0254}
        if st.button("Convertir Longitud"):
            res = (val * factors_l[u_in]) / factors_l[u_out]
            res_str = f"{val} {u_in} = {res:.4f} {u_out}"
            st.markdown(f'<div class="result-box">{res_str}</div>', unsafe_allow_html=True)
            guardar_historial("Conversión Longitud", f"{u_in} -> {u_out}", res_str)

    with t_conv2:
        c1, c2, c3 = st.columns(3)
        val = c1.number_input("Valor a convertir:", value=1.0, key="conv_m_val")
        u_in = c2.selectbox("De:", ["Kilogramos (kg)", "Gramos (g)", "Libras (lb)", "Onzas (oz)"], key="conv_m_in")
        u_out = c3.selectbox("A:", ["Kilogramos (kg)", "Gramos (g)", "Libras (lb)", "Onzas (oz)"], key="conv_m_out")
        
        factors_m = {"Kilogramos (kg)": 1.0, "Gramos (g)": 0.001, "Libras (lb)": 0.453592, "Onzas (oz)": 0.0283495}
        if st.button("Convertir Masa"):
            res = (val * factors_m[u_in]) / factors_m[u_out]
            res_str = f"{val} {u_in} = {res:.4f} {u_out}"
            st.markdown(f'<div class="result-box">{res_str}</div>', unsafe_allow_html=True)
            guardar_historial("Conversión Masa", f"{u_in} -> {u_out}", res_str)

    with t_conv3:
        c1, c2, c3 = st.columns(3)
        val = c1.number_input("Valor a convertir:", value=100.0, key="conv_v_val")
        u_in = c2.selectbox("De:", ["m/s", "km/h", "mph"], key="conv_v_in")
        u_out = c3.selectbox("A:", ["m/s", "km/h", "mph"], key="conv_v_out")
        
        factors_v = {"m/s": 1.0, "km/h": 1/3.6, "mph": 0.44704}
        if st.button("Convertir Velocidad"):
            res = (val * factors_v[u_in]) / factors_v[u_out]
            res_str = f"{val} {u_in} = {res:.4f} {u_out}"
            st.markdown(f'<div class="result-box">{res_str}</div>', unsafe_allow_html=True)
            guardar_historial("Conversión Velocidad", f"{u_in} -> {u_out}", res_str)

    with t_conv4:
        c1, c2, c3 = st.columns(3)
        val = c1.number_input("Valor a convertir:", value=1.0, key="conv_e_val")
        u_in = c2.selectbox("De:", ["Joules (J)", "Calorías (cal)", "Kilovatios-hora (kWh)", "Electronvoltios (eV)"], key="conv_e_in")
        u_out = c3.selectbox("A:", ["Joules (J)", "Calorías (cal)", "Kilovatios-hora (kWh)", "Electronvoltios (eV)"], key="conv_e_out")
        
        factors_e = {"Joules (J)": 1.0, "Calorías (cal)": 4.184, "Kilovatios-hora (kWh)": 3.6e6, "Electronvoltios (eV)": 1.60218e-19}
        if st.button("Convertir Energía"):
            res = (val * factors_e[u_in]) / factors_e[u_out]
            res_str = f"{val} {u_in} = {res:.6e} {u_out}"
            st.markdown(f'<div class="result-box">{res_str}</div>', unsafe_allow_html=True)
            guardar_historial("Conversión Energía", f"{u_in} -> {u_out}", res_str)

    with t_conv5:
        c1, c2, c3 = st.columns(3)
        val = c1.number_input("Valor a convertir:", value=1.0, key="conv_p_val")
        u_in = c2.selectbox("De:", ["Pascales (Pa)", "Atmósferas (atm)", "Bares (bar)", "mmHg (Torr)"], key="conv_p_in")
        u_out = c3.selectbox("A:", ["Pascales (Pa)", "Atmósferas (atm)", "Bares (bar)", "mmHg (Torr)"], key="conv_p_out")
        
        factors_p = {"Pascales (Pa)": 1.0, "Atmósferas (atm)": 101325.0, "Bares (bar)": 100000.0, "mmHg (Torr)": 133.322}
        if st.button("Convertir Presión"):
            res = (val * factors_p[u_in]) / factors_p[u_out]
            res_str = f"{val} {u_in} = {res:.4f} {u_out}"
            st.markdown(f'<div class="result-box">{res_str}</div>', unsafe_allow_html=True)
            guardar_historial("Conversión Presión", f"{u_in} -> {u_out}", res_str)

    st.markdown('</div>', unsafe_allow_html=True)

elif categoria == "Álgebra Vectorial 2D/3D":
    st.subheader("Calculadora y Visualizador Vectorial")
    t_vec1, t_vec2 = st.tabs(["Vectores en 2D", "Vectores en 3D"])
    
    with t_vec1:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.write("#### Operaciones y Gráficos en 2D")
        c1, c2 = st.columns(2)
        ax = c1.number_input("Vector A - Componente X", value=3.0, key="v2d_ax")
        ay = c1.number_input("Vector A - Componente Y", value=4.0, key="v2d_ay")
        bx = c2.number_input("Vector B - Componente X", value=1.0, key="v2d_bx")
        by = c2.number_input("Vector B - Componente Y", value=-2.0, key="v2d_by")
        
        if st.button("Calcular y Graficar 2D"):
            rx, ry = ax + bx, ay + by
            mag_r = math.sqrt(rx**2 + ry**2)
            prod_esc = (ax * bx) + (ay * by)
            
            st.markdown(f'<div class="result-box">Vector Resultante R = ({rx:.2f}, {ry:.2f}) | |R| = {mag_r:.2f}<br>Producto Escalar A · B = {prod_esc:.2f}</div>', unsafe_allow_html=True)
            guardar_historial("Vectores 2D", "A + B", f"R=({rx:.2f}, {ry:.2f}), A·B={prod_esc:.2f}")

            fig = go.Figure()
            fig.add_trace(go.Scatter(x=[0, ax], y=[0, ay], mode='lines+markers+text', name='Vector A', text=["", "A"], textposition="top center"))
            fig.add_trace(go.Scatter(x=[0, bx], y=[0, by], mode='lines+markers+text', name='Vector B', text=["", "B"], textposition="top center"))
            fig.add_trace(go.Scatter(x=[0, rx], y=[0, ry], mode='lines+markers+text', name='Resultante R', line=dict(dash='dash', color='red'), text=["", "R"], textposition="top center"))
            fig.update_layout(title="Representación Vectorial 2D", xaxis_title="Eje X", yaxis_title="Eje Y")
            st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with t_vec2:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.write("#### Operaciones y Gráficos 3D (Producto Cruz / Vectorial)")
        c1, c2 = st.columns(2)
        ax = c1.number_input("A_x", value=1.0, key="v3d_ax")
        ay = c1.number_input("A_y", value=0.0, key="v3d_ay")
        az = c1.number_input("A_z", value=2.0, key="v3d_az")
        
        bx = c2.number_input("B_x", value=0.0, key="v3d_bx")
        by = c2.number_input("B_y", value=3.0, key="v3d_by")
        bz = c2.number_input("B_z", value=1.0, key="v3d_bz")
        
        if st.button("Calcular y Graficar 3D"):
            cx = (ay * bz) - (az * by)
            cy = (az * bx) - (ax * bz)
            cz = (ax * by) - (ay * bx)
            
            st.markdown(f'<div class="result-box">Producto Cruz A × B = ({cx:.2f}, {cy:.2f}, {cz:.2f})</div>', unsafe_allow_html=True)
            guardar_historial("Vectores 3D", "A × B", f"({cx:.2f}, {cy:.2f}, {cz:.2f})")

            fig = go.Figure()
            fig.add_trace(go.Scatter3d(x=[0, ax], y=[0, ay], z=[0, az], mode='lines+markers', name='Vector A', line=dict(width=6, color='blue')))
            fig.add_trace(go.Scatter3d(x=[0, bx], y=[0, by], z=[0, bz], mode='lines+markers', name='Vector B', line=dict(width=6, color='green')))
            fig.add_trace(go.Scatter3d(x=[0, cx], y=[0, cy], z=[0, cz], mode='lines+markers', name='A × B (Producto Cruz)', line=dict(width=6, color='orange')))
            fig.update_layout(title="Visualización Tridimensional de Vectores", scene=dict(xaxis_title='X', yaxis_title='Y', zaxis_title='Z'))
            st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

elif categoria == "Tabla de Constantes Físicas":
    st.subheader("Tabla Periódica de Constantes Físicas Universales")
    st.markdown('<div class="metric-card">', unsafe_allow_html=True)
    
    constantes = [
        {"Nombre": "Velocidad de la luz en el vacío", "Símbolo": "c", "Valor": "2.99792458 × 10⁸", "Unidad": "m/s"},
        {"Nombre": "Constante de Gravitación Universal", "Símbolo": "G", "Valor": "6.67430 × 10⁻¹¹", "Unidad": "N·m²/kg²"},
        {"Nombre": "Constante de Planck", "Símbolo": "h", "Valor": "6.62607015 × 10⁻³⁴", "Unidad": "J·s"},
        {"Nombre": "Carga Elemental del Electrón", "Símbolo": "e", "Valor": "1.602176634 × 10⁻¹⁹", "Unidad": "C"},
        {"Nombre": "Masa del Electrón", "Símbolo": "m_e", "Valor": "9.1093837015 × 10⁻³¹", "Unidad": "kg"},
        {"Nombre": "Masa del Protón", "Símbolo": "m_p", "Valor": "1.67262192369 × 10⁻²⁷", "Unidad": "kg"},
        {"Nombre": "Número de Avogadro", "Símbolo": "N_A", "Valor": "6.02214076 × 10²³", "Unidad": "mol⁻¹"},
        {"Nombre": "Constante de Boltzmann", "Símbolo": "k_B", "Valor": "1.380649 × 10⁻²³", "Unidad": "J/K"},
        {"Nombre": "Permitividad del vacío", "Símbolo": "ε₀", "Valor": "8.8541878128 × 10⁻¹²", "Unidad": "F/m"},
        {"Nombre": "Permeabilidad magnética del vacío", "Símbolo": "μ₀", "Valor": "1.25663706212 × 10⁻⁶", "Unidad": "N/A²"},
        {"Nombre": "Aceleración estándar de la gravedad", "Símbolo": "g", "Valor": "9.80665", "Unidad": "m/s²"}
    ]
    
    busc_c = st.text_input("Filtrar constante física:")
    if busc_c:
        constantes = [c for c in constantes if busc_c.lower() in c["Nombre"].lower() or busc_c.lower() in c["Símbolo"].lower()]
        
    st.table(constantes)
    st.markdown('</div>', unsafe_allow_html=True)

# ------------------------------------------------------------------------------
# 6. MÓDULOS FÍSICOS
# ------------------------------------------------------------------------------

# --- 1. MECÁNICA ---
elif categoria == "Mecánica":
    st.subheader("Mecánica y Cinemática")
    t1, t2, t3, t4, t5 = st.tabs(["MRU", "MRUV", "Leyes de Newton", "Trabajo", "Proyectiles"])
    
    with t1:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        with st.expander("Fundamento Teórico - MRU"):
            st.write("**Movimiento Rectilíneo Uniforme (MRU):** Es aquel movimiento donde la velocidad permanece constante y la trayectoria es una línea recta. No existe aceleración ($a=0$).")
            st.latex(r"d = v \cdot t")
        
        op_mru = st.radio("¿Qué deseas calcular?", ["Distancia (d = v * t)", "Tiempo (t = d / v)"], horizontal=True)
        col1, col2 = st.columns(2)
        if "Distancia" in op_mru:
            v = col1.number_input("Velocidad (m/s)", value=10.0, key="mru_v1")
            t = col2.number_input("Tiempo (s)", value=5.0, key="mru_t1")
            if st.button("Calcular Distancia", key="btn_mru1"):
                res_str = f"Distancia = {v * t:.2f} m"
                st.markdown(f'<div class="result-box">{res_str}</div>', unsafe_allow_html=True)
                guardar_historial(categoria, op_mru, res_str)
        else:
            d = col1.number_input("Distancia (m)", value=50.0, key="mru_d2")
            v = col2.number_input("Velocidad (m/s)", value=10.0, key="mru_v2")
            if st.button("Calcular Tiempo", key="btn_mru2"):
                if v != 0:
                    res_str = f"Tiempo = {d / v:.2f} s"
                    st.markdown(f'<div class="result-box">{res_str}</div>', unsafe_allow_html=True)
                    guardar_historial(categoria, op_mru, res_str)
                else: st.error("La velocidad no puede ser cero.")
        st.markdown('</div>', unsafe_allow_html=True)

    with t2:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        with st.expander("Fundamento Teórico - MRUV"):
            st.write("**MRUV:** Ocurre cuando un cuerpo cambia su velocidad de forma uniforme debido a una aceleración constante.")
            st.latex(r"v_f = v_0 + a \cdot t \quad | \quad d = v_0 \cdot t + \frac{1}{2} a \cdot t^2")
        
        op_mruv = st.radio("Selecciona Fórmula:", ["Velocidad Final (vf = v0 + a*t)", "Distancia (d = v0*t + 0.5*a*t²)"], horizontal=True)
        if "Velocidad Final" in op_mruv:
            c1, c2, c3 = st.columns(3)
            v0 = c1.number_input("Vel. Inicial (m/s)", value=0.0, key="mruv_v0_1")
            a = c2.number_input("Aceleración (m/s²)", value=2.0, key="mruv_a_1")
            t = c3.number_input("Tiempo (s)", value=5.0, key="mruv_t_1")
            if st.button("Calcular y Graficar (v-t / x-t)", key="btn_mruv1"):
                vf = v0 + (a * t)
                res_str = f"Velocidad Final = {vf:.2f} m/s"
                st.markdown(f'<div class="result-box">{res_str}</div>', unsafe_allow_html=True)
                guardar_historial(categoria, op_mruv, res_str)

                t_arr = np.linspace(0, t, 100)
                v_arr = v0 + (a * t_arr)
                x_arr = (v0 * t_arr) + (0.5 * a * (t_arr**2))

                fig = go.Figure()
                fig.add_trace(go.Scatter(x=t_arr, y=x_arr, mode='lines', name='Posición x(t)', line=dict(color='#38BDF8', width=3)))
                fig.add_trace(go.Scatter(x=t_arr, y=v_arr, mode='lines', name='Velocidad v(t)', line=dict(color='#F59E0B', width=3)))
                fig.update_layout(title="Simulación MRUV: Posición y Velocidad vs Tiempo", xaxis_title="Tiempo (s)", yaxis_title="Magnitud")
                st.plotly_chart(fig, use_container_width=True)
        else:
            c1, c2, c3 = st.columns(3)
            v0 = c1.number_input("Vel. Inicial (m/s)", value=0.0, key="mruv_v0_2")
            t = c2.number_input("Tiempo (s)", value=5.0, key="mruv_t_2")
            a = c3.number_input("Aceleración (m/s²)", value=2.0, key="mruv_a_2")
            if st.button("Calcular Distancia", key="btn_mruv2"):
                dist = (v0 * t) + (0.5 * a * (t**2))
                res_str = f"Distancia = {dist:.2f} m"
                st.markdown(f'<div class="result-box">{res_str}</div>', unsafe_allow_html=True)
                guardar_historial(categoria, op_mruv, res_str)
        st.markdown('</div>', unsafe_allow_html=True)

    with t3:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        with st.expander("Fundamento Teórico - Las 3 Leyes de Newton"):
            st.write("""
            * **1ª Ley (Inercia):** Todo cuerpo permanece en reposo o en movimiento rectilíneo uniforme a menos que actúe sobre él una fuerza neta externa ($\sum \\vec{F} = 0$).
            * **2ª Ley (Dinámica):** La aceleración de un objeto es directamente proporcional a la fuerza neta aplicada e inversamente proporcional a su masa ($\vec{F} = m \cdot \vec{a}$).
            * **3ª Ley (Acción y Reacción):** A toda fuerza de acción le corresponde una fuerza de reacción de igual magnitud pero en sentido opuesto ($\vec{F}_{A \\to B} = -\\vec{F}_{B \\to A}$).
            """)
        
        op_new = st.radio(
            "Selecciona la Ley a calcular:", 
            ["1ª Ley: Equilibrio / Inercia", "2ª Ley: Masa, Fuerza y Aceleración", "2ª Ley: Peso (P = m * g)", "3ª Ley: Acción y Reacción"], 
            horizontal=True
        )

        if "1ª Ley" in op_new:
            st.write("#### Estado de Equilibrio (Inercia)")
            f1 = st.number_input("Fuerza en sentido horizontal positivo F1 (N)", value=50.0, key="new1_f1")
            f2 = st.number_input("Fuerza opuesta F2 (N)", value=50.0, key="new1_f2")
            if st.button("Verificar Equilibrio", key="btn_new_1ley"):
                f_neta = f1 - f2
                if math.isclose(f_neta, 0.0, abs_tol=1e-5):
                    res_str = f"Fuerza Neta = {f_neta:.2f} N -> ¡El cuerpo está en EQUILIBRIO!"
                else:
                    res_str = f"Fuerza Neta = {f_neta:.2f} N -> ¡El cuerpo NO está en equilibrio!"
                st.markdown(f'<div class="result-box">{res_str}</div>', unsafe_allow_html=True)
                guardar_historial(categoria, "1ª Ley de Newton (Inercia)", res_str)

        elif "2ª Ley: Masa, Fuerza" in op_new:
            st.write("#### Fundamental de la Dinámica (F = m * a)")
            sub_op_2 = st.selectbox("¿Qué deseas calcular?", ["Fuerza (F = m * a)", "Aceleración (a = F / m)", "Masa (m = F / a)"], key="sub_op_2ley")
            c1, c2 = st.columns(2)
            
            if "Fuerza" in sub_op_2:
                m = c1.number_input("Masa (kg)", value=10.0, key="new2_m")
                a = c2.number_input("Aceleración (m/s²)", value=2.5, key="new2_a")
                if st.button("Calcular Fuerza", key="btn_new2_f"):
                    res_str = f"Fuerza Neta = {m * a:.2f} N"
                    st.markdown(f'<div class="result-box">{res_str}</div>', unsafe_allow_html=True)
                    guardar_historial(categoria, "2ª Ley de Newton (Fuerza)", res_str)
            elif "Aceleración" in sub_op_2:
                f = c1.number_input("Fuerza Neta (N)", value=25.0, key="new2_f_a")
                m = c2.number_input("Masa (kg)", value=10.0, key="new2_m_a")
                if st.button("Calcular Aceleración", key="btn_new2_a"):
                    if m != 0:
                        res_str = f"Aceleración = {f / m:.2f} m/s²"
                        st.markdown(f'<div class="result-box">{res_str}</div>', unsafe_allow_html=True)
                        guardar_historial(categoria, "2ª Ley de Newton (Aceleración)", res_str)
                    else: st.error("La masa debe ser mayor a cero.")
            else:
                f = c1.number_input("Fuerza Neta (N)", value=50.0, key="new2_f_m")
                a = c2.number_input("Aceleración (m/s²)", value=5.0, key="new2_a_m")
                if st.button("Calcular Masa", key="btn_new2_m"):
                    if a != 0:
                        res_str = f"Masa = {f / a:.2f} kg"
                        st.markdown(f'<div class="result-box">{res_str}</div>', unsafe_allow_html=True)
                        guardar_historial(categoria, "2ª Ley de Newton (Masa)", res_str)
                    else: st.error("La aceleración no puede ser cero.")

        elif "Peso" in op_new:
            st.write("#### Cálculo del Peso Gravitacional (P = m * g)")
            c1, c2 = st.columns(2)
            m = c1.number_input("Masa (kg)", value=10.0, key="new_m_peso")
            g = c2.number_input("Gravedad (m/s²)", value=9.81, key="new_g_peso")
            if st.button("Calcular Peso", key="btn_new_peso"):
                res_str = f"Peso = {m * g:.2f} N"
                st.markdown(f'<div class="result-box">{res_str}</div>', unsafe_allow_html=True)
                guardar_historial(categoria, "Peso Gravitacional", res_str)

        else:
            st.write("#### Par de Acción y Reacción")
            f_accion = st.number_input("Fuerza ejercida por Objeto A sobre Objeto B (N)", value=120.0, key="new3_f")
            if st.button("Calcular Fuerza de Reacción", key="btn_new_3ley"):
                f_reaccion = -f_accion
                res_str = f"Fuerza de Acción (F_AB) = {f_accion:.2f} N  ->  Fuerza de Reacción (F_BA) = {f_reaccion:.2f} N"
                st.markdown(f'<div class="result-box">{res_str}</div>', unsafe_allow_html=True)
                guardar_historial(categoria, "3ª Ley de Newton (Acción-Reacción)", res_str)

        st.markdown('</div>', unsafe_allow_html=True)

    with t4:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        with st.expander("Fundamento Teórico - Trabajo"):
            st.write("**Trabajo Mecánico:** Representa la energía transferida a un objeto mediante la aplicación de una fuerza a lo largo de un desplazamiento.")
            st.latex(r"W = F \cdot d \cdot \cos(\theta)")
        
        c1, c2 = st.columns(2)
        f = c1.number_input("Fuerza (N)", value=25.0, key="trab_f")
        d = c2.number_input("Distancia (m)", value=4.0, key="trab_d")
        if st.button("Calcular Trabajo", key="btn_trab"):
            res_str = f"Trabajo Realizado = {f * d:.2f} J"
            st.markdown(f'<div class="result-box">{res_str}</div>', unsafe_allow_html=True)
            guardar_historial(categoria, "Trabajo Mecánico", res_str)
        st.markdown('</div>', unsafe_allow_html=True)

    with t5:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        with st.expander("Fundamento Teórico - Proyectiles"):
            st.write("**Movimiento Parabólico:** Combinación de un MRU en el eje horizontal (x) y un MRUV (caída libre) en el eje vertical (y).")
            st.latex(r"R = \frac{v_0^2 \cdot \sin(2\theta)}{g}")
        
        c1, c2 = st.columns(2)
        v0 = c1.number_input("Velocidad Inicial (m/s)", value=15.0, key="proy_v0")
        ang = c2.number_input("Ángulo (°)", value=45.0, key="proy_ang")
        if st.button("Calcular y Graficar Trayectoria", key="btn_proy"):
            g = 9.81
            rad = math.radians(ang)
            alcance = (v0**2) * math.sin(2 * rad) / g
            res_str = f"Alcance Horizontal Máximo = {alcance:.2f} m"
            st.markdown(f'<div class="result-box">{res_str}</div>', unsafe_allow_html=True)
            guardar_historial(categoria, "Alcance Proyectil", res_str)

            t_total = (2 * v0 * math.sin(rad)) / g
            t_vec = np.linspace(0, t_total, 100)
            x = v0 * math.cos(rad) * t_vec
            y = (v0 * math.sin(rad) * t_vec) - (0.5 * g * (t_vec**2))

            fig = go.Figure()
            fig.add_trace(go.Scatter(x=x, y=y, mode='lines', name='Parábola', line=dict(color='#38BDF8', width=3)))
            fig.update_layout(title="Trayectoria del Proyectil", xaxis_title="Distancia (m)", yaxis_title="Altura (m)")
            st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

# --- 2. MOVIMIENTO ARMÓNICO SIMPLE (MAS) ---
elif categoria == "Movimiento Armónico Simple":
    st.subheader("Movimiento Armónico Simple (MAS)")
    t1, t2 = st.tabs(["Péndulo Simple", "Sistema Masa-Resorte"])

    with t1:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        with st.expander("Fundamento Teórico - Péndulo Simple"):
            st.write("El periodo $T$ de un péndulo simple depende únicamente de la longitud del hilo $L$ y la aceleración de la gravedad $g$ (para pequeñas oscilaciones).")
            st.latex(r"T = 2\pi \sqrt{\frac{L}{g}}")

        c1, c2 = st.columns(2)
        longitud = c1.number_input("Longitud del hilo L (m)", value=1.0, key="mas_pend_l")
        gravedad = c2.number_input("Gravedad g (m/s²)", value=9.81, key="mas_pend_g")

        if st.button("Calcular Periodo y Simular Oscilación", key="btn_mas_pend"):
            periodo = 2 * math.pi * math.sqrt(longitud / gravedad)
            frecuencia = 1 / periodo
            res_str = f"Periodo T = {periodo:.3f} s | Frecuencia f = {frecuencia:.3f} Hz"
            st.markdown(f'<div class="result-box">{res_str}</div>', unsafe_allow_html=True)
            guardar_historial(categoria, "Péndulo Simple", res_str)

            # Simulación gráfica con Plotly adaptada al tema claro/oscuro
            t_vec = np.linspace(0, periodo * 3, 200)
            theta_vec = np.radians(15) * np.cos((2 * np.pi / periodo) * t_vec)

            fig = go.Figure()
            fig.add_trace(go.Scatter(
                x=t_vec, 
                y=np.degrees(theta_vec), 
                mode='lines', 
                name='Ángulo θ(t)', 
                line=dict(color='#818CF8', width=3)
            ))
            fig.update_layout(
                title="Ángulo de Oscilación vs Tiempo",
                xaxis_title="Tiempo (s)",
                yaxis_title="Ángulo (°)",
                template="plotly_dark" if modo == "Oscuro" else "plotly_white"
            )
            st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with t2:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        with st.expander("Fundamento Teórico - Masa-Resorte (Ley de Hooke)"):
            st.write("Un objeto sujeto a un resorte oscila con un periodo determinado por la masa $m$ y la constante elástica del resorte $k$.")
            st.latex(r"T = 2\pi \sqrt{\frac{m}{k}} \quad \text{y} \quad f = \frac{1}{T}")

        c1, c2, c3 = st.columns(3)
        masa = c1.number_input("Masa m (kg)", value=0.5, key="mas_mr_m")
        k_resorte = c2.number_input("Constante k (N/m)", value=50.0, key="mas_mr_k")
        amp = c3.number_input("Amplitud A (m)", value=0.3, key="mas_mr_a")

        if st.button("Calcular MAS Masa-Resorte", key="btn_mas_mr"):
            if k_resorte > 0 and masa > 0:
                periodo = 2 * math.pi * math.sqrt(masa / k_resorte)
                frecuencia = 1 / periodo
                w = math.sqrt(k_resorte / masa)
                res_str = f"Periodo T = {periodo:.3f} s | Frecuencia f = {frecuencia:.3f} Hz | Frecuencia angular ω = {w:.2f} rad/s"
                st.markdown(f'<div class="result-box">{res_str}</div>', unsafe_allow_html=True)
                guardar_historial(categoria, "Masa-Resorte", res_str)

                # Simulación gráfica con Plotly adaptada al tema claro/oscuro
                t_vec = np.linspace(0, periodo * 3, 200)
                x_vec = amp * np.cos(w * t_vec)

                fig = go.Figure()
                fig.add_trace(go.Scatter(
                    x=t_vec, 
                    y=x_vec, 
                    mode='lines', 
                    name='Elongación x(t)', 
                    line=dict(color='#38BDF8', width=3)
                ))
                fig.update_layout(
                    title="Posición x(t) vs Tiempo",
                    xaxis_title="Tiempo (s)",
                    yaxis_title="Posición (m)",
                    template="plotly_dark" if modo == "Oscuro" else "plotly_white"
                )
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.error("La masa y constante deben ser mayores a cero.")
        st.markdown('</div>', unsafe_allow_html=True)
# --- 3. ENERGÍA Y POTENCIA ---
elif categoria == "Energía y Potencia":
    st.subheader("Energía y Potencia")
    t1, t2, t3 = st.tabs(["Energía Cinética / Potencial", "Potencia", "Rendimiento"])

    with t1:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        op_ene = st.radio("Selecciona Fórmula:", ["Energía Cinética (Ec = 0.5*m*v²)", "Energía Potencial (Ep = m*g*h)"], horizontal=True)
        c1, c2 = st.columns(2)
        if "Cinética" in op_ene:
            m = c1.number_input("Masa (kg)", value=2.0, key="ec_m")
            v = c2.number_input("Velocidad (m/s)", value=5.0, key="ec_v")
            if st.button("Calcular Ec", key="btn_ec"):
                res_str = f"Energía Cinética = {0.5 * m * (v**2):.2f} J"
                st.markdown(f'<div class="result-box">{res_str}</div>', unsafe_allow_html=True)
                guardar_historial(categoria, op_ene, res_str)
        else:
            m = c1.number_input("Masa (kg)", value=2.0, key="ep_m")
            h = c2.number_input("Altura (m)", value=10.0, key="ep_h")
            if st.button("Calcular Ep", key="btn_ep"):
                res_str = f"Energía Potencial = {m * 9.81 * h:.2f} J"
                st.markdown(f'<div class="result-box">{res_str}</div>', unsafe_allow_html=True)
                guardar_historial(categoria, op_ene, res_str)
        st.markdown('</div>', unsafe_allow_html=True)

    with t2:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.write("#### Potencia Mecánica (P = W / t)")
        c1, c2 = st.columns(2)
        w = c1.number_input("Trabajo (J)", value=500.0, key="pot_w")
        t = c2.number_input("Tiempo (s)", value=10.0, key="pot_t")
        if st.button("Calcular Potencia", key="btn_pot"):
            if t != 0:
                res_str = f"Potencia = {w / t:.2f} W"
                st.markdown(f'<div class="result-box">{res_str}</div>', unsafe_allow_html=True)
                guardar_historial(categoria, "Potencia Mecánica", res_str)
            else: st.error("El tiempo no puede ser cero.")
        st.markdown('</div>', unsafe_allow_html=True)

    with t3:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.write("#### Eficiencia / Rendimiento (%)")
        c1, c2 = st.columns(2)
        pu = c1.number_input("Potencia Útil (W)", value=80.0, key="rend_pu")
        pt = c2.number_input("Potencia Total Consumida (W)", value=100.0, key="rend_pt")
        if st.button("Calcular Eficiencia", key="btn_rend"):
            if pt != 0:
                res_str = f"Rendimiento = {(pu / pt) * 100:.2f} %"
                st.markdown(f'<div class="result-box">{res_str}</div>', unsafe_allow_html=True)
                guardar_historial(categoria, "Rendimiento", res_str)
            else: st.error("La potencia total no puede ser cero.")
        st.markdown('</div>', unsafe_allow_html=True)

# --- 4. PRESIÓN Y FLUIDOS ---
elif categoria == "Presión y Fluidos":
    st.subheader("Presión y Fluidos")
    t1, t2, t3 = st.tabs(["Presión / Densidad", "Presión Hidrostática", "Caudal"])

    with t1:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        op_pf = st.radio("Selecciona:", ["Presión (P = F / A)", "Densidad (ρ = m / V)"], horizontal=True)
        c1, c2 = st.columns(2)
        if "Presión" in op_pf:
            f = c1.number_input("Fuerza (N)", value=100.0, key="pr_f")
            a = c2.number_input("Área (m²)", value=2.0, key="pr_a")
            if st.button("Calcular Presión", key="btn_pr"):
                if a != 0:
                    res_str = f"Presión = {f / a:.2f} Pa"
                    st.markdown(f'<div class="result-box">{res_str}</div>', unsafe_allow_html=True)
                    guardar_historial(categoria, op_pf, res_str)
                else: st.error("El área no puede ser cero.")
        else:
            m = c1.number_input("Masa (kg)", value=50.0, key="den_m")
            v = c2.number_input("Volumen (m³)", value=0.05, key="den_v")
            if st.button("Calcular Densidad", key="btn_den"):
                if v != 0:
                    res_str = f"Densidad = {m / v:.2f} kg/m³"
                    st.markdown(f'<div class="result-box">{res_str}</div>', unsafe_allow_html=True)
                    guardar_historial(categoria, op_pf, res_str)
                else: st.error("El volumen no puede ser cero.")
        st.markdown('</div>', unsafe_allow_html=True)

    with t2:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.write("#### Presión Hidrostática (P = P0 + ρ * g * h)")
        c1, c2, c3 = st.columns(3)
        p0 = c1.number_input("Presión Atmosférica (Pa)", value=101325.0, key="ph_p0")
        den = c2.number_input("Densidad Fluido (kg/m³)", value=1000.0, key="ph_den")
        h = c3.number_input("Profundidad (m)", value=5.0, key="ph_h")
        if st.button("Calcular Presión Hidrostática", key="btn_ph"):
            p_total = p0 + (den * 9.81 * h)
            res_str = f"Presión Total = {p_total:.2f} Pa"
            st.markdown(f'<div class="result-box">{res_str}</div>', unsafe_allow_html=True)
            guardar_historial(categoria, "Presión Hidrostática", res_str)
        st.markdown('</div>', unsafe_allow_html=True)

    with t3:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.write("#### Caudal Volumétrico (Q = V / t)")
        c1, c2 = st.columns(2)
        v = c1.number_input("Volumen (m³)", value=2.0, key="q_v")
        t = c2.number_input("Tiempo (s)", value=10.0, key="q_t")
        if st.button("Calcular Caudal", key="btn_q"):
            if t != 0:
                res_str = f"Caudal = {v / t:.4f} m³/s"
                st.markdown(f'<div class="result-box">{res_str}</div>', unsafe_allow_html=True)
                guardar_historial(categoria, "Caudal Volumétrico", res_str)
            else: st.error("El tiempo no puede ser cero.")
        st.markdown('</div>', unsafe_allow_html=True)

# --- 5. HIDRODINÁMICA ---
elif categoria == "Hidrodinámica":
    st.subheader("Hidrodinámica Avanzada")
    t1, t2 = st.tabs(["Ecuación de Continuidad", "Ecuación de Bernoulli"])

    with t1:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        with st.expander("Fundamento Teórico - Continuidad"):
            st.write("Para un fluido incompresible, el caudal $Q$ se conserva a lo largo de una tubería de sección variable.")
            st.latex(r"A_1 \cdot v_1 = A_2 \cdot v_2")

        c1, c2, c3 = st.columns(3)
        a1 = c1.number_input("Área Sección 1 A1 (m²)", value=0.05, key="cont_a1")
        v1 = c2.number_input("Velocidad 1 v1 (m/s)", value=2.0, key="cont_v1")
        a2 = c3.number_input("Área Sección 2 A2 (m²)", value=0.02, key="cont_a2")

        if st.button("Calcular Velocidad v2", key="btn_cont"):
            if a2 > 0:
                v2 = (a1 * v1) / a2
                res_str = f"Velocidad v2 = {v2:.2f} m/s | Caudal Q = {a1 * v1:.4f} m³/s"
                st.markdown(f'<div class="result-box">{res_str}</div>', unsafe_allow_html=True)
                guardar_historial(categoria, "Ecuación de Continuidad", res_str)
            else: st.error("El área A2 debe ser mayor que cero.")
        st.markdown('</div>', unsafe_allow_html=True)

    with t2:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        with st.expander("Fundamento Teórico - Bernoulli"):
            st.write("Describe la conservación de energía para un fluido ideal en régimen estacionario.")
            st.latex(r"P_1 + \frac{1}{2}\rho v_1^2 + \rho g h_1 = P_2 + \frac{1}{2}\rho v_2^2 + \rho g h_2")

        c1, c2, c3 = st.columns(3)
        p1 = c1.number_input("Presión 1 P1 (Pa)", value=200000.0, key="bern_p1")
        v1 = c2.number_input("Velocidad 1 v1 (m/s)", value=2.0, key="bern_v1")
        h1 = c3.number_input("Altura 1 h1 (m)", value=0.0, key="bern_h1")

        c4, c5, c6 = st.columns(3)
        rho = c4.number_input("Densidad del fluido ρ (kg/m³)", value=1000.0, key="bern_rho")
        v2 = c5.number_input("Velocidad 2 v2 (m/s)", value=5.0, key="bern_v2")
        h2 = c6.number_input("Altura 2 h2 (m)", value=2.0, key="bern_h2")

        if st.button("Calcular Presión P2", key="btn_bern"):
            g = 9.81
            p2 = p1 + (0.5 * rho * (v1**2 - v2**2)) + (rho * g * (h1 - h2))
            res_str = f"Presión en Punto 2 P2 = {p2:.2f} Pa ({p2/1000:.2f} kPa)"
            st.markdown(f'<div class="result-box">{res_str}</div>', unsafe_allow_html=True)
            guardar_historial(categoria, "Ecuación de Bernoulli", res_str)
        st.markdown('</div>', unsafe_allow_html=True)

# --- 6. ELECTRICIDAD ---
elif categoria == "Electricidad":
    st.subheader("Electricidad y Circuitos")
    t1, t2, t3, t4 = st.tabs(["Ley de Ohm", "Potencia Eléctrica", "Resistencias en Serie", "Resistencias en Paralelo"])

    with t1:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        with st.expander("Teoría - Ley de Ohm"):
            st.latex(r"V = I \cdot R")
        
        op_ohm = st.radio("Variable a Calcular:", ["Voltaje (V = I * R)", "Corriente (I = V / R)", "Resistencia (R = V / I)"], horizontal=True)
        c1, c2 = st.columns(2)
        if "Voltaje" in op_ohm:
            i = c1.number_input("Corriente (A)", value=2.0, key="ohm_i1")
            r = c2.number_input("Resistencia (Ω)", value=10.0, key="ohm_r1")
            if st.button("Calcular Voltaje y Graficar", key="btn_ohm1"):
                res_str = f"Voltaje = {i * r:.2f} V"
                st.markdown(f'<div class="result-box">{res_str}</div>', unsafe_allow_html=True)
                guardar_historial(categoria, op_ohm, res_str)

                i_vec = np.linspace(0, i * 2, 50)
                v_vec = i_vec * r
                fig = go.Figure()
                fig.add_trace(go.Scatter(x=i_vec, y=v_vec, mode='lines+markers', name='V vs I', line=dict(color='#F59E0B', width=3)))
                fig.update_layout(title="Relación Voltaje - Corriente", xaxis_title="Corriente (A)", yaxis_title="Voltaje (V)")
                st.plotly_chart(fig, use_container_width=True)
        elif "Corriente" in op_ohm:
            v = c1.number_input("Voltaje (V)", value=12.0, key="ohm_v2")
            r = c2.number_input("Resistencia (Ω)", value=4.0, key="ohm_r2")
            if st.button("Calcular Corriente", key="btn_ohm2"):
                if r != 0:
                    res_str = f"Corriente = {v / r:.2f} A"
                    st.markdown(f'<div class="result-box">{res_str}</div>', unsafe_allow_html=True)
                    guardar_historial(categoria, op_ohm, res_str)
                else: st.error("La resistencia no puede ser cero.")
        else:
            v = c1.number_input("Voltaje (V)", value=12.0, key="ohm_v3")
            i = c2.number_input("Corriente (A)", value=3.0, key="ohm_i3")
            if st.button("Calcular Resistencia", key="btn_ohm3"):
                if i != 0:
                    res_str = f"Resistencia = {v / i:.2f} Ω"
                    st.markdown(f'<div class="result-box">{res_str}</div>', unsafe_allow_html=True)
                    guardar_historial(categoria, op_ohm, res_str)
                else: st.error("La corriente no puede ser cero.")
        st.markdown('</div>', unsafe_allow_html=True)

    with t2:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.write("#### Potencia Eléctrica (P = V * I)")
        c1, c2 = st.columns(2)
        v = c1.number_input("Voltaje (V)", value=110.0, key="pote_v")
        i = c2.number_input("Corriente (A)", value=5.0, key="pote_i")
        if st.button("Calcular Potencia", key="btn_pote"):
            res_str = f"Potencia Eléctrica = {v * i:.2f} W"
            st.markdown(f'<div class="result-box">{res_str}</div>', unsafe_allow_html=True)
            guardar_historial(categoria, "Potencia Eléctrica", res_str)
        st.markdown('</div>', unsafe_allow_html=True)

    with t3:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.write("#### Resistencia Equivalente en Serie")
        c1, c2 = st.columns(2)
        r1 = c1.number_input("Resistencia 1 (Ω)", value=10.0, key="rs_r1")
        r2 = c2.number_input("Resistencia 2 (Ω)", value=20.0, key="rs_r2")
        if st.button("Calcular Resistencia Serie", key="btn_rs"):
            res_str = f"Resistencia Total = {r1 + r2:.2f} Ω"
            st.markdown(f'<div class="result-box">{res_str}</div>', unsafe_allow_html=True)
            guardar_historial(categoria, "Resistencia en Serie", res_str)
        st.markdown('</div>', unsafe_allow_html=True)

    with t4:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.write("#### Resistencia Equivalente en Paralelo")
        st.latex(r"\frac{1}{R_{eq}} = \frac{1}{R_1} + \frac{1}{R_2}")
        c1, c2 = st.columns(2)
        r1 = c1.number_input("Resistencia 1 (Ω)", value=10.0, key="rp_r1")
        r2 = c2.number_input("Resistencia 2 (Ω)", value=20.0, key="rp_r2")
        if st.button("Calcular Resistencia Paralelo", key="btn_rp"):
            if r1 > 0 and r2 > 0:
                req = (r1 * r2) / (r1 + r2)
                res_str = f"Resistencia Equivalente R_eq = {req:.2f} Ω"
                st.markdown(f'<div class="result-box">{res_str}</div>', unsafe_allow_html=True)
                guardar_historial(categoria, "Resistencia en Paralelo", res_str)
            else: st.error("Las resistencias deben ser mayores a cero.")
        st.markdown('</div>', unsafe_allow_html=True)

# --- 7. TERMODINÁMICA ---
elif categoria == "Termodinámica":
    st.subheader("Termodinámica y Procesos de Gas")
    t1, t2, t3, t4, t5 = st.tabs(["Ley Gases Ideales", "Conversión Temp.", "Calor Sensible", "Dilatación Lineal", "Diagrama P-V"])

    with t1:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        with st.expander("Fundamento Teórico - Ley de Gases Ideales"):
            st.write("Relaciona la presión $P$, el volumen $V$, la cantidad de sustancia $n$ y la temperatura $T$.")
            st.latex(r"P \cdot V = n \cdot R \cdot T")

        op_gas = st.radio("¿Qué variable deseas despejar?", ["Presión (P)", "Volumen (V)", "Temperatura (T)"], horizontal=True)
        c1, c2, c3 = st.columns(3)

        R_gas = 8.314  # J/(mol·K)
        if op_gas == "Presión (P)":
            n = c1.number_input("Moles n (mol)", value=1.0, key="gas_n1")
            vol = c2.number_input("Volumen V (m³)", value=0.025, key="gas_v1")
            temp_k = c3.number_input("Temperatura T (K)", value=300.0, key="gas_t1")
            if st.button("Calcular Presión P", key="btn_gas_p"):
                if vol > 0:
                    p_res = (n * R_gas * temp_k) / vol
                    res_str = f"Presión P = {p_res:.2f} Pa ({p_res/101325:.3f} atm)"
                    st.markdown(f'<div class="result-box">{res_str}</div>', unsafe_allow_html=True)
                    guardar_historial(categoria, "Ley de Gases Ideales (P)", res_str)
                else: st.error("El volumen debe ser mayor a cero.")
        elif op_gas == "Volumen (V)":
            n = c1.number_input("Moles n (mol)", value=1.0, key="gas_n2")
            press = c2.number_input("Presión P (Pa)", value=101325.0, key="gas_p2")
            temp_k = c3.number_input("Temperatura T (K)", value=300.0, key="gas_t2")
            if st.button("Calcular Volumen V", key="btn_gas_v"):
                if press > 0:
                    v_res = (n * R_gas * temp_k) / press
                    res_str = f"Volumen V = {v_res:.5f} m³ ({v_res*1000:.2f} Litros)"
                    st.markdown(f'<div class="result-box">{res_str}</div>', unsafe_allow_html=True)
                    guardar_historial(categoria, "Ley de Gases Ideales (V)", res_str)
                else: st.error("La presión debe ser mayor a cero.")
        else:
            press = c1.number_input("Presión P (Pa)", value=101325.0, key="gas_p3")
            vol = c2.number_input("Volumen V (m³)", value=0.025, key="gas_v3")
            n = c3.number_input("Moles n (mol)", value=1.0, key="gas_n3")
            if st.button("Calcular Temperatura T", key="btn_gas_t"):
                if n > 0:
                    t_res = (press * vol) / (n * R_gas)
                    res_str = f"Temperatura T = {t_res:.2f} K ({t_res - 273.15:.2f} °C)"
                    st.markdown(f'<div class="result-box">{res_str}</div>', unsafe_allow_html=True)
                    guardar_historial(categoria, "Ley de Gases Ideales (T)", res_str)
                else: st.error("El número de moles debe ser mayor a cero.")
        st.markdown('</div>', unsafe_allow_html=True)

    with t2:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        op_temp = st.radio("Convertir de °C a:", ["Kelvin (K)", "Fahrenheit (°F)"], horizontal=True)
        c = st.number_input("Temperatura en °C", value=25.0, key="temp_c")
        if st.button("Convertir Temperatura", key="btn_temp"):
            if "Kelvin" in op_temp:
                res_str = f"Temperatura = {c + 273.15:.2f} K"
            else:
                res_str = f"Temperatura = {(c * 9/5) + 32:.2f} °F"
            st.markdown(f'<div class="result-box">{res_str}</div>', unsafe_allow_html=True)
            guardar_historial(categoria, op_temp, res_str)
        st.markdown('</div>', unsafe_allow_html=True)

    with t3:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.write("#### Calor Sensible (Q = m * c * ΔT)")
        c1, c2, c3 = st.columns(3)
        m = c1.number_input("Masa (kg)", value=1.0, key="cal_m")
        c_esp = c2.number_input("Calor Específico (J/kg·°C)", value=4184.0, key="cal_c")
        dt = c3.number_input("Variación Temp. ΔT (°C)", value=10.0, key="cal_dt")
        if st.button("Calcular Calor Sensible", key="btn_cal"):
            res_str = f"Calor Q = {m * c_esp * dt:.2f} J"
            st.markdown(f'<div class="result-box">{res_str}</div>', unsafe_allow_html=True)
            guardar_historial(categoria, "Calor Sensible", res_str)
        st.markdown('</div>', unsafe_allow_html=True)

    with t4:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.write("#### Dilatación Lineal (ΔL = L0 * α * ΔT)")
        c1, c2, c3 = st.columns(3)
        l0 = c1.number_input("Longitud Inicial L0 (m)", value=10.0, key="dil_l0")
        alpha = c2.number_input("Coeficiente α (1/°C)", value=0.000012, format="%.6f", key="dil_a")
        dt = c3.number_input("Variación Temp. ΔT (°C)", value=50.0, key="dil_dt")
        if st.button("Calcular Dilatación", key="btn_dil"):
            res_str = f"Cambio ΔL = {l0 * alpha * dt:.6f} m"
            st.markdown(f'<div class="result-box">{res_str}</div>', unsafe_allow_html=True)
            guardar_historial(categoria, "Dilatación Lineal", res_str)
        st.markdown('</div>', unsafe_allow_html=True)

    with t5:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.write("#### Simulación: Isoterma de Gas Ideal (Diagrama P-V)")
        c1, c2 = st.columns(2)
        n_moles = c1.number_input("Moles (n)", value=1.0, key="pv_n")
        temp_k = c2.number_input("Temperatura Constante (K)", value=300.0, key="pv_t")
        
        if st.button("Simular Diagrama P-V"):
            R = 8.314
            v_vec = np.linspace(0.001, 0.05, 100)
            p_vec = (n_moles * R * temp_k) / v_vec
            
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=v_vec, y=p_vec, mode='lines', name='Isoterma', line=dict(color='#EF4444', width=3)))
            fig.update_layout(title=f"Diagrama P-V para T = {temp_k} K", xaxis_title="Volumen (m³)", yaxis_title="Presión (Pa)")
            st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

# --- 8. ÓPTICA Y ONDAS ---
elif categoria == "Óptica y Ondas":
    st.subheader("Óptica y Ondas")
    t1, t2, t3 = st.tabs(["Velocidad y Periodo", "Ley de Snell", "Óptica / Fotones"])

    with t1:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        op_ond = st.radio("Selecciona Fórmula:", ["Velocidad de Onda (v = λ * f)", "Frecuencia (f = 1 / T)"], horizontal=True)
        c1, c2 = st.columns(2)
        if "Velocidad" in op_ond:
            lam = c1.number_input("Longitud de Onda λ (m)", value=2.0, key="ond_lam")
            freq = c2.number_input("Frecuencia f (Hz)", value=5.0, key="ond_f")
            if st.button("Calcular y Graficar Onda", key="btn_ond"):
                v_onda = lam * freq
                res_str = f"Velocidad de Onda = {v_onda:.2f} m/s"
                st.markdown(f'<div class="result-box">{res_str}</div>', unsafe_allow_html=True)
                guardar_historial(categoria, op_ond, res_str)

                x = np.linspace(0, lam * 3, 200)
                y = np.sin((2 * np.pi / lam) * x)
                fig = go.Figure()
                fig.add_trace(go.Scatter(x=x, y=y, mode='lines', name='Onda Transversal', line=dict(color='#06B6D4', width=2)))
                fig.update_layout(title="Representación de Onda Sinusoidal", xaxis_title="Posición (m)", yaxis_title="Amplitud")
                st.plotly_chart(fig, use_container_width=True)
        else:
            periodo = c1.number_input("Periodo T (s)", value=0.1, key="ond_t")
            if st.button("Calcular Frecuencia", key="btn_freq"):
                if periodo != 0:
                    res_str = f"Frecuencia = {1 / periodo:.2f} Hz"
                    st.markdown(f'<div class="result-box">{res_str}</div>', unsafe_allow_html=True)
                    guardar_historial(categoria, op_ond, res_str)
                else: st.error("El periodo no puede ser cero.")
        st.markdown('</div>', unsafe_allow_html=True)

    with t2:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.write("#### Ley de Snell (n2 = n1 * sin θ1 / sin θ2)")
        c1, c2, c3 = st.columns(3)
        n1 = c1.number_input("Índice Medio 1 (n1)", value=1.0, key="sn_n1")
        ang1 = c2.number_input("Ángulo Incidencia θ1 (°)", value=30.0, key="sn_a1")
        ang2 = c3.number_input("Ángulo Refracción θ2 (°)", value=20.0, key="sn_a2")
        if st.button("Calcular Índice n2", key="btn_snell"):
            r1, r2 = math.radians(ang1), math.radians(ang2)
            if math.sin(r2) != 0:
                n2_res = (n1 * math.sin(r1)) / math.sin(r2)
                res_str = f"Índice de Refracción n2 = {n2_res:.4f}"
                st.markdown(f'<div class="result-box">{res_str}</div>', unsafe_allow_html=True)
                guardar_historial(categoria, "Ley de Snell", res_str)
            else: st.error("El ángulo de refracción no puede generar seno igual a cero.")
        st.markdown('</div>', unsafe_allow_html=True)

    with t3:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        op_opt = st.radio("Selecciona:", ["Distancia Focal Lente", "Energía de un Fotón (E = h*f)"], horizontal=True)
        c1, c2 = st.columns(2)
        if "Distancia Focal" in op_opt:
            do = c1.number_input("Distancia Objeto (m)", value=0.5, key="foc_do")
            di = c2.number_input("Distancia Imagen (m)", value=0.3, key="foc_di")
            if st.button("Calcular Distancia Focal", key="btn_foc"):
                if (do + di) != 0:
                    foc = (do * di) / (do + di)
                    res_str = f"Distancia Focal f = {foc:.4f} m"
                    st.markdown(f'<div class="result-box">{res_str}</div>', unsafe_allow_html=True)
                    guardar_historial(categoria, op_opt, res_str)
                else: st.error("La suma de distancias no puede ser cero.")
        else:
            freq_foton = c1.number_input("Frecuencia f (Hz)", value=5.0e14, format="%.2e", key="fot_f")
            if st.button("Calcular Energía de Fotón", key="btn_fot"):
                h_const = 6.626e-34
                res_str = f"Energía Fotón E = {h_const * freq_foton:.6e} J"
                st.markdown(f'<div class="result-box">{res_str}</div>', unsafe_allow_html=True)
                guardar_historial(categoria, op_opt, res_str)
        st.markdown('</div>', unsafe_allow_html=True)

# --- 9. ELECTROMAGNETISMO ---
elif categoria == "Electromagnetismo":
    st.subheader("Electromagnetismo")
    t1, t2, t3 = st.tabs(["Ley de Coulomb", "Campo Eléctrico", "Fuerza Magnética"])

    with t1:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.write("#### Ley de Coulomb (F = k * |q1 * q2| / r²)")
        c1, c2, c3 = st.columns(3)
        q1 = c1.number_input("Carga q1 (C)", value=1.0e-6, format="%.2e", key="coul_q1")
        q2 = c2.number_input("Carga q2 (C)", value=2.0e-6, format="%.2e", key="coul_q2")
        r = c3.number_input("Distancia r (m)", value=0.1, key="coul_r")
        if st.button("Calcular Fuerza Electrostática", key="btn_coul"):
            if r != 0:
                k = 8.9875e9
                f_coul = (k * abs(q1 * q2)) / (r**2)
                res_str = f"Fuerza = {f_coul:.4e} N"
                st.markdown(f'<div class="result-box">{res_str}</div>', unsafe_allow_html=True)
                guardar_historial(categoria, "Ley de Coulomb", res_str)
            else: st.error("La distancia no puede ser cero.")
        st.markdown('</div>', unsafe_allow_html=True)

    with t2:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.write("#### Campo Eléctrico (E = F / q)")
        c1, c2 = st.columns(2)
        f = c1.number_input("Fuerza (N)", value=0.05, key="ce_f")
        q = c2.number_input("Carga q (C)", value=1.0e-6, format="%.2e", key="ce_q")
        if st.button("Calcular Campo Eléctrico", key="btn_ce"):
            if q != 0:
                res_str = f"Campo Eléctrico E = {f / q:.4e} N/C"
                st.markdown(f'<div class="result-box">{res_str}</div>', unsafe_allow_html=True)
                guardar_historial(categoria, "Campo Eléctrico", res_str)
            else: st.error("La carga no puede ser cero.")
        st.markdown('</div>', unsafe_allow_html=True)

    with t3:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.write("#### Fuerza de Lorentz sobre Carga Móvil")
        c1, c2, c3, c4 = st.columns(4)
        q = c1.number_input("Carga q (C)", value=1.6e-19, format="%.2e", key="lor_q")
        v = c2.number_input("Velocidad (m/s)", value=3.0e6, format="%.2e", key="lor_v")
        b = c3.number_input("Campo B (T)", value=0.5, key="lor_b")
        ang = c4.number_input("Ángulo θ (°)", value=90.0, key="lor_ang")
        if st.button("Calcular Fuerza Magnética", key="btn_lor"):
            f_lor = abs(q) * v * b * math.sin(math.radians(ang))
            res_str = f"Fuerza de Lorentz = {f_lor:.4e} N"
            st.markdown(f'<div class="result-box">{res_str}</div>', unsafe_allow_html=True)
            guardar_historial(categoria, "Fuerza de Lorentz", res_str)
        st.markdown('</div>', unsafe_allow_html=True)

# --- 10. MECÁNICA CELESTE ---
elif categoria == "Mecánica Celeste":
    st.subheader("Mecánica Celeste y Gravitación")
    t1, t2, t3 = st.tabs(["Gravitación Universal", "Velocidad Orbital", "Gravedad Superficial"])

    with t1:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.write("#### Ley de Gravitación Universal (F = G * m1 * m2 / r²)")
        c1, c2, c3 = st.columns(3)
        m1 = c1.number_input("Masa m1 (kg)", value=5.972e24, format="%.2e", key="gu_m1")
        m2 = c2.number_input("Masa m2 (kg)", value=1000.0, key="gu_m2")
        r = c3.number_input("Distancia r (m)", value=6371000.0, key="gu_r")
        if st.button("Calcular Fuerza Gravitacional", key="btn_gu"):
            if r != 0:
                g_const = 6.67430e-11
                f_gu = (g_const * m1 * m2) / (r**2)
                res_str = f"Fuerza Gravitacional = {f_gu:.4e} N"
                st.markdown(f'<div class="result-box">{res_str}</div>', unsafe_allow_html=True)
                guardar_historial(categoria, "Gravitación Universal", res_str)
            else: st.error("La distancia no puede ser cero.")
        st.markdown('</div>', unsafe_allow_html=True)

    with t2:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.write("#### Velocidad Orbital (v = √(G * M / r))")
        c1, c2 = st.columns(2)
        m = c1.number_input("Masa Cuerpo Central M (kg)", value=5.972e24, format="%.2e", key="vo_m")
        r = c2.number_input("Radio Orbital r (m)", value=6771000.0, key="vo_r")
        if st.button("Calcular Velocidad Orbital", key="btn_vo"):
            if r != 0:
                g_const = 6.67430e-11
                v_orb = math.sqrt((g_const * m) / r)
                res_str = f"Velocidad Orbital = {v_orb:.2f} m/s"
                st.markdown(f'<div class="result-box">{res_str}</div>', unsafe_allow_html=True)
                guardar_historial(categoria, "Velocidad Orbital", res_str)
            else: st.error("El radio no puede ser cero.")
        st.markdown('</div>', unsafe_allow_html=True)

    with t3:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.write("#### Aceleración Gravitacional Superficial (g = G * M / R²)")
        c1, c2 = st.columns(2)
        m = c1.number_input("Masa del Planeta M (kg)", value=5.972e24, format="%.2e", key="gs_m")
        r = c2.number_input("Radio del Planeta R (m)", value=6371000.0, key="gs_r")
        if st.button("Calcular Gravedad Superficial", key="btn_gs"):
            if r != 0:
                g_const = 6.67430e-11
                g_sup = (g_const * m) / (r**2)
                res_str = f"Gravedad Superficial g = {g_sup:.2f} m/s²"
                st.markdown(f'<div class="result-box">{res_str}</div>', unsafe_allow_html=True)
                guardar_historial(categoria, "Gravedad Superficial", res_str)
            else: st.error("El radio no puede ser cero.")
        st.markdown('</div>', unsafe_allow_html=True)

# --- 11. FÍSICA MODERNA ---
elif categoria == "Física Moderna":
    st.subheader("Física Moderna y Relatividad")
    t1, t2, t3 = st.tabs(["Equivalencia Masa-Energía", "Onda de De Broglie", "Factor de Lorentz"])

    with t1:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.write("#### Equivalencia Masa-Energía (E = m * c²)")
        m = st.number_input("Masa m (kg)", value=0.001, format="%.6f", key="me_m")
        if st.button("Calcular Energía Relativista", key="btn_me"):
            c = 299792458
            e_rel = m * (c**2)
            res_str = f"Energía E = {e_rel:.6e} J"
            st.markdown(f'<div class="result-box">{res_str}</div>', unsafe_allow_html=True)
            guardar_historial(categoria, "Masa-Energía", res_str)
        st.markdown('</div>', unsafe_allow_html=True)

    with t2:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.write("#### Longitud de Onda de De Broglie (λ = h / p)")
        p = st.number_input("Momento Lineal p (kg·m/s)", value=1.0e-23, format="%.2e", key="db_p")
        if st.button("Calcular Longitud de Onda", key="btn_db"):
            if p != 0:
                h = 6.62607015e-34
                lam_db = h / p
                res_str = f"Longitud de Onda λ = {lam_db:.6e} m"
                st.markdown(f'<div class="result-box">{res_str}</div>', unsafe_allow_html=True)
                guardar_historial(categoria, "Onda De Broglie", res_str)
            else: st.error("El momento no puede ser cero.")
        st.markdown('</div>', unsafe_allow_html=True)

    with t3:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.write("#### Factor de Lorentz (γ = 1 / √(1 - v²/c²))")
        v = st.number_input("Velocidad v (m/s)", value=2.0e8, format="%.2e", key="lor_v_mod")
        if st.button("Calcular Factor γ y Graficar", key="btn_lor_mod"):
            c = 299792458
            if v < c:
                gamma = 1 / math.sqrt(1 - (v**2 / c**2))
                res_str = f"Factor de Lorentz γ = {gamma:.6f}"
                st.markdown(f'<div class="result-box">{res_str}</div>', unsafe_allow_html=True)
                guardar_historial(categoria, "Factor Lorentz", res_str)

                v_arr = np.linspace(0, 0.99*c, 100)
                gamma_arr = 1 / np.sqrt(1 - (v_arr**2 / c**2))
                fig = go.Figure()
                fig.add_trace(go.Scatter(x=v_arr/c, y=gamma_arr, mode='lines', name='γ(v/c)', line=dict(color='#A855F7', width=3)))
                fig.update_layout(title="Factor de Lorentz γ vs Velocidad (v/c)", xaxis_title="Velocidad Fraccional (v/c)", yaxis_title="Factor γ")
                st.plotly_chart(fig, use_container_width=True)
            else: st.error("La velocidad debe ser strictly menor a la velocidad de la luz (c).")
        st.markdown('</div>', unsafe_allow_html=True)

# --- MÓDULO ADICIONAL: CREADOR DE GRÁFICAS ---
elif categoria.lower() == "creador de gráficas":
    st.subheader("Creador de Gráficas Personalizado")
    st.write("Ingresa los resultados de tus fórmulas para visualizarlos en pantalla.")

    # 1. Selección del tipo de gráfico
    tipo_grafica = st.radio(
        "Selecciona el tipo de gráfica:",
        ["Líneas (tendencia)", "Dispersión XY (Puntos)"],
        horizontal=True,
        key="cg_tipo_radio"
    )

    st.markdown("---")

    # 2. Entradas del usuario para los ejes X e Y
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("#### Configuración Eje X")
        nombre_x = st.text_input("Nombre de la variable X:", "Tiempo (s)", key="cg_nombre_x")
        datos_x_texto = st.text_input("Valores de X (separados por comas):", "1, 2, 3, 4, 5", key="cg_datos_x")

    with col2:
        st.markdown("#### Configuración Eje Y")
        nombre_y = st.text_input("Nombre de la variable Y:", "Distancia (m)", key="cg_nombre_y")
        datos_y_texto = st.text_input("Valores de Y (separados por comas):", "10, 20, 25, 40, 50", key="cg_datos_y")

    # 3. Procesamiento y Renderizado de la gráfica
    if st.button("Generar Gráfica", key="btn_generar_grafica_custom"):
        try:
            # Convertimos el texto ingresado en listas numéricas
            lista_x = [float(n.strip()) for n in datos_x_texto.split(",")]
            lista_y = [float(n.strip()) for n in datos_y_texto.split(",")]

            # Verificación de cantidad equivalente de datos
            if len(lista_x) != len(lista_y):
                st.error(f"Cantidad desigual de datos: Tienes {len(lista_x)} valores en X y {len(lista_y)} valores en Y.")
            else:
                # Creación del gráfico con Plotly
                fig = go.Figure()

                if "Líneas" in tipo_grafica:
                    fig.add_trace(go.Scatter(
                        x=lista_x,
                        y=lista_y,
                        mode='lines+markers',
                        name=nombre_y,
                        line=dict(color='#818CF8', width=3),
                        marker=dict(size=8)
                    ))
                else:
                    fig.add_trace(go.Scatter(
                        x=lista_x,
                        y=lista_y,
                        mode='markers',
                        name=nombre_y,
                        marker=dict(size=12, color='#38BDF8')
                    ))

                # Ajuste de plantilla según el tema
                tema_plotly = "plotly_dark" if 'modo' in locals() and modo == "Oscuro" else "plotly_white"

                fig.update_layout(
                    title=f"Gráfica de {nombre_y} vs {nombre_x}",
                    xaxis_title=nombre_x,
                    yaxis_title=nombre_y,
                    template=tema_plotly
                )

                # Despliegue de la gráfica interactiva
                st.plotly_chart(fig, use_container_width=True)
                st.success("¡Gráfica generada con éxito!")

        except ValueError:
            st.error("Formato incorrecto: Escribe únicamente números separados por comas.")
# --- FIRMA DE AUTOR Y PROPIEDAD ---
st.sidebar.markdown("---")
st.sidebar.markdown("###  Desarrollador")
st.sidebar.write("Aplicación creada por: **Rodrigo Rodriguez**")
st.sidebar.caption("© 2026 PhysiKal. Todos los derechos reservados.")
st.sidebar.markdown("---")
# ------------------------------------------------------------------------------
# 7. HISTORIAL DE CÁLCULOS Y DESCARGA EN MENÚ LATERAL (.TXT, .CSV, .PDF)
# ------------------------------------------------------------------------------
st.sidebar.markdown("---")
st.sidebar.markdown("### Historial de Cálculos")

if st.sidebar.button("Borrar Historial", key="btn_borrar_h"):
    st.session_state.historial = []
    st.rerun()

if st.session_state.historial:
    txt_lines = ["--- HISTORIAL DE CÁLCULOS - Physikal Studio Pro ---\n"]
    csv_lines = ["Categoria,Formula,Resultado\n"]

    for idx, item in enumerate(reversed(st.session_state.historial), 1):
        st.sidebar.markdown(f"**{idx}. [{item['categoria']}]**")
        st.sidebar.caption(f"{item['formula']}")
        st.sidebar.text(item['resultado'])
        st.sidebar.markdown("---")
        
        txt_lines.append(f"[{item['categoria']}] {item['formula']} => {item['resultado']}\n")
        csv_lines.append(f'"{item["categoria"]}","{item["formula"]}","{item["resultado"]}"\n')

    txt_data = "".join(txt_lines)
    csv_data = "".join(csv_lines)

    st.sidebar.download_button(
        label="Descargar (.TXT)",
        data=txt_data,
        file_name="historial_physikal.txt",
        mime="text/plain",
        key="btn_down_txt"
    )

    st.sidebar.download_button(
        label="Descargar (.CSV)",
        data=csv_data,
        file_name="historial_physikal.csv",
        mime="text/csv",
        key="btn_down_csv"
    )

    if REPORTLAB_AVAILABLE:
        pdf_buffer = generar_pdf_historial(st.session_state.historial)
        st.sidebar.download_button(
            label="Descargar Reporte (.PDF)",
            data=pdf_buffer,
            file_name="reporte_physikal.pdf",
            mime="application/pdf",
            key="btn_down_pdf"
        )
    else:
        st.sidebar.caption("Instala `reportlab` para habilitar descargas en PDF.")
else:
    st.sidebar.info("Aún no has realizado cálculos en esta sesión.")
