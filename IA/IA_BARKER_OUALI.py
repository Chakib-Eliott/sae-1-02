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
        self.manche = 1  # Manche actuelle
        self.tour =  0 # Tour actuel
        self.piegesorties = []  # Liste des pièges sortis
        self.cartesorties = []  # Liste des cartes sorties
        self.reliqueattente = []  # Liste des reliques en attente
        self.diamantattente = 0  # Nombre de diamants sur le tapis
        self.iaexplorant = []  # Liste des IA explorant
        self.iasorties = []  # Liste des IA sorties
        # Dictionnaire des statistiques des IA
        # (nombre de diamants sécurisés [int], reliques [list], nombre de diamants temporaires [int])
        self.statsia = self.generation_stat_ia()
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

    def info_ia(self, tour: str) -> None:
        """Appelé à chaque action afin de récupérer les informations concernant les IA.
        Permet d'enregistrer les informations dans les variables comme par exemple
        les diamants sécurisés et reliques des IA.
        
        Le format du tour doit être sous cette forme :
            `A,A,A,A|C`
            (A = Action, C = Carte)

        Args:
            tour (str): descriptif du dernier tour
        """
        assert len(tour) >= 9, 'Tour non conforme'
        
        info = tour.split('|')
        # Récupère le choix des IA
        ia_choix = info[0].split(',')
        
        # Compte le nombre d'IA explorant et explorant
        nombre_explorant = 0
        nombre_sortant = 0
        for ia in ia_choix:
            if ia == 'X':
                nombre_explorant += 1
            elif ia == 'R':
                nombre_sortant += 1
        
        # Vérifie qu'il y a des IA sortant
        if nombre_sortant > 0:    
            # Calcul le nombre de diamants par IA sortant
            diamants_sortant = self.diamantattente//nombre_sortant
            self.diamantattente = self.diamantattente%nombre_sortant  # Retire les diamants de l'attente
        
        diamantattente = None
        carte_tresor = None
        # Vérifie que la carte est un diamant
        if info[1] in [str(y) for y in range(20)]:
            carte_tresor = int(info[1])  # Récupère la carte
            self.cartesorties.append(carte_tresor)  # Ajoute la carte dans la liste des cartes sorties
            diamants_par_psr = carte_tresor//nombre_explorant
            # Calcul le nombre de diamants en attente pour les attribuer après les attributions de points.
            diamantattente = carte_tresor%nombre_explorant
        
        self.iaexplorant = list()  # Réinitialise la liste des IA explorant
        for i in range(len(ia_choix)):  # Parcours les IA
            # Vérifie que l'IA reste et qu'il y a une carte diamant
            if ia_choix[i]=='X' and carte_tresor is not None:
                self.iaexplorant.append(i)  # Ajoute les IA explorant dans la liste
                self.statsia[i][2] += diamants_par_psr  # Ajoute les diamants aux IA explorant
            elif ia_choix[i] == 'R':  # Vérifie que l'IA sort
                self.iasorties.append(i)  # Ajoute les IA sortant dans la liste
                self.statsia[i][2] += diamants_sortant  # Ajoute les diamants aux IA sortant
                # Vérifie qu'il n'y a qu'une IA sortant pour lui attribuer une relique si il y en a une
                if nombre_sortant == 1:
                    if len(self.reliqueattente) > 0:
                        # Ajoute la relique dans les poches de l'IA
                        for y in range(len(self.reliqueattente)):
                            self.statsia[i][1].append(self.reliqueattente[y])
                            self.cartesrestantes['R'+str(self.reliqueattente[y])] -= 1
                        self.reliqueattente = list()  # Réinitialise la liste des reliques en attente
        
        if diamantattente is not None:
            # Ajoute les diamants en attente                
            self.diamantattente += diamantattente
        
        # Vérifie qu'il y a des reliques en attente
        if info[1] == 'R':
            # Vérifie la valeur de la relique
            if self.cartesrestantes['R5'] > 0:
                self.reliqueattente.append(5)
            else:
                self.reliqueattente.append(10)
        
        # Vérifie si la carte est un piège
        if info[1].startswith('P'):
            self.piegesorties.append(info[1])  # Ajoute le piège dans la liste des pièges sortis
        
    def lebonchoix(self) -> str:
        """Algorithme de décision de l'IA.
        
        Returns: 
            str: le choix de l'IA
        """
        risque = 0  # Pourcentage de risque
        risque += self.tour * 5  # Ajoute 5% de risque par tour
        if self.tour == 1:  # Si c'est le premier tour
            risque = 0
        else:
            if len(self.piegesorties) == 0:
                risque = 0
            else:
                diamants, reliques, pieges = 0, 0, 0
                for k,v in self.cartesrestantes.items():
                    
                    if type(k) != int:
                        if k.startswith('P'):  # Vérifie que la carte est un piège
                            pieges += v
                        elif k.startswith('R'):  # Vérifie que la carte est une relique
                            reliques += v
                    else:  # Vérifie que la carte est un diamant
                        diamants += v
                risque += pieges/(diamants+(reliques*2)) * 100  # Calcul le ratio de pièges par rapport aux diamants et reliques
            notreia = self.statsia[int(self.match.split('|')[-1])][0]

            classement = [self.statsia[i][0] for i in range(len(self.statsia))]
            risque += (sorted(classement, reverse=True).index(notreia)/(len(self.statsia)/2)-1)*10
        if risque < 75:  # Vérifie que le risque est inférieur au seuil
            return 'X'
        else:
            #print("######################", risque)
            return 'R'
                

    def action(self, tour: str) -> str:  # Ne pas changer les paramètres
        """Appelé à chaque décision de l'IA
        
        Le format du tour doit être sous cette forme :
            `A,A,A,A|C`
            (A = Action, C = Carte)

        Args:
            tour (str): descriptif du dernier tour de jeu

        Returns:
            str: 'X' ou 'R'
        """
        assert len(tour) >= 9, 'Tour non conforme'
        
        self.info_ia(tour)  # Appel la fonction pour actualiser les informations récupérés du tour.
        self.tour += 1  # Incrémente le tour
        ecrire_fichier(tour)
        
        return self.lebonchoix()  # Appel l'algorithme de décision

    def fin_de_manche(self, raison: str, dernier_tour: str) -> None:  # Ne pas changer les paramètres
        """Appelé à chaque fin de manche

        Args:
            raison (str): 'R' si tout le monde est un piège ou "P1","P2",... si un piège a été déclenché
            dernier_tour (str): descriptif du dernier tour de la manche
        """
        # Retire les cartes pièges qui sont sortis
        if raison != 'R':
            self.cartesrestantes[raison] -= 1
        
        # Vérifie si les IA n'avaient pas perdu et leur donne leurs diamants
        derniere_action = dernier_tour.split('|')[0].split(',')
        for i in range(int(self.match.split('|')[1])):
            if derniere_action[i] != 'X':
                self.statsia[i][0] += self.statsia[i][2]

        ecrire_fichier(dernier_tour)
        ecrire_fichier(raison)
        ecrire_fichier('POCHES : '+str(self.statsia[0][2]))
        ecrire_fichier('COFFRE : '+str(self.statsia[0][0]))
        ecrire_fichier('RELIQUE : '+str(self.statsia[0][1]))
        ecrire_fichier('FIN DE MANCHE')
        print('MANCHE'+str(self.manche))
        print('POCHES : '+str(self.statsia[0][2]))
        print('COFFRE : '+str(self.statsia[0][0]))

        self.iasorties = list()  # Remet à 0 la liste des IA sortant
        self.tour = 0  # Remet le tour à 0
        self.piegesorties = list()  # Remet à 0 la liste des pièges sortis
        self.reliqueattente = list()  # Remet à 0 la liste des reliques en attente
        self.cartesorties = list()  # Remet à 0 la liste des cartes sorties
        self.diamantattente = 0  # Remet à 0 le nombre de diamants en attente
        
        self.manche += 1  # Incrémente le nombre de manche

        # Remet à 0 les diamants temporaires des IA
        for i in range(len(self.statsia)):
            self.statsia[i][2] = 0

        ecrire_fichier(self.manche)
        ecrire_fichier('STATS IA'+str(self.statsia), True)
        ecrire_fichier('CARTES RESTANTES'+str(self.cartesrestantes), True)
        ecrire_fichier('PIEGES SORTIS'+str(self.piegesorties), True)
        ecrire_fichier("------------------", True)
        

    def game_over(self, scores: str) -> None:  # Ne pas changer les paramètres
        """Appelé à la fin du jeu ; sert à ce que vous voulez

        Args:
            scores (str): descriptif des scores de fin de jeu
        """
        # Ajoute les reliques des IA dans leur coffre
        for i in range(len(self.statsia)):
            for relique in self.statsia[i][1]:
                self.statsia[i][0] += relique
        ecrire_fichier('STATS IA'+str(self.statsia))
        ecrire_fichier(scores)

    def generation_stat_ia(self) -> dict:
        """Génère les statistiques des IA.
        Les statistiques sont sous cette forme :
            {0: [0, [], 0], 1: [0, [], 0], 2: [0, [], 0], 3: [0, [], 0]}
        La clé est l'ID de l'IA.
        Le premier élément est le score de l'IA.
        Le deuxième élément est la liste des reliques que possède l'IA.
        Le troisième élément est le nombre de diamants que possède l'IA.

        Returns:
            dict: les statistiques des IA
        """
        stat = {}
        nb_ia = int(self.match.split('|')[1])
        for i in range(nb_ia):
            stat[i] = [0, [], 0]
        return stat
