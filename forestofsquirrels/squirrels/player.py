from .squirrel import Squirrel


class Player(Squirrel):
    """ The player's squirrel.
    """
    def update(self):
        Squirrel.update(self)
        self.forest.camera_x = self.x - 320
        self.forest.camera_y = self.y - 240
