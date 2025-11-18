import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import streamlit as st
import requests
import pandas as pd
import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt
import random
import io
import time
from datetime import datetime
from io import BytesIO
from db import guardar_transaccion, obtener_historial
from streamlit_autorefresh import st_autorefresh
import plotly.express as px
import plotly.graph_objects as go
import pytz






# 🧭 Configuración de página
st.set_page_config(page_title="BBVA - Detección de Fraudes", layout="wide")


st.markdown("""
    <style>
        /* Elimina espacio superior del dashboard */
        .block-container {
            padding-top: 0rem !important;
            padding-bottom: 0rem !important;
        }
    </style>
""", unsafe_allow_html=True)


st.markdown("""
    <style>
        /* Oculta la barra superior (Deploy y menú) */
        [data-testid="stDecoration"] {
            display: none;
        }

        /* Opcional: elimina espacio superior extra */
        header {
            visibility: hidden;
        }
    </style>
""", unsafe_allow_html=True)




# 🎨 Estilo institucional BBVA
st.markdown("""
    <style>
        .stApp { background-color: #F2F2F2 !important; }
        html, body, [class*="css"] { color: #0033A0 !important; }
        h1, h2, h3, h4, h5, h6, .stMarkdown, .stText, .stSubheader, .stHeader {
            color: #0000FF !important;
        }
        div.stButton > button {
            background-color: #0033A0;
            color: white !important;
            font-weight: bold;
            font-size: 16px;
            border-radius: 12px;
            padding: 10px 24px;
            transition: transform 0.2s ease, box-shadow 0.2s ease;
        }
        div.stButton > button:hover {
            transform: scale(1.05);
            box-shadow: 0 4px 12px rgba(0, 51, 160, 0.3);
        }
        .stDataFrame th, .stDataFrame td { color: #FFFFFF !important; }
        input, select, textarea { color: #FFFFFF !important; }
        .stAlert { background-color: white !important; color: #FFFFFF !important; }
        .plot-container .main-svg text { fill: #FFFFFF !important; }
    </style>
""", unsafe_allow_html=True)

# 🛡️ Usuarios válidos
USUARIOS = {
    "dulce": "dulce123",
    "nat": "nat123",
    "luis": "luis123",
    "edwin": "edwin123"
}

# 🔐 Estado de sesión
if "autenticado" not in st.session_state:
    st.session_state.autenticado = False

   



if not st.session_state.autenticado:
    # 🎨 Estilo BBVA aplicado directamente a los campos
    st.markdown("""
        <style>
            .input-container {
                max-width: 90px;
                margin: auto;
            }
            input[type="text"], input[type="password"] {
                background-color: #062C5F !important;
                color: white !important;
                border: none !important;
                border-radius: 8px !important;
                padding: 10px !important;
                font-size: 15px !important;
                text-align: center !important;
                width: 100% !important;
            }
            label {
                color: #0033A0 !important;
                font-size: 14px !important;
            }
        </style>
    """, unsafe_allow_html=True)

    # 🧑‍💼 Encabezado de acceso
    st.markdown("""
        <div style='
            background-color: #F2F2F2;
            padding: 10px;
            border-radius: 16px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.1);
            text-align: center;
        '>
            <h2 style='color: #062C5F; font-size: 50px;'>¡BIENVENIDO!</h2>
            <p style='color: #0033A0; font-size: 15px;'>🔒 Navegas en un entorno confiable, respaldado por la seguridad de BBVA</p>
        </div>
    """, unsafe_allow_html=True)

    "\n"
    "\n"
    # ✅ Centrado con columnas
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        usuario = st.text_input("Usuario", value="", key="usuario")
        contraseña = st.text_input("Contraseña", value="", type="password", key="contraseña")

        # 🔘 Botón de ingreso
        if st.button("Acceso"):
            if usuario in USUARIOS and USUARIOS[usuario] == contraseña:
                st.session_state.autenticado = True
                st.success("✅ Acceso concedido")
                st.rerun()
            else:
                st.error("❌ Usuario o contraseña incorrectos")




    # 🛡️ Cuadro antifraude debajo del botón
    st.markdown("""
        <div style='
            background-color: #F2F2F2;
            padding: 20px;
            border-radius: 12px;
            margin-top: 20px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.1);
            text-align: center;
            '>
            <h4 style='color: #0033A0;'>🔍 Los engaños pueden venir de cualquier lugar</h4>
            <p style='color: #0033A0; font-size: 14px;'>
                Recuerda que un intento de fraude puede llegar desde cualquier medio: llamadas, SMS, correos, redes sociales o incluso en persona.<br>
                Identifica cuándo realmente es BBVA quien te contacta.
            </p>
            </div>
        """, unsafe_allow_html=True)

    st.stop()    

  





