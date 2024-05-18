from typing import Tuple, List
from dataclasses import dataclass
from datetime import datetime

import folium
import pandas as pd

from airdelay.mathutils import angle_between
from airdelay.datasets import get_airport_geolocalization
from airdelay import icons


localizations = get_airport_geolocalization()

Coord = Tuple[float, float]

@dataclass
class Point:
    time: str
    coord: Coord
    icon: str = "/app/static/img/airplane-180.png"
    icon_size = [30, 30]


def get_best_icon(origem: str, destino: str) -> str:
    coord_origem = localizations[origem]
    coord_destino = localizations[destino]

    angle = angle_between(coord_origem, coord_destino)
    # print(angle)
    return icons.get_best_icon_based_on_angle(angle)


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


def create_folium_map(df: pd.DataFrame) -> folium.Map:
    brazil_lat_long = [-18.793889, -45.882778]
    folium_map = folium.Map(
        location=brazil_lat_long,
        tiles="cartodb-voyager",
        zoom_start=5
    )

    points: List[Point] = []
    for row in df.itertuples():
        has_delay = row.espera > 240
        flight_trajectory = [
            Point(
                time=datetime.now().replace(hour=n, minute=1, microsecond=0).isoformat(),
                coord=coord,
                icon=icons.get_airplane_rotating_icon() if has_delay and n > 20 else get_best_icon(row.origem, row.destino)
            )
            for n, coord in enumerate(generate_coordinates(row.origem, row.destino))
        ]

        points.extend(flight_trajectory)

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
                    "iconSize": point.icon_size,
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
        loop=False,
        loop_button=False,
    ).add_to(folium_map)
    return folium_map
