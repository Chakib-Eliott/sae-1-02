import random
import importlib

#mettre à False pour ne plus avoir de sortie dans le terminal
RAPPORT = True

#deck standard
tresors = [1,2,3,4,5,5,7,7,9,1,1,13,14,15,17] 
pieges = {"P1" : 3, "P2" : 3, "P3" : 3, "P4" : 3, "P5" : 3}
valeurs_reliques = [5,5,5,10,10]

##############################################################################
# Structures de données
# servant à simplement à stocker les infos en cours de jeu
# le fait d'utiliser des objets plutot que des dictionnaires 
# permet un débug plus facile
##############################################################################

class Match:
    """infos constantes pendant toute la partie"""
    def __init__(self, nb_manches : int, nb_joueurs : int, noms_joueurs : list, IA):
        self.nb_manches = nb_manches
        self.nb_joueurs = nb_joueurs
        self.noms_joueurs : noms_joueurs
        self.IA = IA

class Etat_Jeu:
    """infos qui évoluent en cours de partie pendant toute la partie"""
    def __init__(self, nb_joueurs : int, deck : list):
        self.scores = [0] * nb_joueurs
        self.nb_reliques_gagnees = 0
        self.deck = deck
        self.dernier_tour_str = ""

class Infos_Manche:
    """infos valables juste pendant cette manche"""
    def __init__(self, nb_joueurs):
        self.scores_manches = [0] * nb_joueurs
        self.en_lice = [True] * nb_joueurs
        self.premier_indice_pioche = 0
        self.rubis_en_jeu = 0
        self.nb_reliques_en_jeu = 0
        self.pieges_reveles = []
    
  
##############################################################################
# Fonctions Auxiliaires
##############################################################################


def charge_IAs(joueurs : list, match : Match):
    """Charge les objets IA contenus dans les fichiers (noms des joueurs) donnés
    
    Args:
        joueurs [str]: noms des joueurs
    Returns:
        list : liste des objet IAs par chaque indice de joueur

    """

    list_ia = []

    for i in range(len(joueurs)):
        #imp = __import__("IA."+nom_fichier)
        imp = importlib.import_module("IA." + joueurs[i])
        list_ia.append(imp.IA_Diamant(match + "|" + str(i)))

    return list_ia

##############################################################################
# Fonctions principales du moteur
##############################################################################


def partie_diamant(nb_manches : int, joueurs : list):
    """
    Simule une partie du jeu diamant

    Args:
        nb_manches (int) : nombre de manches entre 1 et 5 en principe
        joueurs ([str]) : liste contenant les noms des joueurs i.e. les noms des fichiers contenant les IA
            (on peut mettre plusieurs fois le même nom)
    Returns:
        historique (str) : historique complet de la partie
        scores (list) : liste des scores des joueurs en fin de partie
    """

    
    #formation du deck initial
    deck = tresors + \
        [x  for p in pieges for x in [p]*pieges[p] ]

    
    #match contient des constantes de tout le match
    match = Match(nb_manches,len(joueurs),joueurs, None)
    match_str = "|".join(map(str,[nb_manches,len(joueurs),",".join(joueurs)]))

    #chargement des IA
    IAs = charge_IAs(joueurs, match_str)
    match.IA = IAs


    #etat_jeu contient des données qui vont évoluer pendant le match
    ej = Etat_Jeu(len(joueurs), deck)
    
    
    for num_manche in range(nb_manches):
        manche(match, ej)

    #notification aux IA
    for i in range(match.nb_joueurs):
        match.IA[i].game_over(",".join(map(str,ej.scores)))

    return ej.scores
        

def manche(match : Match, ej : Etat_Jeu):
    """_summary_

    Args:
        etat (_type_): _description_
        joueurs (_type_): _description_
    """    

    manche = Infos_Manche(match.nb_joueurs)

    if RAPPORT:
        print("DEBUT MANCHE")
        print("  scores:",ej.scores, ",reliques gagnées:", ej.nb_reliques_gagnees)

    
    #preparation du deck
    ej.deck.append('R')
    random.shuffle(ej.deck)

    ej.dernier_tour_str = ""
    
    if RAPPORT:
        print("  deck :", ej.deck)
    #boucle principale de manche
    fin_de_manche = ""

    while not fin_de_manche:
        fin_de_manche = tour_de_jeu(match, manche, ej)


    #notification aux IAs
    for i in range(match.nb_joueurs):
        match.IA[i].fin_de_manche(fin_de_manche, ej.dernier_tour_str)

    if RAPPORT:
        print("FIN MANCHE")    

