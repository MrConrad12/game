import pygame

pygame.init()

clock = pygame.time.Clock()
FPS = 60

# create game window
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 432


class Parallax:
    def __init__(self, ground_image, filename, screen):
        self.screen = screen
        self.scroll = 0
        self.ground_image = pygame.image.load(ground_image).convert_alpha()
        self.ground_width = self.ground_image.get_width()
        self.ground_height = self.ground_image.get_height()

        self.bg_images = []
        for i in range(1, 6):
            self.bg_image = pygame.image.load(f"{filename}-{i}.png").convert_alpha()
            self.bg_images.append(self.bg_image)
        self.bg_width = self.bg_images[0].get_width()

    def draw_bg(self):
        for x in range(5):
            speed = 1
            for i in self.bg_images:
                self.screen.blit(i, ((x * self.bg_width) - self.scroll * speed, 0))
                speed += 0.2

    def draw_ground(self, screen):
        for x in range(15):
            self.screen.blit(self.ground_image,
                        ((x * self.ground_width) - self.scroll * 2.5, screen.get_height - self.ground_height))


"""
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Parallax")

#define game variables


#game loop
run = True
while run:

  clock.tick(FPS)

  #draw world
  draw_bg()
  draw_ground()

  #get keypresses
  key = pygame.key.get_pressed()
  if key[pygame.K_LEFT] and scroll > 0:
    scroll -= 5
  if key[pygame.K_RIGHT] and scroll < 3000:
    scroll += 5

  #event handlers
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      run = False

  pygame.display.update()


pygame.quit()
"""
