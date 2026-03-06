
import streamlit as st
import pandas as pd
from datetime import datetime
import os

archivo = "gastos.xlsx"

# Crear archivo si no existe
if not os.path.exists(archivo):
    df = pd.DataFrame(columns=["Fecha","Tipo","Categoria","Monto","Descripcion"])
    df.to_excel(archivo, index=False)

df = pd.read_excel(archivo)

st.title("💰 Gestor Personal de Gastos e Ingresos")

st.subheader("Registrar movimiento")

tipo = st.selectbox("Tipo", ["Gasto", "Ingreso"])

if tipo == "Gasto":
    categoria = st.selectbox("Categoría", [
        "Comida",
        "Transporte",
        "Ropa",
        "Entretenimiento",
        "Salud",
        "Otros"
    ])
else:
    categoria = st.selectbox("Categoría", [
        "Salario",
        "Freelance",
        "Regalo",
        "Otros"
    ])

monto = st.number_input("Monto", min_value=0.0)
descripcion = st.text_input("Descripción")

if st.button("Guardar registro"):

    nuevo = {
        "Fecha": datetime.now(),
        "Tipo": tipo,
        "Categoria": categoria,
        "Monto": monto,
        "Descripcion": descripcion
    }

    df = pd.concat([df, pd.DataFrame([nuevo])], ignore_index=True)
    df.to_excel(archivo, index=False)

    st.success("Registro guardado")

st.divider()

st.subheader("Historial de movimientos")

st.dataframe(df)

st.divider()

# Calculos
gastos = df[df["Tipo"]=="Gasto"]["Monto"].sum()
ingresos = df[df["Tipo"]=="Ingreso"]["Monto"].sum()
balance = ingresos - gastos

col1,col2,col3 = st.columns(3)

col1.metric("Ingresos", ingresos)
col2.metric("Gastos", gastos)
col3.metric("Balance", balance)

st.divider()

st.subheader("Gráfico de gastos por categoría")

gastos_df = df[df["Tipo"]=="Gasto"]

if not gastos_df.empty:
    grafico = gastos_df.groupby("Categoria")["Monto"].sum()
    st.bar_chart(grafico)

st.divider()

st.subheader("Descargar reporte")

st.download_button(
    label="Descargar Excel",
    data=open(archivo,"rb"),
    file_name="reporte_gastos.xlsx"
)

