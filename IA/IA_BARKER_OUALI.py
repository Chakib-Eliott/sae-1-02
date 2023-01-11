##############################################################################
# votre IA : à vous de coder
# Rappel : ne pas changer les paramètres des méthodes
# vous pouvez ajouter librement méthodes, fonctions, champs, ...
##############################################################################

import random

FICHIERRECAP = True


def ecrire_fichier(data, data2=False):
    """Ecrit dans le fichier exit.txt les données passées en paramètre
    ou dans le fichier infos.txt.

    Args:
        data: données à écrire dans le fichier.
        data2 (bool, optional): si True, écrit dans le fichier infos.txt.
    """
    if FICHIERRECAP:
        if not data2:
            with open('IA/exit.txt', 'a') as f:
                f.write(str(data) + '\n')
        else:
            with open('IA/infos.txt', 'a') as f:
                f.write(str(data) + '\n')


class IA_Diamant:
    """Classe IA_Diamant.

    Classe qui contient les méthodes de l'IA.
    """

    def __init__(self, match: str):  # Ne pas changer les paramètres
        """génère l'objet de la classe IA_Diamant

        Args:
            match (str): decriptif de la partie
        """
        # ecrire_fichier('\n'+match)
        with open('IA/exit.txt', 'w') as f:
            f.write('\n'+match+'\n')
        self.match = match
        self.coffre = 0  # nombre de diamants que l'IA à sécurisé
        self.diamant_tmp = 0  # nombre de diamants temporaires que l'IA a récupéré pendant l'exploration
        self.reliques = []  # Liste des reliques récupérées
        self.manche = 0  # Manche actuelle
        self.piegesorties = []  # Liste des pièges sortis
        self.reliqueattente = []  # Liste des reliques en attente
        self.diamantattente = 0  # Nombre de diamants sur le tapis
        # Dictionnaire des statistiques des joueurs
        # (nombre de diamants sécurisés [int], reliques [list], nombre de diamants temporaires [int])
        self.statsjoueurs = self.generation_stat_joueur()
        self.cartesrestantes = {
            1: 1,
            2: 1,
            3: 1,
            4: 1,
            5: 2,
            7: 2,
            9: 1,
            11: 2,
            13: 1,
            14: 1,
            15: 1,
            17: 1,
            'P1': 3,
            'P2': 3,
            'P3': 3,
            'P4': 3,
            'P5': 3,
            'R5': 3,
            'R10': 2
        }  # dictionnaires des cartes restantes (carte : nombre de cartes)

    def info_manche_ia(self, tour: str) -> None:
        """Appelé à chaque action afin de récupérer les informations concernant notre IA.
        Permet d'enregistrer les informations dans les variables comme par exemple
        les diamants temporaire et relique de notre IA.

        Args :
            tour (str): descriptif du dernier tour
        """
        info = tour.split('|')
        # Récupère le choix des IA
        ia_choix = info[0].split(',')
        choix = ia_choix[0]

        if info[1] == 'R':
            if self.cartesrestantes['R5'] > 0:
                self.reliqueattente.append(5)
            else:
                self.reliqueattente.append(10)

        if choix == 'X':  # Vérifie que l'IA reste 
            # Compte le nombre d'IA explorant
            nombre_explorant = 0
            for ia in ia_choix:
                if ia == 'X':
                    nombre_explorant += 1

            # Ajoute les diamants à l'IA dans ses 'poches'

            if info[1] in [str(i) for i in range(20)]:
                carte = int(info[1])
                self.diamant_tmp += (carte//nombre_explorant)
                ecrire_fichier('POCHES : '+str(self.diamant_tmp))
        elif choix == 'R':
            entrant = list()
            i = 0
            for ia in ia_choix:
                if ia == 'R':
                    entrant.append(i)
                i += 1
            if len(entrant) == 1:
                if len(self.reliqueattente) > 0:
                    # Ajoute la relique dans les poches de l'IA
                    self.reliques.append(self.reliqueattente[0])
                    self.cartesrestantes['R'+str(self.reliqueattente[0])] -= 1

    def info_joueurs(self, tour: str) -> None:
        """Appelé à chaque action afin de récupérer les informations concernant les autres joueurs.
        Permet d'enregistrer les informations dans les variables comme par exemple
        les diamants sécurisés et reliques des autres joueurs.

        Args:
            tour (str): descriptif du dernier tour
        """
        info = tour.split('|')[0].split(',')
        for joueur in info:
            pass

    def lebonchoix(self) -> str:
        """Algorithme de décision de l'IA.
        
        Returns: 
            str: le choix de l'IA
        """
        if random.randint(0, 1) == 0:
            return 'X'
        else:
            return 'R'

    def action(self, tour: str) -> str:  # Ne pas changer les paramètres
        """Appelé à chaque décision du joueur IA

        Args:
            tour (str): descriptif du dernier tour de jeu

        Returns:
            str: 'X' ou 'R'
        """
        self.info_joueurs(tour)  # Appel la fonction pour actualiser les informations récupérés du tour.
        self.info_manche_ia(tour)  # Appel la fonction pour actualiser les informations récupérés du tour.

        ecrire_fichier(tour)

        return self.lebonchoix()

    def fin_de_manche(self, raison: str, dernier_tour: str) -> None:  # Ne pas changer les paramètres
        """Appelé à chaque fin de manche

        Args:
            raison (str): 'R' si tout le monde est un piège ou "P1","P2",... si un piège a été déclenché
            dernier_tour (str): descriptif du dernier tour de la manche
        """
        # Vérifie que l'IA était sorti et lui ajoute ses diamants dans son coffre
        if dernier_tour[0] != 'X':
            self.coffre += self.diamant_tmp
        # Retire les cartes pièges qui sont sortis
        if raison != 'R':
            self.cartesrestantes[raison] -= 1

        derniere_action = dernier_tour.split('|')[0].split(',')
        for i in range(1, int(self.match.split('|')[1])):
            if derniere_action[i] != 'X':
                self.statsjoueurs[i][0] = self.statsjoueurs[i][2]

        ecrire_fichier(dernier_tour)
        ecrire_fichier(raison)
        ecrire_fichier('POCHES : '+str(self.diamant_tmp))
        ecrire_fichier('COFFRE : '+str(self.coffre))
        ecrire_fichier('FIN DE MANCHE')
        # Remet les diamants temporaires à 0
        self.diamant_tmp = 0
        self.manche += 1

        # Remet à 0 les diamants temporaires des joueurs
        for i in range(1, int(self.match.split('|')[1])):
            self.statsjoueurs[i][2] = 0

        ecrire_fichier(self.manche)
        ecrire_fichier('STATS JOUEURS'+str(self.statsjoueurs), True)
        ecrire_fichier('CARTES RESTANTES'+str(self.cartesrestantes), True)
        ecrire_fichier('PIEGES SORTIS'+str(self.piegesorties), True)
        ecrire_fichier("------------------", True)

    def game_over(self, scores: str) -> None:  # Ne pas changer les paramètres
        """Appelé à la fin du jeu ; sert à ce que vous voulez

        Args:
            scores (str): descriptif des scores de fin de jeu
        """
        with open('IA/exit.txt', 'a') as f:
            f.write('END\n'+scores)

    def generation_stat_joueur(self) -> dict:
        """Génère les statistiques des joueurs

        Returns:
            dict: les statistiques des joueurs
        """
        stat = {}
        nb_joueur = int(self.match.split('|')[1])
        for i in range(nb_joueur):
            stat[i] = [0, [], 0]
        return stat
