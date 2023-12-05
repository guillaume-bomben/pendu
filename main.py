import pygame
import random

pygame.init()



#############################################################################################################################
#------------------------------------------- Paramètre general du programe -------------------------------------------------#
#############################################################################################################################



screen_width = 1200
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Jeux du Pendu")

white = (255, 255, 255)
black = (0, 0, 0)
gray = (128,128,128)
red = (255,0,0)

font = pygame.font.Font('freesansbold.ttf', 32)



#############################################################################################################################
#-------------------------------- Recuperer un mot aléatoire dans le fichier texte -----------------------------------------#
#############################################################################################################################



def mot_aleatoire(nom_fichier):
    with open(nom_fichier, 'r') as fichier:
        lignes = fichier.readlines()
        ligne_aleatoire = random.choice(lignes).strip().upper()
        return ligne_aleatoire

mot_initial = mot_aleatoire("mots.txt")
print(mot_initial)
letters_guessed = set()
word_status = ["_" for _ in mot_initial]



#############################################################################################################################
#------------------------------------------------ Afficher Texte -----------------------------------------------------------#
#############################################################################################################################



def afficher_texte(texte, x, y, couleur=white):
    texte_affiche = font.render(texte, True, couleur)
    screen.blit(texte_affiche, (x, y))



#############################################################################################################################
#-------------------------------------------- Creation des bouton ----------------------------------------------------------#
#############################################################################################################################



def bouton(message, x, y, largeur, hauteur, couleur_base, couleur_survol, action=None):
    souris = pygame.mouse.get_pos()
    clic = pygame.mouse.get_pressed()

    if x + largeur > souris[0] > x and y + hauteur > souris[1] > y:
        pygame.draw.rect(screen, couleur_survol, (x, y, largeur, hauteur))

        if clic[0] == 1 and action is not None:
            action()
    else:
        pygame.draw.rect(screen, couleur_base, (x, y, largeur, hauteur))

    afficher_texte(message, x + 10, y + 10)



#############################################################################################################################
#------------------------------------------ Creation de l'ecran d'aceuil ---------------------------------------------------#
#############################################################################################################################



def home():
    running = True
    while running:
        screen.fill(black)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            # Récupération des coordonnées de la souris
            mouse = pygame.mouse.get_pos()
            click = pygame.mouse.get_pressed()

            # Bouton "Démarrer le jeu"
            if 400 + 300 > mouse[0] > 400 and 200 + 50 > mouse[1] > 200:
                pygame.draw.rect(screen, (150, 150, 150), (400, 200, 200, 50))
                if click[0] == 1:
                    main_game()  # Lancer la fonction main_game()
            
            # Bouton "Autre fonction"
            if 400 + 300 > mouse[0] > 400 and 300 + 50 > mouse[1] > 300:
                pygame.draw.rect(screen, (150, 150, 150), (400, 300, 200, 50))
                if click[0] == 1:
                    add_mot() # Lancer la fonction add_mot()

        # Affichage des boutons
        bouton("Démarrer le jeu", 400, 200, 300, 50, gray, red)
        bouton("Autre fonction", 400, 300, 300, 50, gray, red)
        
        pygame.display.update()



#############################################################################################################################
#--------------------------------------- Ecran de jeux ---------------------------------------------------------------------#
#############################################################################################################################



def main_game():
    global mot_initial, letters_guessed, word_status
    
    running = True
    nbi = 0
    while running:
        if nbi == 8 or ''.join(word_status) == mot_initial:
            nbi = 0
            mot_initial = mot_aleatoire("mots.txt")
            print(mot_initial)
            letters_guessed = set()
            word_status = ["_" for _ in mot_initial]
        
        screen.fill(black)
        # Charger l'image
        image = pygame.image.load(f"Img-Pendu/pendu{nbi}.png")
        image_width, image_height = image.get_rect().size
        # Position de l'image
        image_x = (screen_width - image_width) // 2  # Centrage en largeur
        image_y = 10  # À 10 pixels du haut de la fenêtre

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.unicode.isalpha():
                    letter = event.unicode.upper()
                    letters_guessed.add(letter) 
                    if letter in mot_initial:   #Si la lettre est dans le mot a trouver
                        for i in range(len(mot_initial)):
                            if mot_initial[i] == letter:
                                word_status[i] = letter
                    else:
                        nbi += 1
                        
        screen.blit(image, (image_x, image_y))
        display_word = font.render(' '.join(word_status), True, white)
        screen.blit(display_word, (screen_width // 2 - display_word.get_width() // 2, screen_height // 2))

        pygame.display.flip()



#############################################################################################################################
#--------------------------------------- Ecran de rajout de mot ------------------------------------------------------------#
#############################################################################################################################



def add_mot():
    running = True
    while running:
        screen.fill(black)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            




#############################################################################################################################
#----------------------------------------- Lancez le programe --------------------------------------------------------------#
#############################################################################################################################



home()