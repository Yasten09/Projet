

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





class Competence:
    """
    Classe pour représenter une compétence.
    """
    def __init__(self, name, range, area,attack_power):
        self.name = name
        self.range = range
        self.area = area  # Coordonnées relatives pour la zone d'effet
        self.attack_power=attack_power
    def __repr__(self):
        return f"Competence(name={self.name}, range={self.range}, area={self.area}, attack power= {self.attack_power})"
class FastMove(Competence):
    def __init__(self):
        # La compétence "Fast Move" n'a pas de portée spécifique ni de zone d'effet
        super().__init__(name="Fast Move", range=0, area=[],attack_power=0)

    def apply(self, unit, dx, dy):
        """Applique la compétence Fast Move : déplace l'unité de 3 cases dans la direction spécifiée (dx, dy)."""
        # Déplace l'unité de 3 cases dans la direction donnée (dx, dy)
        isFastMove=True
        for _ in range(3):  # Déplace l'unité de 3 cases

            unit.move(dx, dy,isFastMove)
            
        if unit.remaining_move >0:    
    
            unit.remaining_move-= 1
        isFastmove=False   
    