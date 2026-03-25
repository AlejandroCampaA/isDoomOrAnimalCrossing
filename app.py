import streamlit as st
import tensorflow as tf
from PIL import Image
import numpy as np
import os

# ========================================================
# Configuracion de la pagina
# ========================================================
# Esto hace que la app ocupe mas ancho en la pantalla para que las tablas se vean mejor
st.set_page_config(page_title="Doom vs Animal Crossing", page_icon="🎮", layout="wide")

st.title("🎮 Doom vs Animal Crossing Classifier 🌴")
st.write("Sube una o varias imagenes y la IA adivinara a que juego pertenecen.")

# ========================================================
# Carga del Modelo
# ========================================================
st.sidebar.header("⚙️ Configuracion del Modelo")

uploaded_model = st.sidebar.file_uploader("Sube tu propio modelo (.keras)", type=['keras'])

@st.cache_resource
def load_default_model():
    default_path = 'modelo_doom_vs_ac.keras'
    if os.path.exists(default_path):
        return tf.keras.models.load_model(default_path)
    return None

model = None
if uploaded_model is not None:
    with open("temp_model.keras", "wb") as f:
        f.write(uploaded_model.getbuffer())
    try:
        model = tf.keras.models.load_model("temp_model.keras")
        st.sidebar.success("¡Modelo personalizado cargado!")
    except Exception as e:
        st.sidebar.error("Error al cargar el modelo personalizado. Revisa que el archivo no este danado.")
else:
    model = load_default_model()
    if model:
        st.sidebar.info("Usando el modelo predeterminado.")
    else:
        st.sidebar.warning("No se encontro 'modelo_doom_vs_ac.keras'. Sube uno para probar.")

# ========================================================
# Seccion de Prediccion (Multiaplicacion)
# ========================================================
st.subheader("Sube tus imagenes a analizar")

if "uploader_key" not in st.session_state:
    st.session_state.uploader_key = 0
if "uploaded_images_map" not in st.session_state:
    st.session_state.uploaded_images_map = {}
if "selected_image_names" not in st.session_state:
    st.session_state.selected_image_names = []
if "processed_files" not in st.session_state:
    st.session_state.processed_files = set()

# El parametro 'accept_multiple_files=True' es la magia aqui
uploaded_images = st.file_uploader(
    "Elige las imagenes...", 
    type=["jpg", "jpeg", "png"], 
    accept_multiple_files=True,
    key=f"uploader_{st.session_state.uploader_key}"
)

# Guardamos las imagenes subidas en sesion
if uploaded_images:
    for img in uploaded_images:
        # Usamos un identificador unico por uploader y nombre
        file_id = f"{st.session_state.uploader_key}_{img.name}"
        if file_id not in st.session_state.processed_files:
            st.session_state.uploaded_images_map[img.name] = img
            if img.name not in st.session_state.selected_image_names:
                st.session_state.selected_image_names.append(img.name)
            st.session_state.processed_files.add(file_id)

stored_names = list(st.session_state.uploaded_images_map.keys())

# Sincroniza seleccion si se quitaron elementos
st.session_state.selected_image_names = [
    name for name in st.session_state.selected_image_names if name in stored_names
]

if stored_names and not st.session_state.selected_image_names:
    st.session_state.selected_image_names = stored_names.copy()

if stored_names:
    st.markdown("### Gestiona tus imagenes")
    
    current_selection = st.multiselect(
        "Selecciona cuales quieres analizar",
        options=stored_names,
        default=st.session_state.selected_image_names,
        help="Tambien puedes quitar imagenes de la lista con los botones de abajo."
    )
    # Sincroniza el estado global con la interaccion del componente visual
    st.session_state.selected_image_names = current_selection

    images_to_analyze = [
        st.session_state.uploaded_images_map[name]
        for name in st.session_state.selected_image_names
        if name in st.session_state.uploaded_images_map
    ]
else:
    images_to_analyze = []

if images_to_analyze and model is not None:
    st.write(f"Analizando {len(images_to_analyze)} imagen(es)... 🧠")
    st.markdown("---") # Linea divisoria
    
    # Recorremos cada imagen subida
    for img_file in images_to_analyze:
        # Creamos dos columnas: una para la imagen (30% ancho) y otra para el resultado (70% ancho)
        col1, col2 = st.columns([1, 2])
        
        try:
            # 1. Mostrar la imagen en la primera columna
            image = Image.open(img_file)
            with col1:
                # API nueva de Streamlit: reemplaza use_container_width
                st.image(image, caption=img_file.name, width="stretch")
            
            # 2. Procesar la imagen
            image_rgb = image.convert('RGB')
            img_resized = image_rgb.resize((150, 150))
            img_array = tf.keras.preprocessing.image.img_to_array(img_resized)
            img_array = np.expand_dims(img_array, axis=0)
            
            # 3. Hacer prediccion
            with st.spinner(f"Analizando {img_file.name}..."):
                prediction = model.predict(img_array, verbose=0)
            probabilidad = float(prediction[0][0])
            prob_doom = probabilidad
            prob_ac = 1 - probabilidad
            
            # 4. Mostrar resultados en la segunda columna
            with col2:
                st.markdown(f"### Resultados para: `{img_file.name}`")

                # Estados mas detallados para reflejar mejor la confianza del modelo
                confianza = max(prob_doom, prob_ac)

                if prob_doom >= 0.90:
                    st.error("**Doom casi seguro** 🩸👹")
                    st.write("Nivel de confianza: muy alto.")
                elif prob_doom >= 0.75:
                    st.error("**Muy probable Doom** 👹")
                    st.write("Nivel de confianza: alto.")
                elif prob_doom >= 0.60:
                    st.warning("**Puede que sea Doom** 👺")
                    st.write("Nivel de confianza: medio.")
                elif 0.48 <= prob_doom <= 0.52:
                    st.warning("**Empate tecnico: puede ser ambas** 🤝")
                    st.write("Las probabilidades estan casi iguales entre Doom y Animal Crossing.")
                elif prob_ac >= 0.90:
                    st.success("**Animal Crossing casi seguro** 🦝🌴")
                    st.write("Nivel de confianza: muy alto.")
                elif prob_ac >= 0.75:
                    st.success("**Muy probable Animal Crossing** 🌴")
                    st.write("Nivel de confianza: alto.")
                elif prob_ac >= 0.60:
                    st.info("**Puede que sea Animal Crossing** 🍃")
                    st.write("Nivel de confianza: medio.")
                else:
                    st.info("**No concluyente** 🧐")
                    st.write("El modelo no tiene suficiente certeza en esta imagen.")

                if confianza < 0.65:
                    st.caption("Nota: el resultado puede no corresponder claramente a ninguna de las dos clases.")

                st.write(f"Doom: **{prob_doom * 100:.2f}%** | Animal Crossing: **{prob_ac * 100:.2f}%**")
                st.progress(confianza)
                    
        except Exception as e:
            # Si hay un error con una imagen especifica (ej. archivo corrupto), no tumba toda la app
            with col2:
                st.error(f"Ups, hubo un problema al leer esta imagen. Detalle tecnico: {e}")
                
        st.markdown("---") # Linea divisoria para separar cada imagen en la lista

elif stored_names and model is None:
    st.error("Por favor, asegurate de que el modelo este cargado en la barra lateral.")