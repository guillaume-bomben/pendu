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
#------------------------------------------ Creation de l'ecran d'aceuill --------------------------------------------------#
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
                    player_choice()  # Lancer la fonction player_choice()

            # Bouton "Ajouter un mot"
            if 400 + 300 > mouse[0] > 400 and 300 + 50 > mouse[1] > 300:
                pygame.draw.rect(screen, (150, 150, 150), (400, 300, 200, 50))
                if click[0] == 1:
                    edit_diff_list() # Lancer la fonction edit_diff_list()

            # Bouton "Score"
            if 400 + 300 > mouse[0] > 400 and 400 + 50 > mouse[1] > 400:
                pygame.draw.rect(screen, (150, 150, 150), (400, 300, 200, 50))
                if click[0] == 1:
                    score() # Lancer la fonction add_mot()

        # Affichage des boutons
        bouton("Démarrer le jeu", 400, 200, 300, 50, gray, red)
        bouton("Ajouter un mot", 400, 300, 300, 50, gray, red)
        bouton("Score", 400, 400, 300, 50, gray, red)

        pygame.display.update()



#############################################################################################################################
#--------------------------------------- Ecran de jeux ---------------------------------------------------------------------#
#############################################################################################################################



def main_game():
    global mot_initial, letters_guessed, word_status,diff

    running = True
    nbi = 0
    while running:
        if nbi == 8:
            loose()
        elif ''.join(word_status) == mot_initial :
            if diff == "facile":
                update_score(100)
            elif diff == "moyen":
                update_score(250)
            elif diff == "diff":
                update_score(500)
            win()

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
                if event.key == pygame.K_ESCAPE:
                    home()
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
        afficher_texte("Appuyez sur Echap pour revenir sur l'ecran d'aceuill", 100, 500)

        pygame.display.flip()



#############################################################################################################################
#--------------------------------------- Choix de la Liste de mot a editer -------------------------------------------------#
#############################################################################################################################



def edit_diff_list():
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
                    add_mot("mots_facile.txt")  # Lance l'edit de la liste facile

            # Bouton "Ajouter un mot"
            if 400 + 300 > mouse[0] > 400 and 300 + 50 > mouse[1] > 300:
                pygame.draw.rect(screen, (150, 150, 150), (400, 300, 200, 50))
                if click[0] == 1:
                    add_mot("mots_moyen.txt") # Lance l'edit de la liste moyenne

            # Bouton "Score"
            if 400 + 300 > mouse[0] > 400 and 400 + 50 > mouse[1] > 400:
                pygame.draw.rect(screen, (150, 150, 150), (400, 300, 200, 50))
                if click[0] == 1:
                    add_mot("mots_diff.txt") # Lance l'edit de la liste difficile

        # Affichage des boutons
        bouton("Liste Facile", 400, 200, 300, 50, gray, red)
        bouton("Liste Moyen", 400, 300, 300, 50, gray, red)
        bouton("Liste Difficile", 400, 400, 300, 50, gray, red)

        pygame.display.update()



#############################################################################################################################
#--------------------------------------- Ecran de rajout de mot ------------------------------------------------------------#
#############################################################################################################################



def add_mot(list_mot):
    running = True
    mot_nouveau = ""
    while running:
        screen.fill(black)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    home()
                if event.key == pygame.K_RETURN:
                    # Enregistrer le mot complet dans le fichier mots.txt
                    with open(list_mot, "a") as fichier:
                        fichier.write('\n' + mot_nouveau.lower())
                    mot_nouveau = ""  # Réinitialiser le mot pour le prochain ajout
                else:
                    # Récupérer les touches pressées pour former un mot
                    lettre = chr(event.key)
                    mot_nouveau += lettre

        afficher_texte("Appuyez sur Echap pour revenir sur l'ecran d'aceuill", 100, 100)
        afficher_texte("Ajoutez des mots (Appuyez sur Enter pour terminer) :", 100, 150)
        afficher_texte(f"Mot en cours: {mot_nouveau}", 100, 200)  # Affiche le mot en cours de formation

        pygame.display.update()



#############################################################################################################################
#----------------------------------------------- WIN or LOOSE --------------------------------------------------------------#
#############################################################################################################################



def win():
    running = True
    while running:
        screen.fill(black)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.KEYDOWN:
                home()

        afficher_texte("WIN : press any key to return to home", 100, 100)

        pygame.display.update()



def loose():
    running = True
    while running:
        screen.fill(black)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.KEYDOWN:
                home()

        afficher_texte("LOOSE : press any key to return to home", 100, 100)

        pygame.display.update()



#############################################################################################################################
#----------------------------------------------- Ecran de Score ------------------------------------------------------------#
#############################################################################################################################



