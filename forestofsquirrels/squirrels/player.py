from .squirrel import Squirrel


class Player(Squirrel):
    """ The player's squirrel.
    """

    def __init__(self, forest, *args, **kwargs):
        Squirrel.__init__(self, forest, *args, **kwargs)
        self.forest.player = self

    def update(self):
        Squirrel.update(self)
        self.forest.camera_x = self.x - 320
        self.forest.camera_y = self.y - 240
        if self.climbing:
            self.forest.camera_y -= self.z
