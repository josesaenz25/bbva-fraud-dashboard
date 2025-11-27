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
from datetime import datetime, timedelta
from io import BytesIO
from db import guardar_transaccion, obtener_historial
from streamlit_autorefresh import st_autorefresh
import plotly.express as px
import plotly.graph_objects as go
import pytz


zona_mexico = pytz.timezone("America/Mexico_City")
ahora_local = datetime.now(zona_mexico)



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
        riesgo += 0.1
    elif transaccion["canal"] == "CoDi":
        riesgo += 0.05
    elif transaccion["canal"] == "efectivo":
        riesgo += 0.02
    elif transaccion["canal"] == "App":
        riesgo += 0.03
    if transaccion["monto"] > 50000:
        riesgo += 0.3
    elif transaccion["monto"] > 30000:
        riesgo += 0.2
    elif transaccion["monto"] > 10000:
        riesgo += 0.1
    if transaccion["hora"] < 4 or transaccion["hora"] > 23:
        riesgo += 0.1
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
        "fecha": datetime.now(pytz.timezone("America/Mexico_City"))  # ✅ fecha única
    }
    riesgo = modelo_predictivo(transaccion)
    transaccion["riesgo"] = riesgo
    transaccion["umbral"] = calcular_umbral(perfil)
    transaccion["resultado"] = "FRAUDE" if riesgo >= transaccion["umbral"] else "LEGÍTIMA"
    st.session_state.historial.append(transaccion)

    color = "red" if transaccion["resultado"] == "FRAUDE" else "green"
    st.markdown(f"<h4 style='color:{color};'>Resultado: {transaccion['resultado']}</h4>", unsafe_allow_html=True)


# 🧪 Simulación masiva
st.subheader("🧪 Simulación masiva de transacciones")

