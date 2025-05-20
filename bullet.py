import pygame
import time
from config import SCREEN_WIDTH, SCREEN_HEIGHT

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, angle):
        super().__init__()
        # Cargar imágenes
        self.bullet_image = pygame.image.load('assets/bullet.png').convert_alpha()
        self.shot_image = pygame.image.load('assets/shot.png').convert_alpha()
        self.image = self.bullet_image
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

        # Definir movimiento según el ángulo
        dx = dy = 0
        if self.angle == 0:    # Arriba
            dy = -self.speed
        elif self.angle == 90:  # Izquierda
            dx = -self.speed
        elif self.angle == 180: # Abajo
            dy = self.speed
        elif self.angle == 270: # Derecha
            dx = self.speed

        # Actualizar posición
        next_pos = self.pos + pygame.math.Vector2(dx, dy)

        # Verificar colisiones con los bordes
        hit_border = False
        if next_pos.x < 0:
            self.pos.x = 0
            hit_border = True
        elif next_pos.x > SCREEN_WIDTH:
            self.pos.x = SCREEN_WIDTH
            hit_border = True
        
        if next_pos.y < 0:
            self.pos.y = 0
            hit_border = True
        elif next_pos.y > SCREEN_HEIGHT:
            self.pos.y = SCREEN_HEIGHT
            hit_border = True

        if hit_border:
            self.explode()
        else:
            self.pos = next_pos
            self.rect.center = self.pos

    def explode(self):
        if self.active:  # Solo explotar si la bala está activa
            self.active = False
            self.showing_explosion = True
            self.explosion_time = time.time()
            self.image = self.shot_image
            # Ajustar el rectángulo para la explosión
            old_center = self.rect.center
            self.rect = self.image.get_rect()
            self.rect.center = old_center
    
    def update(self):
        if self.active:
            self.move()
            # Rotar la imagen de la bala
            rotated = pygame.transform.rotate(self.bullet_image, self.angle)
            old_center = self.rect.center
            self.image = rotated
            self.rect = self.image.get_rect()
            self.rect.center = old_center
        elif self.showing_explosion:
            if time.time() - self.explosion_time > 0.25:  # Duración de la explosión
                self.kill()  # Eliminar después de mostrar la explosión