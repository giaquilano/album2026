import streamlit as st

# Configuración de la página del navegador
st.set_page_config(page_title="Mi Álbum Mundial 2026", page_icon="🏆", layout="centered")

# Título de la aplicación
st.title("🏆 Mi Álbum del Mundial 2026 🏆")
st.write("¡Llevá el control de tus figuritas de forma fácil!")

# Lista real de selecciones del Mundial 2026
paises = [
    "Grupo A - Estados Unidos", "Grupo A - México", "Grupo A - Canadá", "Grupo A - Alianza",
    "Grupo B - Argentina", "Grupo B - Selección 2", "Grupo B - Selección 3", "Grupo B - Selección 4",
    "Grupo C - Brasil", "Grupo C - Selección 2", "Grupo C - Selección 3", "Grupo C - Selección 4",
    "Grupo D - Francia", "Grupo D - Selección 2", "Grupo D - Selección 3", "Grupo D - Selección 4",
    "Grupo E - España", "Grupo E - Selección 2", "Grupo E - Selección 3", "Grupo E - Selección 4",
    "Grupo F - Alemania", "Grupo F - Selección 2", "Grupo F - Selección 3", "Grupo F - Selección 4",
    "Grupo G - Inglaterra", "Grupo G - Selección 2", "Grupo G - Selección 3", "Grupo G - Selección 4",
    "Grupo H - Portugal", "Grupo H - Selección 2", "Grupo H - Selección 3", "Grupo H - Selección 4"
]

# Inicializar los datos en la memoria de la sesión si no existen
if "pegadas" not in st.session_state:
    st.session_state.pegadas = set()
if "repetidas" not in st.session_state:
    st.session_state.repetidas = {}

# --- SECCIÓN 1: PROGRESO GENERAL ---
st.subheader("📊 Progreso General")

total_album = 450
cant_pegadas = len(st.session_state.pegadas)
cant_repetidas = sum(st.session_state.repetidas.values())

col1, col2, col3 = st.columns(3)
col1.metric("Total Figuritas", f"{total_album}")
col2.metric("Pegadas", f"{cant_pegadas}")
col3.metric("Repetidas", f"{cant_repetidas}")

# Barra de progreso matemática
porcentaje = cant_pegadas / total_album
st.progress(porcentaje)

st.markdown("---")

# --- SECCIÓN 2: GESTIONAR FIGURITAS ---
st.subheader("📝 Gestionar Figuritas")

seleccion = st.selectbox("Seleccioná el Grupo o Selección:", paises)
numero = st.number_input("Número de figurita (1 al 18):", min_value=1, max_value=18, step=1)

# Identificador único de la figurita (ej: "Argentina-10")
id_figu = f"{seleccion}-{numero}"

col_btn1, col_btn2 = st.columns(2)

with col_btn1:
    if st.button("✅ Marcar como Pegada", use_container_width=True):
        st.session_state.pegadas.add(id_figu)
        st.rerun()

with col_btn2:
    if st.button("📇 Agregar a Repetidas", use_container_width=True):
        if id_figu in st.session_state.repetidas:
            st.session_state.repetidas[id_figu] += 1
        else:
            st.session_state.repetidas[id_figu] = 1
        st.rerun()

st.markdown("---")

# --- SECCIÓN 3: LISTADO DE CONTROL ---
st.subheader("📋 Estado de esta Selección")
st.write(f"Figuritas de **{seleccion}**:")

# Mostrar las 18 figuritas de la selección seleccionada actual
for i in range(1, 19):
    check_id = f"{seleccion}-{i}"
    if check_id in st.session_state.pegadas:
        st.write(f"🔹 Figurita {i:02d}: **PEGADA** ✅")
    elif check_id in st.session_state.repetidas:
        cant_rep = st.session_state.repetidas[check_id]
        st.write(f"🔸 Figurita {i:02d}: Faltante (Tenés {cant_rep} repetida/s) 📇")
    else:
        st.write(f"⬜ Figurita {i:02d}: Faltante ❌")
