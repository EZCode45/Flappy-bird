import random
import sys

import pygame
from pygame.locals import QUIT
from pygame.time import Clock

clock = Clock()
fps = 100
#Initialize values and setup
pygame.init()
WIDTH, HEIGHT = 288, 512
DISPLAYSURF = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Flappy Bird')
score = 0
game_speed = 2
font = pygame.font.Font(None, 70)


bg_img_path = 'sprites/background-day.png'
bg_img = pygame.image.load(bg_img_path)
bg_rect = bg_img.get_rect()

base_img_path = 'sprites/base.png'
base_img = pygame.image.load(base_img_path)
base_rect = base_img.get_rect()
base_rect.center = (WIDTH // 2, HEIGHT)


class Bird(pygame.sprite.Sprite):
  def __init__(self):
    super().__init__()
    #Load the sprites into the game
    bird_img_paths = ['sprites/bluebird-downflap.png',
                     'sprites/bluebird-midflap.png',
                     'sprites/bluebird-upflap.png']
    self.images = [pygame.image.load(image_path) for image_path in bird_img_paths]
    self.current_image = 1
    self.image = self.images[self.current_image]
    self.rect = self.image.get_rect()
    self.rect.center = (WIDTH // 2, HEIGHT // 2)

    #Game variables
    self.bird_y = HEIGHT / 2
    self.bird_y_vel = 0
    self.animation_tick = 0
  def update(self, *_args, **_kwargs):
    #Update the bird's velocity and its position
    self.bird_y += self.bird_y_vel
    self.bird_y_vel += 0.07
    self.rect.center = (WIDTH // 2 - 75, int(self.bird_y))

    self.animation_tick += 1
    if self.animation_tick % 10 == 0:
      self.current_image = (self.current_image + 1) % len(self.images)
      self.image = self.images[self.current_image]
      self.animation_tick = 0
      
    
  def draw(self):
    DISPLAYSURF.blit(self.image, self.rect)
    
class Pipe(pygame.sprite.Sprite):
  def __init__(self, pos, y_inverted = False):
    super().__init__()
    pipe_img_path = 'sprites/pipe-green.png'
    self.image = pygame.image.load(pipe_img_path)
    self.rect = self.image.get_rect()
    if y_inverted:
      self.image = pygame.transform.flip(self.image, False, True)

    x, y = pos
    self.rect.x = x
    self.rect.y = 0 if y_inverted else HEIGHT
    self.rect.bottom = y if y_inverted else y + 430

  def update(self, *_args, **_kwargs):
    global score
    self.rect.x -= int(game_speed)
    if self.rect.right < 0:
      self.kill()
      score += 1
  def draw(self):
    DISPLAYSURF.blit(self.image, self.rect)



#Initialize sprite groups
all_sprites_group = pygame.sprite.Group()
bird_group = pygame.sprite.Group() 
all_pipes_group = pygame.sprite.Group()
bottom_pipe_group = pygame.sprite.Group()
top_pipe_group = pygame.sprite.Group()


#Initialize bird sprite
bird = Bird()
all_sprites_group.add(bird)
bird_group.add(bird)

def spawn_pipes(pipe_x):
  #Spawn spikes in pairs
  pipe_y = random.randint(100, 300)
  top_pipe = Pipe((pipe_x, pipe_y), True)
  top_pipe_group.add(top_pipe)
  all_pipes_group.add(top_pipe)
  all_sprites_group.add(top_pipe)

  bottom_pipe = Pipe((pipe_x, pipe_y),  y_inverted = False)
  bottom_pipe_group.add(bottom_pipe)
  all_pipes_group.add(bottom_pipe)
  all_sprites_group.add(bottom_pipe)
  
for i in range(5):
  spawn_pipes(WIDTH + (i * 200))

#Game Loop
running = True
while running:
  #Event handling
  for event in pygame.event.get():
    if event.type == QUIT:
      running = False
      

  keys = pygame.key.get_pressed()
  if keys[pygame.K_SPACE]:
    bird.bird_y_vel = -1

  bird.update()
  #Update the pipes' position and check if they are off-screen
  all_pipes_group.update()
  


  #Check for collisions between the bird and any pipes
  if pygame.sprite.spritecollideany(bird, all_pipes_group):
    running = False
    print(f'Your score: {score//2}')
    # pass
      
  if bird.rect.colliderect(base_rect):
    running = False

  #Create a new set of pipes once the pipe list length goes below 3
  if len(all_pipes_group) < 6:
    spawn_pipes(WIDTH + 500)

  #Blit sprites into display surface
  DISPLAYSURF.blit(bg_img, bg_rect)
  DISPLAYSURF.blit(base_img, base_rect)
  
  bird_group.draw(DISPLAYSURF)
  
  all_pipes_group.draw(DISPLAYSURF)

  score_text = font.render(f"{score//2}", True, (255, 255, 255))
  DISPLAYSURF.blit(score_text, (WIDTH//2, 50))
  #Update display
  pygame.display.update()
  clock.tick(fps)

pygame.quit()
sys.exit()