if st.session_state.autenticado:
    # 🔙 Botón de salida ejecutiva BBVA alineado a la derecha
    col1, col2 = st.columns([5, 1])  # col2 es más angosta y está a la derecha
    with col2:
        if st.button("🔙 Salir"):
            st.session_state.autenticado = False
            st.rerun()





"\n"
"\n"
from datetime import datetime



# 🎨 Estilo personalizado para scrollbar
st.markdown("""
<style>
::-webkit-scrollbar {
    width: 12px;
}
::-webkit-scrollbar-track {
    background: #e0e0e0;
    border-radius: 6px;
}
::-webkit-scrollbar-thumb {
    background-color: #003366;
    border-radius: 6px;
    border: 2px solid #e0e0e0;
}
::-webkit-scrollbar-horizontal {
    height: 12px;
}
::-webkit-scrollbar-thumb:horizontal {
    background-color: #003366;
    border-radius: 6px;
    border: 2px solid #e0e0e0;
}
</style>
""", unsafe_allow_html=True)

# 🔄 Refrescar cada segundo
st_autorefresh(interval=1000, limit=None, key="reloj_mx")

# 🕒 Obtener hora local de Ciudad de México
zona_mexico = pytz.timezone("America/Mexico_City")
ahora_local = datetime.now(zona_mexico)
fecha_hora = ahora_local.strftime("%d/%m/%Y %H:%M:%S")

# 🧩 Encabezado institucional
st.markdown(f"""
    <div style='
        background-color: white;
        padding: 12px 24px;
        border-radius: 16px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        display: flex;
        justify-content: space-between;
        align-items: center;
        font-family: Arial, sans-serif;
        margin-bottom: 20px;
    '>
        <div style='font-weight: bold; font-size: 25px; color: #0033A0;'>BBVA</div>
        <h2 style='color: #062C5F; font-size: 30px;'>DETECCIÓN DE FRAUDES</h2>    
        <div style='font-size: 25px; color: #0033A0;'>{fecha_hora}</div>
    </div>
""", unsafe_allow_html=True)







# 🔍 Función para consultar la API
def formato_moneda(valor):
    try:
        return f"${valor:,.2f}"
    except:
        return valor

def calcular_umbral(perfil):
    return {"estándar": 0.7, "medio": 0.5, "alto": 0.3}.get(perfil, 0.6)

def modelo_predictivo(transaccion):
    riesgo = 0.0
    if transaccion["canal"] == "SPEI":
        riesgo += 0.3
    elif transaccion["canal"] == "CoDi":
        riesgo += 0.2
    elif transaccion["canal"] == "efectivo":
        riesgo += 0.1
    elif transaccion["canal"] == "App":
        riesgo += 0.15
    if transaccion["monto"] > 20000:
        riesgo += 0.4
    if transaccion["hora"] < 6 or transaccion["hora"] > 22:
        riesgo += 0.2
    return min(riesgo, 1.0)

def convertir_excel(df):
    output = BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='Historial')
    output.seek(0)
    return output

def mostrar_tabla_centrada_con_conteo(df):
    df = df.copy()

    # Insertar columna de conteo
    df.insert(0, "N°", range(1, len(df) + 1))

    # Convertir todos los valores a texto plano
    df = df.astype(str)

    # Generar HTML con estilos condicionales por fila
    def fila_estilo(row):
        resultado = row["resultado"]
        color = "#ffe6e6" if resultado == "FRAUDE" else "#e6ffe6"
        icono = "❌ FRAUDE" if resultado == "FRAUDE" else "✅ LEGÍTIMA"
        row["resultado"] = icono
        return f'<tr style="background-color:{color}; border-bottom:2px solid #0074D9;">' + \
               ''.join([f"<td>{cell}</td>" for cell in row.values()]) + "</tr>"

    filas_html = "\n".join([fila_estilo(dict(zip(df.columns, row))) for row in df.values])
    columnas_html = "".join([f"<th>{col}</th>" for col in df.columns])

    tabla_html = f"""
    <table>
        <thead><tr>{columnas_html}</tr></thead>
        <tbody>{filas_html}</tbody>
    </table>
    """

    estilo = """
    <style>
        table {
            width: 100%;
            border-collapse: collapse;
            margin-top: 20px;
        }
        th, td {
            text-align: center;
            padding: 8px;
            border: 1px solid #0033A0;
            font-family: Arial, sans-serif;
            font-size: 14px;
        }
        th {
            background-color: #0033A0;
            color: white;
        }
    </style>
    """

    st.markdown(estilo, unsafe_allow_html=True)
    st.markdown(tabla_html, unsafe_allow_html=True)





