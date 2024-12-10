import pygame
import random
from unit import*




class Game:
    def __init__(self, screen):
        """
        Initialise le jeu avec une surface de fenêtre et les unités.
        """
        self.screen = screen
        self.turn = 'player'  # le joueur commence le tours
        self.enemy_turn_index = 0  # L'indice de l'ennemi qui va jouer en premier(0, 1, 2)

        # Créer mes 3 joueurs avec leurs types
        self.players = [
            Player(0, 0, "naruto"),
            Player(1, 0, "uchiwa"),
            Player(2, 0, "haruno")
        ]

        # Créer les ennemis avec les images personnalisées
        self.enemies = [
            Enemy(7, 7, "itachi"),
            Enemy(8, 7, "madara"),
            Enemy(9, 7, "zabuza")
        ]

        # Combiner tous les personnages
        self.units = self.players + self.enemies

    def get_move(self, event):
        """Gère les déplacements des joueur"""
        if event.type == pygame.KEYDOWN and self.turn == 'player':
            # le 1er joueur deplace avec les touche( H:gauche, K:droite, U:haut, N:bas)
            if event.key == pygame.K_h:
                self.players[0].move(-1, 0)
            elif event.key == pygame.K_k:
                self.players[0].move(1, 0)
            elif event.key == pygame.K_u:
                self.players[0].move(0, -1)
            elif event.key == pygame.K_n:
                self.players[0].move(0, 1)

            # le 2eme joueur deplace avec les touche( 1:gauche, 2:droite, 3:haut, 4:bas)
            elif event.key == pygame.K_1:
                self.players[1].move(-1, 0)
            elif event.key == pygame.K_2:
                self.players[1].move(1, 0)
            elif event.key == pygame.K_3:
                self.players[1].move(0, -1)
            elif event.key == pygame.K_4:
                self.players[1].move(0, 1)

            # le 3eme joueur deplace avec les fléches
            elif event.key == pygame.K_LEFT:
                self.players[2].move(-1, 0)
            elif event.key == pygame.K_RIGHT:
                self.players[2].move(1, 0)
            elif event.key == pygame.K_UP:
                self.players[2].move(0, -1)
            elif event.key == pygame.K_DOWN:
                self.players[2].move(0, 1)

            # gestion de tour
            self.turn = 'enemy'  # les joueur et les ennemis jouent par tours

    def move_enemy(self, enemy):
        """Déplacement des ennemis de manière aléatoire."""
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        dx, dy = random.choice(directions)
        enemy.move(dx, dy)

    def update_enemy_positions(self):
        """la mise a jour de la position des ennemis"""
        if self.enemy_turn_index < len(self.enemies):
            enemy = self.enemies[self.enemy_turn_index]
            self.move_enemy(enemy)

    def next_enemy_turn(self):
        """Passe au tour suivant pour l'ennemi."""
        self.enemy_turn_index += 1
        if self.enemy_turn_index >= len(self.enemies):
            self.enemy_turn_index = 0  # Recommence à partir du premier ennemi

    def flip_display(self):
        """Affiche le jeu."""
        self.screen.fill(BLACK)

        # Affiche la grille
        for x in range(0, WIDTH, CELL_SIZE):
            for y in range(0, HEIGHT, CELL_SIZE):
                rect = pygame.Rect(x, y, CELL_SIZE, CELL_SIZE)
                pygame.draw.rect(self.screen, WHITE, rect, 1)

        # Affiche les unités
        for unit in self.units:
            unit.draw(self.screen)

        pygame.display.flip()

    def handle_enemy_turn(self):
        """Permet aux ennemis de jouer un à un après le tour du joueur."""
        if self.turn == 'enemy':
            self.update_enemy_positions()
            self.next_enemy_turn()  # Passe à l'ennemi suivant après son mouvement
            self.turn = 'player'  # Après que tous les ennemis aient joué, on passe au tour du joueur


# Fonction principale
def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Mon jeu de stratégie")

    game = Game(screen)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            # Si c'est le tour du joueur, on gère les déplacements
            game.get_move(event)

        # Si c'est le tour des ennemis, on les fait jouer un à un
        game.handle_enemy_turn()

        # Affiche les nouvelles positions des unités
        game.flip_display()

        

    pygame.quit()


if __name__ == "__main__":
    main()