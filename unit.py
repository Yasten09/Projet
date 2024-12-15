

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
# Les cases inaccessibles
INACCESSIBLE_TILES = [
    (6, 0), (6, 1), (6, 2), (6, 3), (6, 4),
    (7, 0), (7, 1), (7, 2), (7, 3), (7, 4), (7, 5), (7, 7),
    (8, 5), (8, 7), (8, 8), (8, 9),
    (9, 8), (9, 9), (9, 10), (9, 11), (9, 12), (9, 14), (9, 15),
    (10, 8), (10, 9), (10, 10), (10, 11), (10, 12), (10, 14), (10, 15)
]


for x in range(0, 16):  
    if (x, 16) not in INACCESSIBLE_TILES:  
        INACCESSIBLE_TILES.append((x, 16))


# Cases qui réduisent la santé
# Cases où les unités sont protégées
DAMAGE_AMOUNT = 10  # Quantité de santé retirée
SHELTER_TILES = [(3, 1), (3, 5), (6, 6), (1, 2), (2, 1), (4, 3), (15, 3), (13, 3), (5, 9), (9, 6),(12,12),(12,14),(14,10)]

# Cases qui réduisent la santé
DAMAGE_TILES = [(3, 3), (5, 5), (2, 8), (2, 15), (1, 15), (3, 8), (12, 8), (13, 15), (13, 2), (13, 5), (8, 4), (6, 9)]


# Liste des cases en feu
active_fire_tiles = []


# Charger l'image de feu
fire_image = pygame.image.load("images/feu.png")
fire_image = pygame.transform.scale(fire_image, (CELL_SIZE, CELL_SIZE))


safe_image = pygame.image.load("images/safe.webp")
safe_image = pygame.transform.scale(safe_image, (CELL_SIZE, CELL_SIZE))






class Unit:

    def __init__(self, x, y, max_health,max_move,remaining_move, health,  team, character_type, competences=None):
        self.x = x
        self.y = y
        self.health = health
        
        self.max_move = max_move
        self.remaining_move = max_move
        self.max_health = health
        self.team = team
        self.is_selected = False
        self.character_type = character_type
        self.competences = competences or []
        

        # Chargement de l'image du personnage
        image_map = {
            "Naruto": "images/naruto.png",
            "Sassuke": "images/Sassuke.png",
            "Sakura": "images/Sakura.png",
            "Madara": "images/madara.png"
        }
        image_path = image_map.get(self.character_type, "images/default.png")

      
        self.image = pygame.image.load(image_path)


    def move(self, dx, dy,is_fast_move=False):
        
        
        if self.remaining_move > 0:
            move_distance = 3 if is_fast_move else 1
            if not is_fast_move:
                i=1
            else :
                i=0    
            for _ in range(move_distance):
                new_x = self.x + dx
                new_y = self.y + dy
            
            # Vérifie si la case cible est dans les limites et n'est pas interdite
            if (0 <= new_x < GRID_SIZE and 0 <= new_y < GRID_SIZE) and (new_x, new_y) not in INACCESSIBLE_TILES :
                distance = abs(dx) + abs(dy)
                if distance <= self.remaining_move:
                    self.x = new_x
                    self.y = new_y
                    
                     


                #print(f"Case ({new_x}, {new_y}) inaccessible.")

                if (new_x, new_y) in DAMAGE_TILES:
                    self.health -= DAMAGE_AMOUNT
                    print(f"L'unité a subi {DAMAGE_AMOUNT} points de dégâts sur la case ({new_x}, {new_y}). Santé restante : {self.health}")
                    
                    # Ajouter la case à la liste des cases en feu
                    if (new_x, new_y) not in active_fire_tiles:
                        active_fire_tiles.append((new_x, new_y))

                    if self.health <= 0:
                        print("L'unité a été éliminée !")

            if i==1:
                self.remaining_move-=1
    def draw(self, screen):

        draw_x = self.x * CELL_SIZE
        draw_y = self.y * CELL_SIZE
        screen.blit(self.image, (draw_x, draw_y))

    def attack_zone(self, cx, cy, opponent_units, competence):
        
        for dx, dy in competence.area:
            target_x = cx + dx
            target_y = cy + dy
            
            if 0 <= target_x < GRID_SIZE and 0 <= target_y < GRID_SIZE:
                for unit in opponent_units:
                    if unit.x == target_x and unit.y == target_y:
                        if (unit.x, unit.y) in SHELTER_TILES:
                            print(f"L'unité {unit.character_type} est dans un abri et ne peut pas être attaquée.")
                        else:
                            print(f"{self.character_type} attaque {unit.character_type} à ({target_x}, {target_y})")
                            unit.health -= competence.attack_power
                            if unit.health <= 0:
                                print(f"{unit.character_type} a été éliminé(e) !")
                        break

    def heal(self,user, target):      #fonction soigne les allier
    
        print(f"{user.character_type} utilise Soin sur {target.character_type} !")
        target.health += 20              
        target.health = max(target.health, 50) 

class UnitWithHealthBar(Unit):
    def __init__(self, x, y, health, max_health, remaining_move,  team, character_type, competences, max_move):
        
        super().__init__(x, y, max_health, max_move, remaining_move, health,  team, character_type, competences)
        
        
        self.remaining_move = remaining_move  
        self.max_move = max_move  

    def draw(self, screen):
        
        # Couleurs pour chaque équipe
        team_colors = {
            'player1': GREEN,  
            'player2': PURPLE    
        }

        # Dessiner le contour coloré
        team_color = team_colors.get(self.team, WHITE)  # Blanc par défaut 
        pygame.draw.rect(
            screen,
            team_color,
            (
                self.x * CELL_SIZE - 2, 
                self.y * CELL_SIZE - 2,
                CELL_SIZE + 4,
                CELL_SIZE + 4
            ),
             4 if self.is_selected else 2   # Épaisseur de la bordure
        )

        # Dessiner l'unité
        super().draw(screen)

        # Barre de santé
        health_ratio = self.health / self.max_health
        bar_width = CELL_SIZE * 0.8
        bar_height = 5
        bar_x = self.x * CELL_SIZE + (CELL_SIZE - bar_width) / 2
        bar_y = self.y * CELL_SIZE - 10

        pygame.draw.rect(screen, RED, (bar_x, bar_y, bar_width, bar_height))
        pygame.draw.rect(screen, GREEN, (bar_x, bar_y, bar_width * health_ratio, bar_height))

        # Texte pour déplacement restant
        font = pygame.font.Font(None, 18)
        move_text = font.render(f"Mv: {self.remaining_move}", True, WHITE)
        screen.blit(move_text, (self.x * CELL_SIZE + 5, self.y * CELL_SIZE + CELL_SIZE - 15))



    # Dessiner le feu sur les cases en feu
        for fire_tile in active_fire_tiles:
            fire_x = fire_tile[0] * CELL_SIZE
            fire_y = fire_tile[1] * CELL_SIZE
            screen.blit(fire_image, (fire_x, fire_y))
     
    # dessiner les cases à l'abris
        for safe_tile in SHELTER_TILES:
            safe_x = safe_tile[0] * CELL_SIZE
            safe_y = safe_tile[1] * CELL_SIZE
            screen.blit(safe_image, (safe_x, safe_y))            
  
