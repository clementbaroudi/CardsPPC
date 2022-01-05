from multiprocessing import Process, Manager, Value
import multiprocessing
import threading
from threading import Thread,Timer, Lock, Semaphore
import sysv_ipc


key = 42
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


def Player(i, ):
    while True :
        
        if state[i] == 1:
            """
            showcartes(i)
            showechanges()
            echan = input("Voulez-vous accepter un des échanges proposés? (oui/non)")
            if echan == oui:
                state[i] = 2
            else :
                off = input ("Voulez-vouz faire une offre? (oui/non)")
                if off == oui:
                    state[i] = 3
            """
            rep = input("proposer offre = 1")
            if rep == 1:
                state[i] = 3

        if state[i] == 2:


        #proposer une offre
        if state[i] == 3:

            showcartes(i)
            moy = input ("quel moyen de transport voulez vous echanger?")

            cartes[]  # toutes les cartes de ce moyen de transport du joueurs

            if cartes.lenght() > 3:
                cartesech = cartes[0:2]
            else:
                cartesech = cartes


            occupé = True
            while occuppe == True:
                if not sem.acquire():
                    sem.release()
                    print("Un échange est déjà en cours, veuillez patienter")
                else:
                    listechanges.append([i, cartesech[]])
                    sem.release()





        if state[i] == 4:


"""pour montrer les cartes du joueur"""
def showcartes(i):

""" afficher tous les échanges proposés"""
def showecahnges():

if __name__ == "__main__":
    nbJoueurs = int(input("Combien de joueurs y aura-t-il ?\n"))
    threads = [threading.Thread(target = Player, args = (i, )) for i in range(nbJoueurs)]
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()
