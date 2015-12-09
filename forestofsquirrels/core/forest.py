import pygame


class Forest(pygame.sprite.LayeredUpdates):
    def __init__(self, camera_x=0, camera_y=0):
        self.camera_x = camera_x
        self.camera_y = camera_y
        self.connections = {}
        pygame.sprite.LayeredUpdates.__init__(self)

    def update(self):
        for s in self.sprites():
            s.update()
        self.camera_x = min(max(self.camera_x, 0), self.width - 640)
        self.camera_y = min(max(self.camera_y, 0), self.height - 480)
        for s in self.sprites():
            s.rect.x -= self.camera_x
            s.rect.y -= self.camera_y

    def draw(self, surface):
        for spr in sorted(self.sprites(), key=lambda s: s.y):
            surface.blit(spr.image, spr.rect)
