from .simplexnoise import SimplexNoise


def get_noise(x, y):
    return noise.noise2d(x / 512.0, y / 512.0)


def num_acorns(x, y):
    return int((get_noise(x, y) + 1) * 10)


def set_seed(seed):
    global noise
    noise = SimplexNoise(seed)
