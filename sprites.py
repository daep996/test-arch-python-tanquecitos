import pygame
import time
from config import SCREEN_WIDTH, SCREEN_HEIGHT

class Tank(pygame.sprite.Sprite):
    def __init__(self, x, y, sprite_path, player_number=0):
        super().__init__()
        self.image = pygame.image.load(sprite_path).convert_alpha()
        self.original_image = self.image
        self.rect = self.image.get_rect(topleft=(x, y))
        self.pos = pygame.math.Vector2(x, y)
        self.angle = 0
        self.speed = 20
        self.lives = 3
        self.width = 100
        self.height = 100
        self.alive = True
        self.respawn_time = 0
        self.respawn_delay = 3.0  # 3 segundos para reaparecer
        self.player_number = player_number
    
    def move(self, dx=0, dy=0, other_tanks=None):
        new_pos = self.pos + pygame.math.Vector2(dx, dy)
        new_rect = pygame.Rect(new_pos.x, new_pos.y, self.width, self.height)
        
        # Verificar colisiones con los bordes
        if not (0 <= new_pos.x <= SCREEN_WIDTH - self.width and 
                0 <= new_pos.y <= SCREEN_HEIGHT - self.height):
            return False
            
        # Verificar colisiones con otros tanques
        if other_tanks:
            for tank in other_tanks:
                if tank != self and tank.alive and new_rect.colliderect(tank.rect):
                    return False
                    
        # Si no hay colisiones, actualizar posición
        self.pos = new_pos
        self.rect.topleft = self.pos
        return True
    
    def rotate(self, angle):
        self.angle = angle
        self.image = pygame.transform.rotate(self.original_image, self.angle)
        self.rect = self.image.get_rect(center=self.rect.center)
    
    def eliminate(self):
        self.alive = False
        self.respawn_time = time.time()
        
    def update(self):
        if not self.alive:
            current_time = time.time()
            if current_time - self.respawn_time >= self.respawn_delay:
                self.alive = True
                self.lives -= 1
        self.rect.topleft = self.pos
        
    def draw(self, surface):
        if self.alive:
            surface.blit(self.image, self.rect)

class PlayerTank(Tank):
    def __init__(self, x, y, player_number=0):
        sprite_path = f'assets/tank{player_number + 1}.png'  # tank1.png, tank2.png, etc.
        super().__init__(x, y, sprite_path, player_number)
        self.last_shot_time = 0
        self.shot_delay = 0.25
    
    def handle_input(self, keys, current_time, other_tanks=None):
        if not self.alive:
            return False
            
        dx = dy = 0
        if keys[pygame.K_LEFT]:
            self.rotate(90)
            dx -= self.speed
        if keys[pygame.K_RIGHT]:
            self.rotate(270)
            dx += self.speed
        if keys[pygame.K_UP]:
            self.rotate(0)
            dy -= self.speed
        if keys[pygame.K_DOWN]:
            self.rotate(180)
            dy += self.speed
        
        if dx != 0 or dy != 0:
            self.move(dx, dy, other_tanks)
        
        if keys[pygame.K_SPACE]:
            if current_time - self.last_shot_time >= self.shot_delay:
                self.last_shot_time = current_time
                return True
        return False
