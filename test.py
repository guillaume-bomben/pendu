import pygame

# Initialisation de Pygame
pygame.init()

# Création d'une surface
width, height = 400, 300
screen = pygame.display.set_mode((width, height))
surface = pygame.Surface((100, 100))

# Définition d'une couleur (ici le vert) comme transparente
transparent_color = pygame.Color(0, 255, 0)  # Couleur verte (R, G, B)
surface.fill(transparent_color)
surface.set_colorkey(transparent_color)

# Affichage de la surface sur l'écran
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((255, 255, 255))  # Fond de l'écran en blanc
    screen.blit(surface, (150, 100))  # Affichage de la surface
    pygame.display.flip()

pygame.quit()
