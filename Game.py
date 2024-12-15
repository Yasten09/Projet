
#from UnitWithHealthBar import *
from unit import *
#from FastMove import *
from CompetenceSelector import *
from CharacterSelectionMenu import *
from Competence import *


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

#Case innaccessible 
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




# Cases où les unités sont protégées

SHELTER_TILES = [(3, 1), (3, 5), (6, 6), (1, 2), (2, 1), (4, 3), (15, 3), (13, 3), (5, 9), (9, 6),(12,12),(12,14),(14,10)]

# Cases qui réduisent la santé
DAMAGE_TILES = [(3, 3), (5, 5), (2, 8), (2, 15), (1, 15), (3, 8), (12, 8), (13, 15), (13, 2), (13, 5), (8, 4), (6, 9)]
DAMAGE_AMOUNT = 10  # Quantité de santé retirée

# Liste des cases en feu
active_fire_tiles = []


# Charger l'image de feu
fire_image = pygame.image.load("images/feu.png")
fire_image = pygame.transform.scale(fire_image, (CELL_SIZE, CELL_SIZE))


safe_image = pygame.image.load("images/safe.webp")
safe_image = pygame.transform.scale(safe_image, (CELL_SIZE, CELL_SIZE))




class Game:
    """
    Classe principale pour gérer le jeu.
    """
    def __init__(self, screen):
        self.screen = screen
        self.winner = None # Variable pour stocker l'équipe gagnante
        self.gameover=0


        # Définition des compétences
        explosion = Competence(name="Explosion", range=2, area=[(0, 0), (1, 0), (0, 1), (1, 1)],attack_power=20)
        fast_move = FastMove()

        # Initialisation des unités des deux joueurs
        self.player1_units = [
            UnitWithHealthBar(0, 0, health=100, max_health=100,remaining_move=6,  team='player1', character_type="Naruto", competences=[],max_move=6),
            #UnitWithHealthBar(1, 0, health=80, max_health=100,remaining_move=7,  team='player1', character_type="Sassuke", competences=[tir_precis],max_move=5),
             UnitWithHealthBar(2, 0, health=80, max_health=100,remaining_move=6,  team='player1', character_type="Sassuke", competences=[],max_move=6)                 
        ]

        self.player2_units = [
            UnitWithHealthBar(6, 6, health=100, max_health=100,remaining_move=6,  team='player2', character_type="Sakura", competences=[],max_move=6),
            #UnitWithHealthBar(7, 6, health=90, max_health=100,remaining_move=3, , team='player2', character_type="Madara", competences=[tir_precis],max_move=4),
             UnitWithHealthBar(5, 6, health=80, max_health=100,remaining_move=6,  team='player2', character_type="Sassuke", competences=[],max_move=6)
        ]

        # Chargement de la carte Tiled (.tmx)
        try:
            self.tmx_data = pytmx.load_pygame("map2.tmx")  # Remplacez par le chemin de votre fichier .tmx
        except Exception as e:
            print(f"Erreur lors du chargement de la carte : {e}")
            self.tmx_data = None
    def select_game_mode(screen):
        """Affiche un menu pour sélectionner le mode de jeu."""
        pygame.mixer.init()  # Initialiser le module audio
        font = pygame.font.Font(None, 48)
        options = ["1. Player vs Player", "2. Player vs IA"]
        selected_option = 0 # Charger l'image de fond
        mode_image = pygame.image.load("mode2.png")  
        mode_image = pygame.transform.scale(mode_image, (WIDTH, HEIGHT))  # Ajuster à la taille de l'écran
        
        pygame.mixer.music.load("mode.mp3")  
        pygame.mixer.music.play(-1)  # Joue en boucle (-1)




        while True:
            screen.fill(BLACK)
            if mode_image:
                screen.blit(mode_image, (0, 0))
            for i, option in enumerate(options):
                color = (255,0, 0) if i == selected_option else WHITE
                text = font.render(option, True, color)
                # pour que le text au debut soit visible on ajoute un fond qui un est un rectangle 
                rect_x = WIDTH // 2 - text.get_width() // 2 - 10 
                rect_y = HEIGHT // 2 - 100 + i * 50 - 5
                rect_width = text.get_width() + 20
                rect_height = text.get_height() + 10

                # Créer une surface pour le fond 
                bg_surface = pygame.Surface((rect_width, rect_height))
                bg_surface.set_alpha(128)  # Transparence (0 = transparent, 255 = opaque)
                bg_surface.fill((0, 0, 0))  # Fond noir
                screen.blit(bg_surface, (rect_x, rect_y))  # Afficher le fond

                # Afficher le texte par-dessus le fond
                screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - 100 + i * 50))

            pygame.display.flip()
    
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP and selected_option > 0:
                        selected_option -= 1
                    elif event.key == pygame.K_DOWN and selected_option < len(options) - 1:
                        selected_option += 1
                    elif event.key == pygame.K_RETURN:
                        pygame.mixer.music.stop() 
                        return selected_option + 1  # 1 pour PvP, 2 pour PvIA
    def check_game_over(self):
        """Vérifie si le jeu est terminé et déclare un gagnant."""
        if self.is_player_eliminated(self.player1_units):
            self.winner = "Player 2"  # Player 2 gagne
            self.gameover=1
            print("we have a winner")
        elif self.is_player_eliminated(self.player2_units):
            self.winner = "Player 1"  # Player 1 gagne
            self.gameover=1
            print("we have a winner")    
        self.display_winner()
    
    def is_player_eliminated(self, player_units):
        """Vérifie si toutes les unités du joueur sont éliminées."""
        return all(unit.health <= 0 for unit in player_units)
    
    def display_winner(self):
        """Affiche l'équipe gagnante."""
        if self.winner:
            
            pygame.mixer.init()
            pygame.mixer.music.load("fin.mp3") 
            pygame.mixer.music.play()

            
            self.screen.fill((0, 0, 0))

                

            font = pygame.font.Font(None, 36)
            winner_text = font.render(f"{self.winner} wins!", True, (255, 255, 255))
            self.screen.blit(winner_text, (WIDTH // 2 - winner_text.get_width() // 2, HEIGHT // 2))
            pygame.display.flip()
            pygame.time.wait(3000)  # Attendre 3 secondes avant de quitter
            pygame.quit()
            exit()

    def handle_player_turn(self, player_units, opponent_units, player_name):
        """Tour d'un joueur : déplacement et choix de zone pour attaquer."""
        if self.is_player_eliminated(player_units):
            self.check_game_over()
            print(f"{player_name} est éliminé, il ne peut plus jouer.")
        if self.is_player_eliminated(opponent_units):
            self.check_game_over    

            
            return
        for selected_unit in player_units:
            if selected_unit.health <= 0:  # Si l'unité est éliminée, passez à la suivante
                continue
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
                        if event.key in [pygame.K_LEFT,pygame.K_RIGHT,pygame.K_UP,pygame.K_DOWN]:

                            if event.key == pygame.K_LEFT:
                                dx = -1
                            elif event.key == pygame.K_RIGHT:
                                dx = 1
                            elif event.key == pygame.K_UP:
                                dy = -1
                            elif event.key == pygame.K_DOWN:
                                dy = 1
                            if any(isinstance(comp, FastMove) for comp in selected_unit.competences):
                                fast_move = next(comp for comp in selected_unit.competences if isinstance(comp, FastMove))
                                fast_move.apply(selected_unit, dx, dy)  # Applique le déplacement de 3 cases
                            else:
                                isFastMove=False
                                selected_unit.move(dx, dy,isFastMove)


                            self.flip_display()
                        if event.key == pygame.K_s or event.key == pygame.K_SPACE:
                            if (selected_unit.x, selected_unit.y) in SHELTER_TILES:
                                print(f"L'unité {selected_unit.character_type} est dans un abri et ne peut pas attaquer.")
                                has_acted = True
                                selected_unit.is_selected = False
                                continue
                            if event.key == pygame.K_s and selected_unit.competences:
                                if selected_unit.competences[1].name in ("Tir précis","Explosion","Soin","Fusil") :
                                    competence = selected_unit.competences[1]
                                    i=1
                                else :
                                    competence = selected_unit.competences[0]
                                    i=0
                            elif event.key == pygame.K_SPACE: 
                                if selected_unit.competences[0].name in  ("Tir précis","Explosion","Soin","Fusil") :
                                    i=0
                                    competence = selected_unit.competences[0]
                                else:
                                    competence = selected_unit.competences[1]   
                                    i=1 
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
                                                    if ally!=selected_unit:
                                                        if ally.x == cx and ally.y == cy:
                                                            if abs(selected_unit.x - cx) <= competence.range and abs(selected_unit.y - cy) <= competence.range:
                                                                selected_unit.heal(selected_unit, ally)
                                                            
                                                                has_acted = True
                                                                in_targeting_mode = False
                                                                                                          
                                                                selected_unit.is_selected = False

                                                
                                                            break
                            elif competence.name == "Explosion" or competence.name == "Tir précis" or competence.name=="Fusil":
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

                            else : 
                                                                                                  
                                    has_acted = True
                                    selected_unit.is_selected = False
                            
                                    in_targeting_mode = False 
    def find_valid_move(self, enemy, target):
        """Trouve un mouvement valide pour l'ennemi en direction de la cible, contournant les obstacles."""
        possible_moves = [
            (1, 0),   # Droite
            (-1, 0),  # Gauche
            (0, 1),   # Bas
            (0, -1)   # Haut
        ]

        # Trie les mouvements par proximité à la cible
        possible_moves.sort(key=lambda move: abs(enemy.x + move[0] - target.x) + abs(enemy.y + move[1] - target.y))

        # Cherche un mouvement valide
        for dx, dy in possible_moves:
            new_x = enemy.x + dx
            new_y = enemy.y + dy
            if (0 <= new_x < GRID_SIZE and 0 <= new_y < GRID_SIZE) and (new_x, new_y) not in INACCESSIBLE_TILES:
                return dx, dy

        # Aucun mouvement valide trouvé
        return 0, 0
                                
    def handle_enemy_turn(self):
        

        # Dessiner la grille
        for x in range(0, WIDTH, CELL_SIZE):
            for y in range(0, HEIGHT, CELL_SIZE):
                rect = pygame.Rect(x, y, CELL_SIZE, CELL_SIZE)
                pygame.draw.rect(self.screen, WHITE, rect, 1)
        """IA pour les ennemis : les ennemis se déplacent et attaquent avec une compétence si une cible est à portée."""
        for enemy in self.player2_units[:]:  # Parcourt une copie pour éviter les problèmes de suppression
            if self.is_player_eliminated(self.player2_units):
                print(f"player 2 est éliminé, il ne peut plus jouer.")    
                self.check_game_over()
                return
            if self.is_player_eliminated(self.player1_units):
                self.check_game_over()
                return
            enemy.remaining_move = enemy.max_move 
            move_restant=enemy.max_move 
            while move_restant>0:
            # Choisir la cible la plus proche parmi les unités du joueur
                target = min(self.player1_units, key=lambda unit: abs(unit.x - enemy.x) + abs(unit.y - enemy.y))
                dx, dy = self.find_valid_move(enemy, target)
                if dx == 0 and dy == 0:
                    break
                enemy.move(dx, dy)
                
                move_restant-=1
            # Calcul de la distance entre l'ennemi et la cible
            distance_to_friend=float('inf')
            distance_to_target = abs(enemy.x - target.x) + abs(enemy.y - target.y)
            #Ami le plus proche
            

            for amiproche in self.player2_units[:]:
                if enemy!=amiproche:
                    dis=abs(enemy.x - amiproche.x) + abs(enemy.y - amiproche.y)
                    if dis<distance_to_friend:
                        distance_to_friend=dis
                        closest_ami=amiproche
            
            # Si la cible n'est pas à portée, se rapprocher

            self.flip_display()
         
           
            if (enemy.x, enemy.y) in SHELTER_TILES:
                print(f"L'unité {enemy.character_type} est dans un abri et ne peut pas attaquer.")
                has_acted = True
                enemy.is_selected = False
                continue
            # Attaquer avec une compétence si possible
            if enemy.competences:
                if enemy.competences[0].name !="Soin" and enemy.competences[1].name != "Soin":
                    closest_x = target.x
                    closest_y = target.y
                    competence0 = enemy.competences[0]
                    competence1 = enemy.competences[1] 
                    comp_utilise=competence0 #par defaut
                    if distance_to_target > enemy.competences[0].range or distance_to_target > enemy.competences[1].range:
                        if distance_to_target > enemy.competences[0].range:
                            comp_utilise=competence0
                        elif distance_to_target > enemy.competences[1].range:
                            comp_utilise=competence1
                        
                
                        print(f"L'ennemi {enemy.team} utilise {comp_utilise.name} sur une cible proche.")

                    # Afficher la zone d'attaque de l'ennemi en rouge pendant qu'il se prépare à attaquer

                    
                    else:
                        # Frapper à la zone la plus proche de la cible


                        if abs(enemy.x - target.x) > comp_utilise.range:
                            closest_x = enemy.x + (comp_utilise.range if enemy.x < target.x else -comp_utilise.range)

                        if abs(enemy.y - target.y) > comp_utilise.range:
                            closest_y = enemy.y + (comp_utilise.range if enemy.y < target.y else -comp_utilise.range)

                        print(f"L'ennemi {enemy.team} attaque la zone la plus proche de la cible ({closest_x}, {closest_y}).")

                    if abs(closest_x - enemy.x) > comp_utilise.range:
                        if closest_x > enemy.x:
                                closest_x -= (closest_x - enemy.x - comp_utilise.range)
                        elif closest_x < enemy.x:
                                closest_x += (enemy.y - closest_x - comp_utilise.range)

                    if abs(closest_y - enemy.y) > comp_utilise.range:
                        if closest_y > enemy.y:
                                closest_y -= (closest_y - enemy.y - comp_utilise.range)
                        elif closest_x < enemy.x:
                                closest_y += (enemy.y - closest_y - comp_utilise.range)


                    self.flip_display_with_enemy_target(enemy, comp_utilise, [closest_x, closest_y])
                    enemy.attack_zone(closest_x, closest_y, self.player1_units, comp_utilise)
                elif enemy.competences[0].name=="Soin" or enemy.competences[1].name == "Soin":
                    if enemy.competences[0].name=="Soin":
                        comp_sante=enemy.competences[0]
                        comp_attack=enemy.competences[1]
                    else: 
                        comp_sante=enemy.competences[1]
                        comp_attack=enemy.competences[0]  
                    print(enemy.competences[0].name,enemy.competences[1].name)    
                    # Verifier si l'enemy est a la porté on applique la competence d'attaque sinon on applique la santé    
                    if distance_to_target < comp_attack.range:
                        self.flip_display_with_enemy_target(enemy, comp_attack, [target.x, target.y])
                        enemy.attack_zone(target.x, target.y, self.player1_units, comp_attack)    
                    elif  closest_ami.health<30:
                         self.flip_display_with_enemy_target(enemy, comp_sante, [closest_ami.x, closest_ami.y])
                         enemy.heal(enemy,closest_ami)                      
                    else:
                        # Frapper à la zone la plus proche de la cible
                        closest_x=target.x
                        closest_y=target.y
                        comp_utilise=comp_attack

                        

                        if abs(closest_x - enemy.x) > comp_utilise.range:
                            if closest_x > enemy.x:
                                closest_x -= (closest_x - enemy.x - comp_utilise.range)
                            elif closest_x < enemy.x:
                                  closest_x += (enemy.y - closest_x - comp_utilise.range)

                        if abs(closest_y - enemy.y) > comp_utilise.range:
                            if closest_y > enemy.y:
                                closest_y -= (closest_y - enemy.y - comp_utilise.range)
                            elif closest_x < enemy.x:
                                closest_y += (enemy.y - closest_y - comp_utilise.range)
                        print(f"L'ennemi {enemy.team} attaque la zone la plus proche de la cible ({closest_x}, {closest_y}).")        
                        self.flip_display_with_enemy_target(enemy, comp_utilise, [closest_x,closest_y])
                        enemy.attack_zone(closest_y, closest_y, self.player1_units, comp_utilise)            

                   

                time.sleep(2) # Pause de 2 secondes pour visualiser l'attaque

            # Vérifie si la cible a été éliminée
            for target in self.player1_units[:]:
                if target.health <= 0:
                    print(f"L'unité du joueur en position ({target.x}, {target.y}) est éliminée.")
                    self.player1_units.remove(target)
                    

    def flip_display_with_enemy_target(self, enemy, competence, target):
        """Affiche le jeu avec le curseur de ciblage et la portée de l'attaque de l'ennemi."""
        

        
        # Afficher la portée de la compétence
        for dx in range(-competence.range, competence.range + 1):
            for dy in range(-competence.range, competence.range + 1):
                if 0 <= enemy.x + dx < GRID_SIZE and 0 <= enemy.y + dy < GRID_SIZE:
                    rect = pygame.Rect((enemy.x + dx) * CELL_SIZE, (enemy.y + dy) * CELL_SIZE, CELL_SIZE, CELL_SIZE)
                    pygame.draw.rect(self.screen, (50, 50, 200), rect, 1)  # Bleu clair pour la portée

        # Dessiner les unités
        for u in self.player1_units + self.player2_units:
            u.draw(self.screen)

        # Dessiner la zone d'attaque de l'ennemi en rouge
        for dx, dy in competence.area:
            tx, ty = target[0] + dx, target[1] + dy  # Coordonnées des cases affectées
            if 0 <= tx < GRID_SIZE and 0 <= ty < GRID_SIZE:
                rect = pygame.Rect(tx * CELL_SIZE, ty * CELL_SIZE, CELL_SIZE, CELL_SIZE)
                pygame.draw.rect(self.screen, RED, rect, 2)  # Rouge pour la zone d'attaque

        # Dessiner le curseur de ciblage de l'ennemi
        rect = pygame.Rect(target[0] * CELL_SIZE, target[1] * CELL_SIZE, CELL_SIZE, CELL_SIZE)
        pygame.draw.rect(self.screen, RED, rect, 3)  # Vert pour le curseur de ciblage

        pygame.display.flip()


    def flip_display(self):
        """Affiche le jeu avec la carte et les unités."""
        
        
        # Afficher la carte Tiled
        if self.tmx_data:
            for layer in self.tmx_data.visible_layers:
                if isinstance(layer, pytmx.TiledTileLayer):
                    for x, y, tile in layer:
                        if tile:
                            tile_image = self.tmx_data.get_tile_image_by_gid(tile)
                            if tile_image:
                                self.screen.blit(tile_image, (x * CELL_SIZE, y * CELL_SIZE))

        # Affichage des unités et de la grille


        for unit in self.player1_units + self.player2_units:
            if unit.health > 0:
               unit.draw(self.screen)

        pygame.display.flip()

    def flip_display_with_target(self, cx, cy, unit, competence):
        """Affiche le jeu avec le curseur de ciblage et la portée de l'attaque."""
        self.screen.fill(BLACK)

        # Afficher la carte Tiled
        if self.tmx_data:
            for layer in self.tmx_data.visible_layers:
                if isinstance(layer, pytmx.TiledTileLayer):
                    for x, y, tile in layer:
                        if tile:
                            tile_image = self.tmx_data.get_tile_image_by_gid(tile)
                            if tile_image:
                                self.screen.blit(tile_image, (x * CELL_SIZE, y * CELL_SIZE))



        for dx in range(-competence.range, competence.range + 1):
            for dy in range(-competence.range, competence.range + 1):
                if 0 <= unit.x + dx < GRID_SIZE and 0 <= unit.y + dy < GRID_SIZE:
                    rect = pygame.Rect((unit.x + dx) * CELL_SIZE, (unit.y + dy) * CELL_SIZE, CELL_SIZE, CELL_SIZE)
                    pygame.draw.rect(self.screen, (50, 50, 200), rect, 1)

        for u in self.player1_units + self.player2_units:
            if u.health > 0:
                u.draw(self.screen)

        for dx, dy in competence.area:
            tx, ty = cx + dx, cy + dy
            if 0 <= tx < GRID_SIZE and 0 <= ty < GRID_SIZE:
                rect = pygame.Rect(tx * CELL_SIZE, ty * CELL_SIZE, CELL_SIZE, CELL_SIZE)
                pygame.draw.rect(self.screen, RED, rect, 2)

        rect = pygame.Rect(cx * CELL_SIZE, cy * CELL_SIZE, CELL_SIZE, CELL_SIZE)
        pygame.draw.rect(self.screen, RED, rect, 3)

        pygame.display.flip()


if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Jeu Player 1 vs Player 2")

    game = Game(screen)
    game_mode =Game.select_game_mode(screen)

    # Compétences disponibles
    explosion = Competence(name="Explosion", range=3, area=[(0, 0), (1, 0), (0, 1), (1, 1)],attack_power=20)
    tir_precis = Competence(name="Tir précis", range=5, area=[(0, 0)],attack_power=15)
    Fusil= Competence(name="Fusil", range=4, area=[(0, 0),[0,1]],attack_power=25)
    soin = Competence(name="Soin", range=3, area=[(0, 0)],attack_power=0)
    fast_move=FastMove()

    available_characters = ["Naruto", "Sassuke", "Sakura", "Itachi","Madara"]
    character_images = {
        "Naruto": pygame.transform.scale(pygame.image.load("images/naruto.png"), (100, 100)),
         "Madara": pygame.transform.scale(pygame.image.load("images/madara.png"), (100, 100)),
        "Sassuke": pygame.transform.scale(pygame.image.load("images/Sassuke.png"), (100, 100)),
        "Sakura": pygame.transform.scale(pygame.image.load("images/Sakura.png"), (100, 100)),
        "Itachi": pygame.transform.scale(pygame.image.load("images/itachi.png"), (100, 100))
    }

    # Initialisation du menu de sélection des personnages
    character_menu = CharacterSelectionMenu(screen, available_characters, character_images)

    # Sélection des personnages pour chaque joueur
    player1_characters = character_menu.select_characters("Player 1")
    player2_characters = character_menu.select_characters("Player 2")
    # Assignation des personnages choisis aux unités
    for i, unit in enumerate(game.player1_units):
        unit.character_type = player1_characters[i]
        unit.image = pygame.image.load(f"images/{unit.character_type}.png")
        unit.image = pygame.transform.scale(unit.image, (CELL_SIZE, CELL_SIZE))

    for i, unit in enumerate(game.player2_units):
        unit.character_type = player2_characters[i]
        unit.image = pygame.image.load(f"images/{unit.character_type}.png")
        unit.image = pygame.transform.scale(unit.image, (CELL_SIZE, CELL_SIZE))
    competences_disponibles = [explosion, tir_precis, soin,Fusil,fast_move]

   
    competence_selector = CompetenceSelector(screen, competences_disponibles)

   
    competence_selector.choose_competences(game.player1_units, "Player 1")


    competence_selector.choose_competences(game.player2_units, "Player 2")

  
    while not game.gameover:
        game.check_game_over()
        game.handle_player_turn(game.player1_units, game.player2_units, "Player 1")
        if game_mode == 1:  # Player vs Player
            game.handle_player_turn(game.player2_units, game.player1_units, "Player 2")
        elif game_mode == 2:  # Player vs IA
            game.handle_enemy_turn()  # Tour de l'IA

