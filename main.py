##############################################################################
# main                                                                       #
##############################################################################

# Dans ce fichier que vous pouvez compléter vous lancez vos expérimentations

from moteur_diamant import partie_diamant
# import numpy as np

stats = {}

if __name__ == '__main__':

    # for i in np.arange(85,87,0.01):
    #     stats[i] = []
    #     for j in range(100):
    #         stats[i].append(partie_diamant(5,['IA_BARKER_OUALI', 'IA_aleatoire','IA_aleatoire','IA_aleatoire','IA_aleatoire','IA_aleatoire','IA_aleatoire','IA_aleatoire','IA_aleatoire'], i))
    for i in range(500):
        stats[i] = []
        for j in range(100):
            stats[i].append(partie_diamant(5,
                       ['IA_BARKER_OUALI', 'IA_aleatoire', 'IA_aleatoire', 'IA_aleatoire']))

# print(stats)

for k, v in stats.items():
    print(k, end=': ')
    tauxv = 0
    for i in v:
        if i[0] == max(i):
            tauxv += 1
    print(tauxv/len(v) * 100)
