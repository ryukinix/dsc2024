import folium

airplane_icon_url = "http://maps.google.com/mapfiles/kml/shapes/airports.png"


folium_map = folium.Map(
    location=[-18.793889, -45.882778],
    tiles="cartodb-voyager",
    zoom_start=6
)

# Lon, Lat order.
lines = [
    {
        "coordinates": [
            [139.76451516151428, 35.68159659061569],
            [139.75964426994324, 35.682590062684206],
        ],
        "dates": ["2017-06-02T00:00:00", "2017-06-02T00:10:00"],
        "color": "red",
    },
    {
        "coordinates": [
            [139.75964426994324, 35.682590062684206],
            [139.7575843334198, 35.679505030038506],
        ],
        "dates": ["2017-06-02T00:10:00", "2017-06-02T00:20:00"],
        "color": "red",
    },
    {
        "coordinates": [
            [139.7575843334198, 35.679505030038506],
            [139.76337790489197, 35.678040905014065],
        ],
        "dates": ["2017-06-02T00:20:00", "2017-06-02T00:30:00"],
        "color": "red",
        "weight": 15,
    },
    {
        "coordinates": [
            [139.76337790489197, 35.678040905014065],
            [139.76451516151428, 35.68159659061569],
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
            "coordinates": line["coordinates"][0],
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
    auto_play=True,
    # , loop_button=True
    # , time_slider_drag_update=True
).add_to(folium_map)