def dificulty():
    global mot_initial, letters_guessed, word_status, diff
    diff = ""
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

            # Bouton "Démarrer le jeu en facile"
            if 400 + 300 > mouse[0] > 400 and 200 + 50 > mouse[1] > 200:
                pygame.draw.rect(screen, (150, 150, 150), (400, 200, 200, 50))
                if click[0] == 1:
                    mot_initial = mot_aleatoire("mots_facile.txt")
                    print(mot_initial)
                    letters_guessed = set()
                    word_status = ["_" for _ in mot_initial]
                    diff = "facile"
                    main_game()  # Lancer la fonction main_game()

            # Bouton "Démarrer le jeu en Moyen"
            if 400 + 300 > mouse[0] > 400 and 300 + 50 > mouse[1] > 300:
                pygame.draw.rect(screen, (150, 150, 150), (400, 300, 200, 50))
                if click[0] == 1:
                    mot_initial = mot_aleatoire("mots_moyen.txt")
                    print(mot_initial)
                    letters_guessed = set()
                    word_status = ["_" for _ in mot_initial]
                    diff = "moyen"
                    main_game()  # Lancer la fonction main_game()

            # Bouton "Démarrer le jeu en Difficile"
            if 400 + 300 > mouse[0] > 400 and 400 + 50 > mouse[1] > 400:
                pygame.draw.rect(screen, (150, 150, 150), (400, 300, 200, 50))
                if click[0] == 1:
                    mot_initial = mot_aleatoire("mots_diff.txt")
                    print(mot_initial)
                    letters_guessed = set()
                    word_status = ["_" for _ in mot_initial]
                    diff = "diff"
                    main_game()  # Lancer la fonction main_game()

        # Affichage des boutons
        bouton("Facile", 400, 200, 300, 50, gray, red)
        bouton("Moyen", 400, 300, 300, 50, gray, red)
        bouton("Difficile", 400, 400, 300, 50, gray, red)

        pygame.display.update()



#############################################################################################################################
#------------------------------------------- Choix du nom de joueur --------------------------------------------------------#
#############################################################################################################################



def player_choice():
    global player
    name_player = ""
    player_exists = False
    running = True
    while running:
        screen.fill(black)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    home()
                if event.key == pygame.K_RETURN:
                    with open("score.txt", "r+") as fichier:
                        lines = fichier.readlines()
                        for line in lines:
                            if line.strip().lower() == name_player.lower():
                                player_exists = True
                                break
                        
                        if not player_exists:
                            fichier.write('\n' + name_player.lower())
                            fichier.write('\n' + "0")
                    player = name_player
                    name_player = ""
                    dificulty()
                else:
                    # Récupérer les touches pressées pour former un mot
                    lettre = chr(event.key)
                    name_player += lettre
            
        afficher_texte("Ajoutez des mots (Appuyez sur Enter pour terminer) :", 100, 150)
        afficher_texte(f"Mot en cours: {name_player}", 100, 200)  # Affiche le mot en cours de formation
        
        pygame.display.update()



#############################################################################################################################
#----------------------------------------------- Ecran de Score ------------------------------------------------------------#
#############################################################################################################################



def score():
    running = True
    scores = []
    
    # Lecture des scores depuis le fichier
    with open("score.txt", "r") as fichier:
        lines = fichier.readlines()
        for i in range(1, len(lines), 3):  # Parcours tous les noms de joueurs
            if i + 1 < len(lines):  # Vérification pour s'assurer qu'on peut accéder à l'indice suivant
                player_name = lines[i].strip()
                player_score = int(lines[i+1].strip())  # Obtient le score du joueur
                scores.append((player_name, player_score))  # Ajoute le nom et le score à la liste

    while running:
        screen.fill(black)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    home()
        y = 100
        for player, score in scores:
            score_text = f"{player}: {score}"
            afficher_texte(score_text, 100, y)
            y += 40  # Espacement vertical entre chaque ligne du tableau

        pygame.display.update()



def update_score(add):
    # Ouvrir le fichier en mode lecture
    with open("score.txt", "r") as fichier:
        lines = fichier.readlines()

    with open("score.txt", "w") as fichier:
        i = 0
        while i < len(lines):
            # Modifier la ligne contenant le nom du joueur
            if lines[i].strip().lower() == player.lower():
                fichier.write(lines[i])  # Écrire le nom du joueur existant
                i += 1  # Passer à la ligne suivante (le score actuel)
                if i < len(lines):
                    score = int(lines[i].strip()) + add  # Récupérer le score et l'incrémenter
                    fichier.write(str(score) + "\n")  # Écrire le score mis à jour
            else:
                fichier.write(lines[i])  # Écrire les autres lignes sans modification
            i += 1



#############################################################################################################################
#----------------------------------------- Lancez le programe --------------------------------------------------------------#
#############################################################################################################################



home()