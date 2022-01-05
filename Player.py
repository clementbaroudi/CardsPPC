""" etats player"""

class Stateplayer:
    wait = 1
    echange = 2
    faire_offre = 3
    Sonner_cloche = 4

def wait() :

def echangercartes(i):
    showcartes(i)
    """proposer les cartes à échanger"""


def Player(i, ):
    while True :
        if state[i] == 1:
            showcartes(i)
            showechanges()
            echan = input("Voulez-vous accepter un des échanges proposés? (oui/non)")
            if echan == oui:
                state[i] = 2
            else :
                off = input ("Voulez-vouz faire une offre? (oui/non)")
                if off == oui:
                    state[i] = 3

        if state[i] == 2:

        if state[i] == 3:

        if state[i] == 4:


"""pour montrer les cartes du joueur"""
def showcartes(i):

""" afficher tous les échanges proposés"""
def showecahnges():
