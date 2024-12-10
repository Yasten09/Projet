import pygame
import random
from unit import *

# Constantes
GRID_SIZE = 10  # la taille de la grille
CELL_SIZE = 60  #la taille de la cellule
WIDTH = GRID_SIZE * CELL_SIZE   #la largeur de la grille
HEIGHT = GRID_SIZE * CELL_SIZE  #la haiteur de la grille
FPS = 30
WHITE = (255, 255, 255)  
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)


class Unit:
    def __init__(self, x, y, image_path):
        """
        Initialise une unité avec une position et une image spécifique.

        Paramètres
        ----------
        x : int
            La position x de l'unité sur la grille.
        y : int
            La position y de l'unité sur la grille.
        image_path : str
            Le chemin de l'image pour cette unité.
        """
        self.x = x
        self.y = y
        self.image = pygame.image.load(image_path)  #charger l'image
        self.image = pygame.transform.scale(self.image, (CELL_SIZE, CELL_SIZE))#mise à l'échelle l'image pour qu'elle soit centré

    def move(self, dx, dy):
        """Déplacement de  l'unité de dx, dy."""
        if 0 <= self.x + dx < GRID_SIZE and 0 <= self.y + dy < GRID_SIZE:
            self.x += dx
            self.y += dy

    def draw(self, screen):
        """Dessine l'unité sur la grille à une position donner."""
        position = (self.x * CELL_SIZE, self.y * CELL_SIZE)
        screen.blit(self.image, position)


# Classe Player hérité de la classe unit 
class Player(Unit):
    def __init__(self, x, y, character_type):
        """
        Initialise un joueur avec une position et un type de personnage.

        character_type  désigne quelle personnage parmi les 3('naruto', 'uchiwa', 'haruno').
        """
        image_map = {
            "naruto": "naruto.png",
            "uchiwa": "uchiwa.png",
            "haruno": "haruno.png"
        }
        image_path = image_map.get(character_type, "default.png")
        super().__init__(x, y, image_path)


# Classe Enemy hérité de la classe unit
class Enemy(Unit):
    def __init__(self, x, y, character_name):
        """
        Initialise un ennemi avec une position fixe et une image spécifique.
         character_type  désigne quelle personnage parmi les 3('itachi', 'madara', 'zabuza').
        """
        # On associe l'image en fonction du nom de l'ennemi
        image_map = {
            "itachi": "itachi.png",
            "madara": "madara.png",
            "zabuza": "zabuza.png"
        }
        image_path = image_map.get(character_name, "default.png")
        super().__init__(x, y, image_path)


