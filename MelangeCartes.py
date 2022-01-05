import random

nbJoueurs = 3
def creation():
    enseignes = ["avion","voiture","train","velo","pieton"]
    valeurs = [1,2,3,4,5]
    return [(x,y) for x in enseignes for y in valeurs]

def get_carte(cartes):
    # Fonction génératrice
    NewCartes=cartes[0:5*nbJoueurs]
    sabot = random.sample(NewCartes, 5*nbJoueurs)
    while sabot:
        # tant qu'il reste des cartes dans le sabot
        yield sabot.pop()

joueurs = [[] for i in range(nbJoueurs)]
# création du générateur de cartes
gen = get_carte(creation())

# distribution, exemple 8 cartes par joueur
for i in range(5):
    for j in joueurs:
        try:
            j.append(next(gen))
        except StopIteration:
            print("Distribution terminée !")
            pass

# contrôle
for j in joueurs:
    print(j)
