import pygame
import random
import time   

GRID_SIZE = 10
CELL_SIZE = 70
WIDTH = GRID_SIZE * CELL_SIZE
HEIGHT = GRID_SIZE * CELL_SIZE
FPS = 30
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)


def heal(user, target, units):      #fonction soigne les allier
    
    #print(f"{user.unit_type} utilise Soin sur {target.unit_type} !")
    target.health += 20              # Ajoute 5 points de vie à la cible
    target.health = max(target.health, 50)              # Limite la santé au maximum (par exemple 10)
class Competence:
    """
    Classe pour représenter une compétence.
    """
    def __init__(self, name, range, area):
        self.name = name
        self.range = range
        self.area = area  # Coordonnées relatives pour la zone d'effet

    def __repr__(self):
        return f"Competence(name={self.name}, range={self.range}, area={self.area})"


class Unit:
    """
    Classe pour représenter une unité.
    """
    def __init__(self, x, y,max_move, health, attack_power, team, competences=None):

        self.x = x
        self.y = y
        self.health = health
        self.attack_power = attack_power
        self.max_move=max_move
        self.remaining_move = max_move  # Déplacement restant pendant le tour
        self.max_health = health
        self.team = team
        self.is_selected = False
        self.competences = competences or []

    def move(self, dx, dy):
            """Déplace l'unité de dx, dy si elle a encore des déplacements disponibles."""
            if self.remaining_move > 0:
                if 0 <= self.x + dx < GRID_SIZE and 0 <= self.y + dy < GRID_SIZE:
                    distance = abs(dx) + abs(dy)  # Calcul du coût de déplacement
                    if distance <= self.remaining_move:
                        self.x += dx
                        self.y += dy
                        self.remaining_move -= distance  # Réduit le déplacement restant

    def attack_zone(self, cx, cy, targets, competence):
        """Applique les dégâts dans une zone définie par une compétence."""
        print(f"{self.team} attaque la zone autour de ({cx}, {cy}) avec {competence.name} !")

        for dx, dy in competence.area:
            tx, ty = cx + dx, cy + dy
            for target in targets:
                if target.x == tx and target.y == ty:
                    target.health -= self.attack_power
                    print(f"{target.team} à ({target.x}, {target.y}) subit {self.attack_power} dégâts. PV restants : {target.health}")
                    if target.health <= 0:
                        print(f"{target.team} à ({target.x}, {target.y}) est éliminé !")
                        targets.remove(target)

    def draw(self, screen):
        """Affiche l'unité à l'écran."""
        color = BLUE if self.team == 'player1' else RED
        if self.is_selected:
            pygame.draw.rect(screen, GREEN, (self.x * CELL_SIZE, self.y * CELL_SIZE, CELL_SIZE, CELL_SIZE))
        pygame.draw.circle(screen, color, (self.x * CELL_SIZE + CELL_SIZE // 2, self.y * CELL_SIZE + CELL_SIZE // 2), CELL_SIZE // 3)


class UnitWithHealthBar(Unit):
    def draw(self, screen):
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


class Game:
    """
    Classe principale pour gérer le jeu.
    """
    def __init__(self, screen):
        self.screen = screen


        self.player1_units = [
            UnitWithHealthBar(0, 0, health=100,max_move=3, attack_power=20, team='player1', competences=[]),
            UnitWithHealthBar(1, 0, health=80,max_move=5, attack_power=25, team='player1', competences=[])
        ]

        self.player2_units = [
            UnitWithHealthBar(6, 6, health=100,max_move=3, attack_power=15, team='player2', competences=[]),
            UnitWithHealthBar(7, 6, health=90,max_move=4, attack_power=30, team='player2', competences=[])
        ]

    def handle_player_turn(self, player_units, opponent_units, player_name):
       
        """Tour d'un joueur : déplacement et choix de zone pour attaquer."""
        for selected_unit in player_units:
            selected_unit.remaining_move = selected_unit.max_move 
            has_acted = False
            selected_unit.is_selected = True
            self.flip_display()

            while not has_acted:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        exit()

                    if event.type == pygame.KEYDOWN:
                        dx, dy = 0, 0
                        if event.key == pygame.K_LEFT:
                            dx = -1
                        elif event.key == pygame.K_RIGHT:
                            dx = 1
                        elif event.key == pygame.K_UP:
                            dy = -1
                        elif event.key == pygame.K_DOWN:
                            dy = 1

                        selected_unit.move(dx, dy)
                        self.flip_display()
                        print(selected_unit.competences)
                        if event.key == pygame.K_s or event.key == pygame.K_SPACE:
                            if event.key == pygame.K_s:
                                i=1
                                competence = selected_unit.competences[1]
                            if event.key == pygame.K_SPACE :
                                i=0
                                competence = selected_unit.competences[0]

                            if competence.name == "Soin":
                                print(f"{player_name} utilise la compétence {competence.name} !")
                                in_targeting_mode = True
                                cx, cy = selected_unit.x, selected_unit.y  # Initialisation du curseur
                                self.flip_display_with_target(cx, cy, selected_unit, competence)

                                while in_targeting_mode:
                                    for target_event in pygame.event.get():
                                        if target_event.type == pygame.QUIT:
                                            pygame.quit()
                                            exit()

                                        if target_event.type == pygame.KEYDOWN:
                         # Déplacement du curseur de ciblage
                                            if target_event.key == pygame.K_LEFT and cx > 0:
                                                cx -= 1
                                            elif target_event.key == pygame.K_RIGHT and cx < GRID_SIZE - 1:
                                                cx += 1
                                            elif target_event.key == pygame.K_UP and cy > 0:
                                                cy -= 1
                                            elif target_event.key == pygame.K_DOWN and cy < GRID_SIZE - 1:
                                                cy += 1


                                            if abs(cx - selected_unit.x) > competence.range:
                                                if cx > selected_unit.x:
                                                        cx -= (cx - selected_unit.x - competence.range)
                                                elif cx < selected_unit.x:
                                                        cx += (selected_unit.x - cx - competence.range)

                                            if abs(cy - selected_unit.y) > competence.range:
                                                if cy > selected_unit.y:
                                                        cy -= (cy - selected_unit.y - competence.range)
                                                elif cy < selected_unit.y:
                                                        cy += (selected_unit.y - cy - competence.range)


                                            self.flip_display_with_target(cx, cy, selected_unit, competence)

                    # Validation de la cible et application du soin
                                            if target_event.key == pygame.K_RETURN:
                                                has_acted = True
                                                in_targeting_mode = False
                                                                                                          
                                                selected_unit.is_selected = False
                                                for ally in player_units:
                                                    if ally.x == cx and ally.y == cy:
                                                        if abs(selected_unit.x - cx) <= competence.range and abs(selected_unit.y - cy) <= competence.range:
                                                            heal(selected_unit, ally, player_units)
                                                            has_acted = True
                                                            in_targeting_mode = False
                                                                                                          
                                                            selected_unit.is_selected = False

                                                
                                                            break
                            else :
                                    if selected_unit.competences:
                                        competence = selected_unit.competences[i]
                                        print(f"{player_name} utilise la compétence : {competence.name}")
                                        in_targeting_mode = True
                                        cx, cy = selected_unit.x, selected_unit.y

                                    while in_targeting_mode:
                                        self.flip_display_with_target(cx, cy, selected_unit, competence)

                                        for target_event in pygame.event.get():
                                            if target_event.type == pygame.QUIT:
                                                pygame.quit()
                                                exit()

                                            if target_event.type == pygame.KEYDOWN:
                                                if target_event.key == pygame.K_LEFT:
                                                    cx -= 1
                                                elif target_event.key == pygame.K_RIGHT:
                                                    cx += 1
                                                elif target_event.key == pygame.K_UP:
                                                    cy -= 1
                                                elif target_event.key == pygame.K_DOWN:
                                                    cy += 1
                                                for dx, dy in competence.area:

                                                    target_x = cx + dx
                                                    target_y = cy + dy
                                                    if abs(target_x - selected_unit.x) > competence.range:
                                                        if target_x > selected_unit.x:
                                                            cx -= (target_x - selected_unit.x - competence.range)
                                                        elif target_x < selected_unit.x:
                                                            cx += (selected_unit.x - target_x - competence.range)

                                                    if abs(target_y - selected_unit.y) > competence.range:
                                                        if target_y > selected_unit.y:
                                                            cy -= (target_y - selected_unit.y - competence.range)
                                                        elif target_y < selected_unit.y:
                                                            cy += (selected_unit.y - target_y - competence.range)
                                            if target_event.type == pygame.KEYDOWN and target_event.key == pygame.K_RETURN:
                                                print(f"Zone ciblée : ({cx}, {cy})")
                                                selected_unit.attack_zone(cx, cy, opponent_units, competence)
                                                has_acted = True
                                                selected_unit.is_selected = False
                                                in_targeting_mode = False                                                        


    def flip_display(self):
        """Affiche le jeu."""
        self.screen.fill(BLACK)

        for x in range(0, WIDTH, CELL_SIZE):
            for y in range(0, HEIGHT, CELL_SIZE):
                rect = pygame.Rect(x, y, CELL_SIZE, CELL_SIZE)
                pygame.draw.rect(self.screen, WHITE, rect, 1)

        for unit in self.player1_units + self.player2_units:
            unit.draw(self.screen)

        pygame.display.flip()

    def flip_display_with_target(self, cx, cy, unit, competence):
        """Affiche le jeu avec le curseur de ciblage et la portée de l'attaque."""
        self.screen.fill(BLACK)

        for x in range(0, WIDTH, CELL_SIZE):
            for y in range(0, HEIGHT, CELL_SIZE):
                rect = pygame.Rect(x, y, CELL_SIZE, CELL_SIZE)
                pygame.draw.rect(self.screen, WHITE, rect, 1)

        for dx in range(-competence.range, competence.range + 1):
            for dy in range(-competence.range, competence.range + 1):
                if 0 <= unit.x + dx < GRID_SIZE and 0 <= unit.y + dy < GRID_SIZE:
                    rect = pygame.Rect((unit.x + dx) * CELL_SIZE, (unit.y + dy) * CELL_SIZE, CELL_SIZE, CELL_SIZE)
                    pygame.draw.rect(self.screen, (50, 50, 200), rect, 1)

        for u in self.player1_units + self.player2_units:
            u.draw(self.screen)

        for dx, dy in competence.area:
            tx, ty = cx + dx, cy + dy
            if 0 <= tx < GRID_SIZE and 0 <= ty < GRID_SIZE:
                rect = pygame.Rect(tx * CELL_SIZE, ty * CELL_SIZE, CELL_SIZE, CELL_SIZE)
                pygame.draw.rect(self.screen, RED, rect, 2)

        rect = pygame.Rect(cx * CELL_SIZE, cy * CELL_SIZE, CELL_SIZE, CELL_SIZE)
        pygame.draw.rect(self.screen, RED, rect, 3)

        pygame.display.flip()
class CompetenceSelector:
    """
    Classe pour gérer la sélection des compétences pour les unités.
    """
    def __init__(self, screen, available_competences, font_size=36):
        """
        Initialise le sélecteur de compétences.
        
        Paramètres :
        - screen : Surface Pygame pour l'affichage.
        - available_competences : Liste des compétences disponibles.
        - font_size : Taille de la police utilisée pour afficher le texte.
        """
        self.screen = screen
        self.available_competences = available_competences
        self.font = pygame.font.Font(None, font_size)

    def choose_competences(self, units, player_name):
        """
        Permet au joueur de choisir des compétences pour chaque unité.
        
        Paramètres :
        - units : Liste des unités du joueur.
        - player_name : Nom du joueur.
        """
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
                        f"{player_name} - Sélectionnez la compétence {i + 1} pour l'unité en ({unit.x}, {unit.y})", True, WHITE
                    )
                    self.screen.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, 50))
                    pathimage="NarutoChoose.jpg"
                    unitimage1=pygame.image.load(pathimage)
                    unitimage = pygame.transform.scale(unitimage1, (700, 1200))
                    image_rect = unitimage.get_rect(center=(WIDTH // 2, 150))
                    self.screen.blit(unitimage, image_rect)
                    # Afficher les compétences disponibles
                    for index, competence in enumerate(self.available_competences):
                        color = GREEN if index == selected_index else WHITE
                        competence_text = self.font.render(
                            f"{competence.name} - Portée: {competence.range}", True, color
                        )
                        self.screen.blit(competence_text, (100, 150 + index * 40))

                    pygame.display.flip()

                    # Gérer les événements
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


    

if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Jeu Player 1 vs Player 2")

    game = Game(screen)

    # Compétences disponibles
    explosion = Competence(name="Explosion", range=2, area=[(0, 0), (1, 0), (0, 1), (1, 1)])
    tir_precis = Competence(name="Tir précis", range=4, area=[(0, 0)])
    soin = Competence(name="Soin", range=1, area=[(0, 0)])
    competences_disponibles = [explosion, tir_precis, soin]

    # Initialisation du sélecteur de compétences
    competence_selector = CompetenceSelector(screen, competences_disponibles)

    # Sélection des compétences pour Player 1
    competence_selector.choose_competences(game.player1_units, "Player 1")

    # Sélection des compétences pour Player 2
    competence_selector.choose_competences(game.player2_units, "Player 2")

    # Lancer le jeu
    while True:
        game.handle_player_turn(game.player1_units, game.player2_units, "Player 1")
        game.handle_player_turn(game.player2_units, game.player1_units, "Player 2")
