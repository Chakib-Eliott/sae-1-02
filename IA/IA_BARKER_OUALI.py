##############################################################################
# votre IA : à vous de coder
# Rappel : ne pas changer les paramètres des méthodes
# vous pouvez ajouter librement méthodes, fonctions, champs, ...
##############################################################################

import random

class IA_Diamant:
    def __init__(self, match : str):
        """génère l'objet de la classe IA_Diamant

        Args:
            match (str): decriptif de la partie
        """
        pass

    def action(self, tour : str) -> str:
        """Appelé à chaque décision du joueur IA

        Args:
            tour (str): descriptif du dernier tour de jeu

        Returns:
            str: 'X' ou 'R'
        """

        ##############################
        #ICI il FAUT compléter !     #
        ##############################
        pass

    def fin_de_manche(self, raison : str, dernier_tour : str) -> None:
        """Appelé à chaque fin de manche

        Args:
            raison (str): 'R' si tout le monde est un piège ou "P1","P2",... si un piège a été déclenché
            dernier_tour (str): descriptif du dernier tour de la manche
        """
        pass

    def game_over(self, scores : str) -> None:
        """Appelé à la fin du jeu ; sert à ce que vous voulez

        Args:
            scores (str): descriptif des scores de fin de jeu
        """
        pass
