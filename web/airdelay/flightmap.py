import folium

airplane_icon_url = "http://maps.google.com/mapfiles/kml/shapes/airports.png"


folium_map = folium.Map(
    location=[-18.793889, -45.882778],
    tiles="cartodb-voyager",
    zoom_start=6
)

# Lon, Lat order (reversed)
lines = [
    {
        "coordinates": [
            [-18.76451516151428, -45.68159659061569],
            [-23.75964426994324, -50.682590062684206],
        ],
        "dates": ["2017-06-02T00:00:00", "2017-06-02T00:10:00"],
        "color": "red",
    },
    {
        "coordinates": [
            [-18.75964426994324, -45.682590062684206],
            [-23.75964426994324, -50.682590062684206],
        ],
        "dates": ["2017-06-02T00:10:00", "2017-06-02T00:20:00"],
        "color": "red",
    },
    {
        "coordinates": [
            [-18.7575843334198, -45.679505030038506],
            [-23.75964426994324, -50.682590062684206],
        ],
        "dates": ["2017-06-02T00:20:00", "2017-06-02T00:30:00"],
        "color": "red",
        "weight": 15,
    },
    {
        "coordinates": [
            [-18.76337790489197, -45.678040905014065],
            [-23.75964426994324, -50.682590062684206],
        ],
        "dates": ["2017-06-02T00:30:00", "2017-06-02T00:40:00"],
        "color": "red",
    },
]

features = [
    {
        "type": "Feature",
        "geometry": {
            "type": "Point",
            "coordinates": list(reversed(line["coordinates"][0])),
        },
        "properties": {
            "time": line["dates"][0],
            "icon": "marker",
            "iconstyle": {
                "iconUrl": airplane_icon_url,
                "iconSize": [20, 20],
            },
        },
    }
    for line in lines
]

folium.plugins.TimestampedGeoJson(
    {"type": "FeatureCollection", "features": features},
    period="PT1M",
    duration="PT9M",
    add_last_point=False,
    auto_play=False,
    # , loop_button=True
    # , time_slider_drag_update=True
).add_to(folium_map)
