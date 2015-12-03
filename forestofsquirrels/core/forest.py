import pygame


class Forest(pygame.sprite.LayeredUpdates):
    def __init__(self, camera_x=0, camera_y=0):
        self.camera_x = camera_x
        self.camera_y = camera_y
        pygame.sprite.LayeredUpdates.__init__(self)

    def update(self):
        for s in self.sprites():
            s.update()
        for s in self.sprites():
            s.rect.x -= self.camera_x
            s.rect.y -= self.camera_y
