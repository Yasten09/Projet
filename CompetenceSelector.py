
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
                    if unit.character_type=="naruto":
                        pathimage="MenuChoix/NarutoChoose.jpg"
                    if unit.character_type=="uchiwa":
                        pathimage="MenuChoix/UchiwaChoose.jpg"
                    if unit.character_type=="haruno":
                        pathimage= "MenuChoix/HarunoChoose.jpg"    
                    if unit.character_type=="itachi": 
                        pathimage= "MenuChoix/ItachiChoose.jpg" 
                    if unit.character_type=="madara": 
                        pathimage= "MenuChoix/MadaraChoose.png"    
       

                    
                    
                    unitimage1=pygame.image.load(pathimage)
                    unitimage = pygame.transform.scale(unitimage1, (1000, 1000))
                    image_rect = unitimage.get_rect(center=(WIDTH // 2, 150*3))
                    self.screen.blit(unitimage, image_rect)
                    self.screen.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, 50))
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
            if unit.competences[0].name=="Fast Move":
                unit.competences=unit.competences[::-1]