##############################################################################
# IA qui explore toujours !                                                  #
##############################################################################

import random

class IA_Diamant:
    def __init__(self, match : str):
        """génère l'objet de la classe IA_Diamant

        Args:
            match (str): decriptif de la partie
        """

        #laissez ou supprimez
        print("IA temeraire reçoit match = '" + match + "'")

    def action(self, tour : str) -> str:
        """Appelé à chaque décision du joueur IA

        Args:
            tour (str): descriptif du dernier tour de jeu

        Returns:
            str: 'X' ou 'R'
        """

        #laissez ou supprimez
        print("    IA temeraire reçoit tour = '" + tour + "'")


        return 'X'
        

    def fin_de_manche(self, raison : str, dernier_tour : str) -> None:
        """Appelé à chaque fin de manche

        Args:
            raison (str): 'R' si tout le monde est un piège ou "P1","P2",... si un piège a été déclenché
            dernier_tour (str): descriptif du dernier tour de la manche
        """

        #laissez ou supprimez
        print("  IA temeraire reçoit en fin de manche raison = '" + raison + "' et dernier_tour = '" + dernier_tour + "'" )


    def game_over(self, scores : str) -> None:
        """Appelé à la fin du jeu ; sert à ce que vous voulez

        Args:
            scores (str): descriptif des scores de fin de jeu
        """

        #laissez ou supprimez
        print("IA temeraire reçoit en fin de jeu scores = '" + scores +"'")

