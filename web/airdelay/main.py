from datetime import datetime
import folium
import streamlit as st

from streamlit_folium import st_folium

# ## filters
with st.sidebar.form("slider"):
    start_date = datetime.today()
    end_date = start_date.replace(year=start_date.year - 1)
    # FIXME: esta resetando o range apos pressionar run
    date_ranger_slider = st.slider(
        "Selecione um intervalo de vôos",
        min_value=start_date,
        value=(start_date, end_date),
        max_value=end_date,
    )
    espera_slider = st.slider(
        "Espera em segundos",
        min_value=0,
        value=0,
        max_value=4000,  # FIXME: use real values
    )
    max_simultaneous_flights = st.slider(
        "Máximo de vôos simultâneos",
        min_value=0,
        value=3,
        max_value=10,  # FIXME: use real values
    )
    airports = ["SBSP", "SBMG"]
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
    st.form_submit_button(label="Run")
# ## filters

# # FOLIUM
# center on Liberty Bell, add marker
m = folium.Map(location=[39.949610, -75.150282], zoom_start=16)
folium.Marker(
    [39.949610, -75.150282], popup="Liberty Bell", tooltip="Liberty Bell"
).add_to(m)

# call to render Folium map in Streamlit
st_data = st_folium(m, width=750)
# # FOLIUM
