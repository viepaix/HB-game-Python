import pygame
from sys import exit
from random import randint, choice

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        
        player_walk1 = (pygame.image.load("resources\images\graphics\player\pixil-frame-0 (4).png").convert_alpha())
        player_walk1 = pygame.transform.scale(player_walk1, (90, 40))

        player_walk2 = pygame.image.load("resources\images\graphics\player\pixil-frame-0 (8).png").convert_alpha()
        player_walk2 = pygame.transform.scale(player_walk2, (90, 40))

        self.player_walk = [player_walk1, player_walk2]
        self.player_index = 0
        
        player_jump = pygame.image.load("resources\images\graphics\player\pixil-frame-0 (9).png").convert_alpha()
        self.player_jump = pygame.transform.scale(player_jump, (90, 40))
        
        self.image = self.player_walk[self.player_index]
        self.rect = self.image.get_rect(midbottom = (200, 300))
        self.gravity = 0
        self.speed = 0
        
        self.jump = pygame.mixer.Sound("resources/audio/jump.mp3")
        self.jump.set_volume(0.2)
                
    def player_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and self.rect.bottom >= 300:
            self.jump.play()
            self.gravity = -20
            
            
    def apply_gravity(self):
        self.gravity += 1
        self.rect.y += self.gravity
        if self.rect.bottom >= 300:
            self.rect.bottom = 300
            
    def movement_player(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            self.rect.x -= 5
        elif keys[pygame.K_d]:
            self.rect.x += 5
            
        if self.rect.left < 0:
            self.rect.left = 0
        elif self.rect.right > 800:
            self.rect.right = 0
            
    def player_animation(self):
        if self.rect.bottom <300:
            self.image = self.player_jump
        else:
            self.player_index += 0.1
            if self.player_index >= len(self.player_walk): self.player_index = 0
            self.image = self.player_walk[int(self.player_index)]
            
    def update(self):
        self.player_input()
        self.apply_gravity()
        self.movement_player()
        self.player_animation()

class Obstacle(pygame.sprite.Sprite):
    def __init__(self, type):
        super().__init__()
        
        if type == 'parrot':
            parrot_surface1 = pygame.image.load("resources\images\graphics\parrot\pixil-frame-0 (6).png").convert_alpha()
            parrot_surface2 = pygame.image.load("resources\images\graphics\parrot\pixil-frame-0 (7).png").convert_alpha()

            parrot_surface1 = pygame.transform.scale(parrot_surface1, (30,22))
            parrot_surface2 = pygame.transform.scale(parrot_surface2, (30,22))

            self.frames = [parrot_surface1, parrot_surface2]
            y_pos = 220
            
        else:
            hollow_surface1 = pygame.image.load("resources\images\graphics\hollow\pixil-frame-0 (5).png").convert_alpha()
            hollow_surface2 = pygame.image.load("resources\images\graphics\hollow\pixil-frame-0 (10).png").convert_alpha()

            hollow_surface1 = pygame.transform.scale(hollow_surface1, (38, 38))
            hollow_surface2 = pygame.transform.scale(hollow_surface2, (38, 38))

            self.frames = [hollow_surface1, hollow_surface2]
            y_pos = 300
            
        self.animation_index = 0
        self.image = self.frames[self.animation_index]
        self.rect = self.image.get_rect(bottomright = (randint(900, 1100),y_pos))

    def animation_state(self):
        self.animation_index += 0.1
        if self.animation_index >= len(self.frames): self.animation_index = 0
        self.image = self.frames[int(self.animation_index)]

    def update(self):
        self.animation_state()
        self.rect.x -= 6
        self.destroy()
        
    def destroy(self):
        if self.rect.x <= -100:
            self.kill     

def display_score():
    current_time = int(pygame.time.get_ticks() / 1000) - start_time
    score_surf = test_font.render(f'{current_time}', False, (64,64,64))
    score_rect = score_surf.get_rect(center = (400, 50))
    screen.blit(score_surf, score_rect)
    return current_time

def collision_sprite():
    if pygame.sprite.spritecollide(player.sprite, obstacle_group, False):
        obstacle_group.empty()
        return False
    else: return True


pygame.init()

screen = pygame.display.set_mode((800,400))
pygame.display.set_caption("Shiko 18 anos")
clock = pygame.time.Clock()
test_font = pygame.font.Font("resources/font/Crang.ttf" , 50 )
alt_font = pygame.font.Font("resources/font/Crang.ttf", 30)
game_active = True
start_time = 0
score = 0

bg_music = pygame.mixer.Sound("resources/audio/y2mate.com - Cumpleaños feliz con Piano y Violin precioso.mp3") 
bg_music.play(loops = -1)
        

cap_audio = pygame.mixer.Sound("resources/audio/ea.mp3")
cap_audio.set_volume(0.2)
cap_audio_playing = False

#groups
player = pygame.sprite.GroupSingle()
Player.add(Player())

obstacle_group = pygame.sprite.Group()


#logo of game
pygame_icon = pygame.image.load("resources\images\hollow-knight.1683709273.8012.jpg")
pygame.display.set_icon(pygame_icon)

#timer
obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer, 1400)


