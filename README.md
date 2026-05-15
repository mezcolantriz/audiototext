# Transcriptor IA para Clases

Aplicación web local desarrollada con Python y Streamlit para grabar clases, transcribir audio automáticamente mediante Whisper y generar apuntes organizados usando IA.

---

# Características

- Grabación de audio desde el navegador
- Transcripción automática de clases
- Guardado automático de grabaciones y transcripciones
- Historial de transcripciones
- Generación de apuntes organizados con IA
- Descarga de transcripciones y apuntes
- Funcionamiento local para transcripción
- Compatible con español

---

# Tecnologías utilizadas

- Python
- Streamlit
- Faster-Whisper
- Hugging Face Inference API
- Streamlit Mic Recorder

---

# Requisitos

- Python 3.11 recomendado

---

# Instalación

## 1. Clonar repositorio

```bash
git clone https://github.com/tuusuario/transcriptor-ia.git

cd transcriptor-ia
```

---

## 2. Crear entorno virtual

### Windows

```bash
python -m venv venv311
```

---

## 3. Activar entorno virtual

### Windows

```bash
venv311\Scripts\activate
```

---

## 4. Instalar dependencias

```bash
pip install -r requirements.txt
```

---

# Configurar Hugging Face

Crear un archivo `.env` en la raíz del proyecto:

```env
hf_token=TU_TOKEN_DE_HUGGING_FACE
```

Puedes obtener tu token desde:

https://huggingface.co/settings/tokens

---

# Ejecutar aplicación

```bash
streamlit run app.py
```

---

# Estructura del proyecto

```text
transcriptor-ia/
│
├── app.py
├── README.md
├── requirements.txt
├── .env
├── grabaciones/
├── transcripciones/
└── venv311/
```

---

# Funcionamiento

1. Introducir nombre de la clase
2. Grabar audio desde el navegador
3. Transcribir automáticamente
4. Generar apuntes organizados con IA
5. Descargar resultados

---

# Dependencias principales

```txt
streamlit
faster-whisper
streamlit-mic-recorder
python-dotenv
requests
```

---

# Futuras mejoras

- Resúmenes automáticos
- Flashcards
- Preguntas tipo examen
- Explicaciones simplificadas
- Chat con las transcripciones
- Exportación a PDF
- Organización por materias
- Búsqueda semántica

---

# Notas

- La transcripción se realiza localmente mediante Whisper
- La generación de apuntes utiliza modelos de IA externos
- Compatible con CPU
- Compatible con GPU NVIDIA en futuras versiones

---

# Licencia

Proyecto educativo y personal.
