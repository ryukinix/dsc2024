from typing import Dict


def get_best_icon_based_on_angle(angle: float) -> str:
    airplane_icons = get_airplane_fixed_icons()
    best_angle = min(airplane_icons.keys(), key=lambda x: abs(angle - x))

    return airplane_icons[best_angle]


def get_airplane_fixed_icons() -> Dict[int, str]:
    return {
        0: "/app/static/img/airplane-0.png",
        135: "/app/static/img/airplane-135.png",
        180: "/app/static/img/airplane-180.png",
        225: "/app/static/img/airplane-225.png",
        270: "/app/static/img/airplane-270.png",
        315: "/app/static/img/airplane-315.png",
        45: "/app/static/img/airplane-45.png",
        90: "/app/static/img/airplane-90.png",
    }


def get_airplane_rotating_icon() -> str:
    return "/app/static/img/airplane-rotating.gif"