#Scenario
sky_surface = pygame.image.load("resources\images\graphics\sky.jpg").convert()
sky = pygame.transform.scale(sky_surface, (800, 400))
ground_surface = pygame.image.load("resources\images\graphics\ground (1).png").convert()
ground = pygame.transform.scale(ground_surface, (0, 400))

#Surface text

player = pygame.sprite.GroupSingle()
player.add(Player())

player_stand = pygame.image.load("resources\images\graphics\player\download (10).png").convert_alpha()
player_stand_scaled = pygame.transform.scale(player_stand, (250,250))
player_stand_rect = player_stand.get_rect(center = (450, 270))

#Losser text

text_losser = test_font.render("TAN TRYHARD Y MUERES EN ESTE JUEGUITO?", False, "white")
text_losser_scaled = pygame.transform.scale(text_losser, (700, 40))
text_losser_rect = text_losser.get_rect(midtop = (680, 20))

restart_text = alt_font.render("Presiona 'Space' para reiniciar", False, "White")
restart_text_scaled = pygame.transform.scale(restart_text, (400, 30))
restart_text_scaled_rect = restart_text_scaled.get_rect(midbottom = (400, 390))
restart_text_rect = restart_text.get_rect(midbottom = (400, 390))


while True:
   #event to close the game
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if game_active:        
            if event.type == obstacle_timer:
                obstacle_group.add(Obstacle(choice(['parrot', 'hollow', 'hollow', 'hollow', 'parrot'])))

        else:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:

                game_active = True
                start_time = int(pygame.time.get_ticks() / 1000)

    if game_active:   
        screen.blit(sky, (0,0))
        screen.blit(ground_surface, (0,300))
        pygame.draw.line(screen, 'Purple', (200, 80), (600, 80), 3)

        score = display_score()
        
        
        player.draw(screen)
        player.update()
        cap_audio.stop()
        
        obstacle_group.draw(screen)
        obstacle_group.update()
        
        game_active = collision_sprite()

    else:
        
        screen.fill((94,129,162))
        screen.blit(player_stand_scaled, player_stand_rect)

        bg_music.stop()
        if not cap_audio_playing:
            cap_audio.play()
            cap_audio_playing = True

        score_message = alt_font.render(f'Puntuacion: {score}', False, 'white')
        score_message_rect = score_message.get_rect(center = (400, 340))
        screen.blit(text_losser_scaled, text_losser_rect)
        
        if score == 0: screen.blit(restart_text, restart_text_rect)
        else:screen.blit(restart_text_scaled, restart_text_scaled_rect), screen.blit(score_message, score_message_rect)        
            
    pygame.display.update()
    clock.tick(60)