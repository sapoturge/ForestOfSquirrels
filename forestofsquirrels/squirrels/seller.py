from .squirrel import Squirrel
import math


class Seller(Squirrel):
    """ Annoying squirrel that says "Hello!" Whenever you get too close to him.
    """
    def update(self):
        Squirrel.update(self)
        for squirrel in self.forest.sprites():
            if isinstance(squirrel, Squirrel) and squirrel != self and math.sqrt(
                                    (self.x - squirrel.x) ** 2 + (self.y - squirrel.y) ** 2) < 150:
                if self.x > squirrel.x:
                    self.image = self.leftimg
                else:
                    self.image = self.rightimg
                self.say("Hello!")
