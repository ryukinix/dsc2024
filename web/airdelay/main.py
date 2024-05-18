import datetime
import streamlit as st
import pandas as pd
import numpy as np
from functools import reduce

from streamlit_folium import st_folium

from airdelay import flightmap
from airdelay import datasets

st.title("Airdelay: estimando espera de vôos")

# ## filters
with st.sidebar.form("slider"):
    airports = list(datasets.get_airport_geolocalization().keys())
    destino_select = st.multiselect(
        label="Destino",
        options=airports,
        default=None,
    )
    origem_select = st.multiselect(
        label="Origem",
        options=airports,
        default=None,
    )

    espera_slider = st.slider(
        "Espera em segundos",
        min_value=0,
        value=200,
        max_value=1000,  # FIXME: use real values
    )
    start_date = datetime.date(year=2022, month=5, day=31)
    end_date = start_date.replace(year=start_date.year + 1)
    # FIXME: esta resetando o range apos pressionar run
    date_ranger_slider = st.slider(
        "Selecione um intervalo de vôos",
        min_value=start_date,
        value=(start_date, end_date),
        max_value=end_date,
    )
    max_simultaneous_flights = st.slider(
        "Máximo de vôos simultâneos",
        min_value=1,
        value=3,
        max_value=10,  # FIXME: use real values
    )
    st.form_submit_button(label="Filter")


def filter_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    espera_filter = df.espera > espera_slider
    start_date, end_date = [d for d in date_ranger_slider]
    date_filter = (df.dt_dep.dt.date >= start_date) & (df.dt_dep.dt.date <= end_date)
    origem_filter = df.origem.isin(origem_select)
    destino_filter = df.destino.isin(destino_select)
    filters = [
        espera_filter,
        date_filter
    ]
    if origem_select:
        filters.append(origem_filter)
    if destino_select:
        filters.append(destino_filter)
    compiled_filter = reduce(np.logical_and, filters)
    df_filtered = df[compiled_filter]

    return df_filtered

# ## filters

# # FOLIUM
# center on Liberty Bell, add marker
# m = folium.Map(location=[39.949610, -75.150282], zoom_start=16)
# folium.Marker(
#     [39.949610, -75.150282], popup="Liberty Bell", tooltip="Liberty Bell"
# ).add_to(m)

# # call to render Folium map in Streamlit
df = datasets.get_catboost_regression()
df_filtered = filter_dataframe(df)
flights = df_filtered.drop_duplicates(subset=["origem", "destino"]).head(max_simultaneous_flights)
folium_map = flightmap.create_folium_map(df_filtered.head(max_simultaneous_flights))
st_data = st_folium(folium_map, width=750)
st.write(f"Flights: {len(df_filtered)}")
st.dataframe(filter_dataframe(df))
# # FOLIUM