# ---------------------- DATOS ----------------------

PERFILES_POR_ID = {
    1001: "estándar",
    1002: "medio",
    1003: "alto"
}

if "historial" not in st.session_state:
    st.session_state.historial = []

# ---------------------- INTERFAZ ----------------------





"\n"
"\n"
"\n"
# 🔄 Simulación individual
st.subheader("🔄 Simular transacción en tiempo real")
col1, col2, col3 = st.columns(3)
id_usuario = col1.selectbox("ID del usuario", options=list(PERFILES_POR_ID.keys()))
canal = col2.selectbox("Canal", options=["SPEI", "CoDi", "efectivo", "App"])
monto = col3.number_input("Monto", min_value=1.0, step=100.0)
hora = st.slider("Hora", 0, 23)

if st.button("Evaluar transacción", key="evaluar_individual"):
    perfil = PERFILES_POR_ID.get(id_usuario, "estándar")
    transaccion = {
        "id_usuario": id_usuario,
        "perfil": perfil,
        "canal": canal,
        "monto": monto,
        "hora": hora,
        "fecha": datetime.now()
    }
    riesgo = modelo_predictivo(transaccion)
    transaccion["riesgo"] = riesgo
    transaccion["umbral"] = calcular_umbral(perfil)
    transaccion["resultado"] = "FRAUDE" if riesgo >= transaccion["umbral"] else "LEGÍTIMA"
    st.session_state.historial.append(transaccion)

    color = "red" if transaccion["resultado"] == "FRAUDE" else "green"
    st.markdown(f"<h4 style='color:{color};'>Resultado: {transaccion['resultado']}</h4>", unsafe_allow_html=True)




"\n"
"\n"
"\n"
# 🧪 Simulación masiva
st.subheader("🧪 Simulación masiva de transacciones")

if st.button("Simular 100 transacciones", key="simular_masiva"):
    nuevas_transacciones = []

    for _ in range(100):
        id_usuario = random.choice(list(PERFILES_POR_ID.keys()))
        perfil = PERFILES_POR_ID[id_usuario]
        canal = random.choice(["SPEI", "CoDi", "efectivo", "App"])
        monto = round(random.uniform(100, 60000), 2)
        hora = random.randint(0, 23)

        transaccion = {
            "id_usuario": id_usuario,
            "perfil": perfil,
            "canal": canal,
            "monto": monto,
            "hora": hora,
            "fecha": datetime.now()
        }

        riesgo = modelo_predictivo(transaccion)
        transaccion["riesgo"] = riesgo
        transaccion["umbral"] = calcular_umbral(perfil)
        transaccion["resultado"] = "FRAUDE" if riesgo >= transaccion["umbral"] else "LEGÍTIMA"

        nuevas_transacciones.append(transaccion)

    # ✅ Actualizar el historial una sola vez
    st.session_state.historial.extend(nuevas_transacciones)

    # ✅ Confirmación visual
    st.success("✅ Simulación completada con 100 transacciones")


"\n"
"\n"
"\n"
# 📂 Historial y filtros
st.subheader("📂 Historial de transacciones")
df = pd.DataFrame(st.session_state.historial)

