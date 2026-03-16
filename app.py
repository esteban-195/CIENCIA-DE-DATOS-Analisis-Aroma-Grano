import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(page_title="BizIntelligence Aroma & Grano", layout="wide")
st.title("📊 BI Dashboard: Aroma & Grano")

# --- CARGA PROFESIONAL ---
@st.cache_data
def cargar_inventario():
    # Usamos low_memory=False para archivos grandes (en este caso es pequeño pero es buena práctica)
    return pd.read_csv("ventas_pro.csv")

df = cargar_inventario()

# --- SONDEO INICIAL (Teoría en acción) ---
st.header("🔍 1. Sondeo de Categorías")
col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Total Productos Únicos", df['producto'].nunique())
    
with col2:
    st.write("Tipos de productos encontrados:")
    st.write(df['tipo'].unique())

with col3:
    st.write("Frecuencia de ventas por producto:")
    st.write(df['producto'].value_counts())


st.text_area("✍️ Tu explicación (Propias palabras, sin IA):", value= """Se cargan los archivos en la funcion  cargar_inventario() y luego se llama la funcion por medio de una variable df.
Segundo, "se col1, col2, col3 = st.columns(3)" mostrar el sondeoen tres columnas y dividir la pantalla en tres partes iguales para mostrar la información de cada una de las columnas.
Tercero, se usa "with" para especificar el contenido de cada columna.
Cuarto, se usa metric para mostrar un numero importante. Se usa "df['producto']" para llamar esa columna del dataframe. Se usa "nunique()" para contar cuantos valores diferentes hay.
Quinto, se usa "unique()" para mostrar los valores diferentes de la columna, en este caso de la columna "tipo".
Sexto, cuenta cuantas veces se repite cada producto usando "value_counts()".
""", height=200)

#------------------------------------------------------------------------------------------

st.divider()
st.header("🛠️ 2. Motor de Limpieza")

# PASO A: Eliminar Duplicados (Vimos el ID 2 y 10 repetidos en el CSV)
df = df.drop_duplicates(subset=['id'])

# PASO B: Corregir Tipos de Datos
# El CSV tiene el ID 12 con cantidad "1" entre comillas (texto). Lo forzamos a número.
df['cantidad'] = pd.to_numeric(df['cantidad'], errors='coerce')

# PASO C: Rellenar Nulos (NaN)
# Si no sabemos la cantidad, asumiremos que se vendió 1 unidad.
df['cantidad'] = df['cantidad'].fillna(1)

st.success("✅ Limpieza automátizada: Duplicados removidos, números corregidos y nulos rellenados.")
st.dataframe(df)
st.text_area("✍️ Tu explicación (Propias palabras, sin IA):",value= """Primero, se usa drop_duplicates() para eliminar filas duplicadas basadas en la columna 'id'.
Segundo, Se usa "to_numeric" para convertir un dato de esa columna a tipo numérico y errors='coerce' para convertir cualquier valor no convertible a NaN.
Tercero, se usa fillna() para rellenar los valores NaN con el valor 1.
""",key="reflexion_paso_3", height=200)

#------------------------------------------------------------------------------------------

st.divider()
st.header("✨ 3. Transformación de Reporte")

# Calculamos el subtotal primero
df['Ingreso_Bruto'] = df['precio'] * df['cantidad']

# CREAMOS UNA VISTA LIMPIA PARA EL REPORTE
# Renombramos y ordenamos de mayor ingreso a menor
reporte_ejecutivo = df.rename(columns={
    'id': 'ID Pedido',
    'producto': 'Producto',
    'Ingreso_Bruto': 'Venta Total ($)'
}).sort_values(by='Venta Total ($)', ascending=False)

