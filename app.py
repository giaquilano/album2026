import streamlit as st
from st_supabase_connection import SupabaseConnection


st.set_page_config(page_title="Mi Álbum Mundial 2026", page_icon="🏆", layout="centered")



@st.cache_resource
def init_connection():
    return st.connection("supabase", type=SupabaseConnection)

try:
    supabase = init_connection()
except Exception:

    supabase = None


lista_paises = [
    ("MEX", "MEX (Mexico)"), ("RSA", "RSA (Sudafrica)"), ("KOR", "KOR (Republica de corea)"), ("CZE", "CZE (Chequia)"),
    ("CAN", "CAN (Canada)"), ("BIH", "BIH (Bosnia y Herzegovina)"), ("QAT", "QAT (Qatar)"), ("SUI", "SUI (Suiza)"),
    ("BRA", "BRA (Brasil)"), ("MAR", "MAR (Marruecos)"), ("HAI", "HAI (Haiti)"), ("SCO", "SCO (Escocia)"),
    ("USA", "USA (Estados Unidos)"), ("PAR", "PAR (Paraguay)"), ("AUS", "AUS (Australia)"), ("TUR", "TUR (Turquia)"),
    ("GER", "GER (Alemania)"), ("CUW", "CUW (Curazao)"), ("CIV", "CIV (Costa de marfil)"), ("ECU", "ECU (Ecuador)"),
    ("NED", "NED (Paises Bajos)"), ("JPN", "JPN (Japon)"), ("SWE", "SWE (Suecia)"), ("TUN", "TUN (Tunes)"),
    ("BEL", "BEL (Belgica)"), ("EGY", "EGY (Egypto)"), ("IRN", "IRN (Iran)"), ("NZL", "NZL (Nueva Zelanda)"),
    ("ESP", "ESP (España)"), ("CPV", "CPV (Cabo Verde)"), ("KSA", "KSA (Arabia Saudita)"), ("URU", "URU (Uruguay)"),
    ("FRA", "FRA (Francia)"), ("SEN", "SEN (Senegal)"), ("IRQ", "IRQ (Iraq)"), ("NOR", "NOR (Noruega)"),
    ("ARG", "ARG (Argentina)"), ("ALG", "ALG (Argelia)"), ("AUT", "AUT (Austria)"), ("JOR", "JOR (Jordania)"),
    ("POR", "POR (Portugal)"), ("COD", "COD (DR Congo)"), ("UZB", "UZB (Uzbekistan)"), ("COL", "COL (Colombia)"),
    ("ENG", "ENG (Inglaterra)"), ("CRO", "CRO (Croacia)"), ("GHA", "GHA (Ghana)"), ("PAN", "PAN (Panama)")
]

secciones_especiales = [
    ("FWC_SPEC", "FWC Specials", 5),
    ("FWC_BALL", "FWC ball and countries", 4),
    ("FWC_HIST", "FWC history", 11),
    ("COCA", "Coca-Cola", 14)
]


def cargar_datos_usuario(usuario):
    if supabase is None:
        return set(), {}
    try:
        
        res = supabase.table("albumes").select("pegadas, repetidas").eq("usuario", usuario).execute()
        if res.data:
            pegadas_db = set(res.data[0].get("pegadas", []))
            repetidas_db = res.data[0].get("repetidas", {})
            return pegadas_db, repetidas_db
    except Exception:
        pass
    return set(), {}

def guardar_datos_usuario(usuario, pegadas, repetidas):
    if supabase is None: return
    try:
        
        lista_pegadas = list(pegadas)
        
        supabase.table("albumes").upsert({
            "usuario": usuario,
            "pegadas": lista_pegadas,
            "repetidas": repetidas
        }, on_conflict="usuario").execute()
    except Exception:
        pass


if "usuario_conectado" not in st.session_state:
    st.session_state.usuario_conectado = None


if st.session_state.usuario_conectado is None:
    st.title("🔐 Iniciar Sesión - Mi Álbum 2026")
    st.write("Ingresá tu nombre de usuario personalizado para guardar tu progreso de forma permanente.")
    
    usuario_input = st.text_input("Nombre de Usuario:", placeholder="Ej: giada_2026").strip().lower()
    
    if st.button("🚀 Ingresar a mi Álbum", use_container_width=True):
        if usuario_input:
            st.session_state.usuario_conectado = usuario_input
            
            pegadas, repetidas = cargar_datos_usuario(usuario_input)
            st.session_state.album_pegadas = pegadas
            st.session_state.album_repetidas = repetidas
            st.rerun()
        else:
            st.error("Por favor, escribí un nombre de usuario válido.")
    st.stop()  


usuario = st.session_state.usuario_conectado


col_tit, col_logout = st.columns([4, 1])
with col_tit:
    st.title("🏆 Mi Álbum del Mundial 2026 🏆")
    st.write(f"Conectado como: **{usuario}** 🟢 (Tus datos se guardan automáticamente en la nube)")
with col_logout:
    if st.button("🔒 Salir"):
        st.session_state.usuario_conectado = None
        st.rerun()

st.markdown("---")


st.subheader("📝 Ingresar Figurita Obtenida")

tipo_figu = st.radio("¿Qué tipo de figurita vas a cargar?", ["País / Selección", "Sección Especial"], horizontal=True)

id_final = ""
nombre_visual = ""

if tipo_figu == "País / Selección":
    pais_elegido = st.selectbox("Seleccioná el País:", lista_paises, format_func=lambda x: x[1])
    num_figu = st.number_input("Número de figurita (1 al 20):", min_value=1, max_value=20, step=1)
    id_final = f"{pais_elegido[0]}-{num_figu}"
    nombre_visual = f"{pais_elegido[1]} - N° {num_figu}"
