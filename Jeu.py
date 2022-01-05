from multiprocessing import Process, Manager, Value
import multiprocessing
import threading
from threading import Thread,Timer, Lock, Semaphore
import sysv_ipc
import random
import os

cloche = Lock()
semaphore = Semaphore(0)

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

        #proposer un echange
        if state[i] == 2:
            showechanges()
            num = input("Quelle offre voulez-vous?")
            cartesech = listeechanges[num[1]]


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
    print("Voulez-vous voir vos cartes? (oui/non)")
    rep = input()
    if rep == oui:
        mq.send("ok", type = 1)

""" afficher tous les échanges proposés"""
def showechanges():
    print("Voulez-vous voir les offres? (oui/non)")
    rep = input()
    if rep == oui:
        mq.send("ok", type = 2)






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

def distribuerCartes(nbJoueurs):
	joueurs = [[] for i in range(nbJoueurs)]
	# création du générateur de cartes
	gen = get_carte(creation())
	for i in range(5):
	    for j in joueurs:
	        try:
	            j.append(next(gen))
	        except StopIteration:
	            pass
	return joueurs

def entreeClavier() :
    pass

def finPartie():
    pass

def Game():
    pass

if __name__ == "__main__":
    #Mise en place du jeu
    key=128
    queue=sysv_ipc.MessageQueue(key, sysv_ipc.IPC_CREAT)
    print("Serveur en service")
	nbJoueurs = int(input("Combien de joueurs y aura-t-il ?\n"))
	Deck=distribuerCartes(nbJoueurs)
    with multiprocessing.Pool(processes = 4) as pool :
        listen=True
        while listen:
            requete,t = queue.receive()
            demande = str(requete.decode())
            if demande == "Type 1":

            elif demande == "Type 2":

            elif demande == "Type 3":

            elif demande == "Type 4":

            elif demande == "Type 5":

            elif demande == "Type 6":

            else:
                print("Requête non reconnue")
                reponse = "Requête non reconnue"
                reponse.encode()
                queue.send(reponse)
        print("Closing connexion")

    '''
	echanges = Semaphore(0)
	state = [State.wait for i in range(nbJoueurs)]
	threads = [threading.Thread(target = Player, args = (i, )) for i in range(nbJoueurs)]'''





for thread in threads:
    thread.start()
for thread in threads:
    thread.join()