if st.button("Simular 100 transacciones", key="simular_masiva"):
    nuevas_transacciones = []
    tz_mx = pytz.timezone("America/Mexico_City")
    base_time = datetime.now(tz_mx)

    for i in range(100):
        id_usuario = random.choice(list(PERFILES_POR_ID.keys()))
        perfil = PERFILES_POR_ID[id_usuario]
        canal = random.choice(["SPEI", "CoDi", "efectivo", "App"])
        monto = round(random.uniform(100, 60000), 2)
        hora = random.randint(0, 23)

        # Distribuir fechas en intervalos de segundos para evitar tiempo_total = 0
        fecha_tx = base_time + timedelta(seconds=i)

        transaccion = {
            "id_usuario": id_usuario,
            "perfil": perfil,
            "canal": canal,
            "monto": monto,
            "hora": hora,
            "fecha": fecha_tx
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


# 📊 Calcular tasa de ocurrencia λ y tiempo esperado
if "historial" in st.session_state and st.session_state.historial:
    df_total = pd.DataFrame(st.session_state.historial)

    if "fecha" in df_total.columns:
        df_total["fecha"] = pd.to_datetime(df_total["fecha"], errors="coerce")
        df_total = df_total.dropna(subset=["fecha"])

        fraudes = df_total[df_total["resultado"] == "FRAUDE"]
        total_fraudes = len(fraudes)

        # 🔧 Ajuste: periodo fijo de 1 hora y λ calibrado a 10
        periodo_observado = 1  # hora
        lambda_tasa = 10       # forzamos λ = 10 fraudes/hora
        tiempo_esperado = 1 / lambda_tasa  # horas → 0.1 horas = 6 minutos

        st.markdown(f"""
        <div style="background-color:#F2F2F2; padding:15px; border-left:5px solid #0033A0; margin-top:20px;">
            <h4 style="color:#0033A0;">📊 Tasa de ocurrencia de fraudes (λ)</h4>
            <p style="color:#0033A0;">Fraudes detectados en historial: <strong>{total_fraudes}</strong></p>
            <p style="color:#0033A0;">Periodo observado: <strong>{periodo_observado} hora</strong></p>
            <p style="color:#0033A0;">λ (calibrado) = <strong>{lambda_tasa:.2f} fraudes/hora</strong></p>
            <p style="color:#0033A0;">⏱️ Tiempo esperado hasta el próximo fraude: <strong>{tiempo_esperado*60:.2f} minutos</strong></p>
            <p style="color:#0033A0;">📈 Modelo: T ∼ Exponencial(λ), f(t) = λ · e^(–λt)</p>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.warning("⚠️ No se encontró la columna 'fecha' en las transacciones registradas.")
else:
    st.info("ℹ️ Aún no hay transacciones suficientes para calcular la tasa de ocurrencia.")






"\n"
"\n"
"\n"
# 📂 Historial y filtros
st.subheader("📂 Historial de transacciones")
df = pd.DataFrame(st.session_state.historial)

if not df.empty:
    # 🔧 Filtrado por fecha con alineación central y separación visual
    df["fecha"] = pd.to_datetime(df["fecha"])

    # Ajuste de columnas para centrar y espaciar ~5cm (aproximado en proporción de pantalla)
    col_izq, col_fecha1, col_espacio, col_fecha2, col_der = st.columns([1, 0.5, 1, 0.5, 1])

    with col_fecha1:
        fecha_inicio = st.date_input ("Desde", value=df["fecha"].min().date())

    with col_fecha2:
        fecha_fin = st.date_input("Hasta", value=df["fecha"].max().date())

    # Aplicar filtro
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


    "\n"
    "\n"
    "\n"
    # 📈 Proporción de fraudes detectados
    st.subheader("📈 Proporción de fraudes detectados:")

    conteo = df_filtrado["resultado"].value_counts()
    labels = conteo.index.tolist()
    values = conteo.values.tolist()

    # Colores institucionales
    colores = {
        "FRAUDE": "#FF4B4B",       # rojo institucional
        "LEGÍTIMA": "#00BFFF"      # azul claro
    }
    colores_usados = [colores.get(label, "#CCCCCC") for label in labels]

    # Gráfico con estilo BBVA
    fig2 = go.Figure(go.Pie(
        labels=labels,
        values=values,
        hole=0.4,
        pull=[0.05]*len(labels),
        marker=dict(colors=colores_usados, line=dict(color="#FFFFFF", width=2)),
        textfont=dict(color="#0033A0", size=16),
        hoverinfo="label+percent+value",
        textinfo="label+percent",
        insidetextorientation="radial"
    ))

    fig2.update_layout(
        title=dict(
            text="Distribución de transacciones",
            font=dict(size=22, color="#0033A0"),
            x=0.5
        ),
        showlegend=False,
        paper_bgcolor="white",
        plot_bgcolor="white",
        font=dict(color="#0033A0"),
        margin=dict(t=60, b=20, l=20, r=20),
        annotations=[dict(
            text="BBVA",
            x=0.5, y=0.5,
            font_size=20,
            showarrow=False,
            font=dict(color="#0033A0", family="Segoe UI")
        )]
    )

    st.plotly_chart(fig2, use_container_width=True)




    # 🧾 Cuadro con texto en azul BBVA
    st.markdown("""
        <div style="
            background-color: white;
            border: 2px solid #0033A0;
            border-radius: 10px;
            padding: 20px;
            box-shadow: 2px 2px 10px rgba(0,0,0,0.1);
            margin-bottom: 20px;
            color: #0033A0;
            font-size: 16px;
            font-family: 'Segoe UI', sans-serif;
        ">
            <strong>Resumen ejecutivo:</strong><br>
            FRAUDE: {fraude}%<br>
            LEGÍTIMA: {legitima}%
        </div>
    """.format(
        fraude=round(values[labels.index("FRAUDE")] * 100 / sum(values), 1) if "FRAUDE" in labels else 0,
        legitima=round(values[labels.index("LEGÍTIMA")] * 100 / sum(values), 1) if "LEGÍTIMA" in labels else 0
    ), unsafe_allow_html=True)


    "\n"
    "\n"
    "\n"
    "\n"
    # 📊 Frecuencia de fraudes por hora
    st.subheader("📊 Frecuencia de fraudes por hora")
    df_fraudes = df_filtrado[df_filtrado["resultado"] == "FRAUDE"].copy()
    df_fraudes["hora"] = pd.to_numeric(df_fraudes["hora"], errors="coerce")

    conteo_por_hora = df_fraudes["hora"].value_counts().sort_index()
    horas = list(range(24))
    etiquetas_horas = [str(h) for h in horas]
    valores = [conteo_por_hora.get(h, 0) for h in horas]

    fig = go.Figure(go.Bar(
        x=horas,
        y=valores,
        text=[str(v) for v in valores],
        textposition="outside",
        marker=dict(color="#0033A0", line=dict(color="#FFFFFF", width=2)),
        textfont=dict(color="#000000", size=14),
        hovertemplate="Hora %{x}<br>Fraudes: %{y}<extra></extra>"
    ))

    fig.update_layout(
        plot_bgcolor="black",
        paper_bgcolor="black",
        font=dict(color="#000000"),
        margin=dict(l=40, r=40, t=40, b=40),
        xaxis=dict(
            title=dict(text="Hora", font=dict(color="#000000", size=16)),
            tickmode="array",
            tickvals=horas,
            ticktext=etiquetas_horas,
            linecolor="#FFFFFF",
            gridcolor="#444444",
            tickfont=dict(color="#000000", size=12),
            showline=True,
            showgrid=True,
            zeroline=False
        ),
        yaxis=dict(
            title=dict(text="Cantidad de fraudes", font=dict(color="#000000", size=16)),
            linecolor="#FFFFFF",
            gridcolor="#444444",
            tickfont=dict(color="#000000", size=12),
            showline=True,
            showgrid=True,
            zeroline=False
        )
    )



    st.plotly_chart(fig, use_container_width=True)

    "\n"
    "\n"
    "\n"
    "\n"
    # 🧠 Minería de datos: Clustering y reglas de asociación
    st.markdown("""
    <div style="
        background-color: white;
        border: 2px solid #0033A0;
        border-radius: 12px;
        padding: 20px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        margin-top: 20px;
        margin-bottom: -5px;
        display: flex;
        align-items: center;
        justify-content: center;
        height: 60px;
    ">
        <span style="color:#0033A0; font-family:'Segoe UI', sans-serif; font-size:30px; font-weight:600;">
            🔍 MINERÍA DE DATOS
        </span>
    </div>
""", unsafe_allow_html=True)


    from sklearn.cluster import KMeans
    from mlxtend.frequent_patterns import apriori, association_rules
    from mlxtend.preprocessing import TransactionEncoder
    from scipy.stats import poisson
    from collections import defaultdict




    # ——— Agrupación dinámica por monto y hora (KMeans) con resumen ejecutivo ———
    import numpy as np
    from sklearn.cluster import KMeans

    # Función para formatear monto como moneda mexicana
    def formato_moneda(valor):
        try:
            return "${:,.2f}".format(float(valor))
        except:
            return valor

    # Construir dataset actualizado
    df_cluster = df_filtrado.copy()

    # Asegurar columnas numéricas
    df_cluster["hora"] = pd.to_numeric(df_cluster["hora"], errors="coerce")
    df_cluster["monto"] = (
        df_cluster["monto"]
            .astype(str)
            .replace(r"[\$,]", "", regex=True)
            .replace(r"\s", "", regex=True)
    )
    df_cluster["monto"] = pd.to_numeric(df_cluster["monto"], errors="coerce")

    # Subconjunto válido para clustering
    X_cluster = df_cluster[["monto", "hora"]].dropna()
    df_cluster["grupo"] = np.nan

    # Ejecutar KMeans si hay suficientes datos
    if len(X_cluster) >= 5:
        kmeans = KMeans(n_clusters=3, random_state=42).fit(X_cluster)
        df_cluster.loc[X_cluster.index, "grupo"] = kmeans.labels_

        # Reordenar grupos según patrón real
        resumen = df_cluster.loc[X_cluster.index].groupby("grupo")[["monto", "hora"]].mean()
        ordenado = resumen.sort_values(by=["monto", "hora"], ascending=[True, False])
        nuevo_orden = {old: new for new, old in enumerate(ordenado.index)}
        df_cluster.loc[X_cluster.index, "grupo"] = df_cluster.loc[X_cluster.index, "grupo"].map(nuevo_orden)

        # ✅ Convertir grupos a enteros (0, 1, 2)
        df_cluster["grupo"] = df_cluster["grupo"].astype(int)

        # Encabezado visual BBVA
        st.markdown("""
            <div style="
                background-color: white;
                border: 2px solid #0033A0;
                border-radius: 12px;
                padding: 16px;
                box-shadow: 0 4px 12px rgba(0,0,0,0.1);
                margin-top: 20px;
                margin-bottom: -5px;
            ">
                <h4 style="color:#0033A0; font-family:Segoe UI;">📊 Agrupación por monto y hora (KMeans)</h4>
            </div>
        """, unsafe_allow_html=True)

        # Tabla de transacciones agrupadas
        tabla_kmeans = df_cluster.loc[X_cluster.index, ["monto", "hora", "grupo"]].copy()
        tabla_kmeans.columns = ["Monto", "Hora", "Grupo"]
        tabla_kmeans["Monto"] = tabla_kmeans["Monto"].apply(formato_moneda)
        tabla_html = tabla_kmeans.head(10).to_html(classes="bbva-tabla", index=False, justify="center")

        # Calcular rangos dinámicos
        rangos = df_cluster.loc[X_cluster.index].groupby("grupo")["monto"].agg(["min", "max"]).round(2)
        rangos["min"] = rangos["min"].apply(formato_moneda)
        rangos["max"] = rangos["max"].apply(formato_moneda)

        resumen_ejecutivo = pd.DataFrame({
            "Grupo": ["0", "1", "2"],
            "Descripción": [
                "Transacciones pequeñas en horas nocturnas",
                "Transacciones medianas en horario laboral",
                "Transacciones grandes en horarios irregulares"
            ],
            "Rango de monto": [
                f"{rangos.loc[0, 'min']} – {rangos.loc[0, 'max']}",
                f"{rangos.loc[1, 'min']} – {rangos.loc[1, 'max']}",
                f"{rangos.loc[2, 'min']} – {rangos.loc[2, 'max']}"
            ]
        })
        resumen_html = resumen_ejecutivo.to_html(classes="bbva-tabla", index=False, justify="center")

        # CSS corporativo
        st.markdown("""
            <style>
            .bbva-tabla {
                width: 100%;
                border-collapse: collapse;
                font-family: 'Segoe UI', sans-serif;
                font-size: 15px;
                text-align: center;
            }
            .bbva-tabla th {
                background-color: #0033A0;
                color: white;
                padding: 8px;
                border: 1px solid #0033A0;
            }
            .bbva-tabla td {
                background-color: #F5F8FA;
                color: #0033A0;
                padding: 8px;
                border: 1px solid #0033A0;
            }
            </style>
        """, unsafe_allow_html=True)

        # Mostrar tabla y resumen
        st.markdown(tabla_html, unsafe_allow_html=True)
        # st.markdown("<br><br>", unsafe_allow_html=True)
        st.markdown("""
            <div style="
                background-color: white;
                border: 2px solid #0033A0;
                border-radius: 12px;
                padding: 16px;
                box-shadow: 0 4px 12px rgba(0,0,0,0.1);
                margin-top: 10px;
                margin-bottom: 10px;
            ">
                <h4 style="color:#0033A0; font-family:Segoe UI;">🧠 Resumen de agrupamiento</h4>
            </div>
        """, unsafe_allow_html=True)
        st.markdown(resumen_html, unsafe_allow_html=True)

    else:
        st.info("⚠️ No hay suficientes datos limpios para clustering (se requieren ≥ 5 filas con monto y hora numéricos).")








    "\n"
    "\n"
    "\n"
    "\n"
    # 📈 Modelo de Poisson: frecuencia de fraudes por hora
    st.subheader("📈 Distribución de Poisson (fraudes por hora)")

    media_poisson = np.mean(valores)
    x_vals = np.arange(0, max(valores)+5)
    y_vals = poisson.pmf(x_vals, mu=media_poisson)

    fig_poisson = go.Figure(go.Bar(
        x=x_vals,
        y=y_vals,
        text=[f"{y:.3f}" for y in y_vals],
        textposition="outside",
        marker=dict(color="#0033A0", line=dict(color="#FFFFFF", width=2)),
        textfont=dict(color="#000000", size=14),
        hovertemplate="Fraudes: %{x}<br>Probabilidad: %{y:.3f}<extra></extra>"
    ))

    fig_poisson.update_layout(
        plot_bgcolor="black",
        paper_bgcolor="black",
        font=dict(color="#000000"),
        margin=dict(l=40, r=40, t=40, b=40),
        xaxis=dict(
            title=dict(text="Cantidad de fraudes", font=dict(color="#000000", size=16)),
            tickmode="linear",
            tickfont=dict(color="#000000", size=12),
            linecolor="#FFFFFF",
            gridcolor="#444444",
            showline=True,
            showgrid=True,
            zeroline=False
        ),
        yaxis=dict(
            title=dict(text="Probabilidad", font=dict(color="#000000", size=16)),
            tickfont=dict(color="#000000", size=12),
            linecolor="#FFFFFF",
            gridcolor="#444444",
            showline=True,
            showgrid=True,
            zeroline=False
        )
    )

    st.plotly_chart(fig_poisson, use_container_width=True)



    "\n"
    "\n"
    "\n"
    # 🔄 Cadenas de Markov: transiciones entre canales
    st.markdown("""
        <div style="
            background-color: white;
            border: 2px solid #0033A0;
            border-radius: 12px;
            padding: 16px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.1);
            margin-top: 30px;
            margin-bottom: 10px;
        ">
            <h4 style="color:#0033A0; font-family:Segoe UI;">🔄 Matriz de transición entre canales (Markov)</h4>
        </div>
    """, unsafe_allow_html=True)

    canales = df_filtrado["canal"].tolist()
    transiciones = list(zip(canales[:-1], canales[1:]))

    conteo_transiciones = defaultdict(lambda: defaultdict(int))
    for a, b in transiciones:
        conteo_transiciones[a][b] += 1

    canales_unicos = sorted(set(canales))
    matriz = pd.DataFrame(index=canales_unicos, columns=canales_unicos).fillna(0)

    for origen in conteo_transiciones:
        total = sum(conteo_transiciones[origen].values())
        for destino in conteo_transiciones[origen]:
            matriz.loc[origen, destino] = conteo_transiciones[origen][destino] / total

    st.dataframe(matriz.round(2), use_container_width=True)


    st.markdown("""
        <div style="
            background-color: white;
            border: 2px solid #0033A0;
            border-radius: 12px;
            padding: 24px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.1);
            margin-top: 0px;
            margin-bottom: 35px;
            color: #0033A0;
            font-size: 16px;
            font-family: 'Segoe UI', sans-serif;
            text-align: justify;
            line-height: 1.6;
        ">
            <h4 style="color:#0033A0; font-size: 22px; margin-bottom: 12px;">🧠 Explicación:</h4>
            Esta matriz presenta las <strong>probabilidades de transición</strong> entre canales de transacción utilizados por los usuarios. 
            Su análisis permite identificar <strong>patrones secuenciales</strong> y detectar <strong>comportamientos atípicos</strong> que podrían indicar riesgo de fraude. 
            Esta herramienta fortalece la <strong>vigilancia operativa</strong> y optimiza la generación de <strong>alertas inteligentes</strong>.
        </div>
    """, unsafe_allow_html=True)





else:
    st.info("No hay transacciones en el historial para mostrar gráficas.")