import pygame
import time
from config import SCREEN_WIDTH, SCREEN_HEIGHT

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, angle):
        super().__init__()
        self.image = pygame.image.load('assets/bullet.png').convert_alpha()
        self.shot_image = pygame.image.load('assets/shot.png').convert_alpha()
        self.rect = self.image.get_rect(center=(x, y))
        self.pos = pygame.math.Vector2(x, y)
        self.angle = angle
        self.speed = 15
        self.active = True
        self.explosion_time = 0
        self.showing_explosion = False
    
    def move(self):
        if not self.active:
            return

        movement = {
            0: (0, -self.speed),    # Arriba
            90: (-self.speed, 0),   # Izquierda
            180: (0, self.speed),   # Abajo
            270: (self.speed, 0),   # Derecha
        }
        
        dx, dy = movement.get(self.angle, (0, 0))
        self.pos += pygame.math.Vector2(dx, dy)
        self.rect.center = self.pos
        # Verificar si llegó a los bordes
        if (self.pos.x < 0 or self.pos.x > SCREEN_WIDTH or 
            self.pos.y < 0 or self.pos.y > SCREEN_HEIGHT):
            self.explode()
    
    def explode(self):
        self.active = False
        self.explosion_time = time.time()
        self.showing_explosion = True
        self.image = self.shot_image
    
    def update(self):
        if self.active:
            self.move()
            self.image = pygame.transform.rotate(self.image, self.angle)
        elif self.showing_explosion and time.time() - self.explosion_time > 0.25:
            self.kill()  # Eliminar el sprite cuando termina la explosión
