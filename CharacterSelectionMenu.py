

import pygame
import pytmx
import random
import time
GRID_SIZE = 20
long_SIZE = 20
haut_SIZE = 16
CELL_SIZE = 48
WIDTH = long_SIZE  * CELL_SIZE
HEIGHT = haut_SIZE * CELL_SIZE
FPS = 30
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
PURPLE = (128, 0, 128)





class CharacterSelectionMenu:
    """
    Classe pour gérer la sélection des personnages pour chaque joueur.
    """
    def __init__(self, screen, available_characters, character_images, font_size=36):

        self.screen = screen
        self.available_characters = available_characters
        self.character_images = character_images
        self.font = pygame.font.Font(None, font_size)

    def select_characters(self, player_name):

        #fond d'ecran 
        imagea = pygame.image.load("images/FondNaruto4.png")
        imageb = pygame.transform.scale(imagea, (960, 760))
        image_rect = imageb.get_rect(center=(WIDTH // 2, HEIGHT//2))
        self.screen.blit(imageb, image_rect)
        selected_characters = []
        for i in range(2):  # Chaque joueur choisit 2 personnages
            selecting = True
            selected_index = 0  # Indice du personnage actuellement surligné

            while selecting:
            

                # Afficher le titre
                title_text = self.font.render(
                    f"{player_name} - Sélectionnez le personnage {i + 1}", True, WHITE
                )
                self.screen.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, 50))

                # Afficher chaque personnage avec son image et son nom
                for index, character in enumerate(self.available_characters):
                    x_pos = 100
                    y_pos = 100 + index * 100

                    # Afficher l'image du personnage
                    character_image = self.character_images[character]
                    image_rect = character_image.get_rect(topleft=(x_pos, y_pos))
                    self.screen.blit(character_image, image_rect)

                    # Afficher le nom du personnage
                    color = GREEN if index == selected_index else WHITE
                    character_text = self.font.render(character, True, [250,250,110])
                    self.screen.blit(character_text, (x_pos + 120, y_pos + 50))

                    # Encadrer l'image du personnage sélectionné
                    if index == selected_index:
                        pygame.draw.rect(self.screen, GREEN, image_rect, 3)
                    else: pygame.draw.rect(self.screen, WHITE, image_rect, 3)

                pygame.display.flip()

                # Gérer les événements de  sélection
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        exit()

                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_UP and selected_index > 0:
                            selected_index -= 1
                        elif event.key == pygame.K_DOWN and selected_index < len(self.available_characters) - 1:
                            selected_index += 1
                        elif event.key == pygame.K_RETURN:  # Valider le personnage
                            selected_character = self.available_characters[selected_index]
                            if selected_character not in selected_characters:
                                
                                selected_characters.append(selected_character)
                                print(f"{player_name} a choisi : {selected_character}")
                                selecting = False
                            else:
                                print("Personnage déjà choisi, veuillez en sélectionner un autre.")
        return selected_characters