else:
    especial_elegida = st.selectbox("Seleccioná la Sección Especial:", secciones_especiales, format_func=lambda x: x[1])
    num_figu = st.number_input(f"Número de figurita (1 al {especial_elegida[2]}):", min_value=1, max_value=especial_elegida[2], step=1)
    id_final = f"{especial_elegida[0]}-{num_figu}"
    nombre_visual = f"{especial_elegida[1]} - N° {num_figu}"

if st.button("➕ Registrar Figurita", use_container_width=True):
    if id_final not in st.session_state.album_pegadas:
        st.session_state.album_pegadas.add(id_final)
        st.success(f"¡Genial! Pegaste una nueva: {nombre_visual}")
    else:
        st.session_state.album_repetidas[id_final] = st.session_state.album_repetidas.get(id_final, 0) + 1
        st.warning(f"Esta ya la tenías pegada. Se guardó en Repetidas: {nombre_visual}")
    
    
    guardar_datos_usuario(usuario, st.session_state.album_pegadas, st.session_state.album_repetidas)
    st.rerun()

st.markdown("---")


st.subheader("📊 Análisis del Álbum")

TOTAL_ALBUM = 980

obtenidas = len(st.session_state.album_pegadas)
faltantes = TOTAL_ALBUM - obtenidas
total_repetidas = sum(st.session_state.album_repetidas.values())
porcentaje = (obtenidas / TOTAL_ALBUM) * 100

col1, col2, col3 = st.columns(3)
col1.metric("Figuritas Obtenidas", f"{obtenidas} / {TOTAL_ALBUM}")
col2.metric("Figuritas Faltantes", f"{faltantes}")
col3.metric("Total Repetidas", f"{total_repetidas}")

st.write(f"**Porcentaje completo del álbum:** {porcentaje:.2f}%")
st.progress(porcentaje / 100)

st.markdown("---")


st.subheader("🔄 Módulo de Intercambio")

def mapear_nombre(codigo_id):
    partes = codigo_id.split("-")
    cod, num = partes[0], partes[1]
    for p_cod, p_nom in lista_paises:
        if p_cod == cod: return f"{p_nom} - N° {num}"
    for e_cod, e_nom, _ in secciones_especiales:
        if e_cod == cod: return f"{e_nom} - N° {num}"
    return codigo_id

if len(st.session_state.album_repetidas) == 0:
    st.info("Todavía no tenés figuritas repetidas cargadas para cambiar.")
else:
    opciones_rep = list(st.session_state.album_repetidas.keys())
    figu_a_cambiar = st.selectbox("Seleccioná la figurita que vas a cambiar:", opciones_rep, format_func=mapear_nombre)
    
    cant_actual = st.session_state.album_repetidas[figu_a_cambiar]
    st.write(f"Tenés **{cant_actual}** repetida(s) de esta figurita.")

    if st.button(f"🤝 Cambié esta figurita", use_container_width=True):
        if st.session_state.album_repetidas[figu_a_cambiar] > 1:
            st.session_state.album_repetidas[figu_a_cambiar] -= 1
            st.success("Se descontó 1 unidad de tus repetidas.")
        else:
            del st.session_state.album_repetidas[figu_a_cambiar]
            st.success("¡Cambiaste la última! Ya no te quedan repetidas de esta.")
        
        
        guardar_datos_usuario(usuario, st.session_state.album_pegadas, st.session_state.album_repetidas)
        st.rerun()

st.markdown("---")


st.subheader("📋 Reporte de Figuritas Faltantes")

filtro_reporte = st.selectbox("Ver faltantes de:", ["Todo el Álbum", "Solo Selecciones", "Solo Secciones Especiales"])

def obtener_numeros_faltantes(codigo, max_num):
    faltan_numeros = []
    for num in range(1, max_num + 1):
        if f"{codigo}-{num}" not in st.session_state.album_pegadas:
            faltan_numeros.append(str(num))
    return faltan_numeros

with st.expander("🔍 Hacer clic acá para desplegar el listado detallado"):
    if faltantes == 0:
        st.balloons()
        st.success("¡FELICITACIONES! Completaste el álbum entero. 🎉")
    else:
        if filtro_reporte in ["Todo el Álbum", "Solo Selecciones"]:
            st.markdown("### 🏳️ Selecciones Nacionales")
            for cod, nombre in lista_paises:
                lista_num = obtener_numeros_faltantes(cod, 20)
                if lista_num:
                    numeros_texto = ", ".join(lista_num)
                    st.write(f"• **{nombre}:** Faltan N° [{numeros_texto}]")
        
        if filtro_reporte in ["Todo el Álbum", "Solo Secciones Especiales"]:
            st.markdown("### 🌟 Secciones Especiales")
            for cod, nombre, max_num in secciones_especiales:
                lista_num = obtener_numeros_faltantes(cod, max_num)
                if lista_num:
                    numeros_texto = ", ".join(lista_num)
                    st.write(f"• **{nombre}:** Faltan N° [{numeros_texto}]")

st.markdown("---")


with st.expander("📇 Ver detalle de tus Figuritas Repetidas"):
    if len(st.session_state.album_repetidas) == 0:
        st.write("No hay repetidas.")
    else:
        for k, v in st.session_state.album_repetidas.items():
            st.write(f"• {mapear_nombre(k)} → **{v} rep.**")