def tour_de_jeu(match : Match, manche : Infos_Manche, ej : Etat_Jeu):
    """Simule un tour de jeu : chaque joueur choisit son action, on révèle une carte, on assigne les scores

    Args:
        etat_jeu (_type_): _description_
        IAs (_type_): _description_
    """

    #valeurs par défaut
    fin_de_manche = ""
    nouvelle_carte = 'N'

    if RAPPORT:
        print('  DEBUT TOUR')
        print("    rubis en jeu:",manche.rubis_en_jeu,",reliques en jeu:",manche.nb_reliques_en_jeu,",pieges:",manche.pieges_reveles)
            

    #on stocke les décisions de chaque joueur encore en lice
    decisions = {'X':[], 'R':[], 'N':[]}
    choix = [None]*match.nb_joueurs
    
    
    for i in range(match.nb_joueurs):
        choix[i] = match.IA[i].action(ej.dernier_tour_str) #renvoie X pour eXplorer ou R pour Rentrer
        if not manche.en_lice[i]:
            choix[i] = 'N'
        decisions[choix[i]].append(i)

    if RAPPORT:
        print('    choix des joueurs:',choix)

    #ceux qui rentrent
    if decisions['R']:
        gain = manche.rubis_en_jeu  // len(decisions['R'])
        manche.rubis_en_jeu = manche.rubis_en_jeu % len(decisions['R']) 
        for i in decisions['R']:
            manche.en_lice[i] = False
            manche.scores_manches[i] += gain
            ej.scores[i] += manche.scores_manches[i]
            if RAPPORT:
                print("    le joueur",i,"rentre et gagne",gain,"sur la route et", manche.scores_manches[i],"dans la manche")
                
        #gain de relique
        if len(decisions['R'])==1:
            heureux = decisions['R'][0]
            for r in range(manche.nb_reliques_en_jeu):
                ej.scores[heureux] += valeurs_reliques[ej.nb_reliques_gagnees]
                ej.nb_reliques_gagnees += 1
                if RAPPORT:
                    print("    le joueur", heureux, "rentre seul et ramasse une relique pour", valeurs_reliques[ej.nb_reliques_gagnees-1],"points")
            manche.nb_reliques_en_jeu = 0

    #ceux qui restent
    if decisions['X']:
        nouvelle_carte = ej.deck[manche.premier_indice_pioche]
        manche.premier_indice_pioche += 1
        if RAPPORT:
            print('    NOUVELLE CARTE REVELEE', nouvelle_carte)
        if nouvelle_carte == 'R':
            # on comptabilise la relique mais on la retire du deck
            manche.nb_reliques_en_jeu += 1
            manche.premier_indice_pioche -= 1
            ej.deck.pop(manche.premier_indice_pioche)
            
            
        
        elif isinstance(nouvelle_carte,int):
            for i in decisions['X']:
                if RAPPORT:
                    print("    le joueur",i,"explore et gagne", nouvelle_carte // len(decisions['X']))
                manche.scores_manches[i]  += nouvelle_carte // len(decisions['X'])
            manche.rubis_en_jeu += nouvelle_carte % len(decisions['X'])
            if RAPPORT:
                print("    il reste", nouvelle_carte % len(decisions['X']),"rubis de ce partage")
                
        else: #c'est donc un piège
            if nouvelle_carte not in manche.pieges_reveles:
                manche.pieges_reveles.append(nouvelle_carte)
            else:
                #on supprime le piege
                ej.deck.pop(manche.premier_indice_pioche-1)
                if RAPPORT:
                    print('  FIN TOUR PIEGE')
                

                fin_de_manche = nouvelle_carte

    #historique du tour
    ej.dernier_tour_str = ",".join(choix) + "|" + str(nouvelle_carte)

    if not any(manche.en_lice):
        fin_de_manche = "R"
        if RAPPORT:
            print('  FIN TOUR AU CAMP')
    
    return fin_de_manche

