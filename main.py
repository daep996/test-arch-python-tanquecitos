import pygame
from sys import exit
import time

# init pygame
pygame.init()
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Tanquecitos')
clock = pygame.time.Clock()
game_active = True

class Bullet:
    def __init__(self, x, y, angle):
        self.x = x
        self.y = y
        self.angle = angle
        self.speed = 15
        self.active = True
        self.explosion_time = 0
        self.showing_explosion = False
        
    def move(self):
        if not self.active:
            return
        if self.angle == 0:
            self.y -= self.speed
        elif self.angle == 90:
            self.x -= self.speed
        elif self.angle == 180:
            self.y += self.speed
        elif self.angle == 270:
            self.x += self.speed
        # Verificar si llegó a los bordes
        if self.x < 0 or self.x > SCREEN_WIDTH or self.y < 0 or self.y > SCREEN_HEIGHT:
            self.explode()
            
    def explode(self):
        self.active = False
        self.explosion_time = time.time()
        self.showing_explosion = True

# Fonts
text_font = pygame.font.Font(None, 50)
# tank 1
tank1_x_pos = 400
tank1_y_pos = 100
tank1_width = 100
tank1_height = 100
tank1_lives = 3
tank1_score = 0
tank1_angle = 0
# tank 2
tank2_x_pos = 600
tank2_y_pos = 100
tank2_width = 100
tank2_height = 100

# Bullets
bullets = []
bullet_surf = pygame.image.load('assets/bullet.png').convert_alpha()
shot_surf = pygame.image.load('assets/shot.png').convert_alpha()
last_shot_time = 0
SHOT_DELAY = 0.25  # Delay entre disparos en segundos

# Surfaces
background_surf = pygame.image.load('assets/bk.png').convert()

# & lives
lives_surf = text_font.render(f"Lives: {tank1_lives}", True, "#f1c40f")
# assets
tank1_surf = pygame.image.load('assets/tank1.png').convert_alpha()
tank1_rect = tank1_surf.get_rect(topleft = (tank1_x_pos, tank1_y_pos))

tank2_surf = pygame.image.load('assets/tank2.png').convert_alpha()
tank2_rect = tank2_surf.get_rect(topleft = (tank2_x_pos, tank2_y_pos))

def display_score():
    global  game_active
    current_time = pygame.time.get_ticks()
    # if(current_time > 1000 * 60 * 0): game_active = False # 10 mins
    score_surf = text_font.render(f"Score: {current_time}", True, "#c0c0c07b")
    score_rect = score_surf.get_rect(topleft = (500, 0))
    screen.blit(score_surf, score_rect)

def handle_keys():
    global tank1_x_pos, tank1_y_pos, tank1_angle, last_shot_time
    keys = pygame.key.get_pressed()
    temp_x = tank1_x_pos
    temp_y = tank1_y_pos
    
    if keys[pygame.K_LEFT]:
        tank1_angle = 90
        temp_x -= 20
    if keys[pygame.K_RIGHT]:
        tank1_angle = 270
        temp_x += 20
    if keys[pygame.K_UP]:
        tank1_angle = 0
        temp_y -= 20
    if keys[pygame.K_DOWN]:
        tank1_angle = 180
        temp_y += 20
    # Manejo de disparos
    if keys[pygame.K_SPACE]:
        current_time = time.time()
        if current_time - last_shot_time >= SHOT_DELAY:
            # Calcular la posición inicial de la bala desde el centro del tanque
            bullet_x = tank1_rect.centerx
            bullet_y = tank1_rect.centery
            bullets.append(Bullet(bullet_x, bullet_y, tank1_angle))
            last_shot_time = current_time
    
    temp_rect = pygame.Rect(temp_x, temp_y, tank1_width, tank1_height)
    if (
        temp_x >= 0 and 
        temp_x + tank1_width <= SCREEN_WIDTH and 
        temp_y >= 0 and 
        temp_y + tank1_height <= SCREEN_HEIGHT and 
        not temp_rect.colliderect(tank2_rect)
    ):
        tank1_x_pos = temp_x
        tank1_y_pos = temp_y

def move_tank():
    rotated_tank1 = pygame.transform.rotate(tank1_surf, tank1_angle)
    rotated_rect = rotated_tank1.get_rect(center=tank1_rect.center)
    screen.blit(rotated_tank1, rotated_rect)
    screen.blit(tank2_surf, tank2_rect)
    tank1_rect.x = tank1_x_pos
    tank1_rect.y = tank1_y_pos

def update_bullets():
    # Actualizar posición de las balas y verificar colisiones
    for bullet in bullets[:]:
        bullet.move()
        bullet_rect = bullet_surf.get_rect(center=(bullet.x, bullet.y))
        if bullet.active and bullet_rect.colliderect(tank2_rect):
            bullet.explode()
        # Remover balas inactivas después de mostrar la explosión
        if bullet.showing_explosion and time.time() - bullet.explosion_time > 0.25:
            bullets.remove(bullet)

def draw_bullets():
    for bullet in bullets:
        if bullet.active:
            # Rotar y dibujar la bala
            rotated_bullet = pygame.transform.rotate(bullet_surf, bullet.angle)
            bullet_rect = rotated_bullet.get_rect(center=(bullet.x, bullet.y))
            screen.blit(rotated_bullet, bullet_rect)
        elif bullet.showing_explosion:
            # Dibujar la explosión
            explosion_rect = shot_surf.get_rect(center=(bullet.x, bullet.y))
            screen.blit(shot_surf, explosion_rect)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        """ if event.type == pygame.KEYDOWN:
            print(event) """
    
    screen.blit(background_surf, (0,0))
    
    if game_active:
        handle_keys()
        move_tank()
        update_bullets()
        draw_bullets()
        display_score()

        screen.blit(lives_surf, (550, 50))
    else:
        screen.fill("#3c3c3c")



    pygame.display.update()
    clock.tick(30)
