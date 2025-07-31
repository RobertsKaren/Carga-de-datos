
import streamlit as st
from PIL import Image
import pytesseract
import pandas as pd
import io

# Opcional: especificar path a tesseract si es necesario
# pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

st.title("🧠 MDS-UPDRS: Extracción automática de puntuaciones")

uploaded_file = st.file_uploader("📤 Subí la foto escaneada de la hoja", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Imagen cargada", use_container_width=True)

    # Aplicar OCR
    with st.spinner("🔍 Analizando imagen..."):
        text = pytesseract.image_to_string(image)

    st.text_area("📄 Texto detectado (OCR)", text, height=300)

    # Extracción simplificada de puntuaciones (puede refinarse)
    items = [
        "1.1", "1.2", "1.3", "1.4", "1.5", "1.6a", "1.7", "1.8", "1.9", "1.10",
        "1.11", "1.12", "1.13", "1.14", "2.1", "2.2", "2.3", "2.4", "2.5", "2.6",
        "2.7", "2.8", "2.9", "2.10", "2.11", "2.12", "2.13", "3.1", "3.2", "3.3a",
        "3.3b", "3.3c", "3.3d", "3.3e", "3.4a", "3.4b", "3.5a", "3.5b", "3.6a", "3.6b",
        "3.7a", "3.7b", "3.8a", "3.8b", "3.9", "3.10", "3.11", "3.12", "3.13", "3.14",
        "3.15a", "3.15b", "3.16a", "3.16b", "3.17a", "3.17b", "3.17c", "3.17d", "3.17e",
        "3.18", "4.1", "4.2", "4.3", "4.4", "4.5", "4.6"
    ]
    data = []
    for item in items:
        for line in text.splitlines():
            if line.strip().startswith(item):
                parts = line.strip().split()
                try:
                    score = int(parts[-1])
                    description = " ".join(parts[1:-1])
                    data.append({"Ítem": item, "Descripción": description, "Puntuación": score})
                except:
                    continue

    if data:
        df = pd.DataFrame(data)
        st.success("✅ Datos extraídos")
        st.dataframe(df)

        # Generar Excel para descarga
        output = io.BytesIO()
        with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
            df.to_excel(writer, index=False, sheet_name='UPDRS')
            writer.save()
        st.download_button(
            label="📥 Descargar Excel",
            data=output.getvalue(),
            file_name="UPDRS_resultados.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
    else:
        st.warning("No se detectaron puntuaciones. Verificá la calidad de la imagen o refiná el OCR.")
