from multiprocessing import Process, Manager, Value
import multiprocessing
import threading
from threading import Thread,Timer, Lock, Semaphore
import sysv_ipc

cloche = Lock()
semaphore = Semaphore(0)
Queue = sysv_ipc.MessageQueue(key)



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

def

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






class Carte:

	def __init__(self, MoyenDeTransport, Valeur):
		self.MoyenDeTransport=MoyenDeTransport
		self.Valeur=Valeur

def distribuerCartes(nbJoueurs):

"""pour montrer les cartes du joueur"""
def showcartes(i):

""" afficher tous les échanges proposés"""
def showecahnges():


def entreeClavier() :
    pass

def finPartie():
    pass

def Game():
    pass

if __name__ == "__main__":

    nbJoueurs = int(input("Combien de joueurs y aura-t-il ?\n"))
    echanges = Semaphore(0)
    state = [State.wait for i in range(nbJoueurs)]
    threads = [threading.Thread(target = Player, args = (i, )) for i in range(nbJoueurs)]


for thread in threads:
    thread.start()
for thread in threads:
    thread.join()
