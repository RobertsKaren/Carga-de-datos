
import streamlit as st
from PIL import Image
import pytesseract
import pandas as pd
import re
import io

st.title("Carga de datos desde imagen - MDS-UPDRS")

uploaded_file = st.file_uploader("Subí la imagen del formulario", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Imagen cargada", use_container_width=True)
    
    st.markdown("---")
    st.write("Procesando...")

    # Procesar la imagen con OCR
    raw_text = pytesseract.image_to_string(image, lang="eng")

    # Extraer los valores usando expresiones regulares simples
    fields = {
        "3.1 Lenguaje": r"3\.1\s+.*?(\d+)",
        "3.2 Expresión facial": r"3\.2\s+.*?(\d+)",
        "3.3a Rigidez - Cuello": r"3\.3a\s+.*?(\d+)",
        "3.3b Rigidez - MSD": r"3\.3b\s+.*?(\d+)",
        "3.3c Rigidez - MSI": r"3\.3c\s+.*?(\d+)",
        "3.18 Persistencia del temblor en reposo": r"3\.18\s+.*?(\d+)",
        "¿Disciensias presentes?": r"¿Disciensias.*?(Sí|No)",
        "¿Estos movimientos interfirieron.*?": r"¿Estos movimientos.*?(Sí|No)",
        "Estadios de Hoehn y Yahr": r"Hoehn y Yahr.*?(\d+)"
    }

    extracted_data = {}
    for label, pattern in fields.items():
        match = re.search(pattern, raw_text, re.IGNORECASE)
        extracted_data[label] = match.group(1) if match else ""

    # Agregar el ID
    extracted_data["ID"] = st.text_input("ID del paciente", value="Paciente 1")

    # Mostrar tabla
    df = pd.DataFrame([extracted_data])
    st.dataframe(df)

    # Permitir descarga como Excel
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine="xlsxwriter") as writer:
        df.to_excel(writer, index=False, sheet_name="Datos")
        writer.close()
    st.download_button("Descargar Excel", data=output.getvalue(), file_name="datos_paciente.xlsx")
