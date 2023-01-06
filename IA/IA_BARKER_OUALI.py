##############################################################################
# votre IA : à vous de coder
# Rappel : ne pas changer les paramètres des méthodes
# vous pouvez ajouter librement méthodes, fonctions, champs, ...
##############################################################################

import random
FICHIERRECAP = True
class IA_Diamant:
    def __init__(self, match : str):
        """génère l'objet de la classe IA_Diamant

        Args:
            match (str): decriptif de la partie
        """
        # self.ecrire_fichier('\n'+match)
        with open('IA/exit.txt', 'w') as f:
                f.write('\n'+match)
        self.coffre = 0  # nombre de diamants que l'IA à sécurisé
        self.diamant_tmp = 0  # nombre de diamants temporaires que l'IA a récupéré pendant l'exploration

    def action(self, tour : str) -> str:
        """Appelé à chaque décision du joueur IA

        Args:
            tour (str): descriptif du dernier tour de jeu

        Returns:
            str: 'X' ou 'R'
        """
        self.ecrire_fichier(tour)
        
        if len(tour) != 0:  # Vérifie que le tour est valide
            info = tour.split('|')
            # Récupère le choix des IA
            ia_choix = info[0].split(',')
            choix = ia_choix[0]
            
            try:  # Vérifie que la carte est bien un trésor
                if choix == 'X':  # Vérifie que l'IA reste
                    # Compte le nombre d'IA explorant
                    nombre_explorant = 0
                    for ia in ia_choix:
                        if ia == 'X':
                            nombre_explorant += 1

                    # Ajoute les diamants à l'IA dans ses 'poches'
                    carte = int(info[1])
                    self.diamant_tmp += (carte//nombre_explorant)
                    self.ecrire_fichier('POCHES : '+str(self.diamant_tmp))
            except:  # Passe outre de l'erreur
                pass

        if random.randint(0,1) == 0:
            return 'X'
        else:
            return 'R'

    def fin_de_manche(self, raison : str, dernier_tour : str) -> None:
        """Appelé à chaque fin de manche

        Args:
            raison (str): 'R' si tout le monde est un piège ou "P1","P2",... si un piège a été déclenché
            dernier_tour (str): descriptif du dernier tour de la manche
        """
        # Vérifie que l'IA était sorti et lui ajoute ses diamants dans son coffre
        if dernier_tour[0]!='X':
            self.coffre += self.diamant_tmp
        self.ecrire_fichier(dernier_tour)
        self.ecrire_fichier(raison)
        self.ecrire_fichier('POCHES : '+str(self.diamant_tmp))
        self.ecrire_fichier('COFFRE : '+str(self.coffre))
        
        # Remet les diamants temporaires à 0
        self.diamant_tmp = 0

    def game_over(self, scores : str) -> None:
        """Appelé à la fin du jeu ; sert à ce que vous voulez

        Args:
            scores (str): descriptif des scores de fin de jeu
        """
        with open('IA/exit.txt', 'a') as f:
            f.write('END\n'+scores)

    def ecrire_fichier(self, data):
        if FICHIERRECAP:
            with open('IA/exit.txt', 'a') as f:
                f.write(str(data)+'\n')