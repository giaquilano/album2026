import streamlit as st

# Configuración de la página (título y diseño)
st.set_page_config(page_title="Mi Álbum Mundial 2026", layout="centered")

# Título principal de la app
st.title("🏆 Mi Álbum del Mundial 2026 🏆")
st.write("¡Llevá el control de tus figuritas de forma fácil!")

# --- SECCIÓN DE ESTADÍSTICAS ---
st.subheader("📊 Progreso General")
col1, col2, col3 = st.columns(3)
with col1:
    st.metric(label="Total Figuritas", value="450")
with col2:
    st.metric(label="Pegadas", value="124")
with col3:
    st.metric(label="Repetidas", value="32")

st.progress(124 / 450) # Barra de progreso visual

# --- SECCIÓN DE CONTROL ---
st.subheader("✏️ Gestionar Figuritas")

# Selector de selección/grupo
grupo = st.selectbox(
    "Seleccioná el Grupo o Selección:",
    ["Grupo A - Argentina", "Grupo A - Canadá", "Grupo B - México", "Grupo B - Alemania"]
)

# Entrada de número de figurita
numero_figu = st.number_input("Número de figurita:", min_value=1, max_value=450, step=1)

# Botones de acción
col_btn1, col_btn2 = st.columns(2)
with col_btn1:
    if st.button("✅ Marcar como Pegada", use_container_width=True):
        st.success(f"¡Figurita {numero_figu} de {grupo} marcada como pegada!")

with col_btn2:
    if st.button("🔁 Agregar a Repetidas", use_container_width=True):
        st.info(f"¡Figurita {numero_figu} de {grupo} agregada a repetidas!")

# --- LISTA DE FIGURITAS QUE FALTAN ---
st.subheader("📝 Figuritas Faltantes")
st.checkbox("Figurita 01 (Escudo)")
st.checkbox("Figurita 10 (Messi)")
st.checkbox("Figurita 18 (Dibu Martínez)")
