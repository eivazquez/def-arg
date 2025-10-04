import streamlit as st
import plotly.express as px
import duckdb
import pandas as pd

# --- Configuración de la Página y Conexión a DB ---

st.set_page_config(
    page_title="Dashboard de Defunciones en Argentina",
    page_icon=":bar_chart:",
    layout="wide"
)

#@st.cache_resource
def get_connection():
    """
    Crea y cachea la conexión a DuckDB.
    Streamlit se asegura de que esta función se ejecute solo una vez.
    """
    conn = duckdb.connect(database='def20152021.duckdb', read_only=True)
    return conn

# Obtenemos la conexión (se creará solo la primera vez)
con = get_connection()

# --- Funciones de Carga y Procesamiento de Datos ---

@st.cache_data
def load_data(anio: int) -> pd.DataFrame:
    """
    Carga los datos para un año específico desde DuckDB.
    El decorador @st.cache_data asegura que la consulta a la base de datos
    solo se ejecute si el 'anio' cambia, haciendo la app muy eficiente.
    """
    query = f"""
        SELECT
           d.region, d.jurisdiccion, d.mes_def as mes, d.anio_def, d.sexo_nombre as sexo,
           d.grupo_etario, g.descripcion as grupo_cie10,
           d.cod_causa_muerte_CIE10 as cie10, c.descripcion as descripcion_cie10, d.cantidad
        FROM
            defunciones d
        JOIN
            cie10 c ON c.Id = d.cod_causa_muerte_CIE10
        JOIN
            cie10grupo g ON c.grupo = g.Id
        WHERE
            d.anio_def = {anio}
        ORDER BY
           d.anio_def, d.mes_def;
    """
    df = con.execute(query).fetchdf()
    return df

def metric_month(title, value, month):
    """
    Función auxiliar para mostrar una métrica con un mes asociado.
    """
    return f"""
    <div style="font-size: 1rem;text-align: right; color: rgba(0, 0, 0, 0.6);">{title}</div>
    <div style="font-size: 1.75rem; text-align: right;font-weight: 600;">{value}</div>
    <div style="font-size: 1.1rem; text-align: right;">{month}</div>
    """

def metric_simple(title, value):
    """
    Función auxiliar para mostrar una métrica simple.
    """
    return f"""
    <div style="font-size: 1rem;text-align: right; color: rgba(0, 0, 0, 0.6);">{title}</div>
    <div style="font-size: 1.75rem; text-align: right;font-weight: 600;">{value}</div>
    """

# --- Definición de Constantes ---

MONTHS_MAP = {
    1: "Enero", 2: "Febrero", 3: "Marzo", 4: "Abril", 5: "Mayo", 6: "Junio",
    7: "Julio", 8: "Agosto", 9: "Septiembre", 10: "Octubre", 11: "Noviembre", 12: "Diciembre"
}

# --- Sidebar de Filtros ---

st.sidebar.header("Filtros")

selected_year = st.sidebar.selectbox(
    "Año",
    options=[2022, 2021, 2020],
)

df = load_data(selected_year)

selected_sexo = st.sidebar.multiselect(
    "Sexo",
    options=df["sexo"].unique(),
    default=df["sexo"].unique()
)

# --- Bloque de código mejorado para el filtro Grupo CIE10 ---

st.sidebar.markdown("---") # Separador visual

# 1. Obtenemos la lista de todas las opciones posibles primero
opciones_cie10 = df["grupo_cie10"].unique()

# 2. Creamos el checkbox que actuará como nuestro controlador "Seleccionar Todos"
seleccionar_todo_cie10 = st.sidebar.checkbox(
    "Seleccionar Todos (Grupo CIE10)",
    value=True  # Hacemos que por defecto esté marcado
)

# 3. Creamos una lista vacía para la selección por defecto
default_cie10 = []
# Si el checkbox está marcado, nuestra selección por defecto será la lista completa de opciones
if seleccionar_todo_cie10:
    default_cie10 = opciones_cie10

# 4. Creamos el multiselect, pasándole la lista 'default_cie10' que acabamos de definir
selected_grupos_cie10 = st.sidebar.multiselect(
    "Selecciona Grupo(s) CIE10",
    options=opciones_cie10,
    default=default_cie10
)

# --- Fin del bloque ---

# El filtrado ocurre en cada re-ejecución del script (cada vez que un widget cambia).
df_filtered = df[
    (df["sexo"].isin(selected_sexo)) &
    (df["grupo_cie10"].isin(selected_grupos_cie10))
]


# --- Layout Principal del Dashboard ---

st.title(f":chart_with_upwards_trend: Defunciones en Argentina - Año {selected_year}")
st.markdown("---")

# Métricas Principales (KPIs)
total_defunciones = df_filtered["cantidad"].sum()
promedio_mensual = total_defunciones / 12

def_por_mes = df_filtered.groupby("mes")["cantidad"].sum()

# Asegurarse de que def_por_mes no esté vacío antes de calcular max/min
if not def_por_mes.empty:
    max_mes_val = def_por_mes.max()
    max_mes_idx = def_por_mes.idxmax()
    min_mes_val = def_por_mes.min()
    min_mes_idx = def_por_mes.idxmin()
else:
    max_mes_val, max_mes_idx, min_mes_val, min_mes_idx = 0, 1, 0, 1 # Valores por defecto

col1, col2, col3, col4 = st.columns(4)
with col1:
    st.markdown(metric_simple("Total", f"{total_defunciones:,}"), unsafe_allow_html=True)
