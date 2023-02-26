# IA Diamants

![iut-velizy](http://eliott-b.tech/iut-velizy/IUT%20Velizy%20Villacoublay%20logo%202020%20ecran.png)

**Auteurs :** Eliott, Chakib  
**Années :** 2022-2023   
**Jeu développé par nous-même :** [https://github.com/Chakib-Eliott/sae-1.01](https://github.com/Chakib-Eliott/sae-1.01)  
**Moteur du jeu sur lequel tourne l'IA :** [lien dropbox](https://www.dropbox.com/s/qco14jtnunbo5st/SAE_2_IA_Diamants_v2.zip?dl=0)  
**Sujet :** [lien dropbox](https://www.dropbox.com/s/jugdkj4u0t0k4ne/SAE1.02_IA_diamant_enonce.pdf?dl=0)  


Ce projet consiste à développer une IA permettant de jouer au jeu de société Diamants.  
L'IA est développé pour jouer à une version du jeu optimisée pour.


# SOMMAIRE  

**[Présentation de notre SAé](#présentation-de-notre-saé)**  

> [But de la SAé](#but-de-la-saé)  
> [Nos outils](#nos-outils)  
> [Nos étapes de développement](#nos-étapes-de-développement)  

**[Détails de notre SAé](#détails-de-notre-saé)**  

> [Première approche du sujet](#première-approche-du-sujet)  
> [Analyse du jeu](#analyse-du-jeu)  
> [Interprétation des informations récoltées](#interprétation-des-informations-récoltées)  
> [Cerveau de l'IA](#cerveau-de-lia)  

**[Problème rencontré](#problème-rencontré)**  

> [Bugs](#bugs)  


# Présentation de notre SAé

## But de la SAé

Cette SAé est une SAé sur le thème de l'intelligence artificielle. Le
but de cette SAé était de créer une intelligence artificielle sur le jeu
'Diamants'. Cette intelligence artificielle devait jouer toute seule et
elle devait affronter d'autres intelligences artificielles.

Pour faire cette SAé nous avions un fichier à remplir avec nos méthodes
et elle devait affronter 3 autres "IA", une avait 50% de chance de
rentrer et 50% de chance d'explorer, une autre explorait tout le temps
et la dernière rentrait directement.

A la fin de la SAé un concours des meilleures IA va être organisé pour
définir la meilleure SAé.

## Nos outils

Pour réaliser ce projet nous avons utilisé plusieurs outils. Le premier
a été un outil traditionnel et commun, un **stylo** et une **feuille**
afin d'établir un plan et les étapes. Nous avons ensuite créé un
**Google Doc** afin d'avoir un espace pour écrire tous les bugs, étapes
et stratégies utilisés. De plus, Google Doc nous a permis d'avoir un
espace collaboratif.

Concernant la programmation, nous avons utilisé plusieurs logiciels
ainsi que leurs extensions.

Premièrement nous avons utilisé le site web **GitHub** pour héberger
notre projet sur un serveur et pouvoir suivre les différentes mises à
jours faites pendant le développement.

Deuxièmement nous avons utilisé l'IDE (environnement de développement
intégré) **Visual Studio Code** (VS Code) ainsi que plusieurs extensions
comme les multiples extensions de **GitHub** qui nous ont permis de
télécharger et mettre à jour notre projet sur le serveur mais aussi
l'extension **Live Share** qui permet de programmer simultanément à
plusieurs et aussi plusieurs autres extensions qui ont rendu notre
développement plus efficace comme des intelligences artificielles qui
complètent la base des DocString et bien d'autres.

Troisièmement nous avons utilisé aussi l'IDE **PyCharm** avec lequel
nous avons corrigé notre code pour respecter les conventions (Pep8).

## Nos étapes de développement

Pour répondre à la consigne, nous avons établi une stratégie de
développement. Nous avons premièrement établi nos étapes de
programmation sur un papier. Deuxièmement nous avons analysé le
programme, les sorties, etc ... avec les IA données dans le fichier ZIP
trouvé dans E-Campus. Puis nous avons établi la liste de toutes les
informations étant possibles de récupérer et qui pouvait être utile.
Ensuite nous avons commencé le croquis du fonctionnement de l'IA. Nous
avons ensuite commencé le développement de l'IA tout en écrivant nos
étapes et nos bugs sur notre Google Doc. Une fois l'IA finie nous
l'avons perfectionné en faisant de nombreux tests.

# Détails de notre SAé

## Première approche du sujet 

La première approche du sujet que nous avons eu est celle d'une IA qui
joue selon les informations qu'elle peut obtenir et/ou calculer. A
chaque fin de tour, l'IA reçoit une chaîne de caractère qui contient les
actions de chaque joueur ainsi que la carte sortie.

A partir de ces informations, l'IA devrait pouvoir détenir les
informations suivantes à chaque tour :

-   Les statuts de chacun des joueurs

-   Les rubis et reliques en leur possession

-   Les cartes déjà sorties et les cartes restantes dans le paquet

-   Les styles de jeu des autres joueurs (savoir la proba. que le joueur sorte directement lors d'une relique, ...)

-   le nombre d'exemplaire restant pour chaque piège

Ces informations peuvent être ensuite utilisées selon des probabilités
pour proposer le coup à jouer le plus pertinent.

## Analyse du jeu

Avant de commencer à développer notre IA, il est primordial de connaître
les informations dont elle dispose pour qu'elle puisse jouer en
conséquence. Par exemple, il faut qu'elle puisse déduire les diamants
qui sont en sa possession. Les informations que nous avons récupérer
sont les suivantes :

-   début du match (nombre de manches, nombre de joueurs, noms des joueurs et numéro de notre joueur)

-   le descriptif du tour à chaque tour (les choix de tous les joueurs à la fin du tour précédent ainsi que la carte révélée)

-   la raison de la fin de la manche (si c'est à cause d'un piège ou si tous les joueurs sont sortis)

Pour faire ceci, nous avons tout inscrit dans un fichier txt via une
fonction appelée à chaque action afin de réaliser l'analyse des parties
de notre IA pour pouvoir l'améliorer.

```python
def ecrire_fichier(data):

if FICHIERRECAP:

with open(\'IA/file.txt\', \'a\') as f:

f.write(str(data)+\'\\n\')
```

*fonction d'écriture dans le fichier*

## Interprétation des informations récoltées

Une fois ces informations récoltées, il faut désormais que notre IA en
déduise les diamants qu'elle possède dans un premier temps. Pour faire
cela, elle devra vérifier le nombre de joueurs qui étaient encore dans
la partie lorsque la carte a été révélée. Nous utilisons plusieurs
variables, une pour le nombre de diamants durant la manche (qu'elle peut
perdre à tout moment), et une autre pour les diamants permanents dont
elle dispose (le coffre), une liste des reliques en notre possession, la
manche actuelle, les pièges déjà sortis au cours de la manche, les
statistiques des autres joueurs ainsi que les cartes restantes dans le
jeu que nous contiendront dans un dictionnaire.

Afin de récupérer ces informations, nous avons utilisé uniquement celles
qui sont en notre possession, il fallait donc interpréter ces
informations et les stocker.

## Cerveau de l'IA

Notre IA fonctionne avec une évaluation des risques. En effet nous
calculons les risques que l'intelligence artificielle a de perdre grâce
aux informations récoltés comme par exemple : les pièges sorties, les
reliques sorties, les diamants restants, etc...

Chaque facteur ajoute ou retire un entier au taux de risque pour le
faire varier et ensuite faire un grand nombre de tests pour définir la
valeur idéale à laquelle comparer ce taux.

Nous ajoutons ensuite une part d'aléatoire, nous ajoutons entre -10 et
10 au taux de risque. Le taux risque pouvant être de base entre -20 et
120, il peut désormais être entre -30 et 130.

Grâce aux nombreux tests faits à la fin nous avons évalué que si le
seuil de risque est à 86?42 nous avons le plus de chance de gagner un
grand nombre de diamants. Donc si le taux de risque est en dessous de
86,42 , nous explorons et si le taux de risque est supérieur ou égal à
86,42 , nous rentrons. Pour arriver à ce résultat, nous avons effectué
plus d'un million de simulations : 10000 simulations pour tous les
entiers entre 0 et 120 puis 500 simulations pour tous les centièmes
entre 85 et 87.

Ainsi, sur 10000 parties contre notre IA et des IA aléatoires, on
retrouve 89,7% de victoire.

# Problème rencontré

## Bugs

Pour commencer nous avons rencontré un bug lors de la récupération des
informations. En effet pour définir les diamants restants après que les
IA soient rentrées, nous actualisons les diamants restants en retirant
seulement la part d'un IA et non tous les diamants récupérés par les IA
sortants. Ce bug faussait donc nos informations comparées aux
informations données à la fin par le moteur du jeu.

De plus, nous avons mal exécuté une règle du jeu et donc les résultats
n'étaient encore pas les mêmes car quand une IA rentrait et qu'il y
avait plusieurs reliques, nous lui attribuons seulement une seule
relique et non toutes celles présentes sur le tapis.

Ainsi, entre deux tours nous oublions de réinitialiser les reliques
découvertes et non récupérées lors du tour précédent. Résultat les IA
récupéraient des reliques qui n'étaient pas sorties lors du tour.
