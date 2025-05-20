import pygame
import sys
import time
from config import *
from sprites import PlayerTank, Tank
from bullet import Bullet

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption('Tanquecitos')
        self.clock = pygame.time.Clock()
        self.running = True
        self.game_active = True
        # Grupos de sprites
        self.all_sprites = pygame.sprite.Group()
        self.bullets = pygame.sprite.Group()
        # Inicializar jugadores
        self.player = PlayerTank(*PLAYER_START_POS)
        self.enemy = Tank(*ENEMY_START_POS, 'assets/tank2.png')
        self.all_sprites.add(self.player, self.enemy)
        # Cargar recursos
        self.load_resources()
        
    def load_resources(self):
        self.background = pygame.image.load('assets/bk.png').convert()
        self.font = pygame.font.Font(None, FONT_SIZE)
        
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                
    def update(self):
        if not self.game_active:
            return
            
        keys = pygame.key.get_pressed()
        current_time = time.time()
        # Actualizar jugador
        if self.player.handle_input(keys, current_time, self.enemy):
            self.shoot()
        # Actualizar sprites
        self.all_sprites.update()
        self.bullets.update()
        # Verificar colisiones
        self.check_collisions()
        
    def shoot(self):
        bullet = Bullet(self.player.rect.centerx, self.player.rect.centery, 
                       self.player.angle)
        self.bullets.add(bullet)
        self.all_sprites.add(bullet)
        
    def check_collisions(self):
        # Verificar colisiones entre balas y tanque enemigo
        hits = pygame.sprite.spritecollide(self.enemy, self.bullets, False)
        for bullet in hits:
            if bullet.active:
                bullet.explode()
        
    def display_score(self):
        current_time = pygame.time.get_ticks()
        score_surf = self.font.render(f"Score: {current_time}", True, SCORE_COLOR)
        score_rect = score_surf.get_rect(topleft=(500, 0))
        self.screen.blit(score_surf, score_rect)
        
        lives_surf = self.font.render(f"Lives: {self.player.lives}", True, YELLOW)
        self.screen.blit(lives_surf, (550, 50))
        
    def draw(self):
        self.screen.blit(self.background, (0, 0))
        
        if self.game_active:
            self.all_sprites.draw(self.screen)
            self.display_score()
        else:
            self.screen.fill(BLACK)
            
        pygame.display.update()
        
    def run(self):
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(FPS)
        
        pygame.quit()
        sys.exit()

if __name__ == '__main__':
    game = Game()
    game.run()
