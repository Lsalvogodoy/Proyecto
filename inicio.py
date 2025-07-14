# Importar librerías
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Configuración de página
st.set_page_config(page_title="SIMCE ", layout="wide")

# Cargar datos 
df = pd.read_csv('simce.csv', encoding='latin1')
df_prom = pd.read_csv('promedio.csv')

# Normalizar nombres
for col in ['region', 'provincia', 'comuna']:
    df[col] = df[col].str.title()

# Limitar regiones a las solicitadas
regiones_permitidas = [
    "Arica Y Parinacota",
    "Antofagasta",
    "Valparaíso",
    "Ñuble",
    "Los Lagos",
    "Metropolitana"    
]    
df = df[df['region'].isin(regiones_permitidas)]

# SIDEBAR 
st.sidebar.title("Dashboard Interactivo\nResultados SIMCE")
st.sidebar.markdown("---")

# Filtros
regiones = sorted(df['region'].unique())
region_sel = st.sidebar.selectbox("Regiones", regiones)

provincias = sorted(df[df['region'] == region_sel]['provincia'].unique())
provincia_sel = st.sidebar.selectbox("Provincias", provincias)

comunas = sorted(df[(df['region'] == region_sel) & (df['provincia'] == provincia_sel)]['comuna'].unique())
comuna_sel = st.sidebar.selectbox("Comunas", comunas)

asignatura_sel = st.sidebar.radio("Asignatura", ["Lenguaje", "Matemáticas"])

st.sidebar.markdown("---")
st.sidebar.write("Exequiel Olivares")
st.sidebar.write("Lucas Salvo")
st.sidebar.write("Cristobal Riquelme")

# PANEL CENTRAL 
st.image("https://otroscruces.org/wp-content/uploads/2019/10/logotipo-UAHC-negro-horizontal-fondo-transparente.png")
st.markdown("<h3 style='text-align:center;'>Introducción a la programación con Python y R</h3>", unsafe_allow_html=True)
st.markdown("")

# Filtrar datos según selección
df_comuna = df[
    (df['region'] == region_sel) &
    (df['provincia'] == provincia_sel) &
    (df['comuna'] == comuna_sel)
].sort_values('agno')

# GRÁFICO 
st.markdown("<h4 style='text-align:center;'>Tendencia de Puntajes por Año (comparado con promedio nacional)</h4>", unsafe_allow_html=True)
if not df_comuna.empty:
    fig, ax = plt.subplots(figsize=(7, 4))
    if asignatura_sel == "Lenguaje":
        ax.plot(df_comuna['agno'], df_comuna['lenguaje'], label=comuna_sel, color='red')
        ax.plot(df_prom['agno'], df_prom['lenguaje'], label='Promedio General', color='skyblue')
        ax.set_ylabel("Lenguaje")
    else:
        ax.plot(df_comuna['agno'], df_comuna['matematicas'], label=comuna_sel, color='red')
        ax.plot(df_prom['agno'], df_prom['matematicas'], label='Promedio General', color='skyblue')
        ax.set_ylabel("Matemáticas")
    ax.set_xlabel("Año")
    ax.legend()
    ax.grid(True, alpha=0.3)
    st.pyplot(fig)
   
else:
    st.info("No hay datos para la selección actual.")


if not df_comuna.empty:
    max_leng = df_comuna['lenguaje'].max()
    min_leng = df_comuna['lenguaje'].min()
    agno_max_leng = df_comuna.loc[df_comuna['lenguaje'].idxmax(), 'agno']
    agno_min_leng = df_comuna.loc[df_comuna['lenguaje'].idxmin(), 'agno']
else:
    max_leng = min_leng = agno_max_leng = agno_min_leng = "N/A"

if not df_comuna.empty:
    max_mat = df_comuna['matematicas'].max()
    min_mat = df_comuna['matematicas'].min()
    agno_max_mat = df_comuna.loc[df_comuna['matematicas'].idxmax(), 'agno']
    agno_min_mat = df_comuna.loc[df_comuna['matematicas'].idxmin(), 'agno']
else:
    max_mat = min_mat = agno_max_mat = agno_min_mat = "N/A"

colt1, colt2 = st.columns(2)
colt1.markdown("<h3 style='text-align: center;'>Lenguaje</h3>", unsafe_allow_html=True)
colt2.markdown("<h3 style='text-align: center;'>Matematicas</h3>", unsafe_allow_html=True)

col1, col2, col3, col4 = st.columns(4)


col1.metric(f"Año: {agno_max_leng}", max_leng, f"Comuna: {comuna_sel}")
col2.metric(f"Año: {agno_min_leng}", min_leng, f"-Comuna: {comuna_sel}")
col3.metric(f"Año: {agno_max_mat}", max_mat, f"Comuna: {comuna_sel}")
col4.metric(f"Año: {agno_min_mat}", min_mat, f"-Comuna: {comuna_sel}")