st.write("Top de ventas del mes (Ordenado):")
st.dataframe(reporte_ejecutivo[['ID Pedido', 'Producto', 'Venta Total ($)']].head(10))
st.text_area("✍️ Tu explicación (Propias palabras, sin IA):",value=
"""
Primero, se multiplica el precio por la cantidad para obtener el ingreso bruto de cada pedido y se guarda en una nueva columna 'Ingreso_Bruto'.
Segundo, se crea un nuevo DataFrame 'reporte_ejecutivo' renombrando las columnas para que sean más amigables y ordenando las filas segun esa columna usando .sort_values(), ordenando los datos por la columna 'Venta Total ($)' de mayor a menor.
Tercero, se muestra una tabla con los 10 pedidos con mayor venta total.
""", key="reflexion_paso_4", height=200)

#------------------------------------------------------------------------------------------

st.sidebar.header("⚙️ Panel de Auditoría")

# Filtro multi-selección
ciudades_filtro = st.sidebar.multiselect(
    "Filtrar por Tipo:",
    options=df['tipo'].unique(),
    default=df['tipo'].unique()
)

# Filtro Slider
monto_min = st.sidebar.slider("Ver ventas superiores a ($):", 0, 100, 0)

# APLICACIÓN DE LÓGICA FILTRADO (AND)
# Que pertenezca al tipo seleccionado Y supere el monto mínimo
df_final = df[(df['tipo'].isin(ciudades_filtro)) & (df['Ingreso_Bruto'] >= monto_min)]

st.subheader("📋 Pedidos Filtrados")
st.table(df_final)
st.text_area("✍️ Tu explicación (Propias palabras, sin IA):",
value= """
Primero, se filtran los datos por el tipo de producto seleccionado, se usa multiselect() para permitir la selección de múltiples tipos, se usa "options" para definir la lista de valores que el usuario puede seleccionar y obtener todos los tipos diferentes que existen en la columna tipo. "default" indica qué opciones aparecen seleccionadas cuando carga la app.
Segundo, se filtran los datos por el monto mínimo de venta.
Tercero, se muestra una tabla con los pedidos que cumplen ambas condiciones. Se usa isin() para verificar si el valor de la columna 'tipo' está dentro de la lista de tipos seleccionados y se usa el operador & para combinar ambas condiciones.
""", key="reflexion_paso_5", height=200)

#------------------------------------------------------------------------------------------

st.divider()
st.header("📈 4. Análisis Agregado")

# Agrupamos por tipo y sumamos ingresos
resumen = df.groupby('tipo')['Ingreso_Bruto'].agg(['sum', 'count', 'mean']).round(2)
st.write(resumen)

st.bar_chart(resumen['sum'])
st.text_area("✍️ Tu explicación (Propias palabras, sin IA):",value=
"""
Primero, se agrupan los datos por tipo de producto.
Segundo, se calculan las estadísticas agregadas (suma, conteo, promedio) para cada tipo, se usa agg() para aplicar múltiples funciones de agregación a la columna 'Ingreso_Bruto' y se redondean los resultados a 2 decimales.
Tercero, hace un gráfico de barras usando solo la columna "sum." resumen['sum'] selecciona la columna.
""", key="reflexion_paso_6", height=200)

#------------------------------------------------------------------------------------------

# Tabla de ejemplo de proveedores
proveedores = pd.DataFrame({
    'producto': ['Espresso', 'Latte', 'Capuccino', 'Muffin', 'Cold Brew', 'Pastel de Chocolate'],
    'Proveedor': ['Granos del Cauca', 'Lácteos Central', 'Lácteos Central', 'Trigo & Sal', 'Refrescantes S.A.', 'Delicias Doña Ana']
})

# Fusión (Merge)
df_maestro = pd.merge(df, proveedores, on='producto', how='left')

st.header("🏢 Contacto de Proveedores por Pedido")
st.dataframe(df_maestro[['id', 'producto', 'Proveedor']])
st.text_area("✍️ Tu explicación (Propias palabras, sin IA):", value=
"""
Primero, se crea una tabla de ejemplo con información de proveedores.
Segundo, se fusionan los datos del DataFrame principal con la tabla de proveedores usando el método pd.merge(), combinando por la columna 'producto'.
Tercero, se muestra una tabla con los pedidos y la información del proveedor correspondiente.
""", key="reflexion_paso_7", height=200)


