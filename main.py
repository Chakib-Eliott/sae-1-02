##############################################################################
# main                                                                       #
##############################################################################

# Dans ce fichier que vous pouvez compléter vous lancez vos expérimentations

from moteur_diamant_simu import partie_diamant

stats = {}

if __name__ == '__main__':


    for i in range(100):
        stats[i] = []
        for j in range(5):
            stats[i].append(partie_diamant(5,['IA_BARKER_OUALI', 'IA_aleatoire','IA_aleatoire','IA_aleatoire','IA_aleatoire','IA_aleatoire','IA_aleatoire','IA_aleatoire','IA_aleatoire'], i))

print(stats)

for k,v in stats.items():
    print(k, end=': ')
    score_moyen = 0
    for i in v:
        score_moyen += i[0]
    print(score_moyen/len(v))