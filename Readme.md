# Dashboard de Análisis de Defunciones en Argentina (2020-2022)

## 📊 Objetivo del Proyecto

Este proyecto tiene como objetivo desarrollar un **dashboard interactivo** para el análisis exploratorio y visual de las defunciones ocurridas en Argentina durante el período 2020-2022. Permite a los usuarios explorar patrones temporales, distribuciones demográficas y causas de muerte clasificadas según el sistema CIE-10 (Clasificación Internacional de Enfermedades).

### Contexto Académico

Este proyecto fue desarrollado como parte del **Trabajo Práctico del Segundo Módulo** de la materia:
- **Materia:** Programación Avanzada en Ciencia de Datos
- **Institución:** Universidad de la Ciudad de Buenos Aires
- **Autor:** Enrique Ignacio Vazquez

---

## 🎯 Funcionalidades Principales

El dashboard permite:
- ✅ Filtrar datos por año (2020, 2021, 2022)
- ✅ Segmentar por sexo y grupos de causas CIE-10
- ✅ Visualizar métricas clave (total de defunciones, promedios mensuales, meses extremos)
- ✅ Analizar proporciones por grupo etario y causas de muerte
- ✅ Explorar distribución mensual mediante gráficos de barras
- ✅ Consultar tablas dinámicas detalladas por mes y causa

---

## 🔍 Proceso de Análisis Exploratorio (EDA)

El archivo `eda.ipynb` documenta el proceso completo de preparación de datos:

### 1. **Carga y Exploración Inicial**
- Lectura del dataset principal (`arg_def_m_20_22.csv`)
- Análisis de estructura: 760,859 registros con 11 columnas
- Verificación de tipos de datos y valores nulos

### 2. **Validación de Datos**
- **Validación de sexo:** Identificación de 4 categorías (`masculino`, `femenino`, `indeterminado`, `desconocido`)
- **Validación temporal:** Confirmación de meses (1-12) y años (2020-2022) sin inconsistencias
- **Integridad:** No se encontraron valores fuera de rango

### 3. **Limpieza de Datos**
Eliminación de columnas redundantes o sin utilidad:
- `grupo_causa_defuncion_CIE10` (redundante con código CIE-10)
- `mes_anio_defuncion` (información duplicada en columnas separadas)
- `sexo_id` (conservando solo la descripción textual)

### 4. **Enriquecimiento con Datos de Referencia**
Incorporación de dos tablas auxiliares:
- **`Cie10.csv`** (2,024 códigos): Descripción detallada de cada código de causa de muerte
- **`Cie10Grupos.csv`** (21 grupos): Clasificación en capítulos principales del CIE-10

### 5. **Migración a DuckDB**
- Creación de base de datos `def20152021.duckdb`
- Generación de 3 tablas relacionales:
  - `defunciones`: Datos principales con 760,859 registros
  - `cie10`: Catálogo de códigos CIE-10
  - `cie10grupo`: Agrupaciones de capítulos CIE-10
- Verificación de integridad mediante consultas SQL

---

## 🛠️ Tecnologías Utilizadas

### Análisis y Visualización
- **Python 3.13.7**: Lenguaje base del proyecto
- **Streamlit 1.50.0**: Framework para el dashboard interactivo
- **Plotly 6.3.1**: Visualizaciones dinámicas (gráficos de torta, barras)
- **Pandas 2.3.3**: Manipulación y análisis de datos
- **DuckDB 1.4.0**: Base de datos analítica embebida

### Desarrollo
- **Jupyter Notebook**: Documentación del proceso EDA
- **Git/GitHub**: Control de versiones

---

## 📁 Estructura del Proyecto

```
proyecto/
│
├── data/                          # Datos fuente
│   ├── arg_def_m_20_22.csv       # Dataset principal de defunciones
│   ├── Cie10.csv                 # Códigos CIE-10 detallados
│   └── Cie10Grupos.csv           # Agrupaciones CIE-10
│
├── def20152021.duckdb            # Base de datos DuckDB (generada)
│
├── dash.py                        # Aplicación principal del dashboard
├── eda.ipynb                      # Notebook de análisis exploratorio
├── requirements.txt               # Dependencias del proyecto
└── README.md                      # Documentación del proyecto
```

