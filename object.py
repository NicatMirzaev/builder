import os
import pygame
import math
class Object:
    def __init__(self, id, objectname, x, y, rotation):
        self.object = objectname
        self.id = id
        self.x = x
        self.y = y
        self.clicked = False
        self.rotation = rotation
        self.object_image = pygame.image.load(os.path.join("Assets", "Objects/{}".format(objectname)))
        self.panel_image = pygame.image.load(os.path.join("Assets", "Game/panel.png"))
        self.delete_image = pygame.image.load(os.path.join("Assets", "Game/delete.png"))
        self.rotate_image = pygame.image.load(os.path.join("Assets", "Game/rotate.png"))

    def draw(self, win):
        rotate = pygame.transform.rotate(self.object_image, int(self.rotation))
        win.blit(rotate, (self.x, self.y))
        if self.clicked == True:
            win.blit(self.panel_image, (self.x + 7, self.y - 30))
            win.blit(self.delete_image, (self.x + 7, self.y - 25))
            win.blit(self.rotate_image, (self.x + 35, self.y - 25))



    def click(self, x, y):
        clickid = -1
        if x >= self.x and x <= self.x + 64 and y >= self.y and y <= self.y + 64:
            clickid = 0
        elif x >= self.x + 7 and x <= self.x + 27 and y >= self.y - 25 and y <= self.y + 20:
            clickid = 1
        elif x >= self.x + 35 and x <= self.x + 55 and y >= self.y - 25 and y <= self.y + 20:
            clickid = 2
        return clickid

    def rotate(self, pos):
        angle = (180 / math.pi) * math.atan2(pos[0] - self.x, pos[1] - self.y)
        self.rotation = angle