if not df.empty:
    # 🔧 Filtrado por fecha
    df["fecha"] = pd.to_datetime(df["fecha"])
    fecha_inicio = st.date_input("Desde", value=df["fecha"].min().date())
    fecha_fin = st.date_input("Hasta", value=df["fecha"].max().date())
    df_filtrado = df[(df["fecha"].dt.date >= fecha_inicio) & (df["fecha"].dt.date <= fecha_fin)]

    # 🔧 Formateo visual
    df_filtrado["fecha"] = pd.to_datetime(df_filtrado["fecha"]).dt.strftime("%Y-%m-%d %H:%M:%S")
    df_filtrado["monto"] = df_filtrado["monto"].apply(formato_moneda)
    df_filtrado["id_usuario"] = df_filtrado["id_usuario"].astype(str)
    df_filtrado["hora"] = df_filtrado["hora"].astype(str)

    # ✅ Mostrar tabla
    mostrar_tabla_centrada_con_conteo(df_filtrado[["fecha", "id_usuario", "perfil", "canal", "monto", "hora", "resultado"]])

    # 📤 Exportar a Excel
    excel_data = convertir_excel(df_filtrado)
    st.download_button("📥 Descargar historial en Excel", data=excel_data, file_name="historial_fraudes.xlsx")

    # 📈 Proporción de fraudes detectados
    st.subheader("📈 Proporción de fraudes detectados:")
    conteo = df_filtrado["resultado"].value_counts()
    labels = conteo.index.tolist()
    values = conteo.values.tolist()

    fig2 = go.Figure(go.Pie(
        labels=labels,
        values=values,
        hole=0.3,
        pull=[0.02]*len(labels),
        marker=dict(colors=["#0033A0", "aqua"], line=dict(color="#0033A0", width=3)),
        textfont=dict(color="#0033A0", size=14),
        hoverinfo="label+percent+value",
        textinfo="percent"
    ))
    fig2.update_layout(showlegend=False, paper_bgcolor="white", plot_bgcolor="white")
    st.plotly_chart(fig2, use_container_width=True)

    # 🧾 Resumen ejecutivo
    st.markdown("""
        <div style="background-color: white; border: 2px solid #0033A0; border-radius: 10px;
        padding: 20px; box-shadow: 2px 2px 10px rgba(0,0,0,0.1); margin-bottom: 20px;
        color: #0033A0; font-size: 16px; font-family: 'Segoe UI', sans-serif;">
            <strong>Resumen ejecutivo:</strong><br>
            FRAUDE: {fraude}%<br>
            LEGÍTIMA: {legitima}%
        </div>
    """.format(
        fraude=round(values[labels.index("FRAUDE")] * 100 / sum(values), 1) if "FRAUDE" in labels else 0,
        legitima=round(values[labels.index("LEGÍTIMA")] * 100 / sum(values), 1) if "LEGÍTIMA" in labels else 0
    ), unsafe_allow_html=True)

# 📊 Frecuencia de fraudes por hora (fondo negro, números azules, sin "undefined")
st.subheader("📊 Frecuencia de fraudes por hora")

df = pd.DataFrame(st.session_state.historial)

# Filtro seguro
if not df.empty:
    df["fecha"] = pd.to_datetime(df["fecha"])
    col_f1, col_f2 = st.columns(2)
    with col_f1:
        fecha_inicio = st.date_input("Desde", value=df["fecha"].min().date(), key="fecha_inicio")
    with col_f2:
        fecha_fin = st.date_input("Hasta", value=df["fecha"].max().date(), key="fecha_fin")
    df_filtrado = df[(df["fecha"].dt.date >= fecha_inicio) & (df["fecha"].dt.date <= fecha_fin)]
else:
    df_filtrado = pd.DataFrame()

# Graficar si hay datos
if not df_filtrado.empty:
    df_fraudes = df_filtrado[df_filtrado["resultado"] == "FRAUDE"].copy()
    df_fraudes["hora"] = pd.to_numeric(df_fraudes["hora"], errors="coerce")

    conteo_por_hora = df_fraudes["hora"].value_counts().sort_index()
    horas = list(range(24))
    etiquetas_horas = [str(h) for h in horas]
    valores = [int(conteo_por_hora.get(h, 0)) for h in horas]  # Asegura que todos sean enteros

    fig = go.Figure(go.Bar(
        x=etiquetas_horas,
        y=valores,
        text=[str(v) for v in valores],  # Asegura que todos los textos sean strings válidos
        textposition="outside",
        marker=dict(color="#0033A0", line=dict(color="#FFFFFF", width=2)),
        textfont=dict(color="#0033A0", size=14),
        hovertemplate="Hora %{x}<br>Fraudes: %{y}<extra></extra>"
    ))

    fig.update_layout(
        plot_bgcolor="black",
        paper_bgcolor="black",
        font=dict(color="#FFFFFF"),
        margin=dict(l=40, r=40, t=40, b=40),
        xaxis=dict(
            title=dict(text="Hora", font=dict(color="#FFFFFF", size=16)),
            tickmode="array",
            tickvals=etiquetas_horas,
            ticktext=etiquetas_horas,
            linecolor="#FFFFFF",
            gridcolor="#444444",
            tickfont=dict(color="#FFFFFF", size=12),
            showline=True,
            showgrid=True,
            zeroline=False
        ),
        yaxis=dict(
            title=dict(text="Cantidad de fraudes", font=dict(color="#FFFFFF", size=16)),
            linecolor="#FFFFFF",
            gridcolor="#444444",
            tickfont=dict(color="#FFFFFF", size=12),
            showline=True,
            showgrid=True,
            zeroline=False,
            rangemode="nonnegative"
        )
    )

    st.plotly_chart(fig, use_container_width=True)
else:
    st.info("No hay transacciones filtradas para mostrar el gráfico.")
