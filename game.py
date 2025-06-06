import pygame
import sys
import time
from config import *
from sprites import PlayerTank, Tank
from bullet import Bullet
from network import NetworkManager

class Game:
    def __init__(self):
        pygame.init()
        # Deshabilitar el sistema de audio
        pygame.mixer.quit()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption('Tanquecitos')
        self.clock = pygame.time.Clock()
        self.running = True
        self.game_active = True
        # Grupos de sprites
        self.all_sprites = pygame.sprite.Group()
        self.bullets = pygame.sprite.Group()
        self.tanks = pygame.sprite.Group()
        # Variables de red
        self.network = NetworkManager(self)
        self.multiplayer_ready = False
        self.player = None
        self.other_players = {}
        self.player_number = 0  # Valor por defecto hasta que el servidor asigne uno
        
        self.load_resources()
        
        # Conectar al servidor
        if not self.network.connect_to_server():
            print("No se pudo conectar al servidor")
        
    def load_resources(self):
        self.background = pygame.image.load('assets/bk.png').convert()
        self.font = pygame.font.Font(None, FONT_SIZE)
        
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                
    def update(self):
        if not self.game_active or not self.multiplayer_ready:
            return
            
        keys = pygame.key.get_pressed()
        current_time = time.time()

        if self.player.alive and self.player.handle_input(keys, current_time, self.tanks):
            self.shoot()
            
        self.all_sprites.update()
        self.bullets.update()
        
        self.check_collisions()
        
        # Enviar actualización de estado al servidor
        self.network.send_player_update({
            'position': (self.player.pos.x, self.player.pos.y),
            'angle': self.player.angle,
            'alive': self.player.alive
        })
        
    def shoot(self):
        bullet = Bullet(self.player.rect.centerx, self.player.rect.centery, 
                       self.player.angle)
        self.bullets.add(bullet)
        self.all_sprites.add(bullet)
        
    def check_collisions(self):
        # Verificar colisiones entre balas y tanques
        for bullet in self.bullets:
            if not bullet.active:
                continue
                
            hits = pygame.sprite.spritecollide(bullet, self.tanks, False)
            for tank in hits:
                if tank != self.player and tank.alive:
                    bullet.explode()
                    if isinstance(tank, Tank):
                        for sid, enemy_tank in self.other_players.items():
                            if enemy_tank == tank:
                                self.network.report_hit(sid)
                                break
        
    def display_score(self):
        if not self.multiplayer_ready:
            connecting_text = self.font.render("Conectando al servidor...", True, YELLOW)
            text_rect = connecting_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2))
            self.screen.blit(connecting_text, text_rect)
            return

        if self.player:
            all_players = [(self.player_number, self.player)]
            all_players.extend([(tank.player_number, tank) for tank in self.other_players.values()])
            all_players.sort(key=lambda x: x[0])
            y_offset = 10
            for player_num, tank in all_players:
                color = WHITE if tank == self.player else YELLOW
                if not tank.alive:
                    color = SCORE_COLOR
                    
                player_info = self.font.render(
                    f"P{player_num + 1} Lives: {tank.lives}",
                    True,
                    color
                )
                self.screen.blit(player_info, (10, y_offset))
                y_offset += 30
                
            # Mostrar mensaje si el jugador está eliminado
            if not self.player.alive:
                if self.player.lives <= 0:
                    game_over_text = self.font.render("GAME OVER", True, YELLOW)
                    text_rect = game_over_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2))
                    self.screen.blit(game_over_text, text_rect)
                else:
                    respawn_text = self.font.render("Respawning...", True, YELLOW)
                    text_rect = respawn_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2))
                    self.screen.blit(respawn_text, text_rect)
        
    def draw(self):
        self.screen.blit(self.background, (0, 0))
        
        if self.game_active:
            # Verificar que los sprites sean válidos antes de dibujarlos
            valid_sprites = [sprite for sprite in self.all_sprites if (hasattr(sprite, 'alive') and sprite.alive) or not hasattr(sprite, 'alive')]
            for sprite in valid_sprites:
                if hasattr(sprite, 'draw'):
                    sprite.draw(self.screen)
                else:
                    self.screen.blit(sprite.image, sprite.rect)
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
        
    def setup_multiplayer(self, player_number, total_players):
        self.player = PlayerTank(*PLAYER_POSITIONS[player_number], player_number)
        self.tanks.add(self.player)
        self.all_sprites.add(self.player)
        self.player_number = player_number
        self.multiplayer_ready = True
        
    def update_players_list(self, players_data):
        for sid, data in players_data.items():
            if data['player_number'] != self.player_number and sid not in self.other_players:
                player_num = data['player_number']
                # Asegurar que cada jugador use su tanque correspondiente
                sprite_path = f'assets/tank{player_num + 1}.png'
                new_tank = Tank(*PLAYER_POSITIONS[player_num], 
                    sprite_path, player_num)
                new_tank.player_number = player_num
                self.other_players[sid] = new_tank
                self.tanks.add(new_tank)
                self.all_sprites.add(new_tank)
        
        # Remover jugadores desconectados
        for sid in list(self.other_players.keys()):
            if sid not in players_data:
                self.other_players[sid].kill()
                del self.other_players[sid]
    
    def update_other_players(self, players_data):
        for sid, data in players_data.items():
            if sid in self.other_players:
                tank = self.other_players[sid]
                tank.pos.x, tank.pos.y = data['position']
                tank.rotate(data['angle'])
    
    def handle_remote_shot(self, data):
        bullet = Bullet(data['position'][0], data['position'][1], data['angle'])
        self.bullets.add(bullet)
        self.all_sprites.add(bullet)
    
    def handle_player_elimination(self, data):
        if data['player'] in self.other_players:
            tank = self.other_players[data['player']]
            tank.alive = False
            tank.lives = data['lives']
            if tank.lives <= 0:
                # Remover el tanque de todos los grupos de sprites
                tank.kill()
                self.tanks.remove(tank)
                self.all_sprites.remove(tank)
                del self.other_players[data['player']]
        elif self.network.sio.sid == data['player']:
            self.player.alive = False
            self.player.lives = data['lives']
            if self.player.lives <= 0:
                # Remover el tanque del jugador de todos los grupos de sprites
                self.player.kill()
                self.tanks.remove(self.player)
                self.all_sprites.remove(self.player)
                self.game_active = False  # Detener el juego para este jugador

if __name__ == '__main__':
    game = Game()
    game.run()
