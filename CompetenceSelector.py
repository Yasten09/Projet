

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

class CompetenceSelector:

    def __init__(self, screen, available_competences, font_size=36):

        self.screen = screen
        self.available_competences = available_competences
        self.font = pygame.font.Font(None, font_size)
        self.small_font = pygame.font.Font(None, 25) 

    def choose_competences(self, units, player_name):

        for unit in units:
            unit.competences = []  # Réinitialise les compétences de l'unité
            print(f"Sélection des compétences pour {player_name} - Unité en ({unit.x}, {unit.y})")

            for i in range(2):  # Chaque unité doit choisir 2 compétences
                selecting = True
                selected_index = 0  # Indice de la compétence actuellement surlignée

                while selecting:
                    self.screen.fill(BLACK)

                    # Afficher le message
                    title_text = self.font.render(
                        f"{player_name} - Sélectionnez la compétence {i + 1} pour {unit.character_type}", True, WHITE
                    )
                    #Afficher les images dans le menu choix des competences
                    if unit.character_type=="Naruto":
                        pathimage="MenuChoix/NarutoChoose.png"
                    if unit.character_type=="Sassuke":
                        pathimage="MenuChoix/SassukeChoose.jpg"
                    if unit.character_type=="Sakura":
                        pathimage= "MenuChoix/SakuraChoose.jpg"    
                    if unit.character_type=="Itachi": 
                        pathimage= "MenuChoix/ItachiChoose.jpg" 
                    if unit.character_type=="Madara": 
                        pathimage= "MenuChoix/MadaraChoose.jpg"    
       

                    
                    
                    unitimage1=pygame.image.load(pathimage)
                    unitimage = pygame.transform.scale(unitimage1, (1000, 1000))
                    image_rect = unitimage.get_rect(center=(WIDTH // 2, 150*3))
                    self.screen.blit(unitimage, image_rect)
                    rect_x = WIDTH // 2 - title_text.get_width() // 2-10
                    rect_y = 45
                    rect_width = title_text.get_width() + 20
                    rect_height = title_text.get_height() + 10

                    # ajouter un fond rectangulaire semi-transparent pour
                    rect_surface = pygame.Surface((rect_width, rect_height))
                    rect_surface.set_alpha(128)  # Transparence (0 = invisible, 255 = opaque)
                    rect_surface.fill((0, 0, 0))  # Couleur noire
                    self.screen.blit(rect_surface, (rect_x, rect_y))                   
                    self.screen.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, 50))
                    # afficher les compétences disponibles
                    for index, competence in enumerate(self.available_competences):
                        color = GREEN if index == selected_index else WHITE
                        if competence.name in ["Explosion", "Tir précis","Fusil"]:
                            competence_text = self.font.render(
                                f"{competence.name} - Portée: {competence.range} - Zone d'effet: {len(competence.area)} - Attack Power : {competence.attack_power}", True, color
                            )
                        else: 
                            competence_text = self.font.render(
                                f"{competence.name} ", True, color)

                        rect_x = 90
                        rect_y = 145 + index * 40
                        rect_width = competence_text.get_width() + 20
                        rect_height = competence_text.get_height() + 10

                        # Ajouter un fond rectangulaire semi-transparent
                        rect_surface = pygame.Surface((rect_width, rect_height))
                        rect_surface.set_alpha(128)  # Transparence (0 = invisible, 255 = opaque)
                        rect_surface.fill((0, 0, 0))  # Couleur noire
                        self.screen.blit(rect_surface, (rect_x, rect_y))

                        # Dessiner le texte
                        self.screen.blit(competence_text, (100, 150 + index * 40))
                        indication_text1 = self.small_font.render(
                        "Appuyez sur ESPACE pour utiliser la 1ère compétence, S pour la 2ème",True,RED)
                        indication_text2 = self.small_font.render("Un curseur rouge apparaîtra pour choisir votre cible.  ",True,RED)
                        indication_text3 = self.small_font.render("Si une compétence est Fast Move, l'unité pourra parcourir  plus de cases,", True, RED)
                        indication_text4 = self.small_font.render("Dans ce cas, Appuyez sur ESPACE pour excuter l'autre competence choisie " ,True, RED)
                        
                        self.screen.blit(indication_text1, (WIDTH // 2 - indication_text1.get_width() // 2, HEIGHT - 100))
                        self.screen.blit(indication_text2, (WIDTH // 2 - indication_text2.get_width() // 2, HEIGHT - 80))
                        self.screen.blit(indication_text3, (WIDTH // 2 - indication_text3.get_width() // 2, HEIGHT - 60))
                        self.screen.blit(indication_text4, (WIDTH // 2 - indication_text3.get_width() // 2, HEIGHT - 40))


                    pygame.display.flip()

                    
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            pygame.quit()
                            exit()

                        if event.type == pygame.KEYDOWN:
                            if event.key == pygame.K_UP and selected_index > 0:
                                selected_index -= 1
                            elif event.key == pygame.K_DOWN and selected_index < len(self.available_competences) - 1:
                                selected_index += 1
                            elif event.key == pygame.K_RETURN:  # Valider la compétence
                                selected_competence = self.available_competences[selected_index]
                                if selected_competence not in unit.competences:  # Vérifie si la compétence n'a pas déjà été choisie
                                    unit.competences.append(selected_competence)
                                    print(f"Compétence choisie : {selected_competence.name}")
                                    selecting = False
                                    break
                                else:
                                    print("Compétence déjà choisie, veuillez en sélectionner une autre.")
            if unit.competences[0].name=="Fast Move":
                unit.competences=unit.competences[::-1]