---

## 🚀 Instalación y Configuración

### Requisitos Previos
- Python 3.13.7 o superior
- pip (gestor de paquetes de Python)

### Pasos de Instalación

1. **Clonar el repositorio**
```bash
git clone <URL_DEL_REPOSITORIO>
cd proyecto
```

2. **Crear entorno virtual (recomendado)**
```bash
python -m venv env_dfm
```

3. **Activar el entorno virtual**
- Windows:
```bash
env_dfm\Scripts\activate
```
- Linux/Mac:
```bash
source env_dfm/bin/activate
```

4. **Instalar dependencias**
```bash
pip install -r requirements.txt
```

5. **Preparar la base de datos**
Ejecutar el notebook `eda.ipynb` para generar el archivo `def20152021.duckdb`:
```bash
jupyter notebook eda.ipynb
```
Ejecutar todas las celdas del notebook.

---

## ▶️ Ejecución del Dashboard

Una vez completada la instalación y preparación de datos:

```bash
streamlit run dash.py
```

El dashboard se abrirá automáticamente en tu navegador en `http://localhost:8501`

### Uso del Dashboard

1. **Panel Lateral (Filtros)**:
   - Seleccionar año de análisis (2020, 2021, 2022)
   - Filtrar por sexo (múltiple selección)
   - Seleccionar grupos CIE-10 (con opción "Seleccionar Todos")
   - Seleccionar región o jurisdicción (con opción "Seleccionar Todos")

2. **Panel Principal**:
   - **Métricas KPI**: Total de defunciones, promedio mensual, meses extremos
   - **Gráficos de Torta**: Distribución por grupo etario y causas principales
   - **Gráfico de Barras**: Evolución mensual
   - **Tablas Dinámicas**: Análisis detallado por grupo CIE-10 y por código específico

---

## 📂 Fuente de Datos

### Dataset Principal
- **Título**: Defunciones Mensuales Ocurridas en la República Argentina
- **Período**: 2020-2022
- **Origen**: [Ministerio de Salud de Argentina - Datos Abiertos](http://datos.salud.gob.ar/dataset/datos-salud-gob-ar-dataset-defunciones-mensuales-ocurridas-en-la-republica-argentina)
- **Formato**: CSV
- **Registros**: 760,859 defunciones

### Tablas de Referencia
- **Códigos CIE-10**: Clasificación Internacional de Enfermedades (versión 10)
  - 2,024 códigos individuales
  - 21 grupos principales (capítulos)

### Variables Principales
- **Geográficas**: Región, jurisdicción
- **Temporales**: Mes y año de defunción
- **Demográficas**: Sexo, grupo etario
- **Clínicas**: Código CIE-10, grupo de causa, descripción

---

## 📈 Características Destacadas

- 🔄 **Actualización dinámica**: Los gráficos y métricas se actualizan instantáneamente al cambiar filtros
- 📊 **Visualizaciones interactivas**: Gráficos Plotly con zoom, pan y tooltips
- 🎨 **Diseño responsive**: Se adapta a diferentes tamaños de pantalla
- ⚡ **Alto rendimiento**: Uso de DuckDB para consultas eficientes
- 💾 **Caché inteligente**: Streamlit cachea datos para evitar recargas innecesarias

---

## 📝 Notas Técnicas

- El dashboard utiliza conexión de solo lectura a DuckDB para garantizar la integridad de los datos
- Los gráficos de torta muestran las 10 causas principales más "Otros" para mejorar la legibilidad
- Las tablas dinámicas incluyen porcentajes calculados automáticamente
- Los formatos numéricos utilizan separadores de miles para mejor legibilidad

---

## 👤 Autor

**Enrique Ignacio Vazquez**  
Universidad de la Ciudad de Buenos Aires  
Programación Avanzada en Ciencia de Datos

---

## 📄 Licencia

Este proyecto fue desarrollado con fines académicos. Los datos utilizados son de dominio público, proporcionados por el Ministerio de Salud de Argentina.