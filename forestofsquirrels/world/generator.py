from .simplexnoise import SimplexNoise


def get_noise(x, y):
    return noise.noise2d(x / 512.0, y / 512.0)


def num_acorns(x, y):
    return int((get_noise(x, y) + 1) * 10)


def set_seed(seed):
    global noise
    noise = SimplexNoise(seed)


def connect(start_area, x, y, side):
    from forestofsquirrels.world.forest import Area
    conn_type = start_area.connections[side]
    if side == "right":
        otherside = "left"
    elif side == "left":
        otherside = "right"
    elif side == "top":
        otherside = "bottom"
    elif side == "bottom":
        otherside = "top"
    else:
        otherside = None
    possibilities = []
    for area_name in Area.area_types:
        if Area.area_types[area_name]["connections"][otherside] == conn_type:
            possibilities.append(area_name)
    for cx, cy, side, otherside in (
            (0, 1, "top", "bottom"), (0, -1, "bottom", "top"), (1, 0, "left", "right"), (-1, 0, "right", "left")):
        if (cx + x, cy + y) in Area.areas:
            conn_type = Area.areas[cx + x, cy + y].connections[side]
            for p in possibilities:
                if Area.area_types[area_name]["connections"][otherside] != conn_type:
                    possibilities.remove(area_name)
    return possibilities[int(get_noise(x, y) + 1 / 2 * len(possibilities))]
