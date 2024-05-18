from typing import Tuple, List

from dataclasses import dataclass
import folium
from datetime import datetime
from datasets import get_airport_geolocalization


localizations = get_airport_geolocalization()

Coord = Tuple[float, float]


@dataclass
class Point:
    time: str
    coord: Coord
    icon: str = "/app/static/img/airplane-180.png"


brazil_lat_long = [-18.793889, -45.882778]

folium_map = folium.Map(
    location=brazil_lat_long,
    tiles="cartodb-voyager",
    zoom_start=6
)


def generate_coordinates(origem, destino, n=23) -> List[Coord]:
    coord_origem = localizations[origem]
    coord_destino = localizations[destino]
    origem_lon, origem_lat = coord_origem
    destino_lon, destino_lat = coord_destino

    lon_step = (destino_lon - origem_lon) / n
    lat_step = (destino_lat - origem_lat) / n
    return [
        (origem_lon + k*lon_step, origem_lat + k*lat_step)
        for k in range(n)
    ]

origem = "SBSP"
destino = "SBRJ"

points: List[Point] = [
    Point(
        time=datetime.now().replace(hour=n, minute=1, microsecond=0).isoformat(),
        coord=coord,
    )

    for n, coord in enumerate(generate_coordinates(origem, destino))
]


features = [
    {
        "type": "Feature",
        "geometry": {
            "type": "Point",
            "coordinates": point.coord,
        },
        "properties": {
            "time": point.time,
            "icon": "marker",
            "iconstyle": {
                "iconUrl": point.icon,
                "iconSize": [30, 30],
            },
        },
    }
    for point in points
]


folium.plugins.TimestampedGeoJson(
    {"type": "FeatureCollection", "features": features},
    period="PT1H",
    duration="PT59M",
    add_last_point=False,
    auto_play=False,
    time_slider_drag_update=True,
    loop_button=True,
).add_to(folium_map)
