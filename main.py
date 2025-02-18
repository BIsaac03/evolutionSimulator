import pygame

pygame.init()
screenWidth, screenHeight = 900, 600
screen = pygame.display.set_mode((screenWidth, screenHeight))
pygame.display.set_caption("Interactive Evolution Simulator")
clock = pygame.time.Clock()

done = False
while not done:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

    screen.fill((255, 255, 255))

    clock.tick(60)
    pygame.display.flip()

pygame.quit()