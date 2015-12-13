import math
import random


class SimplexNoise(object):
    grad3 = ((1, 1, 0), (-1, 1, 0), (1, -1, 0), (-1, -1, 0), (1, 0, 1), (-1, 0, 1), (1, 0, -1), (-1, 0, -1), (0, 1, 1),
             (0, -1, 1), (0, 1, -1), (0, -1, -1))
    grad4 = ((0, 1, 1, 1), (0, 1, 1, -1), (0, 1, -1, 1), (0, 1, -1, -1),
             (0, -1, 1, 1), (0, -1, 1, -1), (0, -1, -1, 1), (0, -1, -1, -1),
             (1, 0, 1, 1), (1, 0, 1, -1), (1, 0, -1, 1), (1, 0, -1, -1),
             (-1, 0, 1, 1), (-1, 0, 1, -1), (-1, 0, -1, 1), (-1, 0, -1, -1),
             (1, 1, 0, 1), (1, 1, 0, -1), (1, -1, 0, 1), (1, -1, 0, -1),
             (-1, 1, 0, 1), (-1, 1, 0, -1), (-1, -1, 0, 1), (-1, -1, 0, -1),
             (1, 1, 1, 0), (1, 1, -1, 0), (1, -1, 1, 0), (1, -1, -1, 0),
             (-1, 1, 1, 0), (-1, 1, -1, 0), (-1, -1, 1, 0), (-1, -1, -1, 0))
    F2 = 0.5 * (math.sqrt(3.0) - 1.0)
    G2 = (3.0 - math.sqrt(3.0)) / 6.0
    F3 = 1.0 / 3.0
    G3 = 1.0 / 6.0
    F4 = (math.sqrt(5.0) - 1.0) / 4.0
    G4 = (5.0 - math.sqrt(5.0)) / 20.0

    def __init__(self, seed):
        self.cache = {}
        perm = range(256)
        random.seed(seed)
        random.shuffle(perm)
        self.perm = [0 for x in range(512)]
        self.perm_12 = [0 for x in range(512)]
        for i in range(256):
            self.perm[i] = perm[i]
            self.perm[i + 256] = perm[i]
            self.perm_12[i] = perm[i] % 12
            self.perm_12[i + 256] = perm[i] % 12

    def fastfloor(self, x):
        xi = int(x)
        return xi - 1 if xi > x else xi

    def dot2d(self, g, x, y):
        return g[0] * x + g[1] * y

    def noise2d(self, x, y):
        if (x, y) in self.cache:
            return self.cache[x, y]
        s = (x + y) * self.F2
        i = self.fastfloor(x + s)
        j = self.fastfloor(y + s)
        t = (i + j) * self.G2
        X0 = i - t
        Y0 = j - t
        x0 = x - X0
        y0 = y - Y0
        if x0 > y0:
            i1 = 1
            j1 = 0
        else:
            i1 = 0
            j1 = 1
        x1 = x0 - i1 + self.G2
        y1 = y0 - j1 + self.G2
        x2 = x0 - 1.0 + 2.0 * self.G2
        y2 = y0 - 1.0 + 2.0 * self.G2
        ii = i & 255
        jj = j & 255
        gi0 = self.perm_12[ii + self.perm[jj]]
        gi1 = self.perm_12[ii + i1 + self.perm[jj + j1]]
        gi2 = self.perm_12[ii + 1 + self.perm[jj + 1]]
        t0 = 0.5 - x0 * x0 - y0 * y0
        if t0 < 0:
            n0 = 0.0
        else:
            t0 *= t0
            n0 = t0 * t0 * self.dot2d(self.grad3[gi0], x0, y0)
        t1 = 0.5 - x1 * x1 - y1 * y1
        if t1 < 0:
            n1 = 0.0
        else:
            t1 *= t1
            n1 = t1 * t1 * self.dot2d(self.grad3[gi1], x1, y1)
        t2 = 0.5 - x2 * x2 - y2 * y2
        if t2 < 0:
            n2 = 0.0
        else:
            t2 *= t2
            n2 = t2 * t2 * self.dot2d(self.grad3[gi2], x2, y2)
        val = 70 * (n0 + n1 + n2)
        self.cache[x, y] = val
        return val
