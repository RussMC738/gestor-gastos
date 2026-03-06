import streamlit as st
import pandas as pd
from datetime import datetime
import os

archivo = "registro_gastos.xlsx"

st.title("Gestor de Gastos")

tipo = st.selectbox("Tipo", ["Gasto", "Ingreso"])

categoria = st.selectbox(
    "Categoría",
    ["Comida", "Transporte", "Bebida", "Ropa", "Entretenimiento", "Otros"]
)

monto = st.number_input("Monto", min_value=0.0)

if st.button("Guardar"):

    fecha = datetime.now().strftime("%Y-%m-%d")
    hora = datetime.now().strftime("%H:%M")

    nuevo = {
        "Fecha": fecha,
        "Hora": hora,
        "Tipo": tipo,
        "Categoria": categoria,
        "Monto": monto
    }

    if os.path.exists(archivo):
        df = pd.read_excel(archivo)
        df = pd.concat([df, pd.DataFrame([nuevo])], ignore_index=True)
    else:
        df = pd.DataFrame([nuevo])

    df.to_excel(archivo, index=False)

    st.success("Registro guardado")

if os.path.exists(archivo):
    df = pd.read_excel(archivo)
    st.dataframe(df)