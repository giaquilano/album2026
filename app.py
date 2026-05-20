import streamlit as st

# Configuración de la página
st.set_page_config(page_title="Mi Álbum Mundial 2026", page_icon="🏆", layout="centered")


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


if "album_pegadas" not in st.session_state:
    st.session_state.album_pegadas = set()  
if "album_repetidas" not in st.session_state:
    st.session_state.album_repetidas = {} 


st.title("🏆 Mi Álbum del Mundial 2026 🏆")
st.write("Ingresá tus figuritas obtenidas y dejá que el sistema analice tu progreso.")

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

if len(st.session_state.album_repetidas) == 0:
    st.info("Todavía no tenés figuritas repetidas cargadas para cambiar.")
else:
    
    def mapear_nombre(codigo_id):
        partes = codigo_id.split("-")
        cod, num = partes[0], partes[1]
      
        for p_cod, p_nom in lista_paises:
            if p_cod == cod: return f"{p_nom} - N° {num}"
        
        for e_cod, e_nom, _ in secciones_especiales:
            if e_cod == cod: return f"{e_nom} - N° {num}"
        return codigo_id

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
        st.rerun()

st.markdown("---")


with st.expander("📋 Ver detalle de tus Figuritas Repetidas"):
    if len(st.session_state.album_repetidas) == 0:
        st.write("No hay repetidas.")
    else:
        for k, v in st.session_state.album_repetidas.items():
            st.write(f"• {mapear_nombre(k)} → **{v} rep.**")
