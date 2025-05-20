import pygame
from config import SCREEN_WIDTH, SCREEN_HEIGHT

class Tank(pygame.sprite.Sprite):
    def __init__(self, x, y, sprite_path):
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
    
    def move(self, dx=0, dy=0, other_tank=None):
        new_pos = self.pos + pygame.math.Vector2(dx, dy)
        new_rect = pygame.Rect(new_pos.x, new_pos.y, self.width, self.height)
        # Verificar colisiones con los bordes y con el otro tanque
        if (0 <= new_pos.x <= SCREEN_WIDTH - self.width and 
            0 <= new_pos.y <= SCREEN_HEIGHT - self.height and
            (other_tank is None or not new_rect.colliderect(other_tank.rect))):
            self.pos = new_pos
            self.rect.topleft = self.pos
    
    def rotate(self, angle):
        self.angle = angle
        self.image = pygame.transform.rotate(self.original_image, self.angle)
        self.rect = self.image.get_rect(center=self.rect.center)
    
    def update(self):
        self.rect.topleft = self.pos

class PlayerTank(Tank):
    def __init__(self, x, y):
        super().__init__(x, y, 'assets/tank1.png')
        self.last_shot_time = 0
        self.shot_delay = 0.25
    
    def handle_input(self, keys, current_time, other_tank=None):
        dx = dy = 0
        if keys[pygame.K_LEFT]:
            self.rotate(90)
            dx = -self.speed
        if keys[pygame.K_RIGHT]:
            self.rotate(270)
            dx = self.speed
        if keys[pygame.K_UP]:
            self.rotate(0)
            dy = -self.speed
        if keys[pygame.K_DOWN]:
            self.rotate(180)
            dy = self.speed
        
        self.move(dx, dy, other_tank)
        
        if keys[pygame.K_SPACE]:
            if current_time - self.last_shot_time >= self.shot_delay:
                self.last_shot_time = current_time
                return True
        return False