with col2:
    st.markdown(metric_simple("Promedio Mensual", f"{promedio_mensual:,.0f}"), unsafe_allow_html=True)
with col3:
   st.markdown(metric_month("Mes con Mayor Cantidad", f"{max_mes_val:,}", MONTHS_MAP[max_mes_idx]), unsafe_allow_html=True)

with col4:
    st.markdown(metric_month("Mes con Menor Cantidad", f"{min_mes_val:,}", MONTHS_MAP[min_mes_idx]), unsafe_allow_html=True)

st.markdown("---")
st.subheader("Análisis de Proporciones por Grupo")

col_pie1, col_pie2 = st.columns(2)
hpie=700
with col_pie1:
    df_pie_etario = df_filtered.groupby('grupo_etario')['cantidad'].sum().reset_index()
    fig_pie_etario = px.pie(
        df_pie_etario,
        names='grupo_etario',
        values='cantidad',
        template="plotly_white"
    )
    fig_pie_etario.update_traces(
        textposition='inside',
        textinfo='percent+label',
        insidetextorientation='radial'
    )
    fig_pie_etario.update_layout(
        title_text='Por Grupo de Edad',
        showlegend=False, height=hpie
    )
    st.plotly_chart(fig_pie_etario, use_container_width=True)

with col_pie2:
    # Agrupamos por grupo_cie10 (lógica Top 10 + Otros)
    df_cie10_grouped = df_filtered.groupby('grupo_cie10')['cantidad'].sum().sort_values(ascending=False).reset_index()

    top_n = 10
    if len(df_cie10_grouped) > top_n:
        df_pie_cie10_top = df_cie10_grouped.head(top_n)
        otros_sum = df_cie10_grouped.tail(-top_n)['cantidad'].sum()
        otros_row = pd.DataFrame([{'grupo_cie10': 'Otros', 'cantidad': otros_sum}])
        df_pie_cie10 = pd.concat([df_pie_cie10_top, otros_row], ignore_index=True)
    else:
        df_pie_cie10 = df_cie10_grouped

    fig_pie_cie10 = px.pie(
        df_pie_cie10,
        names='grupo_cie10',
        values='cantidad',
        template="plotly_white"
    )
    fig_pie_cie10.update_traces(
        textposition='inside',
        textinfo='percent+label',
        insidetextorientation='radial'
    )
    fig_pie_cie10.update_layout(
        title_text='Por Grupo de Causa (Top 10)',
        showlegend=False, height=hpie
    )
    st.plotly_chart(fig_pie_cie10, use_container_width=True)

st.markdown("---")

# Gráfico de Barras
st.subheader("Distribución Mensual")
fig_def_mes = px.bar(
    def_por_mes,
    x=def_por_mes.index.map(MONTHS_MAP),
    y="cantidad",
    text_auto='.2s', # Formato de texto automático
    labels={"cantidad": "Cantidad de Defunciones", "x": "Mes"},
    template="plotly_white",
)

fig_def_mes.update_traces(marker_color="#B83D00", textposition='outside')
fig_def_mes.update_layout(
    plot_bgcolor="rgba(0,0,0,0)",
    xaxis=dict(tickangle=-45), # 'xaxis' es el argumento, y su valor es un diccionario.
)
st.plotly_chart(fig_def_mes, use_container_width=True)




# --- Tabla Dinámica (Pivot Table) ---
st.markdown("---")
st.subheader("Análisis Detallado por grupamiento de CIE10 y Mes")
st.write("La siguiente tabla muestra el total de defunciones para cada grupo de causa, distribuido a lo largo de los meses.")

pivot_table = pd.pivot_table(
    df_filtered,
    index="grupo_cie10",
    columns="mes",
    values="cantidad",
    aggfunc="sum",
    fill_value=0
)

pivot_table = pivot_table.rename(columns=MONTHS_MAP)

pivot_table["Total Anual"] = pivot_table.sum(axis=1)

if total_defunciones > 0:
    pivot_table["%"] = (pivot_table["Total Anual"] / total_defunciones) * 100
else:
    pivot_table["%"] = 0

pivot_table = pivot_table.sort_values(by="Total Anual", ascending=False)

formatter = {
    "%": "{:.2f}%"
}
for col in pivot_table.columns:
    if col != '%':
        formatter[col] = "{:,.0f}"

st.dataframe(pivot_table.style.format(formatter), use_container_width=True)


# --- Tabla Dinámica (Pivot Table) ---
st.markdown("---")
st.write("La siguiente tabla muestra el total de defunciones para cada grupo de causa, distribuido a lo largo de los meses.")
st.subheader("Análisis Detallado por CIE10 y Mes")

pivot_table = pd.pivot_table(
    df_filtered,
    index="descripcion_cie10",
    columns="mes",
    values="cantidad",
    aggfunc="sum",
    fill_value=0
)

pivot_table = pivot_table.rename(columns=MONTHS_MAP)

pivot_table["Total Anual"] = pivot_table.sum(axis=1)

if total_defunciones > 0:
    pivot_table["%"] = (pivot_table["Total Anual"] / total_defunciones) * 100
else:
    pivot_table["%"] = 0

pivot_table = pivot_table.sort_values(by="Total Anual", ascending=False)

formatter = {
    "%": "{:.2f}%"
}
for col in pivot_table.columns:
    if col != '%':
        formatter[col] = "{:,.0f}"

st.dataframe(pivot_table.style.format(formatter), use_container_width=True)
