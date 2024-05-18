# airdelay

In this application, we can visualize the delayed flights estimated
previously using machine learning.

Deployed at https://airdelay.manoel.dev/

## How to run:

```
make run
```

This will use docker and there is no way to use development hot-reload
mode. For this, install properly using python with:

```
make install
```

Then,

```
make run-local
```

## Tecnhologies

- [Streamlit]: data applications exported as http server
- [Folium]: manage and visualize geolocalized data
- [Streamlit_folium]: combine streamlit with folium


[Streamlit]: https://docs.streamlit.io/
[Folium]: https://python-visualization.github.io/folium/latest/
[Streamlit_folium]: https://folium.streamlit.app/
