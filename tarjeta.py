import streamlit as st
import pandas as pd
import requests
from io import StringIO

def leer_csv_desde_url(url, sep=',', encoding='utf-8'):
    try:
        response = requests.get(url)
        response.raise_for_status() # Lanza una excepción para códigos de estado HTTP 4xx/5xx
        content = response.content.decode(encoding)
        csv_data = StringIO(content)
        df = pd.read_csv(csv_data, sep=sep)
        return df

    except requests.exceptions.RequestException as e:
        raise Exception(f"Error de red o al acceder a la URL: {e}")
    except pd.errors.EmptyDataError:
        raise Exception("Error: El archivo CSV está vacío o solo contiene encabezados.")
    except pd.errors.ParserError as e:
        raise Exception(f"Error de análisis CSV. Revisa el delimitador (sep) o el formato del archivo: {e}")
    except Exception as e:
        raise Exception(f"Ocurrió un error inesperado: {e}")
    
# Cargar datos
url = "https://drive.google.com/uc?export=download&id=1UyX7sRATSNbadNxUZ7AAmbeOUm7sVpGF"
df = leer_csv_desde_url(url)

#st.write(df)

# Extraer terremoto mayor magnitud
max_mag = df.loc[df['Magnitude'].idxmax()]
#st.write(max_mag)
# Extraer terremoto mayor muertes
max_death = df.loc[df['Death'].idxmax()]
# Extraer terremoto mayor daño
max_damage = df.loc[df['Damage'].idxmax()]

# Configurar Streamlit
st.set_page_config(page_title="Dashboard Terremotos", layout="wide")

st.title("♿ Dashboard Terremotos")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        label=f"Mayor Magnitud año: {int(max_mag['Year'])}",
        value=max_mag['Magnitude'],
        delta=max_mag['Location_Name']
    )

with col2:
    st.metric(
        label=f"Mayor Daño año: {int(max_damage['Year'])}",
        value=max_damage['Damage'],
        delta=f"-{max_damage['Location_Name']}"
    )

with col3:
    st.metric(
        label=f"Mayor Muerte año: {int(max_death['Year'])}",
        value=max_death['Death'],
        delta=f"-{max_death['Location_Name']}"
    )
    
