import os
from datetime import datetime

import requests
import streamlit as st
from dotenv import load_dotenv
from faster_whisper import WhisperModel
from streamlit_mic_recorder import mic_recorder

# =========================
# CARGAR VARIABLES .ENV
# =========================

load_dotenv()

HF_TOKEN = os.getenv("hf_token")


API_URL = (
    "https://api-inference.huggingface.co/models/"
    "google/flan-t5-base"
)
headers = {
    "Authorization": f"Bearer {HF_TOKEN}"
}

# =========================
# CONFIGURACIÓN APP
# =========================

st.set_page_config(
    page_title="Transcriptor IA",
    page_icon="🎙️",
    layout="centered"
)

st.title("🎙️ Transcriptor de clases")
st.write("Graba audio y obtén apuntes automáticamente")

# =========================
# NOMBRE CLASE
# =========================

nombre_clase = st.text_input(
    "📚 Nombre de la clase",
    placeholder="Ej: Probabilidad Bayesiana"
)

# =========================
# CREAR CARPETAS
# =========================

os.makedirs("grabaciones", exist_ok=True)
os.makedirs("transcripciones", exist_ok=True)

# =========================
# SESSION STATE
# =========================

if "texto" not in st.session_state:
    st.session_state.texto = ""

if "apuntes_limpios" not in st.session_state:
    st.session_state.apuntes_limpios = ""

# =========================
# HISTORIAL TRANSCRIPCIONES
# =========================

st.sidebar.title("📚 Historial")

archivos = [
    archivo
    for archivo in os.listdir("transcripciones")
    if archivo.endswith(".txt")
]

archivos.sort(reverse=True)

if archivos:

    archivo_seleccionado = st.sidebar.selectbox(
        "Selecciona una transcripción",
        archivos
    )

    if st.sidebar.button("📖 Cargar transcripción"):

        ruta = (
            f"transcripciones/{archivo_seleccionado}"
        )

        with open(ruta, "r", encoding="utf-8") as f:

            st.session_state.texto = f.read()

        st.session_state.apuntes_limpios = ""

        st.success("✅ Transcripción cargada")

# =========================
# CARGAR WHISPER
# =========================

@st.cache_resource
def load_model():

    return WhisperModel(
        "base",
        device="cpu",
        compute_type="int8"
    )

model = load_model()

# =========================
# GRABAR AUDIO
# =========================

st.subheader("🎤 Grabar clase")

audio = mic_recorder(
    start_prompt="▶️ Empezar grabación",
    stop_prompt="⏹️ Detener grabación",
    just_once=False,
    use_container_width=True,
    format="wav"
)

# =========================
# TRANSCRIBIR
# =========================

if audio:

    fecha = datetime.now().strftime(
        "%Y%m%d_%H%M%S"
    )

    if nombre_clase == "":
        nombre_clase = "clase"

    nombre_archivo = (
        nombre_clase
        .replace(" ", "_")
        .lower()
    )

    audio_path = (
        f"grabaciones/"
        f"{nombre_archivo}_{fecha}.wav"
    )

    txt_path = (
        f"transcripciones/"
        f"{nombre_archivo}_{fecha}.txt"
    )

    # Guardar audio
    with open(audio_path, "wb") as f:
        f.write(audio["bytes"])

    st.success("✅ Audio grabado")

    st.audio(audio_path)

    if st.button("🧠 Transcribir"):

        with st.spinner(
            "Transcribiendo audio..."
        ):

            segments, info = model.transcribe(
                audio_path,
                language="es"
            )

            st.session_state.texto = ""

            for segment in segments:

                linea = (
                    f"[{segment.start:.2f}s"
                    f" -> "
                    f"{segment.end:.2f}s] "
                    f"{segment.text}\n"
                )

                st.session_state.texto += linea

            with open(
                txt_path,
                "w",
                encoding="utf-8"
            ) as f:

                f.write(
                    st.session_state.texto
                )

        st.success(
            "✅ Transcripción completada"
        )

# =========================
# MOSTRAR TRANSCRIPCIÓN
# =========================

if st.session_state.texto != "":

    st.divider()

    st.subheader("📝 Transcripción")

    st.text_area(
        "Resultado",
        st.session_state.texto,
        height=400,
        key="transcripcion_area"
    )

    st.download_button(
        label="⬇️ Descargar transcripción",
        data=st.session_state.texto,
        file_name="transcripcion.txt",
        mime="text/plain"
    )

    # =========================
    # HERRAMIENTAS ESTUDIO
    # =========================

    st.divider()

    st.subheader(
        "🧠 Herramientas de estudio"
    )

    # =========================
    # APUNTES ORGANIZADOS
    # =========================

    if st.button(
        "📚 Generar apuntes organizados"
    ):

        with st.spinner(
            "La IA está organizando apuntes..."
        ):

            prompt = f"""
            Convierte esta transcripción
            en apuntes organizados.

            Reglas:
            - Usa títulos
            - Usa subtítulos
            - Elimina muletillas
            - Explica claro
            - Mantén conceptos importantes
            - Formato bonito para estudiar
            - Usa markdown
            - Destaca definiciones

            Transcripción:
            {st.session_state.texto[:2000]}
            """
            
            payload = {
                "inputs": prompt,
                }

            try:

                response = requests.post(
                    API_URL,
                    headers=headers,
                    json=payload
                )

                st.write(response.status_code)

                resultado = response.json()

                if isinstance(resultado, list):

                    texto_generado = (
                        resultado[0]["generated_text"]
                    )

                    st.session_state.apuntes_limpios = (
                        texto_generado
                    )

                else:

                    st.error(resultado)

            except Exception as e:

                st.error(
                    f"Error IA: {e}"
                )

# =========================
# MOSTRAR APUNTES IA
# =========================

if st.session_state.apuntes_limpios != "":

    st.divider()

    st.success(
        "✅ Apuntes organizados"
    )

    st.subheader(
        "📚 Apuntes organizados"
    )

    st.markdown(
        st.session_state.apuntes_limpios
    )

    st.download_button(
        label="⬇️ Descargar apuntes IA",
        data=(
            st.session_state
            .apuntes_limpios
        ),
        file_name="apuntes_ia.txt",
        mime="text/plain"
    )